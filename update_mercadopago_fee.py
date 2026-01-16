"""
Mercado Pago Fee Updater Script

Scrapes the official Mercado Pago fees pages for Buenos Aires province
and updates the corresponding entries in data.json.

This script fetches and updates:
1. Point fees (physical card reader): Débito instant, Crédito instant, Crédito 14 días
2. QR fees (code payments): Constructs fee range from all payment methods

Updated 2026-01-16:
- Now uses authoritative sources from mercadopago.com.ar/ayuda
  * Point: /ayuda/2779#tabla1
  * QR: /ayuda/3605#tabla1
- All rates are specific to Buenos Aires province
- QR fees are stored as a range "min% - max% (según medio)" in data.json
- Automatically updates date stamp in index.html after successful update
- Normalizes decimal separators from comma (Argentine) to dot (International)
  * Mercado Pago uses comma: "3,25%" → Converts to dot: "3.25%"
  * Ensures consistent formatting across all data.json entries
"""

import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

DATA_FILE = 'data.json'
INDEX_FILE = 'index.html'
MP_ID = 'mercadopago'

# Official Mercado Pago fees pages (Buenos Aires province rates)
# Updated 2026-01-15: Using authoritative sources with direct anchor to fee tables
POINT_FEE_URL = 'https://www.mercadopago.com.ar/ayuda/2779'  # Point (physical card reader)
QR_FEE_URL = 'https://www.mercadopago.com.ar/ayuda/3605'     # QR (code payments)
# Note: #tabla1 anchor not needed for HTTP requests, only for browser navigation

# Defines the mapping between our data.json structure and the scraped data.
# NOTE: These rates are specific to Buenos Aires province. Mercado Pago applies
# differentiated rates by province. See research_spanish.md for regional details.

# POINT FEE MAPPINGS (from ayuda/2779)
POINT_FEE_MAPPING = [
    {
        "source": "point",
        "json_concept": "Point - Débito",
        "json_term": "En el momento",
        "page_payment_type": "Tarjeta de débito",
        "page_term": "Al instante",
    },
    {
        "source": "point",
        "json_concept": "Point - Crédito",
        "json_term": "En el momento",
        "page_payment_type": "Tarjeta de crédito",
        "page_term": "Al instante",
    },
    {
        "source": "point",
        "json_concept": "Point - Crédito",
        "json_term": "14 días",
        "page_payment_type": "Tarjeta de crédito",
        "page_term": "10 días",  # Mapping discrepancy: site shows "10 días" but we keep "14 días" in data.json for consistency
    },
]

# QR FEE MAPPINGS (from ayuda/3605)
# QR fees in data.json are stored as a range because they vary by payment method
# We scrape all QR payment methods and construct the range "min% - max% (según medio)"
QR_FEE_MAPPING = [
    {
        "source": "qr",
        "json_concept": "QR",
        "json_term": "En el momento",
        "parse_as_range": True,  # Special flag: construct range from all scraped QR fees
    },
]

# Combined mapping for backward compatibility
FEE_MAPPING = POINT_FEE_MAPPING + QR_FEE_MAPPING


def normalize_decimal_separator(rate_string):
    """
    Convert Argentine comma separator to international dot separator.

    Args:
        rate_string: Rate string that may contain comma (e.g., "3,25% + IVA")

    Returns:
        Normalized rate string with dot (e.g., "3.25% + IVA")
    """
    if not rate_string:
        return rate_string
    # Example: "3,25% + IVA" → "3.25% + IVA"
    return rate_string.replace(',', '.')


def scrape_fees_from_page(html_content):
    """
    Parses the HTML to find all fees in the main table and returns them as a structured list.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    scraped_fees = []

    table_div = soup.find('div', id='tabla1')
    if not table_div:
        print("WARN: Could not find the fees table (id='tabla1'). The page structure may have changed.")
        return scraped_fees
        
    table = table_div.find('table')
    if not table:
        print("WARN: Found the table div but no table inside. The page structure may have changed.")
        return scraped_fees

    rows = table.find('tbody').find_all('tr')
    
    current_payment_type = None
    for row in rows:
        cells = row.find_all('td')
        
        # Rows with 3 cells define a new payment type
        if len(cells) == 3:
            current_payment_type = cells[0].get_text(strip=True)
            fee = cells[1].get_text(strip=True)
            term = cells[2].get_text(strip=True)
        # Rows with 2 cells belong to the previous payment type (due to rowspan)
        elif len(cells) == 2:
            fee = cells[0].get_text(strip=True)
            term = cells[1].get_text(strip=True)
        else:
            continue

        if current_payment_type and '%' in fee:
            scraped_fees.append({
                'payment_type': current_payment_type,
                'fee': fee,
                'term': term
            })

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


def find_scraped_fee(scraped_fees, payment_type, term):
    """
    Finds a matching scraped fee by payment type and term.

    Args:
        scraped_fees: List of scraped fee dictionaries
        payment_type: String to match in payment_type field
        term: Exact term string to match

    Returns:
        Formatted rate string "{fee} + IVA" with normalized decimal separator,
        or None if not found
    """
    for scraped_fee in scraped_fees:
        if payment_type in scraped_fee['payment_type'] and term == scraped_fee['term']:
            rate = f"{scraped_fee['fee']} + IVA"
            # Normalize decimal separator from comma to dot
            return normalize_decimal_separator(rate)
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
        print(f"Updating '{fee_dict['concept']}' ({fee_dict['term']}): from '{fee_dict['rate']}' to '{new_rate}'")
        fee_dict['rate'] = new_rate
        return True
    else:
        print(f"Fee '{fee_dict['concept']}' ({fee_dict['term']}) is already up to date: '{fee_dict['rate']}'")
        return False


def construct_qr_fee_range(scraped_fees):
    """
    Constructs a fee range string from all scraped QR fees.

    Args:
        scraped_fees: List of scraped fee dictionaries (all from QR page)

    Returns:
        String in format "min% - max% (según medio)" with normalized decimal
        separators, or None if no fees found
    """
    if not scraped_fees:
        return None

    # Extract numeric fee values (e.g., "3,25%" -> 3.25)
    fee_values = []
    for fee in scraped_fees:
        fee_text = fee.get('fee', '')
        # Extract number before % sign, handle both comma and dot as decimal separator
        match = re.search(r'(\d+[,.]?\d*)\s*%', fee_text)
        if match:
            numeric_value = float(match.group(1).replace(',', '.'))
            fee_values.append((numeric_value, fee_text))

    if not fee_values:
        return None

    # Find min and max
    min_fee = min(fee_values, key=lambda x: x[0])
    max_fee = max(fee_values, key=lambda x: x[0])

    # Construct range string
    if min_fee[0] == max_fee[0]:
        # All fees are the same
        result = f"{min_fee[1]} + IVA"
    else:
        # Create range
        result = f"{min_fee[1]} - {max_fee[1]} + IVA (según medio)"

    # Normalize decimal separator from comma to dot
    return normalize_decimal_separator(result)


def process_single_mapping(mapping, scraped_fees, mp_entity):
    """
    Processes a single fee mapping: finds scraped fee, finds entity fee, and updates.

    Args:
        mapping: Single mapping dictionary from FEE_MAPPING
        scraped_fees: List of all scraped fees
        mp_entity: Mercado Pago entity dictionary

    Returns:
        True if any update was made, False otherwise
    """
    # Special handling for QR range mapping
    if mapping.get('parse_as_range'):
        new_rate = construct_qr_fee_range(scraped_fees)
        if not new_rate:
            print(f"WARN: Could not construct QR fee range from scraped data. Skipping.")
            return False
    else:
        # Standard mapping: find specific fee by payment type and term
        new_rate = find_scraped_fee(
            scraped_fees,
            mapping['page_payment_type'],
            mapping['page_term']
        )

        if not new_rate:
            print(f"WARN: Could not find a matching scraped fee for {mapping['json_concept']} - {mapping['json_term']}. Skipping.")
            return False

    # Find the corresponding fee in data.json
    fee_dict = find_fee_in_entity(
        mp_entity.get('fees', []),
        mapping['json_concept'],
        mapping['json_term']
    )

    if not fee_dict:
        print(f"WARN: Could not find a fee in data.json for concept '{mapping['json_concept']}' and term '{mapping['json_term']}'.")
        return False

    # Update the fee if needed
    return update_single_fee(fee_dict, new_rate)


def update_fees_in_data(data, point_scraped_fees, qr_scraped_fees):
    """
    Reads the data file, updates all mapped fees, and returns the modified data.

    Args:
        data: Loaded data.json content
        point_scraped_fees: Fees scraped from Point page
        qr_scraped_fees: Fees scraped from QR page

    Returns:
        Modified data if updates were made, None otherwise
    """
    # Find Mercado Pago entity
    mp_entity = find_entity_by_id(data, MP_ID)
    if not mp_entity:
        print(f"ERROR: Entity with id '{MP_ID}' not found in {DATA_FILE}.")
        return None

    # Process each mapping and track if anything was updated
    something_was_updated = False

    for mapping in FEE_MAPPING:
        # Select appropriate scraped fees based on source
        if mapping.get('source') == 'qr':
            scraped_fees = qr_scraped_fees
        else:  # default to point
            scraped_fees = point_scraped_fees

        was_updated = process_single_mapping(mapping, scraped_fees, mp_entity)
        something_was_updated = something_was_updated or was_updated

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
    print("Starting Mercado Pago fee update...")
    print("=" * 70)

    try:
        # Scrape Point fees
        print(f"\n1. Fetching Point fees from: {POINT_FEE_URL}")
        point_response = requests.get(POINT_FEE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        point_response.raise_for_status()

        point_scraped_fees = scrape_fees_from_page(point_response.text)

        if not point_scraped_fees:
            print("WARNING: Could not extract any Point fees from the page.")
            point_scraped_fees = []
        else:
            print(f"✓ Successfully scraped {len(point_scraped_fees)} Point fee entries")

        # Scrape QR fees
        print(f"\n2. Fetching QR fees from: {QR_FEE_URL}")
        qr_response = requests.get(QR_FEE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        qr_response.raise_for_status()

        qr_scraped_fees = scrape_fees_from_page(qr_response.text)

        if not qr_scraped_fees:
            print("WARNING: Could not extract any QR fees from the page.")
            qr_scraped_fees = []
        else:
            print(f"✓ Successfully scraped {len(qr_scraped_fees)} QR fee entries")

        # Check if we got any fees at all
        if not point_scraped_fees and not qr_scraped_fees:
            print("\nERROR: Could not extract any fees from either page. No changes were made.")
            exit(1)

        # Update data.json
        print(f"\n3. Updating {DATA_FILE}...")
        print("-" * 70)

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            current_data = json.load(f)

        updated_data = update_fees_in_data(current_data, point_scraped_fees, qr_scraped_fees)

        print("-" * 70)

        if updated_data:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, indent=4, ensure_ascii=False)
            print(f"\n✓ {DATA_FILE} has been successfully updated.")
        else:
            print(f"\n✓ No fee changes detected. {DATA_FILE} remains unchanged.")

        # Update date stamp in HTML
        print(f"\n4. Updating date stamp in {INDEX_FILE}...")
        update_date_in_html()

        print("\n" + "=" * 70)
        print("Script finished successfully.")

    except requests.exceptions.RequestException as e:
        print(f"\nERROR: Failed to fetch URL. Reason: {e}")
        exit(1)
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        exit(1)

