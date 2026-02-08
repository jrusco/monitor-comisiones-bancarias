# Sprint 3: Technical Architecture

**Goal:** Solve the two foundational technical problems: (1) content is invisible to first-pass crawlers because everything is JS-rendered, and (2) performance is degraded by render-blocking CDN scripts. Also add entity-specific deep-link sections and CI/CD automation for SEO assets.

**Depends on:** Sprint 1 (structured data exists to update) and Sprint 2 (FAQ + methodology sections exist).

---

## Task 3.1 — Replace Tailwind CDN with Static CSS Build

**Priority:** P0 — This is the single biggest performance win available.

### Problem

`index.html` line 8:
```html
<script src="https://cdn.tailwindcss.com"></script>
```

This downloads ~115KB of JavaScript, scans the DOM, and generates CSS at runtime. It's marked "for development only" by Tailwind. Impact: 300–800ms LCP penalty, FOUC, main-thread blocking.

### Solution: Tailwind CLI standalone binary

Use the standalone Tailwind CLI binary (no Node.js/npm project required — keeps the project simple).

### 3.1.1 Create input CSS file

**File:** `input.css` (new, project root)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Preserve existing custom styles from index.html <style> block */
/* These will be moved here from the inline <style> in index.html */
```

### 3.1.2 Create Tailwind config

**File:** `tailwind.config.js` (new, project root)

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html'],
  theme: {
    extend: {
      colors: {
        'bna-primary': '#057EA3',
        'bapro-primary': '#FFFFFF',
        'bapro-dark': '#2E7D32',
        'mercadopago-primary': '#00bcff',
        'mercadopago-dark': '#0a0080',
        'uala-primary': '#022A9A',
      },
      fontFamily: {
        sans: ['DM Sans', 'system-ui', 'sans-serif'],
        serif: ['DM Serif Display', 'serif'],
      },
    },
  },
  plugins: [],
}
```

### 3.1.3 Build process

```bash
# Download standalone binary (one-time, or in CI/CD)
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64

# Build minified CSS
./tailwindcss-linux-x64 -i input.css -o tailwind.min.css --minify
```

### 3.1.4 Update index.html

Replace:
```html
<script src="https://cdn.tailwindcss.com"></script>
```

With:
```html
<link rel="stylesheet" href="/tailwind.min.css" fetchpriority="high">
```

### 3.1.5 Move custom styles

Move all custom CSS from the `<style>` block in `index.html` into `input.css` (after the `@tailwind` directives). This includes:

- Font family declarations
- `.chart-container` dimensions
- `.card-hover` effects
- `.custom-scroll` scrollbar styles
- `.entity-card` border styles
- `.status-badge` pulse animation
- Color variable definitions for entity brand colors
- Animation keyframes

The inline `<style>` block can then be removed entirely from `index.html`.

### 3.1.6 Add to CI/CD

Update `.github/workflows/update-fees.yml`:

```yaml
      - name: Build Tailwind CSS
        run: |
          curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
          chmod +x tailwindcss-linux-x64
          ./tailwindcss-linux-x64 -i input.css -o tailwind.min.css --minify
```

### 3.1.7 Add tailwind.min.css to .gitignore (optional)

If you prefer to build on every deploy, add `tailwind.min.css` to `.gitignore` and always build in CI. Alternatively, commit the built file for simpler local development.

**Recommended approach:** Commit the built file. This keeps the project simple (no build step for local dev) and matches the vanilla JS philosophy.

### Acceptance criteria

- [ ] `<script src="https://cdn.tailwindcss.com"></script>` is removed
- [ ] `<link rel="stylesheet" href="/tailwind.min.css">` replaces it
- [ ] All Tailwind classes still render correctly
- [ ] No FOUC (Flash of Unstyled Content) on page load
- [ ] CSS file size is under 50KB (vs 115KB JS before)
- [ ] Lighthouse Performance score improves by 10+ points

---

## Task 3.2 — Build Pre-render Script

**Priority:** P0 — Solves the "empty page" indexing problem.

### Problem

When Googlebot first crawls `index.html`, the entity grid, chart, hero metrics, and fee tables are all empty placeholders. Content only appears after JavaScript fetches `data.json` and renders it. This delays indexing and may result in incomplete or no indexing.

### Solution

A Node.js script that reads `data.json` and injects static HTML into `index.html` at build time. JavaScript then enhances (not replaces) this content.

**File:** `scripts/prerender.js` (new)

```javascript
#!/usr/bin/env node

/**
 * Pre-render script: Injects static content from data.json into index.html
 * at build time so that crawlers see full content without executing JavaScript.
 *
 * Run: node scripts/prerender.js
 * Called by: .github/workflows/update-fees.yml after scrapers run
 */

const fs = require('fs');
const path = require('path');

const DATA_PATH = path.join(__dirname, '..', 'data.json');
const HTML_PATH = path.join(__dirname, '..', 'index.html');

function loadData() {
    const raw = fs.readFileSync(DATA_PATH, 'utf-8');
    return JSON.parse(raw);
}

function loadHTML() {
    return fs.readFileSync(HTML_PATH, 'utf-8');
}

function saveHTML(html) {
    fs.writeFileSync(HTML_PATH, html, 'utf-8');
}

// --- Hero Metrics ---

function computeHeroMetrics(entities) {
    let minDebit = Infinity;
    let minDebitEntity = '';
    let minCredit = Infinity;
    let minCreditEntity = '';

    for (const entity of entities) {
        for (const fee of entity.fees) {
            const rateMatch = fee.rate.match(/^([\d.]+)%/);
            if (!rateMatch) continue;
            const rate = parseFloat(rateMatch[1]);

            const concept = fee.concept.toLowerCase();
            if (concept.includes('débito') || concept === 'débito') {
                if (rate < minDebit) {
                    minDebit = rate;
                    minDebitEntity = entity.name;
                }
            }
            if (concept.includes('crédito') || concept === 'crédito') {
                if (rate < minCredit) {
                    minCredit = rate;
                    minCreditEntity = entity.name;
                }
            }
        }
    }

    return {
        debit: minDebit === Infinity ? 'N/A' : `${minDebit}% + IVA`,
        debitEntity: minDebitEntity,
        credit: minCredit === Infinity ? 'N/A' : `${minCredit}% + IVA`,
        creditEntity: minCreditEntity,
    };
}

// --- Noscript Fee Table ---

function generateNoscriptTable(entities) {
    let rows = '';
    for (const entity of entities) {
        for (const fee of entity.fees) {
            rows += `        <tr>
          <td style="padding:8px;border-bottom:1px solid #e2e8f0">${entity.name}</td>
          <td style="padding:8px;border-bottom:1px solid #e2e8f0">${fee.concept}</td>
          <td style="padding:8px;border-bottom:1px solid #e2e8f0">${fee.term}</td>
          <td style="padding:8px;border-bottom:1px solid #e2e8f0"><strong>${fee.rate}</strong></td>
        </tr>\n`;
        }
    }

    return `<noscript>
    <section style="max-width:1280px;margin:0 auto;padding:2rem 1rem">
      <h2 style="font-size:1.5rem;font-weight:bold;margin-bottom:1rem">Comisiones por cobro con tarjeta en Argentina</h2>
      <p style="margin-bottom:1rem;color:#64748b">Comparativa de comisiones de las principales entidades de pago argentinas. Datos obtenidos de fuentes oficiales.</p>
      <table style="width:100%;border-collapse:collapse;background:white;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.1)">
        <thead>
          <tr style="background:#f1f5f9">
            <th style="padding:8px;text-align:left;font-weight:600">Entidad</th>
            <th style="padding:8px;text-align:left;font-weight:600">Concepto</th>
            <th style="padding:8px;text-align:left;font-weight:600">Plazo</th>
            <th style="padding:8px;text-align:left;font-weight:600">Comisión</th>
          </tr>
        </thead>
        <tbody>
${rows}        </tbody>
      </table>
    </section>
  </noscript>`;
}

// --- JSON-LD Fee Update ---

function updateStructuredData(html, entities) {
    // Find the JSON-LD block
    const jsonLdRegex = /<script type="application\/ld\+json">([\s\S]*?)<\/script>/;
    const match = html.match(jsonLdRegex);
    if (!match) {
        console.warn('Warning: No JSON-LD block found in index.html');
        return html;
    }

    try {
        const data = JSON.parse(match[1]);
        const graph = data['@graph'];

        // Find the ItemList
        const itemList = graph.find(item => item['@type'] === 'ItemList');
        if (itemList && itemList.itemListElement) {
            for (const listItem of itemList.itemListElement) {
                const service = listItem.item;
                if (!service) continue;

                // Match by provider name
                const providerName = service.provider?.name;
                const entity = entities.find(e =>
                    e.name.includes(providerName) || providerName?.includes(e.name)
                );

                if (entity) {
                    // Build fee summary text
                    const feeSummary = entity.fees
                        .map(f => `${f.concept}: ${f.rate} (${f.term})`)
                        .join('. ');
                    service.feesAndCommissionsSpecification = feeSummary;
                }
            }
        }

        // Update FAQPage answers with current rates (if FAQ exists)
        const faqPage = graph.find(item => item['@type'] === 'FAQPage');
        if (faqPage && faqPage.mainEntity) {
            // Update specific answers that reference rates
            // This is a targeted update — only modify answers about specific rates
            for (const q of faqPage.mainEntity) {
                if (q.name.includes('Mercado Pago') && q.name.includes('débito')) {
                    const mp = entities.find(e => e.id === 'mercadopago');
                    const debitFee = mp?.fees.find(f =>
                        f.concept.includes('Débito') && f.concept.includes('Point')
                    );
                    if (debitFee) {
                        q.acceptedAnswer.text = q.acceptedAnswer.text.replace(
                            /[\d.]+% \+ IVA por ventas con tarjeta de débito/,
                            `${debitFee.rate} por ventas con tarjeta de débito`
                        );
                    }
                }
            }
        }

        const updatedJsonLd = JSON.stringify(data, null, 2);
        html = html.replace(jsonLdRegex,
            `<script type="application/ld+json">\n${updatedJsonLd}\n</script>`
        );
    } catch (e) {
        console.error('Error updating JSON-LD:', e.message);
    }

    return html;
}

// --- Sitemap lastmod ---

function updateSitemap() {
    const sitemapPath = path.join(__dirname, '..', 'sitemap.xml');
    if (!fs.existsSync(sitemapPath)) return;

    const today = new Date().toISOString().split('T')[0];
    let sitemap = fs.readFileSync(sitemapPath, 'utf-8');
    sitemap = sitemap.replace(/<lastmod>.*<\/lastmod>/, `<lastmod>${today}</lastmod>`);
    fs.writeFileSync(sitemapPath, sitemap, 'utf-8');
    console.log(`Updated sitemap.xml lastmod to ${today}`);
}

// --- Main ---

function main() {
    console.log('Pre-render: Starting...');

    const entities = loadData();
    let html = loadHTML();

    // 1. Update hero metrics with pre-rendered values
    const metrics = computeHeroMetrics(entities);
    html = html.replace(
        /(<p id="heroMinDebit"[^>]*>).*?(<\/p>)/,
        `$1${metrics.debit} <span class="text-sm font-normal text-blue-200">(${metrics.debitEntity})</span>$2`
    );
    html = html.replace(
        /(<p id="heroMinCredit"[^>]*>).*?(<\/p>)/,
        `$1${metrics.credit} <span class="text-sm font-normal text-blue-200">(${metrics.creditEntity})</span>$2`
    );

    // 2. Inject noscript fallback table
    //    Place it right after <body ...> opening tag
    const noscriptBlock = generateNoscriptTable(entities);
    if (!html.includes('<noscript>')) {
        html = html.replace(
            /(<body[^>]*>)/,
            `$1\n  ${noscriptBlock}`
        );
        console.log('Pre-render: Injected <noscript> fallback table');
    } else {
        // Replace existing noscript block
        html = html.replace(
            /<noscript>[\s\S]*?<\/noscript>/,
            noscriptBlock
        );
        console.log('Pre-render: Updated existing <noscript> block');
    }

    // 3. Update structured data with current fee values
    html = updateStructuredData(html, entities);
    console.log('Pre-render: Updated JSON-LD structured data');

    // 4. Save
    saveHTML(html);
    console.log('Pre-render: Saved index.html');

    // 5. Update sitemap lastmod
    updateSitemap();

    console.log('Pre-render: Done.');
}

main();
```

### Implementation notes

- The script is idempotent — running it multiple times produces the same result.
- Hero metrics are pre-rendered with actual values instead of "Cargando...". JavaScript will overwrite these on load (same values), so there's no flash.
- The `<noscript>` block uses inline styles (not Tailwind classes) because Tailwind CSS may not be available to noscript-mode browsers.
- JSON-LD fee data is updated dynamically so structured data always matches visible content (Google requirement).
- The script has zero npm dependencies — only uses Node.js built-ins (`fs`, `path`).

### Acceptance criteria

- [ ] `node scripts/prerender.js` runs without errors
- [ ] Hero metrics show actual values (not "Cargando...") in the raw HTML source
- [ ] `<noscript>` block contains all entities and all fees
- [ ] JSON-LD `feesAndCommissionsSpecification` fields contain current rate text
- [ ] `sitemap.xml` lastmod updated to today's date
- [ ] Re-running the script produces identical output (idempotent)

---

## Task 3.3 — Add Pre-render Step to CI/CD

**File:** `.github/workflows/update-fees.yml`

### Updated workflow

```yaml
name: Update Fees

on:
  schedule:
    - cron: '0 3 * * 0'  # Sundays 3 AM UTC
  workflow_dispatch:

permissions:
  contents: write

concurrency:
  group: update-fees
  cancel-in-progress: false

jobs:
  update-fees:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: '1.24'
          cache: true

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Run scrapers
        run: |
          failed=0
          go run ./cmd/update-mercadopago || { echo "::warning::mercadopago failed"; failed=1; }
          go run ./cmd/update-bna || { echo "::warning::bna failed"; failed=1; }
          go run ./cmd/update-bapro || { echo "::warning::bapro failed"; failed=1; }
          go run ./cmd/update-uala || { echo "::warning::uala failed"; failed=1; }
          [ $failed -ne 0 ] && echo "::warning::Some scrapers failed"
          exit 0

      - name: Validate data.json
        run: jq empty data.json

      - name: Build Tailwind CSS
        run: |
          curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
          chmod +x tailwindcss-linux-x64
          ./tailwindcss-linux-x64 -i input.css -o tailwind.min.css --minify

      - name: Pre-render content into HTML
        run: node scripts/prerender.js

      - name: Validate structured data
        run: |
          node -e "
            const html = require('fs').readFileSync('index.html','utf8');
            const match = html.match(/<script type=\"application\/ld\+json\">([\\s\\S]*?)<\\/script>/);
            if (!match) { console.error('No JSON-LD found'); process.exit(1); }
            const data = JSON.parse(match[1]);
            console.log('JSON-LD valid. Types:', data['@graph'].map(i => i['@type']).join(', '));
          "

      - name: Commit and push if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data.json index.html sitemap.xml tailwind.min.css
          git diff --staged --quiet || git commit -m "chore: update fees [automated]"
          git push
```

### Changes from current workflow

1. **Added `actions/setup-node@v4`** — Required for the pre-render script.
2. **Added Tailwind CSS build step** — Rebuilds CSS in case HTML classes changed.
3. **Added pre-render step** — Runs `scripts/prerender.js` after scrapers.
4. **Added JSON-LD validation** — Catches broken structured data before deploy.
5. **Expanded `git add`** — Now includes `sitemap.xml` and `tailwind.min.css`.
6. **Increased `timeout-minutes`** from 5 to 10 — Tailwind build adds time.

### Acceptance criteria

- [ ] Workflow runs successfully on manual trigger
- [ ] `data.json`, `index.html`, `sitemap.xml`, and `tailwind.min.css` are committed when changes detected
- [ ] JSON-LD validation step passes
- [ ] Pre-rendered hero metrics are visible in committed `index.html`

---

## Task 3.4 — Remove Cache-Buster from data.json Fetch

**File:** `index.html` — JavaScript section

### Current code

```javascript
const response = await fetch('data.json?t=' + new Date().getTime());
```

### Updated code

```javascript
const response = await fetch('data.json');
```

### Implementation notes

- The `?t=timestamp` forces a unique URL on every page load, defeating browser caching entirely.
- With weekly updates and pre-rendered content, stale data for a few minutes is acceptable.
- GitHub Pages sets `Cache-Control: max-age=600` by default (10 minutes), which is reasonable.
- The pre-rendered content in the HTML is always current (updated by CI/CD), so even if `data.json` is cached, the page shows correct data.

### Acceptance criteria

- [ ] No `?t=` query parameter in data.json fetch
- [ ] Browser DevTools Network tab shows `data.json` served from cache on repeat visits
- [ ] Page still works correctly on first visit (cache miss)

---

## Task 3.5 — Reserve Layout Dimensions for CLS Prevention

**File:** `input.css` (or `index.html` if styles are still inline)

### Problem

When JavaScript renders content into empty containers, the page layout shifts. This hurts CLS (Cumulative Layout Shift), one of the three Core Web Vitals.

### Fix: Set minimum heights on dynamic containers

```css
/* Chart container — already has height:280px, verify it's set before JS runs */
.chart-container {
    min-height: 280px;
}

@media (max-width: 768px) {
    .chart-container {
        min-height: 240px;
    }
}

/* Entity grid container — reserve space for cards */
#entityGrid {
    min-height: 400px;
}

/* Ad containers — reserve space to prevent CLS when ads load */
.ad-container {
    min-height: 100px;
    contain: layout;
}

/* Hero metric cards — prevent shift when values load */
#heroMinDebit,
#heroMinCredit {
    min-height: 2rem; /* Match text-2xl line height */
}
```

### Also: Move first ad below the fold

Currently, an ad sits between the hero and the chart (line 350). On mobile, this may be above the fold, which:
- Causes CLS when the ad loads
- May trigger Google's "top heavy" penalty
- Competes with the chart for LCP

**Recommendation:** Move this ad below the chart section, or remove it and keep only the pre-footer ad.

### Acceptance criteria

- [ ] CLS score under 0.1 (measured by Lighthouse)
- [ ] No visible layout shift when content loads
- [ ] Chart container doesn't collapse before Chart.js renders
- [ ] Ad containers have reserved space

---

## Task 3.6 — Add Entity-Specific Anchor Sections

**File:** `index.html` — entity grid section

### Goal

Add `id` attributes to entity sections so Google can deep-link to specific entities:

- `https://cobrocontarjeta.com.ar/#mercado-pago`
- `https://cobrocontarjeta.com.ar/#uala`
- `https://cobrocontarjeta.com.ar/#banco-nacion`
- `https://cobrocontarjeta.com.ar/#banco-provincia`

### Implementation

In the JavaScript that renders entity cards, add `id` attributes:

```javascript
function renderEntityCard(entity) {
    const anchorId = entity.id.replace(/_/g, '-');
    return `
    <div id="${anchorId}" class="entity-card bg-white rounded-xl shadow-sm border ..."
         style="--entity-color: ${getColorHex(entity.color)}">
        <div class="p-4">
            <h3 class="font-semibold text-lg text-slate-900">${entity.name}</h3>
            ...
        </div>
    </div>`;
}
```

Map entity IDs to URL-friendly anchors:

| Entity ID | Anchor |
|-----------|--------|
| `mercadopago` | `#mercadopago` |
| `uala` | `#uala` |
| `bna` | `#banco-nacion` |
| `bapro` | `#banco-provincia` |

### Add smooth scrolling CSS

```css
html {
    scroll-behavior: smooth;
    scroll-padding-top: 5rem; /* Account for sticky navbar height */
}
```

### Add internal navigation links

Consider adding anchor links in the hero section or a mini-navigation:

```html
<nav class="flex flex-wrap gap-2 justify-center mt-4" aria-label="Ir a entidad">
    <a href="#mercadopago" class="text-xs bg-white/20 px-3 py-1 rounded-full text-white hover:bg-white/30">Mercado Pago</a>
    <a href="#uala" class="text-xs bg-white/20 px-3 py-1 rounded-full text-white hover:bg-white/30">Ualá</a>
    <a href="#banco-nacion" class="text-xs bg-white/20 px-3 py-1 rounded-full text-white hover:bg-white/30">Banco Nación</a>
    <a href="#banco-provincia" class="text-xs bg-white/20 px-3 py-1 rounded-full text-white hover:bg-white/30">Banco Provincia</a>
</nav>
```

### Acceptance criteria

- [ ] Navigating to `/#mercadopago` scrolls to the Mercado Pago card
- [ ] Scroll offset accounts for the sticky navbar (content not hidden behind it)
- [ ] Google can display these as sitelinks in search results (verify after indexing)

---

## Task 3.7 — Lazy-Load Chart.js (Performance)

**File:** `index.html` — `<head>` and JavaScript section

### Remove from `<head>`

```html
<!-- Remove these two lines -->
<script src="https://cdn.jsdelivr.net/npm/chart.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2" defer></script>
```

### Add lazy-loading via Intersection Observer

In the JavaScript section, before the chart rendering code:

```javascript
// Lazy-load Chart.js when the chart section approaches the viewport
function lazyLoadChart(entities) {
    const chartSection = document.querySelector('.chart-container');
    if (!chartSection) return;

    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            observer.disconnect();

            const chartScript = document.createElement('script');
            chartScript.src = 'https://cdn.jsdelivr.net/npm/chart.js';
            chartScript.onload = () => {
                const pluginScript = document.createElement('script');
                pluginScript.src = 'https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2';
                pluginScript.onload = () => {
                    renderChart(entities); // Existing chart render function
                };
                document.head.appendChild(pluginScript);
            };
            document.head.appendChild(chartScript);
        }
    }, { rootMargin: '300px' }); // Start loading 300px before visible

    observer.observe(chartSection);
}

// Call in initApp() instead of renderChart() directly:
// Before: renderChart(entities);
// After:  lazyLoadChart(entities);
```

### Show a lightweight placeholder

While Chart.js loads, show a simple placeholder:

```html
<div class="chart-container">
    <canvas id="feeChart"></canvas>
    <p id="chartPlaceholder" class="text-center text-sm text-slate-400 py-12">
        Cargando gráfico comparativo...
    </p>
</div>
```

Remove the placeholder when the chart renders:

```javascript
function renderChart(entities) {
    const placeholder = document.getElementById('chartPlaceholder');
    if (placeholder) placeholder.remove();
    // ... existing chart code ...
}
```

### Acceptance criteria

- [ ] Chart.js is NOT loaded on initial page load (verify in Network tab)
- [ ] Chart.js loads when user scrolls near the chart section
- [ ] Chart renders correctly after lazy loading
- [ ] Placeholder text shows while Chart.js loads
- [ ] Initial page weight reduced by ~230KB

---

## Sprint 3 Commit Plan

```bash
# Commit 1: Tailwind build setup
git add input.css tailwind.config.js tailwind.min.css index.html
git commit -m "perf: replace Tailwind CDN with static CSS build

Remove runtime Tailwind CSS generation (115KB JS + render-blocking)
and replace with pre-built, minified CSS file (~25KB). Eliminates
FOUC and improves LCP by 300-800ms."

# Commit 2: Pre-render script
git add scripts/prerender.js
git commit -m "feat(seo): add build-time pre-render script

Injects static content from data.json into index.html: hero metrics,
noscript fallback table, and dynamic JSON-LD structured data.
Ensures crawlers see full content without JS execution."

# Commit 3: Updated CI/CD
git add .github/workflows/update-fees.yml
git commit -m "ci: add Tailwind build, pre-render, and JSON-LD validation

Pipeline now builds Tailwind CSS, pre-renders content into HTML,
validates structured data, and updates sitemap lastmod on each run."

# Commit 4: Performance + anchors
git add index.html input.css
git commit -m "perf: lazy-load Chart.js, reserve CLS dimensions, add entity anchors

Chart.js loaded via IntersectionObserver (saves 230KB initial load).
Min-height on dynamic containers prevents CLS. Entity-specific
anchors enable deep-linking and potential Google sitelinks."

# Commit 5: Cache-buster removal
git add index.html
git commit -m "perf: remove cache-buster from data.json fetch

Allow browser caching of data.json. Pre-rendered content ensures
page shows current data regardless of cache state."
```

---

## Verification Checklist (Post-Deploy)

| Check | Tool | Expected Result |
|-------|------|-----------------|
| No Tailwind CDN request | DevTools Network tab | No request to cdn.tailwindcss.com |
| CSS file cached | DevTools Network → data.json | `(disk cache)` on repeat visit |
| Hero metrics in source | View page source | Actual values, not "Cargando..." |
| Noscript table | Disable JS in browser | Full fee table visible |
| Chart lazy-loads | DevTools Network tab | chart.js loaded only after scroll |
| CLS score | Lighthouse | Under 0.1 |
| LCP score | Lighthouse | Under 2.5s |
| Entity anchors | Navigate to /#mercadopago | Page scrolls to Mercado Pago |
| JSON-LD current | Rich Results Test | Fee data matches data.json |
| Sitemap lastmod | `curl sitemap.xml` | Today's date |
