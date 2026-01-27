# monitor-comisiones-bancarias

A one-day vibe coded project to aggregate and show and compare credit card transaction fees from the most popular Argentinian financial entities.

Currently hosted in GitHub pages at <https://jrusco.github.io/monitor-comisiones-bancarias/>

## Running the Project

The application is a static single-page app with no build process needed.

```bash
# Option 1: Open directly in browser
open index.html

# Option 2: Run a local HTTP server
python3 -m http.server 8000
# Then visit http://localhost:8000
```

No dependencies are required to view the application—it uses vanilla JavaScript and Tailwind CSS from CDN.

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

## Backend Server

The project includes a Flask backend that exposes endpoints to trigger updater scripts via HTTP.

### Running in Production

```bash
source venv/bin/activate
pip install -r requirements.txt
API_KEY=your-secret-key gunicorn server:app
```

For development, you can run directly with Flask:

```bash
python server.py
```

### Authentication

Set the `API_KEY` environment variable to enable authentication. When set, all `/update` endpoints require a Bearer token:

```bash
curl -X POST http://localhost:8000/update/mercadopago \
  -H "Authorization: Bearer your-secret-key"
```

If `API_KEY` is not set, no authentication is required.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/status` | Health check (no auth required) |
| `POST` | `/update/mercadopago` | Run Mercado Pago updater |
| `POST` | `/update/bna` | Run BNA updater |
| `POST` | `/update/bapro` | Run Banco Provincia updater |
| `POST` | `/update/uala` | Run Ualá updater |
| `POST` | `/update/all` | Run all updaters sequentially |

### Fee data sources

- BNA -> [maspagos](https://maspagos.com.ar/simulador-de-ventas) and [Fiserv](aranceles.fiservargentina.com)
- MercadoPago -> [Phisycal card reader "Point" in Buenos Aires province](https://www.mercadopago.com.ar/ayuda/2779#tabla1) and [QR code payments in Buenos Aires province](https://www.mercadopago.com.ar/ayuda/3605#tabla1)
- Banco Provincia (de Buenos Aires) -> [BP adhesion comercios](https://www.bancoprovincia.com.ar/web/adhesion_comercios)
- Uala -> [Phisycal card reader "Pos Pro"](https://www.ualabis.com.ar/pos-pro)
