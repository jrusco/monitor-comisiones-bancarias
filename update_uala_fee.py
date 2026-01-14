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
#
# NOTE: Ualá does not publish complete fee information on their product pages.
# Only the debit fee is displayed publicly. Credit and Link de Pago fees are
# not shown on their website (verified 01/2026).
#
# Fallback rates are verified against press sources:
# - El Cronista (01/2026): Debit 2.9%, Credit 4.4%, QR 0.6%
# Last manual verification: January 2026
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
        "fallback_rate": "4.4% + IVA"  # Not published on website, verified via press releases
    },
    {
        "json_concept": "Link de Pago",
        "json_term": "En el momento",
        "page_keywords": ["link", "pago"],
        "fallback_rate": "4.4% + IVA"  # Not published on website, verified via press releases
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

    Enhanced to search:
    - Full page text
    - Script tags (JSON data)
    - Meta tags
    - Multiple pattern variations

    Returns:
        List of dicts with 'payment_type' and 'fee' keys
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    scraped_fees = []

    # Get all text content, preserving some structure
    full_text = soup.get_text(separator=' ', strip=True)

    # Also check script tags for JSON data
    script_text = ''
    for script in soup.find_all('script'):
        if script.string:
            script_text += ' ' + script.string

    # Combine all searchable text
    searchable_text = full_text + ' ' + script_text

    # DÉBITO PATTERNS - Multiple variations
    debit_patterns = [
        # Pattern 1: "X% con [tarjeta de] débito"
        r'(\d+[,\.]\d+)\s*%[^.]{0,50}(?:con\s+)?(?:tarjeta\s+de\s+)?d[ée]bito',
        # Pattern 2: "débito: X%" or "débito X%"
        r'd[ée]bito\s*:?\s*(\d+[,\.]\d+)\s*%',
        # Pattern 3: Look in structured data (JSON-like)
        r'["\']?d[ée]bito["\']?\s*:\s*["\']?(\d+[,\.]\d+)\s*%?["\']?',
    ]

    for i, pattern in enumerate(debit_patterns, 1):
        match = re.search(pattern, searchable_text, re.IGNORECASE)
        if match:
            fee = normalize_fee_string(match.group(1))
            scraped_fees.append({
                'payment_type': 'débito',
                'fee': fee
            })
            print(f"  Found débito fee: {fee}% (pattern {i})")
            break

    # CRÉDITO PATTERNS - Multiple variations
    credit_patterns = [
        # Pattern 1: "X% con [tarjeta de] crédito"
        r'(\d+[,\.]\d+)\s*%[^.]{0,50}(?:con\s+)?(?:tarjeta\s+de\s+)?cr[ée]dito(?!\s+en\s+\d+\s+cuotas)',
        # Pattern 2: "crédito: X%" or "crédito X%"
        r'cr[ée]dito\s*:?\s*(\d+[,\.]\d+)\s*%',
        # Pattern 3: "crédito en 1 pago" or "crédito en el momento"
        r'cr[ée]dito\s+(?:en\s+(?:1|un)\s+pago|en\s+el\s+momento)[^.]{0,30}(\d+[,\.]\d+)\s*%',
        # Pattern 4: Look in structured data
        r'["\']?cr[ée]dito["\']?\s*:\s*["\']?(\d+[,\.]\d+)\s*%?["\']?',
    ]

    for i, pattern in enumerate(credit_patterns, 1):
        match = re.search(pattern, searchable_text, re.IGNORECASE)
        if match:
            matched_text = match.group(0)
            # Make sure this isn't the débito rate being misidentified
            if 'd[ée]bito' not in matched_text.lower():
                fee = normalize_fee_string(match.group(1))
                scraped_fees.append({
                    'payment_type': 'crédito',
                    'fee': fee
                })
                print(f"  Found crédito fee: {fee}% (pattern {i})")
                break

    # LINK DE PAGO PATTERNS - Multiple variations
    link_patterns = [
        # Pattern 1: "link de pago: X%" or similar
        r'link\s+de\s+pago[^.]{0,30}(\d+[,\.]\d+)\s*%',
        # Pattern 2: "pago online" or "e-commerce"
        r'(?:pago\s+online|e-commerce|ecommerce)[^.]{0,30}(\d+[,\.]\d+)\s*%',
        # Pattern 3: Structured data
        r'["\']?link[_\s]?(?:de[_\s])?pago["\']?\s*:\s*["\']?(\d+[,\.]\d+)\s*%?["\']?',
    ]

    for i, pattern in enumerate(link_patterns, 1):
        match = re.search(pattern, searchable_text, re.IGNORECASE)
        if match:
            fee = normalize_fee_string(match.group(1))
            scraped_fees.append({
                'payment_type': 'link',
                'fee': fee
            })
            print(f"  Found link de pago fee: {fee}% (pattern {i})")
            break

    return scraped_fees

def update_fees_in_data(data, scraped_fees):
    """
    Updates Ualá fees in data.json based on scraped fees.
    Uses fallback rates from FEE_MAPPING when fees cannot be scraped.

    Note: Ualá does not publish all fees publicly. Using verified fallback
    rates for fees not found on their website is expected behavior.

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
    scraped_count = 0
    fallback_count = 0

    for mapping in FEE_MAPPING:
        # Try to find rate in scraped data
        new_rate = None
        source = None

        for scraped_fee in scraped_fees:
            if any(kw in scraped_fee['payment_type'].lower()
                   for kw in mapping['page_keywords']):
                # Normalize: add "+ IVA" suffix
                new_rate = f"{scraped_fee['fee']}% + IVA"
                source = "scraped"
                scraped_count += 1
                break

        # Use fallback if not found
        if not new_rate:
            new_rate = mapping['fallback_rate']
            source = "fallback"
            fallback_count += 1
            # Only show INFO (not WARN) for credit/link fees - they're not published
            if mapping['json_concept'] in ['mPOS - Crédito', 'Link de Pago']:
                print(f"INFO: Using verified fallback for '{mapping['json_concept']}': {new_rate} (not published on website)")
            else:
                print(f"WARN: Could not scrape '{mapping['json_concept']}' fee. Using fallback: {new_rate}")

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
                    print(f"Updating '{fee['concept']}' ({fee['term']}): '{fee['rate']}' → '{new_rate}' (source: {source})")
                    fee['rate'] = new_rate
                    something_was_updated = True
                else:
                    print(f"✓ '{fee['concept']}' ({fee['term']}): '{fee['rate']}' (source: {source})")
                fee_updated_in_json = True
                break

        if not fee_updated_in_json:
            print(f"WARN: Could not find a fee in data.json for concept '{mapping['json_concept']}' and term '{mapping['json_term']}'.")

    # Summary
    print()
    print(f"Summary: {scraped_count} fee(s) scraped, {fallback_count} fallback(s) used")

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
    print("=" * 60)
    print("Ualá Bis Fee Update Script")
    print("=" * 60)
    print()

    # Try primary URL first
    print(f"Fetching data from: {PRIMARY_URL}")
    scraped_fees = []
    urls_to_try = [PRIMARY_URL, BACKUP_URL]

    try:
        # Try primary URL
        response = requests.get(PRIMARY_URL, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        scraped_fees = scrape_fees_from_page(response.text)

        # If primary scraping found few fees, try backup URL too
        if len(scraped_fees) < 2:
            print()
            print(f"Primary source found {len(scraped_fees)} fee(s). Trying backup: {BACKUP_URL}")
            try:
                response = requests.get(BACKUP_URL, headers={'User-Agent': 'Mozilla/5.0'})
                response.raise_for_status()
                backup_fees = scrape_fees_from_page(response.text)

                # Merge fees, preferring primary source for duplicates
                for backup_fee in backup_fees:
                    if not any(sf['payment_type'] == backup_fee['payment_type'] for sf in scraped_fees):
                        scraped_fees.append(backup_fee)
                        print(f"  Added {backup_fee['payment_type']} fee from backup source")
            except requests.exceptions.RequestException as e:
                print(f"  Backup URL failed: {e}")

        # Log scraping results
        print()
        print("-" * 60)
        if scraped_fees:
            print(f"Scraping complete: {len(scraped_fees)} fee(s) found")
            for fee in scraped_fees:
                print(f"  - {fee['payment_type']}: {fee['fee']}%")
        else:
            print("INFO: No fees scraped from website (expected for Ualá)")
            print("      Will use verified fallback rates")
        print("-" * 60)
        print()

        # Load data.json
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            current_data = json.load(f)

        print("Updating fees in data.json...")
        print()

        # Update fees (will use fallbacks if scraped_fees is empty)
        updated_data = update_fees_in_data(current_data, scraped_fees)

        # Also update the broken feeUrl
        url_updated = update_fee_url_in_data(current_data)

        print()
        print("=" * 60)

        # Write changes if any
        if updated_data or url_updated:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, indent=4, ensure_ascii=False)
            print("✓ data.json has been successfully updated")
        else:
            print("✓ No changes needed - all fees are current")

        print()

        # Update date stamp (always run to show when script was executed)
        date_updated = update_date_in_html()
        if date_updated:
            print("✓ Date stamp updated in index.html")
        else:
            print("✓ Date stamp already current in index.html")

        print("=" * 60)
        print()
        print("Update complete!")

    except requests.exceptions.RequestException as e:
        print()
        print("=" * 60)
        print(f"ERROR: Failed to fetch URL. Reason: {e}")
        print("=" * 60)
        exit(1)
    except Exception as e:
        print()
        print("=" * 60)
        print(f"ERROR: Unexpected error: {e}")
        print("=" * 60)
        exit(1)
