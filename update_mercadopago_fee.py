import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

DATA_FILE = 'data.json'
INDEX_FILE = 'index.html'
MP_ID = 'mercadopago'
# This is the specific page for Point fees, not the generic one.
FEE_URL = 'https://www.mercadopago.com.ar/ayuda/2779'

# Defines the mapping between our data.json structure and the scraped data.
FEE_MAPPING = [
    {
        "json_concept": "Point - Débito",
        "json_term": "En el momento",
        "page_payment_type": "Tarjeta de débito",
        "page_term": "Al instante",
    },
    {
        "json_concept": "Point - Crédito",
        "json_term": "En el momento",
        "page_payment_type": "Tarjeta de crédito",
        "page_term": "Al instante",
    },
    {
        "json_concept": "Point - Crédito",
        "json_term": "14 días",
        "page_payment_type": "Tarjeta de crédito",
        "page_term": "10 días", # Mapping discrepancy noted here as the site shows 10, not 14.
    },
]

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

def update_fees_in_data(data, scraped_fees):
    """
    Reads the data file, updates all mapped fees, and returns the modified data.
    Returns None if no updates were made.
    """
    mp_entity = None
    for entity in data:
        if entity.get('id') == MP_ID:
            mp_entity = entity
            break
    
    if not mp_entity:
        print(f"ERROR: Entity with id '{MP_ID}' not found in {DATA_FILE}.")
        return None

    something_was_updated = False
    for mapping in FEE_MAPPING:
        # Find the new rate from the scraped data
        new_rate = None
        for scraped_fee in scraped_fees:
            if mapping['page_payment_type'] in scraped_fee['payment_type'] and \
               mapping['page_term'] == scraped_fee['term']:
                # Re-add "+ IVA" for format consistency with our data file
                new_rate = f"{scraped_fee['fee']} + IVA"
                break
        
        if not new_rate:
            print(f"WARN: Could not find a matching scraped fee for {mapping['json_concept']} - {mapping['json_term']}. Skipping.")
            continue

        # Find the corresponding fee in our data.json and update it
        fee_updated_in_json = False
        for fee in mp_entity.get('fees', []):
            if fee.get('concept') == mapping['json_concept'] and fee.get('term') == mapping['json_term']:
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
    
    print(f"Fetching data from: {FEE_URL}")
    try:
        response = requests.get(FEE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        scraped_fees = scrape_fees_from_page(response.text)
        
        if not scraped_fees:
            print("Could not extract any fees from the page. No changes were made.")
            exit(1)
            
        print(f"Successfully scraped {len(scraped_fees)} fee entries from the page.")
        
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
            
        updated_data = update_fees_in_data(current_data, scraped_fees)
        
        if updated_data:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, indent=4, ensure_ascii=False)
            print("data.json has been successfully updated.")
        else:
            print("No fee changes detected. data.json remains unchanged.")

        # Update date stamp in HTML (always update to reflect when script was run)
        print()
        update_date_in_html()

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to fetch URL {FEE_URL}. Reason: {e}")
        exit(1)

    print("Script finished.")

