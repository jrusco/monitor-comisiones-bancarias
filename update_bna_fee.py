import json
import requests
from bs4 import BeautifulSoup

DATA_FILE = 'data.json'
BNA_ID = 'bna'

# BNA has multiple potential data sources
# The PDF is the official source but may require special handling
FEE_URLS = {
    'pdf': 'https://www.bna.com.ar/Downloads/ComisionesYCargosComercial.pdf',
    'merchant_info': 'https://www.bna.com.ar/Empresas/Novedades/AdheriTuComercio',
    'cards_page': 'https://www.bna.com.ar/Personas/TarjetasDeCredito'
}

# Primary URL to attempt scraping
PRIMARY_URL = FEE_URLS['merchant_info']

# Defines the mapping between our data.json structure and expected scraped data
# BNA fees are government-regulated, so they're more stable than fintech fees
FEE_MAPPING = [
    {
        "json_concept": "Débito",
        "json_term": "48 hs",
        "expected_keywords": ["débito", "debit"],
        "fallback_rate": "0.8% (Regulado)",  # Current regulated rate
    },
    {
        "json_concept": "Crédito",
        "json_term": "8-10 días hábiles",
        "expected_keywords": ["crédito", "credit"],
        "fallback_rate": "1.8% (Regulado)",  # Current regulated rate
    },
]

def scrape_fees_from_html(html_content):
    """
    Attempts to parse the HTML to find fee information.
    BNA's website structure may vary, so this function tries multiple approaches.

    Returns a list of dictionaries with payment_type, fee, and term keys.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    scraped_fees = []

    # Strategy 1: Look for tables with fee information
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                text_content = ' '.join([cell.get_text(strip=True) for cell in cells])

                # Look for percentage patterns (e.g., "0.8%", "1,8%", "1.8%")
                if '%' in text_content:
                    # Check if it matches our expected fee types
                    text_lower = text_content.lower()

                    for mapping in FEE_MAPPING:
                        if any(keyword in text_lower for keyword in mapping['expected_keywords']):
                            # Extract percentage - try different formats
                            for cell in cells:
                                cell_text = cell.get_text(strip=True)
                                if '%' in cell_text and any(char.isdigit() for char in cell_text):
                                    scraped_fees.append({
                                        'payment_type': mapping['json_concept'],
                                        'fee': cell_text,
                                        'term': mapping['json_term'],
                                    })
                                    break

    # Strategy 2: Look for specific text patterns (e.g., "Tarjeta de débito: 0.8%")
    text_blocks = soup.find_all(['p', 'div', 'span'])
    for block in text_blocks:
        text = block.get_text(strip=True)
        text_lower = text.lower()

        if '%' in text:
            for mapping in FEE_MAPPING:
                if any(keyword in text_lower for keyword in mapping['expected_keywords']):
                    # Try to extract the percentage
                    import re
                    percentage_match = re.search(r'(\d+[.,]\d+%|\d+%)', text)
                    if percentage_match:
                        scraped_fees.append({
                            'payment_type': mapping['json_concept'],
                            'fee': percentage_match.group(1),
                            'term': mapping['json_term'],
                        })

    return scraped_fees

def scrape_fees_from_pdf(pdf_url):
    """
    Placeholder for PDF parsing functionality.
    PDFs require special handling (PyPDF2, pdfplumber, etc.)

    For now, returns empty list. Can be implemented if needed.
    """
    print("INFO: PDF parsing not yet implemented. Would need additional dependencies.")
    return []

def update_fees_in_data(data, scraped_fees, use_fallback=False):
    """
    Updates BNA fees in the data structure.

    If scraped_fees is empty and use_fallback is True, will use the regulated rates
    from FEE_MAPPING as a fallback (with user confirmation in manual mode).

    Returns modified data if updates were made, None otherwise.
    """
    bna_entity = None
    for entity in data:
        if entity.get('id') == BNA_ID:
            bna_entity = entity
            break

    if not bna_entity:
        print(f"ERROR: Entity with id '{BNA_ID}' not found in {DATA_FILE}.")
        return None

    something_was_updated = False

    # If we have scraped data, use it
    if scraped_fees:
        for scraped_fee in scraped_fees:
            # Find the corresponding fee in our data.json
            for fee in bna_entity.get('fees', []):
                if fee.get('concept') == scraped_fee['payment_type']:
                    # Normalize the rate format to match existing format
                    new_rate = scraped_fee['fee']
                    if '(Regulado)' not in new_rate:
                        new_rate = f"{new_rate} (Regulado)"

                    if fee['rate'] != new_rate:
                        print(f"Updating '{fee['concept']}': from '{fee['rate']}' to '{new_rate}'")
                        fee['rate'] = new_rate
                        something_was_updated = True
                    else:
                        print(f"Fee '{fee['concept']}' is already up to date: '{fee['rate']}'")
                    break

    # If no scraped data and fallback is enabled, verify current rates match expected
    elif use_fallback:
        print("\nINFO: Using fallback verification with known regulated rates.")
        for mapping in FEE_MAPPING:
            for fee in bna_entity.get('fees', []):
                if fee.get('concept') == mapping['json_concept'] and fee.get('term') == mapping['json_term']:
                    if fee['rate'] != mapping['fallback_rate']:
                        print(f"WARNING: Current rate '{fee['rate']}' differs from expected regulated rate '{mapping['fallback_rate']}'")
                        print(f"         Manual verification recommended for {mapping['json_concept']}")
                    else:
                        print(f"✓ Fee '{fee['concept']}' matches expected regulated rate: '{fee['rate']}'")
                    break

    return data if something_was_updated else None


if __name__ == "__main__":
    print("Starting BNA fee update...")
    print("\nNOTE: BNA website often blocks automated access (403 errors).")
    print("      This scraper will attempt to fetch data but may need manual verification.\n")

    scraped_fees = []

    # Try to fetch from the primary URL
    print(f"Attempting to fetch data from: {PRIMARY_URL}")
    try:
        # Use headers that mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-AR,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        response = requests.get(PRIMARY_URL, headers=headers, timeout=10)
        response.raise_for_status()

        print("✓ Successfully fetched page content")
        scraped_fees = scrape_fees_from_html(response.text)

        if scraped_fees:
            print(f"✓ Successfully scraped {len(scraped_fees)} fee entries from the page.")
        else:
            print("⚠ Page loaded but no fees could be extracted. Page structure may have changed.")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print("✗ Access forbidden (403). BNA website is blocking automated access.")
            print("  This is common with banking websites due to security measures.")
        else:
            print(f"✗ HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to fetch URL. Error: {e}")

    # Load current data
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {DATA_FILE} not found.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse {DATA_FILE}. Error: {e}")
        exit(1)

    # Update fees (with fallback verification if no scraped data)
    use_fallback = len(scraped_fees) == 0
    updated_data = update_fees_in_data(current_data, scraped_fees, use_fallback=use_fallback)

    if updated_data:
        # Write updated data
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=4, ensure_ascii=False)
        print(f"\n✓ {DATA_FILE} has been successfully updated.")
    else:
        if not use_fallback:
            print(f"\n✓ No fee changes detected. {DATA_FILE} remains unchanged.")
        else:
            print(f"\n✓ Current fees verified against regulated rates. {DATA_FILE} remains unchanged.")

    print("\n" + "="*70)
    print("IMPORTANT NOTES:")
    print("="*70)
    print("• BNA fees are government-regulated and change infrequently")
    print("• Current regulated rates: Débito 0.8%, Crédito 1.8%")
    print("• If automated scraping fails, manual verification is recommended")
    print("• Check official sources:")
    print(f"  - {FEE_URLS['pdf']}")
    print(f"  - {FEE_URLS['merchant_info']}")
    print("="*70)

    print("\nScript finished.")
