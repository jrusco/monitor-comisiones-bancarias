"""
Banco Provincia Fee Updater

Scrapes merchant acquiring fees from Banco Provincia's official adhesion page
and updates data.json with current rates.

Banco Provincia publishes fees at:
  https://www.bancoprovincia.com.ar/web/adhesion_comercios

For Clave DNI specifics:
  https://www.provinciamicrocreditos.com.ar/comunidad/cdnicomercios2024/

Updated 2026-01-16:
- Scrapes primary adhesion page for Débito, Crédito, Clave DNI, and QR rates
- Uses verified fallback rates from research_spanish.md (Table 2)
- Normalizes decimal separators from comma (Argentine) to dot (International)
- Splits Cuenta DNI range into two separate payment methods:
  * Clave DNI (Token): 0.6%
  * QR (Saldo en Cuenta): 0.8%
- Updates index.html date stamp after successful updates
- Follows BNA pattern for defensive text-based parsing
"""

import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

DATA_FILE = 'data.json'
INDEX_FILE = 'index.html'
BAPRO_ID = 'bapro'

# Official Banco Provincia page for commercial adhesion
PRIMARY_FEE_URL = 'https://www.bancoprovincia.com.ar/web/adhesion_comercios'

# Fallback rates from research_spanish.md (Table 2: Tarifario de Adquirencia Banco Provincia)
# Source: https://www.provinciamicrocreditos.com.ar/comunidad/cdnicomercios2024/
# These are verified rates from authoritative sources
FALLBACK_RATES = {
    'debito': '0.8% + IVA',
    'credito': '1.8% + IVA',
    'clave_dni': '0.6% + IVA',
    'qr_saldo': '0.8% + IVA',
}

# Defines the mapping between data.json structure and scraped data
# Each mapping specifies what fee to look for on the page and where to put it in data.json
FEE_MAPPING = [
    {
        "json_concept": "Débito",
        "json_term": "48 hs",
        "page_keywords": ["débito", "debito", "debit", "d[ée]bito"],
        "rate_patterns": [
            # Pattern for: "Tarjetas de débito:</strong><br><span>Fiserv: 0,8% + IVA"
            r'tarjetas\s+de\s+d[ée]bito[^<]*<[^>]*>\s*[^:]*fiserv[^:]*:\s*(\d+[,\.]\d+)\s*%',
            # Simpler pattern without HTML tags in between
            r'tarjetas\s+de\s+d[ée]bito.*?fiserv[^:]*:\s*(\d+[,\.]\d+)\s*%',
            # Original patterns as fallback
            r'(?:débito|debito)[:\s]+(\d+[,\.]\d+)\s*%',
            r'(\d+[,\.]\d+)\s*%[^.]{0,40}(?:con\s+)?(?:tarjeta\s+de\s+)?d[ée]bito',
        ],
        "fallback_rate": FALLBACK_RATES['debito'],
        "expected_range": (0.7, 1.0),
    },
    {
        "json_concept": "Crédito",
        "json_term": "8-10 días hábiles",
        "page_keywords": ["crédito", "credito", "credit", "cr[ée]dito"],
        "rate_patterns": [
            # Pattern for: "Tarjetas de crédito en un pago: 1,8% + IVA"
            r'tarjetas\s+de\s+cr[ée]dito\s+en\s+un\s+pago[^:]*:\s*(\d+[,\.]\d+)\s*%',
            # Original patterns as fallback
            r'(?:crédito|credito)[:\s]+(\d+[,\.]\d+)\s*%',
            r'(\d+[,\.]\d+)\s*%[^.]{0,40}(?:con\s+)?(?:tarjeta\s+de\s+)?cr[ée]dito(?!\s+en\s+\d+)',
        ],
        "fallback_rate": FALLBACK_RATES['credito'],
        "expected_range": (1.7, 2.0),
    },
    {
        "json_concept": "Clave DNI (Token)",
        "json_term": "Inmediato",
        "page_keywords": ["clave dni", "clave dni token", "token"],
        "rate_patterns": [
            r'(?:clave\s+)?dni[:\s]+(\d+[,\.]\d+)\s*%(?!\s*-)',  # 0.6% not followed by dash
            r'clave\s+(?:dni\s+)?token[:\s]*(\d+[,\.]\d+)\s*%',
            r'(?:clave\s+)?dni\s+(?:token|inmediata)[^.]{0,50}(\d+[,\.]\d+)\s*%(?!\s*-)',
        ],
        "fallback_rate": FALLBACK_RATES['clave_dni'],
        "expected_range": (0.5, 0.7),
    },
    {
        "json_concept": "QR (Saldo en Cuenta)",
        "json_term": "Inmediato",
        "page_keywords": ["qr", "saldo en cuenta", "saldo"],
        "rate_patterns": [
            # Pattern for: "QR a través de débito en cuenta: 0,8% + IVA"
            r'qr\s+a\s+trav[ée]s\s+de\s+d[ée]bito\s+en\s+cuenta[^:]*:\s*(\d+[,\.]\d+)\s*%',
            # Original patterns as fallback
            r'qr[:\s]+(\d+[,\.]\d+)\s*%(?!\s*-)',  # 0.8% not followed by dash
            r'(?:qr|transferencia).*?saldo[^.]{0,50}(\d+[,\.]\d+)\s*%(?!\s*-)',
            r'saldo\s+en\s+cuenta[^.]{0,50}(\d+[,\.]\d+)\s*%(?!\s*-)',
        ],
        "fallback_rate": FALLBACK_RATES['qr_saldo'],
        "expected_range": (0.7, 0.9),
    },
]


def normalize_decimal_separator(rate_string):
    """
    Convert Argentine comma separator to international dot separator.

    Args:
        rate_string: Rate string that may contain comma (e.g., "0,8% + IVA")

    Returns:
        Normalized rate string with dot (e.g., "0.8% + IVA")
    """
    if not rate_string:
        return rate_string
    # Example: "0,8% + IVA" → "0.8% + IVA"
    return rate_string.replace(',', '.')


def scrape_bapro_fees(html_content):
    """
    Parses HTML from Banco Provincia adhesion page using defensive regex patterns.

    Searches for fee percentages associated with payment types (Débito, Crédito,
    Clave DNI, QR). Uses multiple regex patterns to handle variations in page
    structure and marketing copy formatting.

    Args:
        html_content: HTML string from Banco Provincia page

    Returns:
        List of dictionaries with 'payment_type', 'fee', and 'source' keys
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text(separator=' ', strip=True)

    scraped_fees = []

    for mapping in FEE_MAPPING:
        found = False

        # Try each regex pattern in order
        for pattern_idx, pattern in enumerate(mapping['rate_patterns'], 1):
            try:
                matches = list(re.finditer(pattern, text_content, re.IGNORECASE))

                if matches:
                    # Take first match for this pattern
                    match = matches[0]
                    fee_text = match.group(1).strip()

                    # Validate the extracted value
                    try:
                        fee_value = float(fee_text.replace(',', '.'))

                        # Check if within expected range
                        if mapping['expected_range']:
                            min_expected, max_expected = mapping['expected_range']
                            if not (min_expected <= fee_value <= max_expected):
                                # Out of range, skip this pattern
                                continue
                    except ValueError:
                        # Could not convert to float, skip
                        continue

                    # Format the fee string
                    if not fee_text.endswith('%'):
                        fee_text = f"{fee_text}%"

                    if '+ IVA' not in fee_text and '+ iva' not in fee_text:
                        fee_text = f"{fee_text} + IVA"

                    scraped_fees.append({
                        'payment_type': mapping['json_concept'],
                        'fee': fee_text,
                        'source': 'scraped',
                        'pattern': pattern_idx
                    })
                    found = True
                    print(f"  ✓ Found {mapping['json_concept']}: {fee_text} (pattern {pattern_idx})")
                    break

            except re.error as e:
                print(f"  ⚠ Regex error in pattern {pattern_idx}: {e}")
                continue

        if not found:
            print(f"  ℹ Could not scrape {mapping['json_concept']} fee (will use fallback)")

    return scraped_fees


def find_entity_by_id(data, entity_id):
    """
    Finds and returns an entity from data by its ID.

    Args:
        data: List of entity dictionaries
        entity_id: String ID to search for

    Returns:
        Entity dictionary if found, None otherwise
    """
    for entity in data:
        if entity.get('id') == entity_id:
            return entity
    return None


def find_fee_in_entity(entity_fees, concept, term):
    """
    Finds a specific fee entry in an entity's fees list.

    Args:
        entity_fees: List of fee dictionaries from entity
        concept: Exact concept string to match
        term: Exact term string to match

    Returns:
        Fee dictionary if found, None otherwise
    """
    for fee in entity_fees:
        if fee.get('concept') == concept and fee.get('term') == term:
            return fee
    return None


def validate_fee_value(rate_string, expected_range):
    """
    Validates that a numeric fee falls within expected range.

    Args:
        rate_string: Rate string (e.g., "0.8% + IVA")
        expected_range: Tuple (min, max) or None to skip validation

    Returns:
        Tuple (is_valid, numeric_value) or (False, None) if invalid
    """
    if not expected_range:
        # No validation needed
        return (True, None)

    match = re.search(r'(\d+[.,]\d+)', rate_string)
    if match:
        try:
            value = float(match.group(1).replace(',', '.'))
            min_expected, max_expected = expected_range
            is_valid = min_expected <= value <= max_expected
            return (is_valid, value)
        except ValueError:
            return (False, None)

    return (False, None)


def update_single_fee(fee_dict, new_rate):
    """
    Updates a single fee's rate if it differs from the current value.

    Args:
        fee_dict: Fee dictionary to update
        new_rate: New rate string to set

    Returns:
        True if fee was updated, False if already current
    """
    if fee_dict['rate'] != new_rate:
        print(f"  ✓ Updating '{fee_dict['concept']}' ({fee_dict['term']}): '{fee_dict['rate']}' → '{new_rate}'")
        fee_dict['rate'] = new_rate
        return True
    else:
        print(f"  ℹ Fee '{fee_dict['concept']}' ({fee_dict['term']}) already current: '{fee_dict['rate']}'")
        return False


def update_fees_in_data(data, scraped_fees):
    """
    Updates Banco Provincia fees in data.json.

    Logic:
    1. Try to find rate in scraped_fees
    2. If found and valid, use it
    3. If not found or invalid, use fallback (verified from research)
    4. Update data.json only if rate changed

    Args:
        data: Full data.json structure
        scraped_fees: List of fees scraped from Banco Provincia page

    Returns:
        Updated data if changes were made, None otherwise
    """
    bapro_entity = find_entity_by_id(data, BAPRO_ID)
    if not bapro_entity:
        print(f"✗ ERROR: Entity with id '{BAPRO_ID}' not found in {DATA_FILE}")
        return None

    something_was_updated = False

    for mapping in FEE_MAPPING:
        new_rate = None
        source = None

        # Try to find fee in scraped data
        for scraped_fee in scraped_fees:
            if scraped_fee['payment_type'] == mapping['json_concept']:
                # Validate the fee
                is_valid, value = validate_fee_value(
                    scraped_fee['fee'],
                    mapping['expected_range']
                )

                if is_valid or mapping['expected_range'] is None:
                    new_rate = normalize_decimal_separator(scraped_fee['fee'])
                    source = "scraped"
                    print(f"  Using scraped rate for '{mapping['json_concept']}': {new_rate}")
                else:
                    print(f"  ⚠ Scraped {mapping['json_concept']} value ({value}%) out of range. Using fallback.")
                break

        # Use fallback if not found in scraped data
        if not new_rate:
            new_rate = mapping['fallback_rate']
            source = "fallback (verified from research)"
            print(f"  Using verified fallback for '{mapping['json_concept']}': {new_rate}")

        # Find and update fee in data.json
        fee_dict = find_fee_in_entity(
            bapro_entity.get('fees', []),
            mapping['json_concept'],
            mapping['json_term']
        )

        if not fee_dict:
            print(f"  ⚠ Fee entry not found for '{mapping['json_concept']}' in data.json")
            print(f"    You may need to add this fee manually or update the fee structure.")
            continue

        was_updated = update_single_fee(fee_dict, new_rate)
        something_was_updated = something_was_updated or was_updated

    return data if something_was_updated else None


def update_date_in_html():
    """
    Updates the \"Actualizado\" date stamp in index.html to the current date.

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
            print(f"  ✓ Updated date stamp to: {current_date}")
            return True
        else:
            print(f"  ℹ Date stamp already current: {current_date}")
            return False

    except FileNotFoundError:
        print(f"  ⚠ Warning: {INDEX_FILE} not found, skipping date update")
        return False
    except Exception as e:
        print(f"  ⚠ Warning: Failed to update date in {INDEX_FILE}: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("Banco Provincia Fee Updater")
    print("=" * 70)
    print()

    try:
        # Step 1: Load current data.json
        print(f"1. Loading {DATA_FILE}...")
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
        print(f"   ✓ Successfully loaded {DATA_FILE}")
        print()

        # Step 2: Fetch Banco Provincia page
        print(f"2. Fetching Banco Provincia fees from:")
        print(f"   {PRIMARY_FEE_URL}")
        response = requests.get(
            PRIMARY_FEE_URL,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        response.raise_for_status()
        print(f"   ✓ Successfully fetched page")
        print()

        # Step 3: Scrape fees
        print(f"3. Parsing fees from page...")
        scraped_fees = scrape_bapro_fees(response.text)

        if not scraped_fees:
            print("   ℹ Info: No fees scraped from page (page structure may vary)")
            print("   Will use verified fallback rates from research_spanish.md")
        else:
            print(f"   ✓ Scraped {len(scraped_fees)} fee entry(entries)")
        print()

        # Step 4: Update data.json
        print(f"4. Updating {DATA_FILE}...")
        print("-" * 70)

        updated_data = update_fees_in_data(current_data, scraped_fees)

        print("-" * 70)
        print()

        if updated_data:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, indent=4, ensure_ascii=False)
            print(f"✓ {DATA_FILE} has been successfully updated.")
        else:
            print(f"✓ No fee changes detected. {DATA_FILE} remains unchanged.")

        print()

        # Step 5: Update date stamp in HTML
        print(f"5. Updating date stamp in {INDEX_FILE}...")
        update_date_in_html()

        print()
        print("=" * 70)
        print("✓ Script finished successfully.")
        print("=" * 70)
        print()
        print("NOTES:")
        print("  • Rates source: https://www.bancoprovincia.com.ar/web/adhesion_comercios")
        print("  • Fallback rates verified from: research_spanish.md (Table 2)")
        print("  • Splits Cuenta DNI into two distinct payment methods:")
        print("    - Clave DNI (Token): 0.6%")
        print("    - QR (Saldo en Cuenta): 0.8%")
        print("  • Decimal separators normalized to international format (dot)")
        print()

    except requests.exceptions.RequestException as e:
        print()
        print("=" * 70)
        print("✗ ERROR: Failed to fetch Banco Provincia page")
        print(f"  Reason: {e}")
        print("=" * 70)
        exit(1)

    except FileNotFoundError as e:
        print()
        print("=" * 70)
        print(f"✗ ERROR: File not found")
        print(f"  Reason: {e}")
        print("=" * 70)
        exit(1)

    except json.JSONDecodeError as e:
        print()
        print("=" * 70)
        print(f"✗ ERROR: Failed to parse {DATA_FILE}")
        print(f"  Reason: {e}")
        print("=" * 70)
        exit(1)

    except Exception as e:
        print()
        print("=" * 70)
        print(f"✗ ERROR: Unexpected error occurred")
        print(f"  Reason: {e}")
        print("=" * 70)
        exit(1)
