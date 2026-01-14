import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

DATA_FILE = 'data.json'
INDEX_FILE = 'index.html'
UALA_ID = 'uala'
PRIMARY_URL = 'https://mpos.ualabis.com.ar/productos/mpos/'
BACKUP_URL = 'https://www.ualabis.com.ar/'

# Defines the mapping between our data.json structure and the scraped data.
# Includes fallback rates for when scraping fails or fees aren't found.
FEE_MAPPING = [
    {
        "json_concept": "mPOS - Débito",
        "json_term": "En el momento",
        "page_keywords": ["débito", "debito"],
        "fallback_rate": "2.9% + IVA"
    },
    {
        "json_concept": "mPOS - Crédito",
        "json_term": "En el momento",
        "page_keywords": ["crédito", "credito"],
        "fallback_rate": "4.4% + IVA"
    },
    {
        "json_concept": "Link de Pago",
        "json_term": "En el momento",
        "page_keywords": ["link", "pago"],
        "fallback_rate": "4.4% + IVA"
    }
]

def normalize_fee_string(fee_text):
    """
    Normalizes fee text by removing 'desde' prefix and standardizing format.

    Examples:
        "Desde 2,9%" → "2.9"
        "2,9%" → "2.9"
    """
    # Remove "desde" prefix (case insensitive)
    fee_text = re.sub(r'^[Dd]esde\s+', '', fee_text.strip())

    # Convert comma decimals to dots (Spanish to standard format)
    fee_text = fee_text.replace(',', '.')

    # Remove % sign if present
    fee_text = fee_text.replace('%', '').strip()

    return fee_text

def scrape_fees_from_page(html_content):
    """
    Parses unstructured HTML to extract Ualá Bis fees from marketing copy.

    Returns:
        List of dicts with 'payment_type' and 'fee' keys
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    scraped_fees = []

    # Get all text content, preserving some structure
    full_text = soup.get_text(separator=' ', strip=True)

    # Pattern 1: Look for "X% con [tarjeta de] débito" (most specific)
    # Matches: "Desde 2,9% con tarjeta de débito" or "2,9% con débito"
    debit_pattern1 = r'(\d+[,\.]\d+)\s*%[^.]{0,30}(?:con\s+)?(?:tarjeta\s+de\s+)?d[ée]bito'
    match = re.search(debit_pattern1, full_text, re.IGNORECASE)
    if match:
        fee = normalize_fee_string(match.group(1))
        scraped_fees.append({
            'payment_type': 'débito',
            'fee': fee
        })
        print(f"  Found débito fee: {fee}% (using pattern 1)")

    # Pattern 2: Look for "X% con [tarjeta de] crédito" (most specific)
    # Matches: "4,4% con tarjeta de crédito" or "4,4% con crédito"
    credit_pattern1 = r'(\d+[,\.]\d+)\s*%[^.]{0,30}(?:con\s+)?(?:tarjeta\s+de\s+)?cr[ée]dito'
    match = re.search(credit_pattern1, full_text, re.IGNORECASE)
    if match:
        matched_text = match.group(0)
        # Make sure this isn't the débito rate being misidentified
        # Check if "débito" appears before "crédito" in the matched text
        if 'd[ée]bito' not in matched_text.lower():
            fee = normalize_fee_string(match.group(1))
            scraped_fees.append({
                'payment_type': 'crédito',
                'fee': fee
            })
            print(f"  Found crédito fee: {fee}% (using pattern 2)")

    # Link de Pago is rarely shown explicitly on Ualá pages, so it's okay if not found

    return scraped_fees

def update_fees_in_data(data, scraped_fees):
    """
    Updates Ualá fees in data.json based on scraped fees.
    Uses fallback rates from FEE_MAPPING when fees cannot be scraped.

    Returns:
        Updated data if changes were made, None otherwise
    """
    uala_entity = None
    for entity in data:
        if entity.get('id') == UALA_ID:
            uala_entity = entity
            break

    if not uala_entity:
        print(f"ERROR: Entity with id '{UALA_ID}' not found in {DATA_FILE}.")
        return None

    something_was_updated = False

    for mapping in FEE_MAPPING:
        # Try to find rate in scraped data
        new_rate = None

        for scraped_fee in scraped_fees:
            if any(kw in scraped_fee['payment_type'].lower()
                   for kw in mapping['page_keywords']):
                # Normalize: add "+ IVA" suffix
                new_rate = f"{scraped_fee['fee']}% + IVA"
                break

        # Use fallback if not found
        if not new_rate:
            new_rate = mapping['fallback_rate']
            print(f"WARN: Could not scrape '{mapping['json_concept']}' fee. Using fallback rate: {new_rate}")

        # Validate rate is reasonable (2-6% range)
        rate_match = re.search(r'(\d+\.?\d*)', new_rate)
        if rate_match:
            rate_value = float(rate_match.group(1))
            if not (2.0 <= rate_value <= 6.0):
                print(f"WARN: Unusual rate {rate_value}% for '{mapping['json_concept']}' (expected 2-6%)")

        # Update in data.json
        fee_updated_in_json = False
        for fee in uala_entity.get('fees', []):
            if (fee.get('concept') == mapping['json_concept'] and
                fee.get('term') == mapping['json_term']):
                if fee['rate'] != new_rate:
                    print(f"Updating '{fee['concept']}' ({fee['term']}): from '{fee['rate']}' to '{new_rate}'")
                    fee['rate'] = new_rate
                    something_was_updated = True
                else:
                    print(f"Fee '{fee['concept']}' ({fee['term']}) is already up to date: '{fee['rate']}'")
                fee_updated_in_json = True
                break

        if not fee_updated_in_json:
            print(f"WARN: Could not find a fee in data.json for concept '{mapping['json_concept']}' and term '{mapping['json_term']}'.")

    return data if something_was_updated else None

def update_fee_url_in_data(data):
    """
    Updates the feeUrl in data.json to point to a working page.
    The old URL (https://www.ualabis.com.ar/costos) returns 404.
    """
    NEW_FEE_URL = 'https://mpos.ualabis.com.ar/productos/mpos/'

    for entity in data:
        if entity.get('id') == UALA_ID:
            old_url = entity.get('feeUrl')
            if old_url != NEW_FEE_URL:
                print(f"Updating feeUrl: '{old_url}' → '{NEW_FEE_URL}'")
                entity['feeUrl'] = NEW_FEE_URL
                return True
            else:
                print(f"feeUrl is already up to date: '{NEW_FEE_URL}'")
    return False

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
            print(f"Warning: Could not find date pattern in {INDEX_FILE}")
            return False

        # Replace the date
        updated_html = re.sub(date_pattern, replacement, html_content)

        # Only write if something changed
        if updated_html != html_content:
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            print(f"Updated date stamp to: {current_date}")
            return True
        else:
            print(f"Date stamp already current: {current_date}")
            return False

    except FileNotFoundError:
        print(f"Warning: {INDEX_FILE} not found, skipping date update")
        return False
    except Exception as e:
        print(f"Warning: Failed to update date in {INDEX_FILE}: {e}")
        return False


if __name__ == "__main__":
    print("Starting Ualá fee update...")
    print()

    # Try primary URL first
    print(f"Fetching data from: {PRIMARY_URL}")
    scraped_fees = []

    try:
        response = requests.get(PRIMARY_URL, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        scraped_fees = scrape_fees_from_page(response.text)

        # If primary scraping failed, try backup URL
        if not scraped_fees:
            print(f"Primary source returned no fees. Trying backup: {BACKUP_URL}")
            print()
            response = requests.get(BACKUP_URL, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            scraped_fees = scrape_fees_from_page(response.text)

        # Log scraping results
        if scraped_fees:
            print(f"Successfully scraped {len(scraped_fees)} fee entries from the page.")
        else:
            print("WARNING: Could not scrape any fees from either source.")
            print("Will use fallback rates from FEE_MAPPING.")

        print()

        # Load data.json
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            current_data = json.load(f)

        # Update fees (will use fallbacks if scraped_fees is empty)
        updated_data = update_fees_in_data(current_data, scraped_fees)

        # Also update the broken feeUrl
        url_updated = update_fee_url_in_data(current_data)

        print()

        # Write changes if any
        if updated_data or url_updated:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, indent=4, ensure_ascii=False)
            print("data.json has been successfully updated.")
        else:
            print("No changes detected. data.json remains unchanged.")

        print()

        # Update date stamp (always run to show when script was executed)
        update_date_in_html()

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to fetch URL. Reason: {e}")
        exit(1)

    print()
    print("Script finished.")
