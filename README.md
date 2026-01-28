# monitor-comisiones-bancarias

A project to aggregate, compare, and display credit card transaction fees from popular Argentine financial entities.

Hosted at <https://jrusco.github.io/monitor-comisiones-bancarias/>

## Quick Start

The application is a static single-page app with no build process needed.

```bash
# Open directly in browser
xdg-open index.html

# Or run a local HTTP server
python3 -m http.server 8000
# Then visit http://localhost:8000
```

## Fee Updates

Fee data is updated automatically via GitHub Actions every Sunday. You can also trigger updates manually.

### Automated Updates

The workflow at `.github/workflows/update-fees.yml` runs weekly and:
- Executes all Go scrapers
- Validates the resulting `data.json`
- Commits changes if any fees were updated

To trigger manually: Go to **Actions** → **Update Fees** → **Run workflow**

### Manual Updates (Local)

Requires Go 1.24+

```bash
go run ./cmd/update-mercadopago
go run ./cmd/update-bna
go run ./cmd/update-bapro
go run ./cmd/update-uala
```

Scrapers only modify `data.json` if changes are detected.

## Fee Data Sources

| Entity | Source |
|--------|--------|
| BNA | [Fiserv Argentina](https://aranceles.fiservargentina.com) |
| Mercado Pago | [Point fees](https://www.mercadopago.com.ar/ayuda/2779), [QR fees](https://www.mercadopago.com.ar/ayuda/3605) |
| Banco Provincia | [Adhesion comercios](https://www.bancoprovincia.com.ar/web/adhesion_comercios) |
| Uala | [mPOS](https://mpos.ualabis.com.ar/productos/mpos/) |
