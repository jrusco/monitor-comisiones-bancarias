import json
import requests
import pdfplumber
import re
from io import BytesIO
from datetime import datetime

DATA_FILE = 'data.json'
INDEX_FILE = 'index.html'
BNA_ID = 'bna'
PDF_URL = 'https://www.bna.com.ar/Downloads/ComisionesYCargosComercial.pdf'

# Defines the mapping between our data.json structure and the PDF content
FEE_MAPPING = [
    {
        "json_concept": "Débito",
        "json_term": "48 hs",
        "pdf_pattern": r"d[ée]bito",
        "pdf_section": "ARANCEL DE VENTAS",
        "fallback_rate": "0.8% (Regulado)",  # Keep if not found in PDF
    },
    {
        "json_concept": "Crédito",
        "json_term": "8-10 días hábiles",
        "pdf_pattern": r"Otros Rubros",  # General merchant category
        "pdf_section": "ARANCEL DE VENTAS",
        "fallback_rate": "1.8% (Regulado)",
    },
    {
        "json_concept": "Mantenimiento Terminal",
        "json_term": "Mensual",
        "pdf_pattern": r"Equipos móvil.*?web",
        "pdf_section": "EQUIPO DE CAPTURA",
        "fallback_rate": "Bonificado o Variable",
    }
]


def download_pdf(url):
    """
    Downloads the PDF from the given URL and returns it as a BytesIO object.

    Args:
        url: The URL of the PDF to download

    Returns:
        BytesIO object containing the PDF data

    Raises:
        requests.exceptions.RequestException: If download fails
    """
    print(f"Downloading PDF from: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    print(f"✓ Successfully downloaded PDF ({len(response.content)} bytes)")
    return BytesIO(response.content)


def normalize_rate(rate_str, concept):
    """
    Normalizes rate strings to match data.json format.

    Args:
        rate_str: Raw rate string extracted from PDF (e.g., "1,8%", "Bonificado")
        concept: The fee concept (e.g., "Débito", "Crédito")

    Returns:
        Normalized rate string suitable for data.json
    """
    # Convert comma decimals to dots
    rate_str = rate_str.replace(',', '.')

    # Handle terminal fee variations
    if any(term in rate_str for term in ["Bonificado", "SIN COSTO", "Importes a determinar"]):
        return "Bonificado o Variable"

    # Add (Regulado) suffix for debit/credit rates
    if concept in ["Débito", "Crédito"] and "(Regulado)" not in rate_str:
        if '%' in rate_str:
            return f"{rate_str} (Regulado)"

    return rate_str


def extract_fees_from_pdf(pdf_bytes):
    """
    Parses the PDF to extract fee information.

    The function looks for the "CLIENTE COMERCIO" section in the PDF and extracts
    rates for different payment types using regex patterns.

    Args:
        pdf_bytes: BytesIO object containing the PDF data

    Returns:
        List of dictionaries with 'concept' and 'rate' keys
    """
    extracted_fees = []

    print("Parsing PDF content...")

    try:
        with pdfplumber.open(pdf_bytes) as pdf:
            full_text = ""

            # Extract text from all pages
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    full_text += f"\n--- Page {page_num} ---\n{page_text}"

            # Check if we found the merchant section
            if "CLIENTE COMERCIO" not in full_text:
                print("⚠ Warning: 'CLIENTE COMERCIO' section not found in PDF")
                print("   Trying alternative section markers...")

                if "ARANCEL DE VENTAS" not in full_text:
                    print("⚠ Warning: Could not find expected sections in PDF")
                    print("   PDF structure may have changed. Using fallback rates.")
                    return extracted_fees
            else:
                print("✓ Found 'CLIENTE COMERCIO' section in PDF")

            # Extract "Otros Rubros" rate (general credit card merchant rate)
            # Pattern: "Otros Rubros" followed by a percentage (1,8% or 1.8%)
            otros_rubros_pattern = r"Otros\s+Rubros.*?(\d+[,\.]\d+)\s*%"
            match = re.search(otros_rubros_pattern, full_text, re.IGNORECASE | re.DOTALL)

            if match:
                rate = match.group(1) + "%"
                print(f"✓ Extracted 'Otros Rubros' rate: {rate}")
                extracted_fees.append({
                    'concept': 'Crédito',
                    'rate': rate
                })
            else:
                print("⚠ Could not find 'Otros Rubros' rate in PDF")

            # Extract debit rate
            # Pattern: Look for "débito" or "debito" followed by a percentage
            debito_pattern = r"d[ée]bito.*?(\d+[,\.]\d+)\s*%"
            match = re.search(debito_pattern, full_text, re.IGNORECASE | re.DOTALL)

            if match:
                rate = match.group(1) + "%"
                print(f"✓ Extracted 'Débito' rate: {rate}")
                extracted_fees.append({
                    'concept': 'Débito',
                    'rate': rate
                })
            else:
                print("⚠ Could not find explicit 'Débito' rate in PDF")

            # Extract terminal equipment fee
            # Pattern: Look for "Equipos móvil" or similar with fee information
            terminal_patterns = [
                r"Equipos\s+m[oó]vil.*?(Bonificado|SIN COSTO|Importes\s+a\s+determinar)",
                r"Terminal.*?(Bonificado|SIN COSTO|Variable)",
            ]

            for pattern in terminal_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
                if match:
                    rate = match.group(1)
                    print(f"✓ Extracted terminal fee: {rate}")
                    extracted_fees.append({
                        'concept': 'Mantenimiento Terminal',
                        'rate': rate
                    })
                    break
            else:
                print("⚠ Could not find terminal equipment fee in PDF")

    except Exception as e:
        print(f"✗ Error parsing PDF: {e}")
        print("   Using fallback rates...")
        return extracted_fees

    print(f"✓ Extracted {len(extracted_fees)} fee entries from PDF")
    return extracted_fees


def update_fees_in_data(data, extracted_fees):
    """
    Updates BNA fees in the data structure based on extracted fees.
    Uses fallback rates from FEE_MAPPING when fees are not found in PDF.

    Args:
        data: The full data.json structure
        extracted_fees: List of extracted fees from PDF

    Returns:
        Updated data if changes were made, None otherwise
    """
    bna_entity = None
    for entity in data:
        if entity.get('id') == BNA_ID:
            bna_entity = entity
            break

    if not bna_entity:
        print(f"✗ ERROR: Entity with id '{BNA_ID}' not found in {DATA_FILE}")
        return None

    something_was_updated = False

    # Process each mapping
    for mapping in FEE_MAPPING:
        # Try to find the rate in extracted fees
        new_rate = None

        for extracted_fee in extracted_fees:
            if extracted_fee['concept'] == mapping['json_concept']:
                # Normalize the rate
                new_rate = normalize_rate(extracted_fee['rate'], mapping['json_concept'])
                print(f"  Using extracted rate for {mapping['json_concept']}: {new_rate}")
                break

        # If not found in extracted fees, use fallback
        if not new_rate:
            new_rate = mapping['fallback_rate']
            print(f"  Using fallback rate for {mapping['json_concept']}: {new_rate}")

        # Validate regulated rates are within expected range
        if mapping['json_concept'] in ['Débito', 'Crédito']:
            # Extract numeric value for validation
            rate_match = re.search(r'(\d+\.?\d*)', new_rate)
            if rate_match:
                rate_value = float(rate_match.group(1))

                if mapping['json_concept'] == 'Débito':
                    if not (0.5 <= rate_value <= 1.1):
                        print(f"  ⚠ Warning: Débito rate {rate_value}% is outside expected range (0.5-1.1%)")
                elif mapping['json_concept'] == 'Crédito':
                    if not (1.5 <= rate_value <= 2.1):
                        print(f"  ⚠ Warning: Crédito rate {rate_value}% is outside expected range (1.5-2.1%)")

        # Find and update the corresponding fee in data.json
        for fee in bna_entity.get('fees', []):
            if fee.get('concept') == mapping['json_concept'] and fee.get('term') == mapping['json_term']:
                if fee['rate'] != new_rate:
                    print(f"✓ Updating '{fee['concept']}' ({fee['term']}): '{fee['rate']}' → '{new_rate}'")
                    fee['rate'] = new_rate
                    something_was_updated = True
                else:
                    print(f"  No change needed for '{fee['concept']}' ({fee['term']}): {fee['rate']}")
                break

    return data if something_was_updated else None


def update_date_in_html():
    """
    Updates the "Actualizado" date stamp in index.html to the current date.

    Returns:
        True if the date was updated, False otherwise
    """
    try:
        print(f"Updating date stamp in {INDEX_FILE}...")

        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Get current date in DD/MM/YY format
        current_date = datetime.now().strftime('%d/%m/%y')

        # Pattern to match: Actualizado: DD/MM/YY
        date_pattern = r'(Actualizado:\s*)\d{2}/\d{2}/\d{2}'
        replacement = rf'\g<1>{current_date}'

        # Check if pattern exists
        if not re.search(date_pattern, html_content):
            print(f"  ⚠ Warning: Could not find date pattern in {INDEX_FILE}")
            return False

        # Replace the date
        updated_html = re.sub(date_pattern, replacement, html_content)

        # Only write if something changed
        if updated_html != html_content:
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            print(f"✓ Updated date stamp to: {current_date}")
            return True
        else:
            print(f"  Date stamp already current: {current_date}")
            return False

    except FileNotFoundError:
        print(f"  ⚠ Warning: {INDEX_FILE} not found, skipping date update")
        return False
    except Exception as e:
        print(f"  ⚠ Warning: Failed to update date in {INDEX_FILE}: {e}")
        return False


if __name__ == "__main__":
    print("="*70)
    print("BNA Fee Updater Script")
    print("="*70)
    print()

    try:
        # Step 1: Download PDF
        pdf_bytes = download_pdf(PDF_URL)
        print()

        # Step 2: Extract fees from PDF
        extracted_fees = extract_fees_from_pdf(pdf_bytes)
        print()

        # Step 3: Load current data.json
        print(f"Loading {DATA_FILE}...")
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
        print(f"✓ Successfully loaded {DATA_FILE}")
        print()

        # Step 4: Update fees
        print("Processing fee updates...")
        updated_data = update_fees_in_data(current_data, extracted_fees)
        print()

        # Step 5: Write changes if any
        if updated_data:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, indent=4, ensure_ascii=False)
            print("="*70)
            print("✓ SUCCESS: data.json has been updated with new BNA fees")
            print("="*70)
        else:
            print("="*70)
            print("✓ No changes needed: All fees are already up to date")
            print("="*70)

        # Step 6: Update date stamp in HTML (always update to reflect when script was run)
        print()
        update_date_in_html()

    except requests.exceptions.RequestException as e:
        print()
        print("="*70)
        print(f"✗ ERROR: Failed to download PDF from {PDF_URL}")
        print(f"  Reason: {e}")
        print("="*70)
        print()
        print("Possible solutions:")
        print("  • Check your internet connection")
        print("  • Verify the PDF URL is still valid")
        print("  • Try running the script again later")
        exit(1)

    except FileNotFoundError:
        print()
        print("="*70)
        print(f"✗ ERROR: {DATA_FILE} not found")
        print("="*70)
        exit(1)

    except json.JSONDecodeError as e:
        print()
        print("="*70)
        print(f"✗ ERROR: Failed to parse {DATA_FILE}")
        print(f"  Reason: {e}")
        print("="*70)
        exit(1)

    except Exception as e:
        print()
        print("="*70)
        print(f"✗ ERROR: Unexpected error occurred")
        print(f"  Reason: {e}")
        print("="*70)
        exit(1)

    print()
    print("IMPORTANT NOTES:")
    print("  • BNA fees are government-regulated and change infrequently")
    print("  • Regulated rates: Débito 0.8%, Crédito 1.8%")
    print("  • Terminal fees may vary by service provider")
    print("  • Manual verification recommended after fee changes")
    print()
    print("Script finished successfully.")
