# SEO Strategy Plan — Monitor de Comisiones Bancarias

## Executive Summary

This document outlines a comprehensive SEO strategy to achieve first-page (ideally first-position) placement for relevant searches related to credit/debit card processing fees in Argentina. The analysis is structured around three perspectives: **Frontend Engineering**, **SEO/Marketing**, and **Software Architecture**.

**Current state:** The site has solid UX, good semantic HTML, and a unique value proposition (automated, real-time fee monitoring), but is missing nearly all fundamental SEO signals — no meta description, no structured data, no sitemap, no robots.txt, no Open Graph tags, and critically, all content is rendered client-side via JavaScript.

**Target outcome:** Rank #1 for high-intent queries like "comisiones cobro con tarjeta argentina", "comparar comisiones mercado pago", and "cuanto cobra mercado pago por venta".

---

## Part 1: Current State Audit

### What's Working

| Aspect | Status |
|--------|--------|
| Semantic HTML (nav, main, section, footer, aside) | Good |
| Heading hierarchy (single H1, logical H2/H3/H4) | Good |
| Mobile responsive via Tailwind CSS | Good |
| HTTPS via GitHub Pages | Good |
| ARIA attributes and accessibility | Good |
| Automated weekly data updates (freshness signal) | Excellent |
| Official source links for every fee | Excellent |
| Interactive tools (chart, simulator) | Good |
| `lang="es"` on html element | Present (needs refinement to `es-AR`) |

### Critical Gaps

| Gap | SEO Impact | Priority |
|-----|-----------|----------|
| No `<meta name="description">` | ~30% CTR loss on SERPs | P0 |
| All content rendered via JS (SPA) | Googlebot may not index content | P0 |
| No JSON-LD structured data | No rich snippets, missed SERP features | P0 |
| No Open Graph / Twitter Card tags | Poor social sharing, no link previews | P1 |
| No `<link rel="canonical">` | Duplicate content risk | P1 |
| No sitemap.xml | Slower crawl discovery | P1 |
| No robots.txt | No crawl directives | P1 |
| No favicon or apple-touch-icon | Poor branding in tabs/bookmarks | P2 |
| No Google Search Console setup | No search performance data | P1 |
| No analytics (GA4 or alternative) | No traffic/behavior insights | P2 |
| GitHub Pages subdomain (no .com.ar) | Weak geo-signal for Argentina | P2 |
| No FAQ section | Missing long-tail keyword capture | P1 |
| No `<noscript>` fallback content | Zero content for JS-disabled crawlers | P0 |
| `lang="es"` instead of `lang="es-AR"` | Imprecise geo-linguistic signal | P2 |
| Cache-busting `?t=timestamp` on data.json | Prevents CDN/browser caching | P2 |

---

## Part 2: Competitive Landscape

### Direct Competitors

| Competitor | Type | Strengths | Weaknesses |
|-----------|------|-----------|------------|
| **iKiwi** (ikiwi.net.ar) | Broad financial portal | .net.ar domain, deep content, POS comparator, fee calculator | Broad scope dilutes focus; not automated |
| **Taca Taca** (taca-taca.com.ar) | Fee simulator | .com.ar domain, detailed simulator with card brands | Not a persistent comparison tool; narrower scope |
| **Posnetify** (posnetify.com) | Content blog | Good keyword-targeted articles | No interactive tool; content-only |
| **iProup** (iproup.com) | News media | Massive domain authority, frequent articles | Articles go stale; not a tool |

### Our Competitive Advantages

1. **Automated real-time data** — No competitor scrapes and auto-updates fees weekly
2. **Focused scope** — Not a broad portal; purpose-built for fee comparison
3. **Interactive tools** — Chart visualization + fee simulator on a single page
4. **Official sources** — Every fee links to its authoritative source URL
5. **Open source** — Transparency builds E-E-A-T trust signals
6. **Uncontested brand term** — "monitor comisiones bancarias" has zero competition

### Keyword Targets

**Primary (high volume, high intent):**
- `comisiones cobro con tarjeta argentina`
- `cuanto cobra mercado pago por venta`
- `comparar comisiones mercado pago uala`
- `comisiones posnet argentina`

**Secondary (medium volume):**
- `mercado pago vs uala cual conviene`
- `comisiones point mercado pago 2026`
- `comisiones billeteras virtuales argentina`
- `arancel tarjeta credito debito comercio`

**Long-tail (low volume, high conversion):**
- `cuanto me descuentan si cobro con tarjeta de credito`
- `comisiones cobro QR argentina`
- `que conviene mas mercado pago o posnet`
- `simulador comisiones venta con tarjeta`
- `calculadora comisiones mercado pago`

**Brand (own):**
- `monitor comisiones bancarias`

---

## Part 3: Implementation Plan

### Phase 1 — Critical Foundation (Quick Wins)

These changes are high-impact, low-effort, and should be implemented first.

#### 1.1 Meta Tags & Head Optimization

**File:** `index.html`

```html
<html lang="es-AR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Primary SEO -->
  <title>Comisiones por Cobro con Tarjeta en Argentina — Comparador Actualizado | Monitor Comisiones</title>
  <meta name="description" content="Compara comisiones de Mercado Pago, Ualá, Banco Nación y Banco Provincia para cobrar con tarjeta de débito y crédito en Argentina. Datos actualizados automáticamente desde fuentes oficiales.">
  <link rel="canonical" href="https://jrusco.github.io/monitor-comisiones-bancarias/">
  <meta name="robots" content="index, follow">

  <!-- Geographic targeting -->
  <meta name="geo.region" content="AR">
  <meta name="geo.placename" content="Argentina">
  <link rel="alternate" href="https://jrusco.github.io/monitor-comisiones-bancarias/" hreflang="es-AR">
  <link rel="alternate" href="https://jrusco.github.io/monitor-comisiones-bancarias/" hreflang="x-default">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="Comparador de Comisiones por Cobro con Tarjeta en Argentina">
  <meta property="og:description" content="Compara comisiones de Mercado Pago, Ualá, Banco Nación y Banco Provincia. Datos actualizados semanalmente desde fuentes oficiales.">
  <meta property="og:url" content="https://jrusco.github.io/monitor-comisiones-bancarias/">
  <meta property="og:locale" content="es_AR">
  <meta property="og:site_name" content="Monitor de Comisiones Bancarias">
  <meta property="og:image" content="https://jrusco.github.io/monitor-comisiones-bancarias/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Comparador de Comisiones por Cobro con Tarjeta en Argentina">
  <meta name="twitter:description" content="Compara comisiones de Mercado Pago, Ualá, Banco Nación y Banco Provincia. Datos actualizados semanalmente.">
  <meta name="twitter:image" content="https://jrusco.github.io/monitor-comisiones-bancarias/og-image.png">

  <!-- Theme & Branding -->
  <meta name="theme-color" content="#1e40af">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  ...
</head>
```

**Rationale:**
- The title tag is the single most important on-page signal. It targets the primary keyword "comisiones por cobro con tarjeta en Argentina" while including the brand name.
- The meta description targets the most-searched entity names (Mercado Pago, Ualá) and emphasizes the "updated automatically" differentiator.
- Open Graph and Twitter Card tags ensure proper link previews when shared on social media and messaging apps (WhatsApp is critical in Argentina).
- `hreflang="es-AR"` provides an explicit Argentine Spanish signal.

#### 1.2 Structured Data (JSON-LD)

Add a `<script type="application/ld+json">` block in the `<head>` with the following structure:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebApplication",
      "@id": "https://jrusco.github.io/monitor-comisiones-bancarias/#app",
      "name": "Monitor de Comisiones Bancarias",
      "description": "Comparador de comisiones por cobro con tarjeta de débito y crédito en Argentina",
      "url": "https://jrusco.github.io/monitor-comisiones-bancarias/",
      "applicationCategory": "FinanceApplication",
      "operatingSystem": "All",
      "inLanguage": "es-AR",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "ARS"
      },
      "author": {
        "@type": "Person",
        "name": "jrusco",
        "url": "https://github.com/jrusco"
      }
    },
    {
      "@type": "ItemList",
      "name": "Procesadores de pago en Argentina",
      "description": "Comparativa de comisiones de procesadores de pago con tarjeta en Argentina",
      "numberOfItems": 4,
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "item": {
            "@type": "PaymentService",
            "name": "Mercado Pago",
            "provider": {
              "@type": "Organization",
              "name": "Mercado Pago",
              "url": "https://www.mercadopago.com.ar"
            },
            "areaServed": { "@type": "Country", "name": "Argentina" },
            "feesAndCommissionsSpecification": "https://www.mercadopago.com.ar/ayuda/cuanto-cuesta-recibir-pagos-con-point_2779"
          }
        },
        {
          "@type": "ListItem",
          "position": 2,
          "item": {
            "@type": "PaymentService",
            "name": "Ualá Bis",
            "provider": {
              "@type": "Organization",
              "name": "Ualá",
              "url": "https://www.uala.com.ar"
            },
            "areaServed": { "@type": "Country", "name": "Argentina" },
            "feesAndCommissionsSpecification": "https://www.uala.com.ar/bis/costos"
          }
        },
        {
          "@type": "ListItem",
          "position": 3,
          "item": {
            "@type": "PaymentService",
            "name": "Banco de la Nación Argentina",
            "provider": {
              "@type": "BankOrCreditUnion",
              "name": "Banco de la Nación Argentina",
              "url": "https://www.bna.com.ar"
            },
            "areaServed": { "@type": "Country", "name": "Argentina" },
            "feesAndCommissionsSpecification": "https://www.bna.com.ar/Empresas/PagosConTarjeta"
          }
        },
        {
          "@type": "ListItem",
          "position": 4,
          "item": {
            "@type": "PaymentService",
            "name": "Banco Provincia",
            "provider": {
              "@type": "BankOrCreditUnion",
              "name": "Banco de la Provincia de Buenos Aires",
              "url": "https://www.bancoprovincia.com.ar"
            },
            "areaServed": { "@type": "Country", "name": "Argentina" },
            "feesAndCommissionsSpecification": "https://www.bancoprovincia.com.ar/comercios"
          }
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": []
    }
  ]
}
```

The `FAQPage` entity will be populated once the FAQ section is built (Phase 2).

**Rationale:**
- `WebApplication` tells Google this is a finance tool, not just a content page.
- `ItemList` + `PaymentService` enables potential carousel rich results.
- `BankOrCreditUnion` is the Schema.org type specifically designed for banks.
- `feesAndCommissionsSpecification` links to official sources, building E-E-A-T trust.

#### 1.3 robots.txt

**File:** `robots.txt` (new, project root)

```
User-agent: *
Allow: /
Disallow: /cmd/
Disallow: /internal/

Sitemap: https://jrusco.github.io/monitor-comisiones-bancarias/sitemap.xml
```

#### 1.4 sitemap.xml

**File:** `sitemap.xml` (new, project root)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://jrusco.github.io/monitor-comisiones-bancarias/</loc>
    <lastmod>2026-02-07</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

The `<lastmod>` date should be updated automatically by the CI/CD pipeline each time fees change. Add a step to the GitHub Actions workflow:

```yaml
- name: Update sitemap lastmod
  run: |
    TODAY=$(date -u +%Y-%m-%d)
    sed -i "s|<lastmod>.*</lastmod>|<lastmod>$TODAY</lastmod>|" sitemap.xml
```

#### 1.5 .nojekyll

**File:** `.nojekyll` (new, empty file in project root)

This tells GitHub Pages to skip Jekyll processing and serve files as-is. Required for `robots.txt` and other root files to be served correctly.

#### 1.6 Favicon

Create a simple SVG favicon using the site's brand colors (blue gradient):

**File:** `favicon.svg`

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#2563eb"/>
  <text x="16" y="22" font-family="system-ui" font-size="18" font-weight="bold"
        fill="white" text-anchor="middle">MC</text>
</svg>
```

Additionally, generate a 180x180 PNG for `apple-touch-icon.png` and a 1200x630 PNG for `og-image.png` (the Open Graph social sharing image). The OG image should include:
- The site name "Monitor de Comisiones Bancarias"
- A visual showing a comparison (e.g., entity logos with fee percentages)
- The tagline "Compara comisiones de cobro con tarjeta en Argentina"

---

### Phase 2 — Content & E-E-A-T (Medium Effort, High Impact)

#### 2.1 FAQ Section with Schema.org FAQPage Markup

Add a dedicated FAQ section to `index.html` targeting long-tail queries. Each Q&A pair should be marked up with `FAQPage` JSON-LD.

**Target questions (based on keyword research):**

1. **"¿Cuánto cobra Mercado Pago por cobrar con tarjeta de débito?"**
   Answer with current rate from data.json, link to official source.

2. **"¿Qué conviene más: Mercado Pago o Ualá para cobrar con tarjeta?"**
   Objective comparison based on rates, settlement terms, features.

3. **"¿Cuánto me descuentan si cobro con tarjeta de crédito en Argentina?"**
   General explanation of fee structure + IVA, with current rates.

4. **"¿Cuáles son las comisiones de Banco Nación para comercios?"**
   Current rates from data.json with official source link.

5. **"¿Qué es un agregador de pagos y en qué se diferencia de un banco adquirente?"**
   Educational content explaining entity types (directly relevant to the site's type classification).

6. **"¿Cada cuánto se actualizan las comisiones en este sitio?"**
   Explain the automated weekly scraping pipeline. Builds trust and E-E-A-T.

7. **"¿Cómo se comparan las comisiones de cobro por QR vs Point/POS?"**
   Comparison by payment method using current data.

**Implementation approach:**
- Render the FAQ section in static HTML (not JS-generated) for immediate crawlability.
- Use `<details>` and `<summary>` elements for progressive disclosure.
- Dynamically inject current fee values from data.json into pre-existing HTML structure.
- Update the JSON-LD `FAQPage` entity with structured Q&A pairs.

**Rationale:** FAQ sections with proper Schema.org markup can trigger rich FAQ snippets in Google SERPs, which dramatically increase CTR and occupy more SERP real estate, pushing competitors down.

#### 2.2 "About / Methodology" Section

Add a brief section explaining:
- How data is collected (automated scrapers from official sources)
- Update frequency (weekly via GitHub Actions)
- Data accuracy commitments (no hardcoded fallbacks)
- Link to the open-source repository

This section directly addresses Google's E-E-A-T requirements for YMYL (Your Money or Your Life) content. Financial information must demonstrate expertise and trustworthiness.

#### 2.3 "Last Updated" Timestamps

Display per-entity "last updated" dates prominently. This serves dual purposes:
- **User trust:** Users can see data is current
- **Freshness signal:** Google rewards recently updated YMYL content

Implementation: Add a `lastUpdated` field to each entity in `data.json`, updated by scrapers. Render as `<time datetime="2026-02-02">` in the UI.

#### 2.4 Expose Official Source Links Prominently

The `feeUrl` field already exists in data.json for each entity but should be displayed visibly in the UI, not just used internally. Each entity card should show a "Ver fuente oficial" link. This:
- Builds E-E-A-T through transparent sourcing
- Provides outbound links to authoritative domains (a positive trust signal)
- Gives users a way to verify data

---

### Phase 3 — Technical Architecture (High Effort, Critical Impact)

#### 3.1 Build-Time Pre-rendering (The Most Important Technical Change)

**Problem:** The entire site content is generated by JavaScript at runtime. When Googlebot crawls `index.html`, it sees an empty shell with a loading spinner. Google does execute JavaScript, but in a deferred "second wave" of indexing that can take days to weeks, and rendering may fail or be incomplete.

**Solution:** Pre-render the content into the HTML at build time during the CI/CD pipeline.

**Approach: Static HTML generation in CI/CD**

After scrapers update `data.json`, a new build step generates static HTML content and injects it into `index.html`:

```yaml
# In .github/workflows/update-fees.yml
- name: Pre-render content into HTML
  run: |
    node scripts/prerender.js
```

The `scripts/prerender.js` script would:

1. Read `data.json`
2. Generate the comparison table HTML, entity cards HTML, and key metrics
3. Inject them into `index.html` inside a `<noscript>` tag and also as the default content of the dynamic containers
4. Update structured data (JSON-LD) with current fee values

**Alternative lighter approach:** Instead of full pre-rendering, inject a comprehensive `<noscript>` block containing:
- A static HTML table with all current fees
- Entity names and key rates as plain text
- The FAQ section in static HTML

This ensures Googlebot always has content to index, regardless of JS execution.

**Example `<noscript>` block:**

```html
<noscript>
  <section>
    <h2>Comisiones por Cobro con Tarjeta en Argentina</h2>
    <table>
      <thead>
        <tr><th>Entidad</th><th>Concepto</th><th>Plazo</th><th>Comisión</th></tr>
      </thead>
      <tbody>
        <!-- Pre-generated from data.json during CI/CD -->
        <tr><td>Mercado Pago</td><td>Point - Débito</td><td>En el momento</td><td>0.80% + IVA</td></tr>
        ...
      </tbody>
    </table>
  </section>
</noscript>
```

**Recommendation:** Implement both — pre-render the primary content into the page containers AND include a `<noscript>` fallback. The JS then enhances the content with interactivity (charts, simulator, filtering).

#### 3.2 Optimize data.json Loading

Current code:
```javascript
const response = await fetch('data.json?t=' + new Date().getTime());
```

The `?t=timestamp` cache-buster forces a fresh fetch on every page load, which:
- Prevents browser caching (slower repeat visits, hurts Core Web Vitals)
- Creates unique URLs that waste crawl budget

**Recommendation:** Remove the cache-buster. Use HTTP cache headers instead. GitHub Pages serves files with reasonable caching. The weekly update frequency means stale data is acceptable for short periods.

```javascript
const response = await fetch('data.json');
```

If strict freshness is needed, use a content-based hash instead:
```javascript
const response = await fetch('data.json?v=20260207');
// Updated by CI/CD when data changes
```

#### 3.3 Core Web Vitals Optimization

**LCP (Largest Contentful Paint):**
- The hero section H1 text is the likely LCP element. Since it's in static HTML, this is already good.
- Pre-connect to CDN hosts (`cdn.tailwindcss.com`, `cdn.jsdelivr.net`) earlier in `<head>`.
- Consider self-hosting Tailwind CSS (purged/minified) instead of CDN to reduce dependency on third-party latency.

**CLS (Cumulative Layout Shift):**
- Reserve explicit dimensions for the Chart.js canvas element to prevent layout shift when the chart renders.
- Set min-height on entity grid containers to prevent layout shift during JS rendering.

**FID/INP (First Input Delay / Interaction to Next Paint):**
- Current JS is lightweight vanilla JavaScript, which is good.
- Ensure the simulator input is interactive immediately on load (don't block on data.json fetch).

#### 3.4 Preload Critical Resources

```html
<link rel="preload" href="data.json" as="fetch" crossorigin>
<link rel="preconnect" href="https://cdn.tailwindcss.com">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

---

### Phase 4 — Content Strategy & Link Building

#### 4.1 Programmatic SEO Content

The site currently has one page. While it covers the core use case well, Google tends to favor sites with topical depth. Consider generating entity-specific anchor sections that can be linked to directly:

- `/#mercado-pago` — Dedicated section for Mercado Pago fees
- `/#uala` — Dedicated section for Ualá fees
- `/#banco-nacion` — Dedicated section for BNA fees
- `/#banco-provincia` — Dedicated section for BAPRO fees

Each section should have:
- An H2 with the entity name + "comisiones"
- A complete fee breakdown table
- Official source link
- Last-updated timestamp
- A brief description of the entity and its services

This allows Google to deep-link to specific entity sections in search results using fragment identifiers, and helps capture entity-specific queries like "comisiones mercado pago 2026".

#### 4.2 Blog / Updates Section (Optional, High ROI)

If willing to expand scope, a lightweight blog covering fee changes over time would be powerful:

- "Mercado Pago actualizó sus comisiones en febrero 2026"
- "Comparativa de comisiones: ¿qué cambió en el último trimestre?"
- "Guía completa: cómo elegir procesador de pagos para tu comercio"

This can be automated: when scrapers detect a fee change, auto-generate a changelog entry. This creates continuous fresh content tied to high-intent keywords.

#### 4.3 Link Building Opportunities

- **Reddit / Argentine forums:** Share the tool in r/argentina, r/merval, forums for commercial activity
- **Argentine fintech media:** Pitch to iProup, iProUP, El Cronista as a useful tool
- **Small business communities:** Argentine PYME associations, monotributista communities
- **GitHub visibility:** The open-source nature can attract links from developer communities
- **BCRA / regulatory context:** Reference the tool in discussions about fee transparency (Ley 27253)

---

### Phase 5 — Infrastructure & Domain

#### 5.1 Custom Domain (Recommended)

A `.com.ar` domain provides:
- Strong geographic signal for Google Argentina
- Brand credibility for Argentine users
- Shorter, memorable URL

**Recommended domain candidates:**
- `comisionesargentina.com.ar`
- `monitorcomisiones.com.ar`
- `comisionescobro.com.ar`

Cost: ~$3,000-5,000 ARS/year for a `.com.ar` domain. This is the single highest-ROI infrastructure investment for SEO.

**Setup:** Purchase domain, configure DNS to point to GitHub Pages, add CNAME file to repo.

#### 5.2 Google Search Console

- Verify ownership via HTML meta tag or DNS record
- Submit sitemap.xml
- Set target country to Argentina (International Targeting)
- Monitor coverage, performance, and Core Web Vitals
- Use URL Inspection to verify Google can render the JS content

#### 5.3 Google Analytics 4 (or Privacy-Friendly Alternative)

Add analytics to track:
- Organic search traffic and queries
- User engagement (simulator usage, entity clicks)
- Bounce rate and session duration
- Geographic distribution (confirm Argentine audience)

Privacy-friendly alternatives: Plausible, Umami (self-hosted), or Fathom.

---

## Implementation Roadmap

### Sprint 1: Foundation (Immediate)

| # | Task | Impact | Effort | Dependencies |
|---|------|--------|--------|-------------|
| 1 | Add meta description, canonical URL, robots meta | Critical | Low | None |
| 2 | Add Open Graph + Twitter Card tags | High | Low | OG image asset |
| 3 | Change `lang="es"` to `lang="es-AR"` | Medium | Trivial | None |
| 4 | Add JSON-LD structured data (WebApplication + ItemList + PaymentService) | High | Medium | None |
| 5 | Create robots.txt | High | Trivial | None |
| 6 | Create sitemap.xml | High | Trivial | None |
| 7 | Create .nojekyll file | Medium | Trivial | None |
| 8 | Add favicon.svg | Medium | Low | Design asset |
| 9 | Add preconnect hints for CDNs | Medium | Trivial | None |
| 10 | Register with Google Search Console | Critical | Low | DNS/meta access |

### Sprint 2: Content & E-E-A-T

| # | Task | Impact | Effort | Dependencies |
|---|------|--------|--------|-------------|
| 11 | Build FAQ section with FAQPage schema | High | Medium | Content writing |
| 12 | Add "About / Methodology" section | High | Low | Content writing |
| 13 | Add `lastUpdated` field to data.json + scraper output | Medium | Medium | Scraper code changes |
| 14 | Display "last updated" timestamps per entity in UI | Medium | Low | Task 13 |
| 15 | Display official source links ("Ver fuente oficial") in UI | High | Low | None |
| 16 | Create OG image asset (1200x630) | Medium | Medium | Design |
| 17 | Create apple-touch-icon (180x180) | Low | Low | Design |

### Sprint 3: Technical Architecture

| # | Task | Impact | Effort | Dependencies |
|---|------|--------|--------|-------------|
| 18 | Build pre-render script (scripts/prerender.js) | Critical | High | Node.js setup |
| 19 | Add pre-render step to CI/CD workflow | Critical | Medium | Task 18 |
| 20 | Add `<noscript>` fallback with static fee table | High | Medium | data.json |
| 21 | Remove cache-buster from data.json fetch | Medium | Trivial | None |
| 22 | Reserve layout dimensions (chart canvas, grid containers) | Medium | Low | CLS measurement |
| 23 | Add entity-specific anchor sections (/#mercado-pago, etc.) | High | Medium | UI refactoring |
| 24 | Update CI/CD to auto-update sitemap lastmod | Low | Low | Task 6 |
| 25 | Update CI/CD to auto-update JSON-LD with current fees | High | Medium | Task 4, Task 18 |

### Sprint 4: Infrastructure & Growth

| # | Task | Impact | Effort | Dependencies |
|---|------|--------|--------|-------------|
| 26 | Purchase and configure .com.ar domain | High | Medium | Budget approval |
| 27 | Setup Google Analytics 4 (or alternative) | Medium | Low | None |
| 28 | Submit site to Google Search Console + Bing Webmaster | High | Low | Task 10 |
| 29 | Build automated changelog (fee change detection) | Medium | High | Scraper changes |
| 30 | Community outreach and link building | High | Ongoing | Content ready |

---

## Success Metrics

| Metric | Current | Target (3 months) | Target (6 months) |
|--------|---------|-------------------|-------------------|
| Google Search Console impressions | 0 | 1,000/week | 5,000/week |
| Organic clicks | 0 | 100/week | 500/week |
| Position for "comisiones cobro con tarjeta argentina" | Not indexed | Top 20 | Top 5 |
| Position for "cuanto cobra mercado pago por venta" | Not indexed | Top 20 | Top 10 |
| Position for "monitor comisiones bancarias" | Not indexed | #1 | #1 |
| Rich results (FAQ snippets, etc.) | None | FAQ snippet | FAQ + app snippet |
| Core Web Vitals (all 3 metrics) | Unknown | All "Good" | All "Good" |
| Referring domains | 0 | 5 | 20 |

---

## Key Architectural Decision: Pre-rendering Strategy

The most impactful technical decision is **how to handle the SPA indexing problem**. Three options, ranked by recommendation:

### Option A: Build-time HTML injection (Recommended)

During CI/CD, after scrapers run, a Node.js script reads `data.json` and generates the entity cards, comparison tables, and key metrics as static HTML, injecting them directly into `index.html`. The JavaScript then hydrates/enhances this content with interactivity.

**Pros:** Zero runtime overhead, guaranteed crawlability, works with GitHub Pages, no external dependencies.
**Cons:** Requires maintaining a pre-render script, slight complexity in CI/CD.

### Option B: Comprehensive `<noscript>` fallback

Add a `<noscript>` block with a complete static HTML representation of all fee data. The JS-rendered version handles the interactive experience.

**Pros:** Simpler than Option A, ensures Googlebot always sees content.
**Cons:** `<noscript>` content may be treated as lower priority by Google; duplicate content concerns.

### Option C: Server-side rendering (Over-engineered)

Move to a framework like Astro, Next.js, or Eleventy with SSG (static site generation).

**Pros:** Clean architecture, built-in SSG, component model.
**Cons:** Massive overhaul for a single-page tool, unnecessary complexity, moves away from the project's vanilla JS philosophy.

**Recommendation:** Implement **Option A** with **Option B** as a fallback safety net. This provides belt-and-suspenders crawlability while maintaining the current simple architecture.

---

## YMYL Considerations

This site falls under Google's "Your Money or Your Life" (YMYL) classification because it provides financial information that could impact users' business decisions. YMYL pages are held to higher quality standards:

1. **Accuracy:** Every fee must trace to an official source (already done via `feeUrl`)
2. **Freshness:** Data must be current (weekly scraping handles this)
3. **Transparency:** Methodology must be clear (Phase 2: About section)
4. **Authority:** The site/author should have demonstrable expertise (open source + official sources help)
5. **Trust signals:** HTTPS (done), clear sourcing (to improve), no deceptive practices (good)

The automated scraping pipeline is a genuine competitive advantage for YMYL compliance — no competitor updates their fee data automatically from official sources.
