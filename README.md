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
python3 update_mercadopago_fee.py
python3 update_bna_fee.py
python3 update_uala_fee.py
```

Scrapers will only modify `data.json` if changes are detected.
