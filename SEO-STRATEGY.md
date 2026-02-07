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

---

## Part 4: Performance Deep Dive — What the First Plan Missed

The original plan covers SEO fundamentals well but underestimates several **performance-critical issues** that directly affect ranking. Google's Page Experience signals are not just "nice to have" — for YMYL content in a competitive niche, they are tie-breakers that determine position #1 vs. position #5.

### 4.1 Tailwind CSS via CDN Is a Performance Anti-Pattern

**Current state:** `<script src="https://cdn.tailwindcss.com"></script>` (line 8 of index.html)

This is the **single biggest performance problem** on the site. The Tailwind CDN is explicitly marked "for development only" by the Tailwind team. Here's what it does at runtime:

1. Downloads ~115KB of JavaScript
2. Scans the entire DOM for class names
3. Generates CSS on-the-fly in the browser
4. Injects a `<style>` tag with the computed styles

This means:
- **Render-blocking JS** — The browser can't paint anything until Tailwind finishes generating CSS
- **FOUC (Flash of Unstyled Content)** — Users see raw HTML briefly before styles apply
- **LCP degradation** — The Largest Contentful Paint is delayed by 200-500ms+
- **FID/INP impact** — The main thread is blocked during CSS generation
- **No caching benefit** — Generated CSS changes if DOM changes

**Fix: Build a static CSS file.**

```bash
# Install Tailwind CLI (no Node.js project needed)
npx @tailwindcss/cli -i input.css -o dist/tailwind.min.css --minify
```

Or use the standalone Tailwind CLI binary (no npm required):

```bash
# Download standalone binary
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64
./tailwindcss-linux-x64 -i input.css -o tailwind.min.css --minify
```

The resulting CSS file will be ~15-30KB (vs. 115KB JS + runtime generation), loads as a `<link rel="stylesheet">`, is fully cacheable, and eliminates FOUC entirely.

**Add to CI/CD:** Regenerate the CSS file whenever index.html changes:

```yaml
- name: Build Tailwind CSS
  run: npx @tailwindcss/cli -i input.css -o tailwind.min.css --minify
```

**Impact:** This single change could improve LCP by 300-800ms, which is the difference between a "Good" and "Poor" Core Web Vitals score.

### 4.2 Chart.js Load Strategy

**Current state:** Chart.js (~200KB) and its datalabels plugin (~30KB) are loaded synchronously in `<head>`.

The chart is below the fold — users don't see it until they scroll. Loading it synchronously delays everything above the fold.

**Fix:**
1. Add `defer` to Chart.js script tags (at minimum)
2. Better: Lazy-load Chart.js only when the chart section enters the viewport

```javascript
// Intersection Observer to lazy-load Chart.js
const chartObserver = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = () => {
            // Load plugin, then render chart
        };
        document.head.appendChild(script);
        chartObserver.disconnect();
    }
}, { rootMargin: '200px' }); // Start loading 200px before visible
chartObserver.observe(document.querySelector('.chart-container'));
```

**Impact:** Reduces initial page weight by ~230KB, significantly improving Time to Interactive.

### 4.3 Google Fonts: Eliminate Render-Blocking Chain

**Current state:** Google Fonts loaded via `<link>` in `<head>` — this creates a render-blocking request chain:
1. Browser requests the CSS file from fonts.googleapis.com
2. CSS file contains `@font-face` declarations pointing to fonts.gstatic.com
3. Browser then downloads the actual font files

**Fix:** Use `font-display: swap` (already default in Google Fonts) AND preload the most critical font weight:

```html
<link rel="preload" href="https://fonts.gstatic.com/s/dmsans/v15/...wght@500.woff2"
      as="font" type="font/woff2" crossorigin>
```

Or better yet, self-host the fonts:
- Download DM Sans (400, 500, 600, 700) and DM Serif Display
- Serve from the same domain — eliminates DNS lookup, connection, and TLS handshake to two external domains
- Use `font-display: swap` in the local `@font-face` declarations

### 4.4 AdSense Placement vs. Core Web Vitals

**Current state:** An ad is placed directly between the hero section and the chart (line 350-361). This is the **first content users see below the hero**.

**Problems:**
- **CLS (Cumulative Layout Shift):** AdSense ads load asynchronously with unknown dimensions. When the ad loads, it pushes all content below it down, causing layout shift — one of the three Core Web Vitals.
- **Above-the-fold ad density:** Google's "page layout" algorithm (informally called the "top heavy" update) can demote pages where ads are more prominent than content above the fold on mobile.
- **LCP interference:** On mobile, the ad container may become the LCP element if it's the largest visible element — and its load timing is unpredictable.

**Fix:**
1. **Reserve space:** Set explicit `min-height` on ad containers to prevent CLS:
   ```css
   .ad-container { min-height: 100px; } /* Match expected ad height */
   ```
2. **Move first ad below the fold:** Push the first ad unit below the chart section, or at minimum after two content sections. The pre-footer ad placement (line 548) is fine.
3. **Lazy-load ads:** Only initialize AdSense when the ad container is near the viewport:
   ```javascript
   // Don't push ad immediately; wait for visibility
   const adObserver = new IntersectionObserver((entries) => {
       entries.forEach(entry => {
           if (entry.isIntersecting) {
               (adsbygoogle = window.adsbygoogle || []).push({});
               adObserver.unobserve(entry.target);
           }
       });
   }, { rootMargin: '300px' });
   document.querySelectorAll('.adsbygoogle').forEach(ad => adObserver.observe(ad));
   ```

### 4.5 Resource Loading Priority

**Current `<head>` order creates a suboptimal loading waterfall:**

```
1. Tailwind CDN (sync JS — render-blocking)
2. Chart.js (sync JS — render-blocking)
3. Chart.js plugin (sync JS — render-blocking)
4. Google Fonts (render-blocking CSS → font files)
5. AdSense (async JS)
```

**Optimized order should be:**

```
1. Critical CSS (inlined <style> or local stylesheet — minimal, no external request)
2. Preconnect hints (fonts, CDNs)
3. Google Fonts (with preload for key weight)
4. AdSense (async, deferred)
5. Chart.js + plugin (defer or lazy-load)
6. Application JS (defer)
```

**Use `fetchpriority` attribute** on critical resources:
```html
<link rel="stylesheet" href="tailwind.min.css" fetchpriority="high">
<script src="https://cdn.jsdelivr.net/npm/chart.js" defer fetchpriority="low"></script>
```

---

## Part 5: Expert SEO Review — What Senior SEO Specialists Would Flag

### 5.1 Title Tag Is Too Long

The proposed title in Phase 1:
> "Comisiones por Cobro con Tarjeta en Argentina — Comparador Actualizado | Monitor Comisiones"

This is **~90 characters**. Google truncates titles at approximately **55-60 characters** on desktop and **50-55 on mobile** (or more precisely, ~580 pixels). Everything after the cut-off is replaced with "...".

Users would see: `Comisiones por Cobro con Tarjeta en Argentina — Com...`

**Revised recommendation:**

```html
<!-- Primary (55 chars): -->
<title>Comisiones Tarjeta Argentina — Comparador 2026</title>

<!-- Alternative targeting specific intent (58 chars): -->
<title>Comparar Comisiones Cobro con Tarjeta | Argentina 2026</title>
```

Include the year — it's a powerful freshness signal for financial queries and dramatically improves CTR because users want current rates. Update it annually (or via CI/CD when the year changes).

**SEO pro tip:** The `|` or `—` separators eat precious character space. Use them sparingly. Front-load the primary keyword.

### 5.2 The `<noscript>` Strategy Has a Flaw

The original plan proposes `<noscript>` as a fallback for Googlebot. However, **Googlebot executes JavaScript**. When JS rendering succeeds, Googlebot does NOT read `<noscript>` content — it only reads it when JS execution fails entirely.

This means `<noscript>` is a safety net for rendering failures, not a primary crawlability solution. The plan correctly identifies Option A (build-time HTML injection) as the better approach, but the emphasis should be stronger:

**The pre-rendered HTML should be the DEFAULT content of the containers**, not hidden in `<noscript>`. The JavaScript should then *replace* this static content with the interactive version. This pattern is called "progressive enhancement" and ensures:

1. Googlebot's first-pass HTML crawl sees full content (no JS needed)
2. Googlebot's JS rendering sees the enhanced version (also fine)
3. Users with slow connections see content immediately (better perceived performance)
4. Users with JS disabled still get a complete, usable page

```html
<!-- The container starts with static pre-rendered content -->
<div id="entity-grid">
  <!-- Pre-rendered by CI/CD from data.json -->
  <div class="entity-card">
    <h3>Mercado Pago</h3>
    <table>...</table>
  </div>
  <!-- More entities... -->
</div>

<script>
  // JS replaces static content with interactive version
  async function initApp() {
    const data = await fetch('data.json').then(r => r.json());
    document.getElementById('entity-grid').innerHTML = renderInteractiveGrid(data);
  }
</script>
```

### 5.3 Missing: IndexNow for Instant Indexing

When fees change (detected by scrapers), the site should notify search engines immediately rather than waiting for them to re-crawl. **IndexNow** is a protocol supported by Bing, Yandex, and other search engines (Google has its own Indexing API).

**Implementation in CI/CD:**

```yaml
- name: Notify IndexNow
  if: steps.check_changes.outputs.has_changes == 'true'
  run: |
    curl -X POST "https://api.indexnow.org/indexnow" \
      -H "Content-Type: application/json" \
      -d '{
        "host": "jrusco.github.io",
        "key": "${{ secrets.INDEXNOW_KEY }}",
        "urlList": [
          "https://jrusco.github.io/monitor-comisiones-bancarias/"
        ]
      }'
```

For Google, use the Search Console URL Inspection API or the Indexing API (requires setup).

This is particularly valuable because the site updates weekly — you want those changes indexed within hours, not days.

### 5.4 Missing: Google Discover Optimization

Google Discover (the feed on the Google app home screen and Chrome new tab page on Android) drives massive mobile traffic in Latin America. To appear in Discover:

1. **Large, high-quality images are mandatory** — Google requires images at least 1200px wide with `max-image-preview:large` meta tag:
   ```html
   <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
   ```
2. **Compelling, non-clickbait title** — The current title lacks emotional hook. For Discover, consider dynamic titles tied to data: "Mercado Pago cobra 3.25% — Mirá quién cobra menos"
3. **Freshness** — Discover strongly favors recently updated content. The weekly update cycle is an asset.
4. **Entity association** — Using structured data to link the page to known entities (Mercado Pago, banks) helps Discover's topic matching.

Note: Discover works best with multiple pages/articles. This reinforces the case for the automated changelog/blog in Phase 4.2.

### 5.5 Missing: Bing Webmaster Tools

The plan only mentions Google Search Console. Bing has grown significantly in Argentina due to:
- Microsoft Edge's increased market share
- Bing's integration with Windows Search
- ChatGPT/Copilot using Bing for web results

Submit the site to Bing Webmaster Tools separately. Bing's crawler behaves differently from Google's and may not handle JS rendering as well — another reason the pre-rendering approach (Phase 3.1) is critical.

### 5.6 Missing: Content Depth and Word Count

The current `index.html` has almost **zero static text content** visible to first-pass crawlers. Everything meaningful is generated by JavaScript. Even with pre-rendering, the page is thin on explanatory content.

Google's **Helpful Content System** (HCS) evaluates whether a page provides genuine value beyond what competitors offer. For YMYL content, this bar is higher.

**Recommendation:** Add 300-500 words of static, crawlable explanatory text to the page:

- **Hero sub-text:** Brief explanation of what the tool does and why it matters (2-3 sentences targeting primary keywords naturally)
- **Section intros:** Before the chart, a sentence explaining what the comparison shows
- **Educational preamble:** Before the entity grid, a paragraph explaining how Argentine payment processing fees work (IVA, settlement terms, the difference between acquiring banks and aggregators)
- **Footer content:** Expand the footer with methodology notes, legal context (Ley 27253), and links to official regulatory information

This text should be **static HTML** (not JS-injected), use natural Argentine Spanish, and weave in target keywords without stuffing.

### 5.7 Missing: Breadcrumb and Navigation Structured Data

Even for a single page, `BreadcrumbList` structured data helps Google understand the page's position and can generate breadcrumb rich results:

```json
{
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Inicio",
      "item": "https://jrusco.github.io/monitor-comisiones-bancarias/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Comparador de Comisiones"
    }
  ]
}
```

This becomes more valuable when entity-specific anchors (Phase 4.1) are implemented — each section can have its own breadcrumb trail.

### 5.8 Missing: `<time>` Elements for Freshness Signals

The original plan mentions timestamps but doesn't emphasize their HTML implementation. Google parses `<time datetime="...">` elements to understand content freshness:

```html
<time datetime="2026-02-07" itemprop="dateModified">
  Actualizado: 7 de febrero de 2026
</time>
```

Place this prominently in the hero section or above the entity grid. Update it via pre-render script every time data changes.

### 5.9 Missing: Security Headers

While not a direct ranking factor, security signals contribute to overall site trust. GitHub Pages provides basic headers, but consider adding a `_headers` file (supported by some static hosts) or ensuring:

- **Content-Security-Policy** — Restricts which scripts can execute (helps prevent XSS, builds trust)
- **X-Content-Type-Options: nosniff**
- **Referrer-Policy: strict-origin-when-cross-origin**

On GitHub Pages, many of these are set automatically, but verify with a tool like SecurityHeaders.com.

### 5.10 The Canonical URL Must Account for Domain Changes

The plan proposes a canonical URL with the GitHub Pages domain. If a `.com.ar` domain is later added (Phase 5.1), all canonical URLs, OG URLs, sitemap URLs, and structured data URLs must be updated simultaneously. Failure to do this causes:

- Canonical confusion (Google sees two versions of the site)
- Loss of accumulated PageRank during migration
- Deindexing of one version

**Recommendation:** When migrating to a custom domain:
1. Set up 301 redirects from `jrusco.github.io/monitor-comisiones-bancarias/` to the new domain
2. Update all canonical/OG/structured data URLs
3. Submit a Change of Address in Google Search Console
4. Keep the old sitemap for 6 months with the new URLs

Plan the URL structure from day one to minimize migration pain.

### 5.11 Link Attribute Strategy for Outbound Links

The current plan recommends displaying "Ver fuente oficial" links. Ensure these use proper attributes:

```html
<!-- Outbound link to official fee source -->
<a href="https://www.mercadopago.com.ar/ayuda/2779"
   rel="noopener"
   target="_blank">
  Ver fuente oficial
</a>
```

**Do NOT use `rel="nofollow"` on these links.** Linking to authoritative sources (bank websites, official fee pages) without `nofollow` passes a trust signal to Google — it shows you're citing legitimate sources. This is a positive E-E-A-T signal for YMYL content.

### 5.12 Missing: Keyword Cannibalization Prevention

If the blog/changelog section (Phase 4.2) is implemented, there's a risk of keyword cannibalization — blog posts about "comisiones mercado pago" competing with the main comparison page for the same query.

**Prevention strategy:**
- The main page targets **comparison** and **tool** intent ("comparar comisiones", "calculadora comisiones")
- Blog posts target **news** and **update** intent ("nuevas comisiones mercado pago 2026", "cambios comisiones febrero")
- Use `rel="canonical"` on blog posts to point to the main page if overlap is too strong
- Use internal links from blog posts to the main comparison page with relevant anchor text

---

## Part 6: Nice-to-Have Features for Future Development

These features are not SEO in themselves, but each creates **indirect SEO advantages** through improved engagement, shareability, backlink generation, or user retention.

### 6.1 Embeddable Widget (High Backlink Potential)

Build a lightweight, embeddable `<iframe>` widget that other sites can embed to show fee comparisons. Example:

```html
<!-- Embed code for other sites -->
<iframe src="https://jrusco.github.io/monitor-comisiones-bancarias/widget.html?entity=mercadopago"
        width="400" height="300" frameborder="0"></iframe>
<p><a href="https://jrusco.github.io/monitor-comisiones-bancarias/">
  Powered by Monitor de Comisiones Bancarias</a></p>
```

**Why it matters for SEO:** Every site that embeds the widget includes a backlink. This is the same strategy that powered early growth of YouTube, Google Maps, and Spotify embeds. Target:
- Argentine e-commerce blogs
- Monotributista/PYME resource sites
- Accounting firm websites
- Fintech news outlets

### 6.2 Historical Fee Tracking with Trend Charts

Store fee snapshots over time (monthly or per-change) and display trend lines showing how each entity's fees have evolved. This could be stored as a `history.json` file updated by CI/CD.

**SEO benefit:**
- Creates unique, high-value data that no one else has
- Generates ongoing content ("Mercado Pago fees have decreased 15% in the last 6 months")
- Targets informational queries like "historico comisiones mercado pago"
- Increases dwell time (users explore trends = positive engagement signal)

### 6.3 Export to PDF / CSV

Allow users to download fee comparisons as PDF reports or CSV files.

**SEO benefit:**
- Increases user engagement metrics (interaction = quality signal)
- PDFs can be indexed by Google separately (more SERP real estate)
- CSV downloads are valuable for accountants/financial advisors who may share or link to the tool
- Creates a "utility" signal — Google increasingly favors tools over static content

### 6.4 Fee Change Notifications (Email / Push)

Allow users to subscribe to notifications when fees change for specific entities.

**SEO benefit:**
- Repeat visitors are a strong engagement signal
- Push notifications bring users back regularly (higher return visit rate)
- Email list enables direct re-engagement for link building campaigns
- Creates a "loyal audience" signal that correlates with quality

Implementation: Use a lightweight service like Web Push API (free, no server needed) or integrate with a simple email service (Buttondown, Mailchimp free tier).

### 6.5 WhatsApp Sharing with Pre-Built Message

WhatsApp is the dominant messaging platform in Argentina (~95% penetration). Add a WhatsApp share button that generates a pre-built message:

```
Encontré esta herramienta para comparar comisiones de cobro con tarjeta 🔍

Mercado Pago Point Débito: 3.25% + IVA
Banco Nación Débito: 0.8% + IVA

Mirá la comparativa completa: https://jrusco.github.io/monitor-comisiones-bancarias/
```

**SEO benefit:**
- WhatsApp shares generate direct traffic (referral traffic is a positive signal)
- Viral potential in Argentine business groups (monotributistas, comerciantes)
- URL sharing creates brand awareness, which leads to branded searches (strongest ranking signal)

### 6.6 PWA (Progressive Web App) with Offline Support

Add `manifest.json` and a basic service worker for:
- "Add to Home Screen" prompt on mobile
- Offline access to last-fetched fee data
- Faster repeat visits (service worker caching)

```json
{
  "name": "Monitor de Comisiones Bancarias",
  "short_name": "Comisiones AR",
  "start_url": "/monitor-comisiones-bancarias/",
  "display": "standalone",
  "background_color": "#f8fafc",
  "theme_color": "#1e40af",
  "icons": [
    { "src": "icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

**SEO benefit:**
- PWA installability is a positive signal for Lighthouse/Page Experience
- Offline mode increases perceived reliability
- Home screen icon creates brand recall and repeat visits
- Service worker enables faster loading on return visits (better Core Web Vitals for returning users)

### 6.7 Multi-Entity Comparison Mode

Let users select 2-3 specific entities and view a side-by-side comparison table. Currently, the grid shows all entities but doesn't support head-to-head comparisons.

**SEO benefit:**
- Targets "vs" queries ("mercado pago vs uala", "banco nacion vs banco provincia")
- Creates deep-linkable comparison URLs (e.g., `?compare=mercadopago,uala`)
- Increases time-on-page and interactions
- Could generate entity-specific anchor fragments for Google Sitelinks

### 6.8 Community Contributions (Entity Requests)

Add a simple feedback mechanism where users can request new entities to be added (e.g., Payway, MODO, Naranja X, Claro Pay). This could be a GitHub Issues template or a simple Google Form.

**SEO benefit:**
- User engagement signal
- Crowdsourced keyword research (users tell you what they're searching for)
- Community involvement builds brand loyalty and word-of-mouth
- GitHub Issues create additional indexable content about the project

### 6.9 Dark Mode

Not SEO-related at all, but relevant for user experience metrics. Dark mode is increasingly expected, especially on mobile. If users stay longer and interact more because the UI is comfortable, that's a positive engagement signal.

Implementation is straightforward with Tailwind's `dark:` variant and a toggle persisted to `localStorage`.

### 6.10 API for Developers

Expose the fee data as a simple JSON API endpoint (the `data.json` file effectively already is one). Document it and promote it to Argentine developers. Each developer blog post, tutorial, or project that references the API is a backlink.

**Implementation:** The `data.json` file is already publicly accessible. Simply:
1. Document it with a proper API reference
2. Add CORS headers (GitHub Pages includes these by default)
3. Promote on Argentine developer communities (MeetupJS, FreeCodeCamp BA, etc.)

---

## Part 7: Expert Tips, Tricks, and Overlooked Tactics

### 7.1 The "Topical Authority" Play

Google increasingly rewards sites that demonstrate **topical authority** — deep, comprehensive coverage of a specific topic. A single comparison page, no matter how well-optimized, may struggle against broad portals like iKiwi that have dozens of pages on related topics.

**The counter-strategy for a single-page tool:**

1. **Depth within the page:** Make the single page the most comprehensive resource on Argentine payment processing fees. Include every entity, every fee type, settlement terms, IVA calculations, and regulatory context.
2. **Structured internal content:** Use anchor-linked sections that function like "virtual pages" — Google can display these as sitelinks.
3. **Supporting content ring:** Even 3-5 additional pages dramatically help topical authority:
   - `/glosario` — Glossary of payment terms (arancel, adquirente, agregador, IVA, etc.)
   - `/como-funciona` — How card processing works in Argentina
   - `/regulacion` — BCRA regulations and Ley 27253 explained
   - `/changelog` — Automated fee change history

### 7.2 The "People Also Ask" (PAA) Hijack

Google's "People Also Ask" boxes appear for almost every financial query in Spanish. Each PAA answer links to a source page. To appear in PAA:

1. **Use the exact question as an H2 or H3** (not paraphrased)
2. **Answer concisely in the first 40-60 words** immediately after the heading
3. **Then expand** with details, tables, or links

Example:

```html
<h3>¿Cuánto cobra Mercado Pago por cobrar con tarjeta de débito?</h3>
<p>Mercado Pago cobra <strong>3.25% + IVA</strong> por ventas con tarjeta de débito
a través de Point, con acreditación en el momento. Para cobros por QR, la comisión
varía entre 0.80% y 6.29% + IVA según el medio de pago utilizado por el comprador.</p>
```

The FAQ section (Phase 2.1) should be specifically engineered for PAA capture.

### 7.3 Dynamic Structured Data via Pre-rendering

The original plan proposes static JSON-LD. But the most powerful approach is **dynamically-generated JSON-LD that reflects current fee data**. The pre-render script should:

1. Read `data.json`
2. Generate JSON-LD with actual current rates in `feesAndCommissionsSpecification`
3. Inject it into `index.html`

This means the structured data stays synchronized with displayed data — a requirement for Google's structured data policies (structured data must match visible content).

```json
{
  "@type": "PaymentService",
  "name": "Mercado Pago Point - Débito",
  "provider": { "@type": "Organization", "name": "Mercado Pago" },
  "feesAndCommissionsSpecification": "Comisión: 3.25% + IVA. Acreditación: En el momento.",
  "areaServed": { "@type": "Country", "name": "Argentina" }
}
```

### 7.4 Leverage `max-snippet` and `max-image-preview`

```html
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
```

- `max-snippet:-1` — Allows Google to show as much text snippet as it wants (longer snippets = more SERP real estate)
- `max-image-preview:large` — Required for Google Discover eligibility and enables large image thumbnails in search results
- `max-video-preview:-1` — Future-proofing if video content is added

### 7.5 The ".com.ar" Domain Timing Matters

The plan lists a custom domain in Phase 5 (last sprint). **SEO experts would move this to Sprint 1.** Here's why:

- Domain age is a ranking signal — the sooner you register, the sooner the clock starts
- Every day of SEO work on the GitHub Pages URL accumulates PageRank and backlinks on the wrong domain
- Domain migration always causes a temporary ranking dip (2-8 weeks), so it's better to migrate before you have rankings to lose
- A `.com.ar` domain costs ~$5,000 ARS/year (~$5 USD) — negligible cost

**Revised recommendation:** Purchase the domain in Sprint 1. Do all SEO work on the final domain from the start. If budget doesn't allow, at minimum register the domain early to start aging it.

### 7.6 Structured Data Testing Workflow

Add a structured data validation step to CI/CD:

```yaml
- name: Validate structured data
  run: |
    # Extract JSON-LD from index.html and validate
    node -e "
      const html = require('fs').readFileSync('index.html','utf8');
      const match = html.match(/<script type=\"application\/ld\+json\">([\s\S]*?)<\/script>/);
      if (!match) { console.error('No JSON-LD found'); process.exit(1); }
      const data = JSON.parse(match[1]);
      console.log('JSON-LD valid:', data['@context'] === 'https://schema.org');
    "
```

This prevents deploying broken structured data, which can lose rich results eligibility.

### 7.7 The "Freshness Boost" Tactic

Google gives a temporary ranking boost to recently updated content, especially for YMYL topics. The current weekly scraping schedule is good, but can be enhanced:

1. **Update the page's visible "last updated" date** every time scrapers run (even if no fees changed, a "Verified: [date]" message shows freshness)
2. **Vary the content slightly** on each update — rotate the hero subtitle, update the FAQ with seasonal advice, change the chart's default view
3. **Submit to Indexing API** after each update to ensure Google recrawls promptly

### 7.8 Internal Search Data as Keyword Research

If the site grows and a search feature is added, log search queries (anonymized). This reveals:
- What users are looking for but can't find (content gap = opportunity)
- Entity names that should be added
- Query patterns that inform blog content

Even without site search, Google Search Console's "Queries" report provides this data for free.

### 7.9 "Above-the-Fold Content" Test

A simple but often overlooked test: **take a screenshot of the site on a mobile device (375x667 viewport) and assess what is visible without scrolling.**

If the answer is "a hero banner + an ad + loading spinners," the page fails the above-the-fold content test. Google expects meaningful content to be visible immediately.

**Target:** On first mobile paint, the user should see:
1. The site title/H1 (identity)
2. At least one concrete data point (e.g., "Menor comisión débito: 0.8%")
3. A clear value proposition (what this tool does)
4. NO loading spinners (pre-rendered content handles this)
5. NO ads above the primary content

### 7.10 Review Schema for User Ratings (Future)

If user reviews or ratings are ever added (e.g., "Rate your experience with Mercado Pago"), `AggregateRating` schema can trigger star ratings in search results:

```json
{
  "@type": "PaymentService",
  "name": "Mercado Pago",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.2",
    "reviewCount": "156"
  }
}
```

Star ratings in SERPs dramatically increase CTR (estimated 15-30% improvement). However, **only add this if genuine user ratings exist** — fake review markup violates Google's guidelines and will result in a manual action.

---

## Revised Priority Matrix

After the expert review, the implementation priority shifts. Here's the updated order, re-ranked by **actual impact on reaching position #1**:

| Rank | Action | Why It Moves Up/Down |
|------|--------|---------------------|
| 1 | **Purchase .com.ar domain** | Moved from Sprint 4 → Sprint 1. Every day of work on the wrong domain is wasted authority. |
| 2 | **Replace Tailwind CDN with static CSS** | New addition. The single biggest performance win — 300-800ms LCP improvement. |
| 3 | **Build-time pre-rendering of content** | Unchanged (P0). Solves the fundamental "empty page" indexing problem. |
| 4 | **Meta description + title + canonical + robots** | Unchanged (P0). Basic SEO hygiene. |
| 5 | **Add 300-500 words of static explanatory text** | New addition. Addresses content thinness under Helpful Content System. |
| 6 | **JSON-LD structured data (dynamic, pre-rendered)** | Enhanced from static to dynamic generation. |
| 7 | **FAQ section targeting PAA boxes** | Unchanged but refined with PAA capture technique. |
| 8 | **OG/Twitter tags + social image** | Unchanged. |
| 9 | **robots.txt + sitemap.xml + .nojekyll** | Unchanged. |
| 10 | **Chart.js lazy loading + font optimization** | New addition. Secondary performance wins. |
| 11 | **Ad placement optimization** | New addition. CLS/above-fold fixes. |
| 12 | **Google Search Console + Bing Webmaster** | Split — Bing is now explicitly included. |
| 13 | **IndexNow integration in CI/CD** | New addition. Instant indexing on fee changes. |
| 14 | **Entity-specific anchor sections** | Unchanged. |
| 15 | **Embeddable widget** | New addition (nice-to-have). Highest backlink potential. |
| 16 | **Historical fee tracking** | New addition (nice-to-have). Creates unique data moat. |
| 17 | **WhatsApp sharing** | New addition (nice-to-have). Viral potential in AR market. |
| 18 | **PWA manifest + service worker** | New addition (nice-to-have). Engagement and performance. |
| 19 | **Supporting content pages (glossary, regulations)** | New addition. Topical authority building. |
| 20 | **Automated changelog / blog** | Unchanged. Long-term content strategy. |
