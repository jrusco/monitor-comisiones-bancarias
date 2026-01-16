"""
BNA Fee Updater - Fiserv Authoritative Source

This script scrapes BCRA-regulated merchant acquiring fees from Fiserv Argentina
(the infrastructure provider for BNA) and updates data.json with current rates.

Unlike other entities, BNA does not publish specific merchant acquiring rate
schedules publicly on their own site. However, BNA uses Fiserv infrastructure
for payment processing, and Fiserv publishes the BCRA-regulated rates at:
  https://aranceles.fiservargentina.com/

These rates are legally mandated caps set by Argentina's Central Bank (BCRA):
  - Debit cards: 0.8% + IVA (maximum regulated rate)
  - Credit cards: 1.8% + IVA (maximum regulated rate)

Updated 2026-01-16:
- Now uses authoritative Fiserv source: https://aranceles.fiservargentina.com/
- Scrapes actual rates instead of hardcoding values
- Converts Argentine comma separator to international dot separator
- Follows update_mercadopago_fee.py pattern for consistency
"""

import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

DATA_FILE = 'data.json'
INDEX_FILE = 'index.html'
BNA_ID = 'bna'

# Authoritative source: Fiserv Argentina (BNA's infrastructure provider)
FISERV_FEE_URL = 'https://aranceles.fiservargentina.com/'

# Defines the mapping between data.json structure and scraped data
# These are the primary fees we scrape from Fiserv
FEE_MAPPING = [
    {
        "json_concept": "Débito",
        "json_term": "24 hs",
        "page_payment_type": "Débito",
    },
    {
        "json_concept": "Crédito",
        "json_term": "8-10 días hábiles",
        "page_payment_type": "Crédito",
    },
    {
        "json_concept": "Mantenimiento Terminal",
        "json_term": "Mensual",
        "static_rate": "Bonificado o Variable",  # Not on Fiserv page, keep as static
    }
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


def scrape_fiserv_fees(html_content):
    """
    Parses HTML from Fiserv to extract BCRA-regulated rates.

    Fiserv publishes rates in a card/box layout with sections for different
    payment types (Débito, Crédito, etc.). This function searches for these
    text labels and extracts the associated percentages.

    Args:
        html_content: HTML string from Fiserv page

    Returns:
        List of dictionaries with 'payment_type', 'fee', and 'term' keys
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    scraped_fees = []

    # Get text content to search for payment types and rates
    text_content = soup.get_text()

    # Strategy: Find all percentages in the page, then match them to Débito/Crédito
    # Extract all percentages with their positions
    percentage_matches = list(re.finditer(r'(\d+[,.]?\d*)\s*%', text_content))

    if percentage_matches:
        # Find position of "Débito" and "Crédito" labels
        # Note: Handle potential encoding issues with accented characters
        # (the page may contain "DÃ©bito" or "Débito" depending on encoding)
        debito_positions = [m.start() for m in re.finditer(r'[Dd](?:Ã©|é)bito|[Dd]ebito', text_content)]
        credito_positions = [m.start() for m in re.finditer(r'[Cc](?:rÃ©|ré)dito|[Cc]redito', text_content)]

        # Find percentages closest to Débito (should be ~0.8%)
        if debito_positions:
            # Find percentage closest to the first Débito position
            debito_pos = debito_positions[0]
            closest_debit_percentage = None
            closest_distance = float('inf')

            for match in percentage_matches:
                distance = abs(match.start() - debito_pos)
                # Only consider percentages within 300 characters of Débito label
                if distance < 300 and distance < closest_distance:
                    fee_value = float(match.group(1).replace(',', '.'))
                    # Should be < 1.0 for debit
                    if fee_value < 1.0:
                        closest_debit_percentage = match.group(1)
                        closest_distance = distance

            if closest_debit_percentage:
                scraped_fees.append({
                    'payment_type': 'Débito',
                    'fee': f'{closest_debit_percentage}%',
                    'term': '24 horas hábiles'
                })

        # Find percentages closest to Crédito (should be ~1.8%)
        if credito_positions:
            # Find percentage closest to the first Crédito position
            credito_pos = credito_positions[0]
            closest_credit_percentage = None
            closest_distance = float('inf')

            for match in percentage_matches:
                distance = abs(match.start() - credito_pos)
                # Only consider percentages within 300 characters of Crédito label
                if distance < 300 and distance < closest_distance:
                    fee_value = float(match.group(1).replace(',', '.'))
                    # Should be > 1.0 for credit
                    if fee_value > 1.0:
                        closest_credit_percentage = match.group(1)
                        closest_distance = distance

            if closest_credit_percentage:
                scraped_fees.append({
                    'payment_type': 'Crédito',
                    'fee': f'{closest_credit_percentage}%',
                    'term': '8-10 días hábiles'
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


def find_scraped_fee_by_type(scraped_fees, payment_type):
    """
    Finds a scraped fee by payment type (Débito, Crédito, etc.).

    Args:
        scraped_fees: List of scraped fee dictionaries
        payment_type: String payment type to match

    Returns:
        Fee text with IVA suffix and normalized decimal separator,
        or None if not found
    """
    for scraped_fee in scraped_fees:
        if payment_type.lower() in scraped_fee['payment_type'].lower():
            fee_text = f"{scraped_fee['fee']} + IVA"
            # Apply decimal separator normalization
            return normalize_decimal_separator(fee_text)
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
        print(f"  ✓ Updating '{fee_dict['concept']}' ({fee_dict['term']}): '{fee_dict['rate']}' → '{new_rate}'")
        fee_dict['rate'] = new_rate
        return True
    else:
        print(f"  ℹ Fee '{fee_dict['concept']}' ({fee_dict['term']}) already current: '{fee_dict['rate']}'")
        return False


def update_fees_in_data(data, scraped_fees):
    """
    Updates BNA fees in data.json with scraped values.

    Args:
        data: Full data.json structure
        scraped_fees: List of fees scraped from Fiserv

    Returns:
        Updated data if changes were made, None otherwise
    """
    bna_entity = find_entity_by_id(data, BNA_ID)
    if not bna_entity:
        print(f"✗ ERROR: Entity with id '{BNA_ID}' not found in {DATA_FILE}")
        return None

    something_was_updated = False

    # Process each mapping
    for mapping in FEE_MAPPING:
        # Handle static rates (not scraped from Fiserv)
        if 'static_rate' in mapping:
            new_rate = mapping['static_rate']
            print(f"  Using static rate for {mapping['json_concept']}: {new_rate}")

            # Find and update the fee in data.json
            fee_dict = find_fee_in_entity(
                bna_entity.get('fees', []),
                mapping['json_concept'],
                mapping['json_term']
            )

            if fee_dict:
                was_updated = update_single_fee(fee_dict, new_rate)
                something_was_updated = something_was_updated or was_updated
            continue

        # For scraped rates, find the matching fee from Fiserv
        new_rate = find_scraped_fee_by_type(scraped_fees, mapping['page_payment_type'])

        if not new_rate:
            print(f"  ⚠ WARN: Could not find {mapping['json_concept']} rate from Fiserv. Skipping.")
            continue

        # Validate the rate is within expected range
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
        fee_dict = find_fee_in_entity(
            bna_entity.get('fees', []),
            mapping['json_concept'],
            mapping['json_term']
        )

        if not fee_dict:
            print(f"  ⚠ WARN: Could not find fee entry for '{mapping['json_concept']}' ({mapping['json_term']}) in data.json")
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
    print("BNA Fee Updater (Fiserv Authoritative Source)")
    print("=" * 70)
    print()

    try:
        # Step 1: Load current data.json
        print(f"1. Loading {DATA_FILE}...")
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
        print(f"   ✓ Successfully loaded {DATA_FILE}")
        print()

        # Step 2: Fetch and scrape Fiserv page
        print(f"2. Fetching Fiserv fees from: {FISERV_FEE_URL}")
        fiserv_response = requests.get(
            FISERV_FEE_URL,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        fiserv_response.raise_for_status()
        print(f"   ✓ Successfully fetched Fiserv page")
        print()

        # Step 3: Parse fees from HTML
        print(f"3. Parsing BCRA-regulated rates from Fiserv...")
        scraped_fees = scrape_fiserv_fees(fiserv_response.text)

        if not scraped_fees:
            print("   ✗ ERROR: Could not extract any fees from Fiserv page.")
            print("   The page structure may have changed. Please check the HTML manually.")
            exit(1)
        else:
            print(f"   ✓ Successfully scraped {len(scraped_fees)} fee entries:")
            for fee in scraped_fees:
                print(f"      - {fee['payment_type']}: {fee['fee']} (Settlement: {fee['term']})")
        print()

        # Step 4: Update data.json
        print(f"4. Updating {DATA_FILE} with scraped values...")
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
        print("  • Rates sourced from: https://aranceles.fiservargentina.com/")
        print("  • These are BCRA-regulated maximum rates for BNA")
        print("  • Decimal separators normalized to international format (dot)")
        print("  • Rates include IVA as per Fiserv publication")
        print()

    except requests.exceptions.RequestException as e:
        print()
        print("=" * 70)
        print("✗ ERROR: Failed to fetch Fiserv URL")
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
