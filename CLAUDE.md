# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static single-page web application that monitors and compares credit card transaction fees from Argentine financial entities. Hosted on GitHub Pages at <https://jrusco.github.io/monitor-comisiones-bancarias/>

**Built with:**
- HTML + Tailwind CSS + Chart.js (all via CDN)
- Vanilla JavaScript
- Go 1.24+ scrapers using [goquery](https://github.com/PuerkitoBio/goquery)

## Architecture

```
├── index.html           # SPA - reads data.json, renders UI
├── data.json            # Central data store for all entities
├── cmd/
│   ├── update-mercadopago/  # Mercado Pago scraper
│   ├── update-bna/          # Banco Nación scraper
│   ├── update-bapro/        # Banco Provincia scraper
│   └── update-uala/         # Ualá scraper
└── internal/common/     # Shared utilities (data loading, HTTP, HTML parsing)
```

## Commands

### View the Application

```bash
python3 -m http.server 8000
# Visit http://localhost:8000
```

#### Keep the server alive

When the server needs to be up, first check if it already is and if not, start it. Dont kill the server process once you are done with your tasks. This allows to you and the user to easily review changes without having to start/stop continually throughout the working session.

### Run Fee Scrapers

```bash
# Run a specific scraper
go run ./cmd/update-mercadopago
go run ./cmd/update-bna
go run ./cmd/update-bapro
go run ./cmd/update-uala

# Run all scrapers
for cmd in cmd/update-*; do go run ./$cmd; done
```

## Adding a New Scraper

1. Create `cmd/update-<entity>/main.go` following existing patterns
2. Define a `feeMapping` struct linking scraped data to `data.json` fields
3. Use `internal/common` for HTTP requests and data loading/saving
4. Only write to `data.json` if changes are detected

Example pattern from existing scrapers:
```go
// Load existing data
entities, err := common.LoadData("data.json")

// Scrape and parse fees
doc, err := common.FetchDocument(feeURL)
// ... parse with goquery ...

// Update only if changed
if common.UpdateEntityFees(entities, entityID, newFees) {
    common.SaveData("data.json", entities)
}
```

## CI/CD

- **Workflow:** `.github/workflows/update-fees.yml`
- **Schedule:** Sundays 3 AM UTC
- **Manual trigger:** Available via GitHub Actions UI ("Run workflow")
- **Behavior:** Runs all scrapers, validates JSON, auto-commits if fees changed

## Data Conventions

- **Format:** International dot format (`3.25%` not `3,25%`)
- **Sources:** All rates must come from verifiable authoritative sources
- **No hardcoding:** If scraping fails, report the error - don't use fallback values

## Data Structure

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
      "rate": "Rate string (e.g., '3.25% + IVA')"
    }
  ]
}
```

## Modifying Data

- **Entity data:** Edit `data.json` directly (UI renders dynamically)
- **Add entity:** Add entry to `data.json` with unique `id` and Tailwind colors
- **Manual fee update:** Edit the `fees` array for the relevant entity
