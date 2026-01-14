"""
BNA Fee Updater - BCRA Regulated Rates

This script updates BNA (Banco de la Nación Argentina) merchant acquiring fees in data.json.

Unlike other entities, BNA does not publish specific merchant acquiring rate schedules publicly.
As a government-regulated bank, BNA charges the maximum rates permitted by Argentina's
Central Bank (BCRA):
  - Debit cards: 0.8% (maximum regulated rate)
  - Credit cards: 1.8% (maximum regulated rate)

These rates are hardcoded as they are legally mandated caps that rarely change.
No PDF scraping is performed - the script simply validates and updates the data structure
with the correct regulated rates.
"""

import json
import re
from datetime import datetime

DATA_FILE = 'data.json'
INDEX_FILE = 'index.html'
BNA_ID = 'bna'

# Defines the BCRA-regulated rates for BNA merchant acquiring
# These are the maximum rates permitted by Argentina's Central Bank
FEE_MAPPING = [
    {
        "json_concept": "Débito",
        "json_term": "48 hs",
        "regulated_rate": "0.8% (Regulado)",
    },
    {
        "json_concept": "Crédito",
        "json_term": "8-10 días hábiles",
        "regulated_rate": "1.8% (Regulado)",
    },
    {
        "json_concept": "Mantenimiento Terminal",
        "json_term": "Mensual",
        "regulated_rate": "Bonificado o Variable",
    }
]


def update_fees_in_data(data):
    """
    Updates BNA fees in the data structure with BCRA-regulated rates.

    Args:
        data: The full data.json structure

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
        # Use BCRA-regulated rate
        new_rate = mapping['regulated_rate']
        print(f"  Using BCRA-regulated rate for {mapping['json_concept']}: {new_rate}")

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
    print("BNA Fee Updater (BCRA Regulated Rates)")
    print("="*70)
    print()

    try:
        # Step 1: Load current data.json
        print(f"Loading {DATA_FILE}...")
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
        print(f"✓ Successfully loaded {DATA_FILE}")
        print()

        # Step 2: Update fees with BCRA-regulated rates
        print("Applying BCRA-regulated rates...")
        updated_data = update_fees_in_data(current_data)
        print()

        # Step 3: Write changes if any
        if updated_data:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, indent=4, ensure_ascii=False)
            print("="*70)
            print("✓ SUCCESS: data.json has been updated with BNA fees")
            print("="*70)
        else:
            print("="*70)
            print("✓ No changes needed: All fees are already up to date")
            print("="*70)

        # Step 4: Update date stamp in HTML (always update to reflect when script was run)
        print()
        update_date_in_html()

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
    print("  • BNA rates are set to BCRA-regulated maximums")
    print("  • Regulated rates: Débito 0.8%, Crédito 1.8%")
    print("  • These are legally mandated caps by Argentina's Central Bank")
    print("  • Rates rarely change as they are government-controlled")
    print("  • BNA does not publish specific merchant acquiring rate schedules")
    print()
    print("Script finished successfully.")
