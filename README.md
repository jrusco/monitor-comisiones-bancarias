# monitor-comisiones-bancarias
A one-day vibe coded project to aggregate and show and compare credit card transaction fees from the most popular Argentinian financial entities.

Currently hosted in GitHub pages at <https://jrusco.github.io/monitor-comisiones-bancarias/>

## Updating Fee Data

The project includes automated scrapers to update fee information from financial entities.

```bash
# Setup (first time only)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run scrapers
python update_mercadopago_fee.py  # Updates Mercado Pago Point fees
python update_bna_fee.py          # Updates BNA fees from official PDFs
```

Scrapers will only modify `data.json` if changes are detected.
