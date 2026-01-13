# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static single-page web application that monitors and compares credit card transaction fees from popular financial entities in Argentina. The project is hosted on GitHub Pages at https://jrusco.github.io/monitor-comisiones-bancarias/

The application is built with:
- Plain HTML (index.html)
- Tailwind CSS (loaded via CDN)
- Chart.js for data visualization (loaded via CDN)
- Vanilla JavaScript for interactivity

## Architecture

### Data Flow
1. **data.json** - Central data store containing all financial entity information (fees, URLs, metadata)
2. **index.html** - Single-page application that reads from data.json and renders the UI
3. **update_mercadopago_fee.py** - Python script that scrapes Mercado Pago's fee page and updates data.json

### Key Files
- `index.html` - Complete application with embedded JavaScript and styling
- `data.json` - Structured data for all financial entities (banks and fintechs)
- `update_mercadopago_fee.py` - Web scraper for automated fee updates
- `research_spanish.md` - Research notes on the Argentinian payment processing market

### Data Structure
The `data.json` file contains an array of financial entities with this structure:
```json
{
  "id": "unique-identifier",
  "name": "Display Name",
  "type": "Banco (Adquirente) | Agregador (Fintech) | Procesador / Adquirente",
  "color": "Tailwind bg-color class",
  "textColor": "Tailwind text-color class",
  "logo": "Two-letter abbreviation",
  "feeUrl": "Official fee information URL",
  "apiUrl": "API endpoint or N/A",
  "apiDocs": "Developer documentation URL (optional)",
  "hasApi": boolean,
  "fees": [
    {
      "concept": "Fee category (e.g., 'Point - Débito')",
      "term": "Settlement term (e.g., 'En el momento', '14 días')",
      "rate": "Rate string (e.g., '3,25% + IVA')"
    }
  ]
}
```

## Common Commands

### Running the Application
No build process is required. Open `index.html` directly in a browser:
```bash
# On Linux
xdg-open index.html

# Or use a simple HTTP server
python3 -m http.server 8000
# Then visit http://localhost:8000
```

### Python Environment Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Updating Mercado Pago Fees
The scraper targets the Mercado Pago Point fees page and updates specific fee entries in data.json:
```bash
# Activate venv first
source venv/bin/activate

# Run the updater
python update_mercadopago_fee.py
```

The script:
- Scrapes https://www.mercadopago.com.ar/ayuda/2779
- Maps scraped data to data.json entries using FEE_MAPPING
- Updates only the fees defined in the mapping (Point - Débito/Crédito rates)
- Preserves all other data.json content unchanged
- Only writes to file if changes are detected

## Development Guidelines

### Modifying Entity Data
All data changes should be made to `data.json`, not `index.html`. The HTML file reads from the JSON file dynamically.

### Adding New Financial Entities
1. Add a new entry to `data.json` following the structure above
2. Assign a unique `id` and choose appropriate Tailwind color classes
3. The UI will automatically render the new entity

### Updating Fees Manually
Edit the `fees` array in `data.json` for the relevant entity. The rate format should match existing entries (e.g., "X% + IVA" or "X% (Regulado)").

### Extending the Scraper
To add more scrapers for other entities:
1. Follow the pattern in `update_mercadopago_fee.py`
2. Define a FEE_MAPPING that links scraped data to data.json structure
3. Use BeautifulSoup to parse the target page
4. Only update data.json if changes are detected

### Styling Conventions
- Uses Tailwind utility classes throughout
- Color palette: Slate (backgrounds/text), Blue (primary), Emerald (success/money)
- Each entity has assigned `color` and `textColor` properties for consistent theming
- Responsive design with mobile-first breakpoints

## Important Notes

- The "updated date" badge in the navbar (index.html:95) is hardcoded and must be manually updated after data changes
- The scraper has a mapping discrepancy: data.json uses "14 días" while the Mercado Pago page shows "10 días" - this is intentional (see update_mercadopago_fee.py:28)
- Fee rates from banks (BNA, Bapro) are often labeled "(Regulado)" as they follow government-mandated caps
- Fintech aggregators (Mercado Pago, Ualá) typically charge higher fees than regulated bank rates
