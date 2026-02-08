# Sprint 1: SEO Foundation

**Goal:** Establish all baseline SEO signals so the site can be properly discovered, crawled, indexed, and presented in search results.

**Prerequisite:** Domain `cobrocontarjeta.com.ar` DNS must be configured and propagated before starting (see task 1.0).

---

## Task 1.0 — Configure Custom Domain

**Priority:** Blocker — all other tasks depend on this

### 1.0.1 Create CNAME file

**File:** `CNAME` (project root, no extension)

```
cobrocontarjeta.com.ar
```

### 1.0.2 Configure DNS records

At the `.com.ar` registrar, add:

```
A     @    185.199.108.153
A     @    185.199.109.153
A     @    185.199.110.153
A     @    185.199.111.153

AAAA  @    2606:50c0:8000::153
AAAA  @    2606:50c0:8001::153
AAAA  @    2606:50c0:8002::153
AAAA  @    2606:50c0:8003::153

CNAME www  jrusco.github.io.
```

### 1.0.3 Enable HTTPS in GitHub

1. Repository → Settings → Pages
2. Custom domain: `cobrocontarjeta.com.ar`
3. Check **Enforce HTTPS**
4. Wait for green checkmark (up to 24h for SSL provisioning)

### 1.0.4 Verify

```bash
dig cobrocontarjeta.com.ar +short
# Expect: 185.199.108.153 ...

curl -I https://cobrocontarjeta.com.ar
# Expect: HTTP/2 200
```

### 1.0.5 Add domain to AdSense

1. Google AdSense → Sites → Add site → `cobrocontarjeta.com.ar`
2. Verify `ads.txt` is accessible at `https://cobrocontarjeta.com.ar/ads.txt`
3. Wait for approval (24h–2 weeks)

### Acceptance criteria

- [ ] `https://cobrocontarjeta.com.ar` serves the site over HTTPS
- [ ] `https://jrusco.github.io/monitor-comisiones-bancarias/` 301-redirects to the new domain
- [ ] `ads.txt` accessible at new domain root

---

## Task 1.1 — Meta Description, Canonical URL, Robots Meta

**File:** `index.html` — `<head>` section

### Current state (lines 2–7)

```html
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor de Comisiones y Recursos: Pagos Argentina</title>
```

### Target state

```html
<html lang="es-AR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparar Comisiones Cobro con Tarjeta | Argentina 2026</title>
    <meta name="description" content="Compará comisiones de Mercado Pago, Ualá, Banco Nación y Banco Provincia para cobrar con tarjeta de débito y crédito. Datos actualizados semanalmente desde fuentes oficiales.">
    <link rel="canonical" href="https://cobrocontarjeta.com.ar/">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
```

### Implementation notes

- **Title:** 55 characters. Front-loads primary keyword "Comisiones Cobro con Tarjeta". Year "2026" provides freshness signal and CTR boost. Update the year annually via CI/CD or manually each January.
- **Description:** 185 characters. Includes all four entity names (Mercado Pago, Ualá, Banco Nación, Banco Provincia) and the differentiator "actualizado semanalmente". Uses Argentine Spanish "Compará" (voseo).
- **Canonical:** Self-referencing canonical to the new domain. Prevents duplicate content from any trailing-slash or query-string variants.
- **Robots:** `max-snippet:-1` allows Google to show full-length snippets. `max-image-preview:large` is required for Google Discover eligibility.
- **lang change:** `es` → `es-AR` for precise geo-linguistic targeting (also covers Task 1.3).

### Acceptance criteria

- [ ] `<html lang="es-AR">` replaces `<html lang="es">`
- [ ] `<title>` is under 60 characters and contains primary keyword
- [ ] `<meta name="description">` is 150–160 characters and mentions entity names
- [ ] `<link rel="canonical">` points to `https://cobrocontarjeta.com.ar/`
- [ ] `<meta name="robots">` includes `max-image-preview:large`
- [ ] View page source confirms all tags are in the raw HTML (not JS-injected)

---

## Task 1.2 — Open Graph + Twitter Card Tags

**File:** `index.html` — `<head>` section, after the robots meta

### Code to add

```html
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Comparador de Comisiones por Cobro con Tarjeta en Argentina">
    <meta property="og:description" content="Compará comisiones de Mercado Pago, Ualá, Banco Nación y Banco Provincia. Datos actualizados semanalmente desde fuentes oficiales.">
    <meta property="og:url" content="https://cobrocontarjeta.com.ar/">
    <meta property="og:locale" content="es_AR">
    <meta property="og:site_name" content="Cobro con Tarjeta Argentina">
    <meta property="og:image" content="https://cobrocontarjeta.com.ar/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Comparador de Comisiones por Cobro con Tarjeta en Argentina">
    <meta name="twitter:description" content="Compará comisiones de Mercado Pago, Ualá, Banco Nación y Banco Provincia. Datos actualizados semanalmente.">
    <meta name="twitter:image" content="https://cobrocontarjeta.com.ar/og-image.png">
```

### OG Image placeholder

Until the final OG image is designed (Sprint 2, Task 16), create a simple placeholder:

```html
<!-- Temporary: generate via https://og-image-generator tools or create a simple 1200x630 PNG -->
<!-- Must include: site name, tagline, visual hint of comparison (chart/table) -->
```

The OG image should eventually contain:
- "Cobro con Tarjeta Argentina" as headline text
- "Compará comisiones de cobro con tarjeta" as subtext
- Entity logos or a visual comparison element
- Blue gradient background matching the hero section (#2563eb → #1d4ed8)
- Minimum 1200x630px (required for `max-image-preview:large`)

### Acceptance criteria

- [ ] Sharing the URL on WhatsApp/Telegram/Twitter shows a rich preview with title + description
- [ ] `og:url` points to `https://cobrocontarjeta.com.ar/`
- [ ] `og:locale` is `es_AR`
- [ ] `og:site_name` uses the new brand name "Cobro con Tarjeta Argentina"

---

## Task 1.3 — Change `lang="es"` to `lang="es-AR"`

Covered in Task 1.1 above. The single edit `<html lang="es-AR">` satisfies both tasks.

---

## Task 1.4 — JSON-LD Structured Data

**File:** `index.html` — inside `<head>`, before `</head>`

### Code to add

```html
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "WebApplication",
          "@id": "https://cobrocontarjeta.com.ar/#app",
          "name": "Cobro con Tarjeta Argentina",
          "alternateName": "Monitor de Comisiones Bancarias",
          "description": "Comparador de comisiones por cobro con tarjeta de débito y crédito en Argentina",
          "url": "https://cobrocontarjeta.com.ar/",
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
          "@type": "BreadcrumbList",
          "itemListElement": [
            {
              "@type": "ListItem",
              "position": 1,
              "name": "Inicio",
              "item": "https://cobrocontarjeta.com.ar/"
            },
            {
              "@type": "ListItem",
              "position": 2,
              "name": "Comparador de Comisiones"
            }
          ]
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
                "feesAndCommissionsSpecification": "https://aranceles.fiservargentina.com/"
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
                "feesAndCommissionsSpecification": "https://www.bancoprovincia.com.ar/web/adhesion_comercios"
              }
            }
          ]
        }
      ]
    }
    </script>
```

### Implementation notes

- The `feesAndCommissionsSpecification` URLs match the actual `feeUrl` values from `data.json` (verified).
- `BreadcrumbList` is included now — will become more valuable once entity anchors are added (Sprint 3).
- The `FAQPage` schema is intentionally omitted here — it will be added in Sprint 2 when the FAQ content exists.
- In Sprint 3 (Task 25), the pre-render script will dynamically update the `feesAndCommissionsSpecification` fields with actual rate text.

### Validation

After deploying, test at:
- https://search.google.com/test/rich-results (paste URL)
- https://validator.schema.org/ (paste JSON-LD)

### Acceptance criteria

- [ ] JSON-LD block is valid JSON (no parse errors)
- [ ] Google Rich Results Test shows "WebApplication" and "ItemList" detected
- [ ] All `feesAndCommissionsSpecification` URLs return 200 OK
- [ ] `@id` and `url` use `https://cobrocontarjeta.com.ar/`

---

## Task 1.5 — Create robots.txt

**File:** `robots.txt` (new, project root)

```
User-agent: *
Allow: /
Disallow: /cmd/
Disallow: /internal/
Disallow: /scripts/

Sitemap: https://cobrocontarjeta.com.ar/sitemap.xml
```

### Implementation notes

- `/cmd/` and `/internal/` contain Go source code — no value in indexing these.
- `/scripts/` will contain the pre-render script (Sprint 3) — also no indexing value.
- The `Sitemap` directive points to the new domain.
- GitHub Pages serves `robots.txt` from the repo root when `.nojekyll` is present (Task 1.7).

### Acceptance criteria

- [ ] `https://cobrocontarjeta.com.ar/robots.txt` returns 200 and correct content
- [ ] `Sitemap:` URL matches the actual sitemap location

---

## Task 1.6 — Create sitemap.xml

**File:** `sitemap.xml` (new, project root)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://cobrocontarjeta.com.ar/</loc>
    <lastmod>2026-02-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

### Implementation notes

- Single URL for now. Additional pages (glossary, changelog) can be added later.
- `<lastmod>` will be automatically updated by CI/CD (Sprint 3, Task 24).
- `<changefreq>weekly` matches the scraper schedule (Sundays 3 AM UTC).

### Acceptance criteria

- [ ] `https://cobrocontarjeta.com.ar/sitemap.xml` returns valid XML
- [ ] `<loc>` uses the canonical domain URL
- [ ] `<lastmod>` reflects the most recent data update

---

## Task 1.7 — Create .nojekyll File

**File:** `.nojekyll` (new, empty, project root)

```bash
touch .nojekyll
```

This is an empty file. Its presence tells GitHub Pages to skip Jekyll processing and serve all files as-is. Without it, `robots.txt`, `sitemap.xml`, and files starting with underscores may not be served.

### Acceptance criteria

- [ ] File exists and is committed
- [ ] `robots.txt` and `sitemap.xml` are served correctly (not 404)

---

## Task 1.8 — Add Favicon

**File:** `favicon.svg` (new, project root)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2563eb"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
  </defs>
  <rect width="32" height="32" rx="6" fill="url(#g)"/>
  <text x="16" y="22" font-family="system-ui,sans-serif" font-size="16" font-weight="bold"
        fill="white" text-anchor="middle">CT</text>
</svg>
```

### Add to `<head>` in `index.html`

```html
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta name="theme-color" content="#1e40af">
```

### Implementation notes

- "CT" abbreviation for "Cobro con Tarjeta" matches the new brand.
- SVG favicons are supported in all modern browsers and scale perfectly.
- `theme-color` controls the browser chrome color on mobile (Android Chrome, Safari).
- `apple-touch-icon` (PNG) will be created in Sprint 2 (Task 17) — omit it for now rather than adding a broken reference.

### Acceptance criteria

- [ ] Browser tab shows the favicon
- [ ] Mobile Chrome address bar tints to `#1e40af` (dark blue)

---

## Task 1.9 — Add Preconnect Hints for CDNs

**File:** `index.html` — `<head>`, right after `<meta name="viewport">`

### Code to add

Place these **before** any CDN script/stylesheet references so the browser starts DNS+TCP+TLS handshakes early:

```html
    <!-- Preconnect to CDN origins -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
    <link rel="preload" href="data.json" as="fetch" crossorigin>
```

### Implementation notes

- `crossorigin` attribute is required for font origins and CDN origins that serve with CORS.
- The existing `<link rel="preconnect" href="//pagead2.googlesyndication.com">` for AdSense should remain.
- `data.json` preload tells the browser to start fetching data immediately, rather than waiting for JS to execute and issue the `fetch()` call.
- The Tailwind CDN preconnect is intentionally omitted — it will be removed entirely in Sprint 3 when replaced with static CSS.

### Reordered `<head>` structure

After Sprint 1 is complete, the `<head>` should follow this order:

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- SEO Meta -->
    <title>...</title>
    <meta name="description" content="...">
    <link rel="canonical" href="...">
    <meta name="robots" content="...">

    <!-- Geographic -->
    <meta name="geo.region" content="AR">
    <meta name="geo.placename" content="Argentina">
    <link rel="alternate" href="https://cobrocontarjeta.com.ar/" hreflang="es-AR">
    <link rel="alternate" href="https://cobrocontarjeta.com.ar/" hreflang="x-default">

    <!-- Open Graph -->
    <meta property="og:...">
    ...

    <!-- Twitter Card -->
    <meta name="twitter:...">
    ...

    <!-- Preconnect + Preload (early hints) -->
    <link rel="preconnect" href="...">
    ...

    <!-- Favicon + Theme -->
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta name="theme-color" content="#1e40af">

    <!-- Stylesheets -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/..." rel="stylesheet">

    <!-- Scripts (defer where possible) -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js" defer></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2" defer></script>

    <!-- AdSense -->
    <link rel="preconnect" href="//pagead2.googlesyndication.com">
    <link rel="dns-prefetch" href="//pagead2.googlesyndication.com">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/..." crossorigin="anonymous"></script>

    <!-- Inline Styles -->
    <style>...</style>

    <!-- Structured Data -->
    <script type="application/ld+json">...</script>
</head>
```

### Quick performance win: `defer` on Chart.js

While in `<head>`, add `defer` to Chart.js scripts (zero-risk change that prevents render-blocking):

```html
<!-- Before -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>

<!-- After -->
<script src="https://cdn.jsdelivr.net/npm/chart.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2" defer></script>
```

Note: Verify the chart still renders correctly since `defer` changes script execution timing. The chart initialization in the inline `<script>` block uses `DOMContentLoaded`, which fires after deferred scripts, so this should work. Test locally before deploying.

### Acceptance criteria

- [ ] Preconnect hints appear before CDN resource requests in the HTML
- [ ] `data.json` preload appears in DevTools Network tab as "preload" priority
- [ ] Chart.js scripts have `defer` attribute
- [ ] Chart still renders correctly with deferred loading

---

## Task 1.10 — Register with Google Search Console

This is a manual task (not code).

### Steps

1. Go to https://search.google.com/search-console/
2. Click **Add property**
3. Choose **Domain** property type
4. Enter `cobrocontarjeta.com.ar`
5. Add the provided DNS TXT record at the registrar:
   ```
   TXT  @  "google-site-verification=XXXXXXXXXXXXX"
   ```
6. Wait for DNS propagation and verify
7. Submit sitemap: enter `sitemap.xml` in the Sitemaps section
8. Go to **Legacy tools and reports → International Targeting** → set country to **Argentina**
9. Use **URL Inspection** to request indexing of `https://cobrocontarjeta.com.ar/`

### Also register with Bing Webmaster Tools

1. Go to https://www.bing.com/webmasters/
2. Add `cobrocontarjeta.com.ar`
3. Verify via DNS CNAME:
   ```
   CNAME  _bingverify  verify.bing.com.
   ```
4. Submit sitemap

### Acceptance criteria

- [ ] Google Search Console shows "Property verified" for `cobrocontarjeta.com.ar`
- [ ] Sitemap status shows "Success" (no errors)
- [ ] URL Inspection shows the page as "URL is on Google" (may take a few days)
- [ ] Bing Webmaster Tools shows property verified

---

## Sprint 1 Commit Plan

Commit changes in logical groups:

```bash
# Commit 1: Domain setup
git add CNAME .nojekyll
git commit -m "feat(seo): configure cobrocontarjeta.com.ar custom domain"

# Commit 2: SEO meta tags + head restructure
git add index.html
git commit -m "feat(seo): add meta description, OG tags, canonical, structured data

Add complete SEO head section: title optimization, meta description,
canonical URL, robots directives, Open Graph, Twitter Card, hreflang,
geo-targeting, JSON-LD structured data (WebApplication + ItemList +
PaymentService + BreadcrumbList), preconnect hints, favicon, and
theme-color. Defer Chart.js loading."

# Commit 3: Crawl infrastructure
git add robots.txt sitemap.xml favicon.svg
git commit -m "feat(seo): add robots.txt, sitemap.xml, and favicon"

# Push
git push -u origin main
```

---

## Verification Checklist (Post-Deploy)

Run these checks after Sprint 1 is deployed:

| Check | Tool | Expected Result |
|-------|------|-----------------|
| Meta tags in source | View page source | All tags visible in raw HTML |
| OG preview | https://www.opengraph.xyz/ | Title, description, image preview |
| Structured data | https://search.google.com/test/rich-results | WebApplication + ItemList detected |
| robots.txt | `curl https://cobrocontarjeta.com.ar/robots.txt` | 200 OK, correct content |
| sitemap.xml | `curl https://cobrocontarjeta.com.ar/sitemap.xml` | 200 OK, valid XML |
| HTTPS | `curl -I https://cobrocontarjeta.com.ar` | HTTP/2 200 |
| Redirect | `curl -I http://cobrocontarjeta.com.ar` | 301 → https:// |
| Favicon | Browser tab | CT icon visible |
| Mobile meta | Chrome DevTools mobile view | Theme color in address bar |
