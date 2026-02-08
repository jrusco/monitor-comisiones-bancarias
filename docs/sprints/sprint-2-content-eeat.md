# Sprint 2: Content & E-E-A-T

**Goal:** Add the content layers that Google requires for YMYL (Your Money or Your Life) financial pages — FAQ section targeting People Also Ask boxes, methodology transparency, freshness signals, and source attribution. Create visual branding assets.

**Depends on:** Sprint 1 complete (meta tags, structured data, domain configured).

---

## Task 2.1 — FAQ Section with FAQPage Schema

**Files:** `index.html`, JSON-LD block in `<head>`

### 2.1.1 Add FAQ HTML section

Insert a new section in `index.html` **before** the footer, **after** the fee simulator aside. This section must be **static HTML** (not JS-generated) for guaranteed crawlability.

Use `<details>` / `<summary>` for progressive disclosure, and structure questions as H3 headings for PAA (People Also Ask) capture.

```html
    <!-- FAQ Section -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h2 class="text-2xl font-bold text-slate-900 mb-6">Preguntas frecuentes sobre comisiones</h2>

        <div class="space-y-4">
            <details class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden group" open>
                <summary class="px-6 py-4 cursor-pointer font-semibold text-slate-800 hover:bg-slate-50 transition-colors list-none flex justify-between items-center">
                    <h3 class="text-base font-semibold">¿Cuánto cobra Mercado Pago por cobrar con tarjeta de débito?</h3>
                    <svg class="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                </summary>
                <div class="px-6 pb-4 text-slate-600 text-sm leading-relaxed">
                    <p>Mercado Pago cobra <strong>3.25% + IVA</strong> por ventas con tarjeta de débito
                    a través de Point, con acreditación en el momento. Para cobros por QR, la comisión
                    varía entre 0.80% y 6.29% + IVA según el medio de pago utilizado por el comprador.
                    Podés consultar las tarifas oficiales en la
                    <a href="https://www.mercadopago.com.ar/ayuda/2779" rel="noopener" target="_blank"
                       class="text-blue-600 underline hover:text-blue-800">página de costos de Mercado Pago</a>.</p>
                </div>
            </details>

            <details class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden group">
                <summary class="px-6 py-4 cursor-pointer font-semibold text-slate-800 hover:bg-slate-50 transition-colors list-none flex justify-between items-center">
                    <h3 class="text-base font-semibold">¿Qué conviene más: Mercado Pago o Ualá para cobrar con tarjeta?</h3>
                    <svg class="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                </summary>
                <div class="px-6 pb-4 text-slate-600 text-sm leading-relaxed">
                    <p>Depende de tu volumen y tipo de ventas. <strong>Ualá Bis cobra 2.9% + IVA en débito</strong>
                    (vs 3.25% de Mercado Pago Point), lo que lo hace más económico para ventas con débito.
                    En crédito, Ualá cobra 4.4% + IVA mientras Mercado Pago cobra 4.39% + IVA con acreditación a 10 días.
                    Ambos acreditan en el momento para débito. Usá el simulador de arriba para comparar
                    cuánto recibirías según tu monto de venta.</p>
                </div>
            </details>

            <details class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden group">
                <summary class="px-6 py-4 cursor-pointer font-semibold text-slate-800 hover:bg-slate-50 transition-colors list-none flex justify-between items-center">
                    <h3 class="text-base font-semibold">¿Cuánto me descuentan si cobro con tarjeta de crédito en Argentina?</h3>
                    <svg class="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                </summary>
                <div class="px-6 pb-4 text-slate-600 text-sm leading-relaxed">
                    <p>El descuento depende del procesador que utilices. Los <strong>bancos adquirentes</strong>
                    (como Banco Nación y Banco Provincia) cobran <strong>1.8% + IVA</strong> por ventas con
                    crédito, con acreditación en 8-10 días hábiles. Los <strong>agregadores fintech</strong>
                    (Mercado Pago, Ualá) cobran entre 4.39% y 6.29% + IVA, pero ofrecen acreditación
                    inmediata o en menor plazo. A la comisión base siempre se suma el 21% de IVA sobre
                    el monto de la comisión.</p>
                </div>
            </details>

            <details class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden group">
                <summary class="px-6 py-4 cursor-pointer font-semibold text-slate-800 hover:bg-slate-50 transition-colors list-none flex justify-between items-center">
                    <h3 class="text-base font-semibold">¿Cuáles son las comisiones de Banco Nación para comercios?</h3>
                    <svg class="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                </summary>
                <div class="px-6 pb-4 text-slate-600 text-sm leading-relaxed">
                    <p>Banco Nación cobra <strong>0.8% + IVA para débito</strong> (acreditación en 24 horas)
                    y <strong>1.8% + IVA para crédito</strong> (acreditación en 8-10 días hábiles). El
                    mantenimiento de la terminal POS puede ser bonificado o variable según el acuerdo
                    comercial. Consultá los aranceles oficiales en la
                    <a href="https://aranceles.fiservargentina.com/" rel="noopener" target="_blank"
                       class="text-blue-600 underline hover:text-blue-800">página de Fiserv Argentina</a>.</p>
                </div>
            </details>

            <details class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden group">
                <summary class="px-6 py-4 cursor-pointer font-semibold text-slate-800 hover:bg-slate-50 transition-colors list-none flex justify-between items-center">
                    <h3 class="text-base font-semibold">¿Qué es un agregador de pagos y en qué se diferencia de un banco adquirente?</h3>
                    <svg class="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                </summary>
                <div class="px-6 pb-4 text-slate-600 text-sm leading-relaxed">
                    <p>Un <strong>banco adquirente</strong> (como Banco Nación o Banco Provincia) tiene relación
                    directa con las marcas de tarjetas (Visa, Mastercard) y opera bajo los aranceles regulados
                    por el BCRA. Un <strong>agregador de pagos</strong> (como Mercado Pago o Ualá) funciona como
                    intermediario: procesa pagos bajo su propia cuenta adquirente y fija sus propias comisiones,
                    generalmente más altas pero con mayor simplicidad de alta y acreditación más rápida. Los bancos
                    requieren trámites de adhesión y una terminal POS; los agregadores permiten empezar a cobrar
                    con solo descargar una app.</p>
                </div>
            </details>

            <details class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden group">
                <summary class="px-6 py-4 cursor-pointer font-semibold text-slate-800 hover:bg-slate-50 transition-colors list-none flex justify-between items-center">
                    <h3 class="text-base font-semibold">¿Cada cuánto se actualizan las comisiones en este sitio?</h3>
                    <svg class="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                </summary>
                <div class="px-6 pb-4 text-slate-600 text-sm leading-relaxed">
                    <p>Las comisiones se actualizan <strong>automáticamente cada semana</strong> (domingos a las
                    3 AM UTC). Nuestros scrapers consultan las páginas oficiales de cada entidad y, si detectan
                    cambios, actualizan los datos automáticamente. No usamos valores fijos ni estimaciones:
                    todos los datos provienen de fuentes oficiales verificables. Podés ver el
                    <a href="https://github.com/jrusco/monitor-comisiones-bancarias" rel="noopener" target="_blank"
                       class="text-blue-600 underline hover:text-blue-800">código fuente en GitHub</a>.</p>
                </div>
            </details>

            <details class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden group">
                <summary class="px-6 py-4 cursor-pointer font-semibold text-slate-800 hover:bg-slate-50 transition-colors list-none flex justify-between items-center">
                    <h3 class="text-base font-semibold">¿Cómo se comparan las comisiones de cobro por QR vs Point/POS?</h3>
                    <svg class="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                </summary>
                <div class="px-6 pb-4 text-slate-600 text-sm leading-relaxed">
                    <p>El cobro por <strong>QR</strong> generalmente tiene comisiones más bajas que un dispositivo
                    POS/Point porque no requiere hardware. En Mercado Pago, el QR cobra entre 0.80% y 6.29% + IVA
                    según el medio de pago del comprador (débito, crédito, saldo en cuenta), mientras que el Point
                    cobra 3.25% + IVA en débito. Banco Provincia ofrece QR con saldo en cuenta a 0.8% + IVA y
                    Clave DNI (token) a 0.6% + IVA. La diferencia principal está en la experiencia de usuario:
                    QR requiere que el comprador escanee un código, mientras que Point/POS acepta contactless y
                    chip directamente.</p>
                </div>
            </details>
        </div>
    </section>
```

### 2.1.2 Add FAQPage schema to JSON-LD

Update the `@graph` array in the existing JSON-LD block (Sprint 1, Task 1.4). Add this as a new entry:

```json
        {
          "@type": "FAQPage",
          "mainEntity": [
            {
              "@type": "Question",
              "name": "¿Cuánto cobra Mercado Pago por cobrar con tarjeta de débito?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Mercado Pago cobra 3.25% + IVA por ventas con tarjeta de débito a través de Point, con acreditación en el momento. Para cobros por QR, la comisión varía entre 0.80% y 6.29% + IVA según el medio de pago utilizado por el comprador."
              }
            },
            {
              "@type": "Question",
              "name": "¿Qué conviene más: Mercado Pago o Ualá para cobrar con tarjeta?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Depende de tu volumen y tipo de ventas. Ualá Bis cobra 2.9% + IVA en débito (vs 3.25% de Mercado Pago Point). En crédito, Ualá cobra 4.4% + IVA mientras Mercado Pago cobra 4.39% + IVA con acreditación a 10 días. Ambos acreditan en el momento para débito."
              }
            },
            {
              "@type": "Question",
              "name": "¿Cuánto me descuentan si cobro con tarjeta de crédito en Argentina?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Los bancos adquirentes (Banco Nación, Banco Provincia) cobran 1.8% + IVA con acreditación en 8-10 días hábiles. Los agregadores fintech (Mercado Pago, Ualá) cobran entre 4.39% y 6.29% + IVA, pero ofrecen acreditación inmediata o en menor plazo."
              }
            },
            {
              "@type": "Question",
              "name": "¿Cuáles son las comisiones de Banco Nación para comercios?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Banco Nación cobra 0.8% + IVA para débito (acreditación en 24 horas) y 1.8% + IVA para crédito (acreditación en 8-10 días hábiles). El mantenimiento de la terminal POS puede ser bonificado o variable según el acuerdo comercial."
              }
            },
            {
              "@type": "Question",
              "name": "¿Qué es un agregador de pagos y en qué se diferencia de un banco adquirente?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Un banco adquirente tiene relación directa con las marcas de tarjetas y opera bajo aranceles regulados por el BCRA. Un agregador de pagos funciona como intermediario, fijando sus propias comisiones (generalmente más altas) pero con mayor simplicidad de alta y acreditación más rápida."
              }
            },
            {
              "@type": "Question",
              "name": "¿Cada cuánto se actualizan las comisiones en este sitio?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Las comisiones se actualizan automáticamente cada semana. Los scrapers consultan las páginas oficiales de cada entidad y actualizan los datos si detectan cambios. Todos los datos provienen de fuentes oficiales verificables."
              }
            },
            {
              "@type": "Question",
              "name": "¿Cómo se comparan las comisiones de cobro por QR vs Point/POS?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "El cobro por QR generalmente tiene comisiones más bajas que un dispositivo POS/Point. En Mercado Pago, el QR cobra entre 0.80% y 6.29% + IVA según el medio de pago, mientras que el Point cobra 3.25% + IVA en débito. Banco Provincia ofrece QR con saldo en cuenta a 0.8% + IVA."
              }
            }
          ]
        }
```

### Implementation notes

- Each FAQ answer begins with a direct, concise response (40–60 words) — this is the Google PAA snippet format.
- All fee values are current as of `data.json`. In Sprint 3 (Task 25), the pre-render script will auto-update these values.
- Links to official sources use `rel="noopener"` (NOT `rel="nofollow"`) — citing authoritative sources is a positive E-E-A-T signal.
- The FAQ section is static HTML, not JS-generated, ensuring guaranteed crawlability.

### Acceptance criteria

- [ ] FAQ section visible on the page without JavaScript
- [ ] Google Rich Results Test detects `FAQPage` with 7 questions
- [ ] Each `<details>` opens/closes correctly
- [ ] Links to official sources work and have `rel="noopener"`

---

## Task 2.2 — "About / Methodology" Section

**File:** `index.html` — insert between the FAQ section and the footer

### Code to add

```html
    <!-- Methodology Section -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
        <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
            <h2 class="text-xl font-bold text-slate-900 mb-4">Cómo funciona este comparador</h2>
            <div class="prose prose-sm prose-slate max-w-none">
                <p>Este comparador recopila las comisiones de cobro con tarjeta de débito y crédito de las
                principales entidades de pago de Argentina. Los datos se obtienen <strong>directamente de
                las páginas oficiales</strong> de cada entidad mediante scrapers automatizados que se
                ejecutan semanalmente.</p>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 not-prose">
                    <div class="bg-slate-50 rounded-lg p-4">
                        <p class="font-semibold text-slate-800 text-sm mb-1">Fuentes oficiales</p>
                        <p class="text-xs text-slate-500">Todas las tasas provienen de las páginas oficiales
                        de cada entidad. No usamos valores estimados ni datos de terceros.</p>
                    </div>
                    <div class="bg-slate-50 rounded-lg p-4">
                        <p class="font-semibold text-slate-800 text-sm mb-1">Actualización automática</p>
                        <p class="text-xs text-slate-500">Los scrapers se ejecutan todos los domingos a las
                        3 AM UTC. Si detectan cambios, los datos se actualizan automáticamente.</p>
                    </div>
                    <div class="bg-slate-50 rounded-lg p-4">
                        <p class="font-semibold text-slate-800 text-sm mb-1">Código abierto</p>
                        <p class="text-xs text-slate-500">El código fuente es público y verificable en
                        <a href="https://github.com/jrusco/monitor-comisiones-bancarias"
                           rel="noopener" target="_blank"
                           class="text-blue-600 underline">GitHub</a>. Cualquiera puede auditar la metodología.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
```

### Implementation notes

- This section directly addresses Google's E-E-A-T requirements for YMYL content.
- "Código abierto" + GitHub link demonstrates transparency and builds trust.
- The three-column layout provides scannable information about methodology.
- Static HTML, not JS-generated.

### Acceptance criteria

- [ ] Section visible without JavaScript
- [ ] GitHub link works and has `rel="noopener"`
- [ ] Content accurately describes the actual data pipeline

---

## Task 2.3 — Add `lastUpdated` Field to data.json + Scrapers

**Files:** `data.json`, `internal/common/*.go`, each `cmd/update-*/main.go`

### 2.3.1 Update data.json schema

Add a `lastUpdated` field to each entity:

```json
{
    "id": "mercadopago",
    "name": "Mercado Pago",
    "lastUpdated": "2026-02-08T03:00:00Z",
    ...
}
```

### 2.3.2 Update common utilities

In `internal/common/`, the data loading/saving functions should handle the new field. When `UpdateEntityFees()` detects changes and writes back, it should set `lastUpdated` to the current UTC timestamp:

```go
// In the UpdateEntityFees function or wherever fees are saved:
import "time"

// When fees change:
entity.LastUpdated = time.Now().UTC().Format(time.RFC3339)
```

The entity struct needs the new field:

```go
type Entity struct {
    // ... existing fields ...
    LastUpdated string `json:"lastUpdated,omitempty"`
}
```

### 2.3.3 Update each scraper

Each scraper (`cmd/update-mercadopago/main.go`, etc.) should update the `lastUpdated` field whenever it successfully verifies or updates fees. Two strategies:

- **Option A (recommended):** Only update `lastUpdated` when fees actually change (already implied by `UpdateEntityFees` only writing on change).
- **Option B:** Update `lastUpdated` on every successful scrape run (shows "last verified" even if fees didn't change). This provides stronger freshness signals.

Recommend Option B for SEO purposes — even if fees haven't changed, showing "Verificado: 8 de febrero de 2026" is more trustworthy than showing a month-old date.

### Acceptance criteria

- [ ] Each entity in `data.json` has a `lastUpdated` ISO 8601 timestamp
- [ ] Running a scraper updates the timestamp for that entity
- [ ] `jq '.[] | .lastUpdated' data.json` returns valid dates for all entities

---

## Task 2.4 — Display "Last Updated" Timestamps in UI

**File:** `index.html` — entity card rendering JavaScript

### Update the entity card template

In the JavaScript function that renders entity cards (look for `renderEntityGrid` or similar), add a timestamp display:

```javascript
// Inside the card rendering function, add after the entity name:
const lastUpdated = entity.lastUpdated
    ? new Date(entity.lastUpdated).toLocaleDateString('es-AR', {
        day: 'numeric', month: 'long', year: 'numeric'
    })
    : 'Sin datos';

// In the card HTML template, add:
`<time datetime="${entity.lastUpdated || ''}" class="text-xs text-slate-400">
    Actualizado: ${lastUpdated}
</time>`
```

### Also add a global "last updated" timestamp in the hero section

Replace the hardcoded navbar date with a dynamic one. In the hero section, add:

```html
<time id="globalLastUpdated" datetime="" class="text-xs text-blue-200">
    Datos actualizados semanalmente
</time>
```

Then in JavaScript, compute the most recent `lastUpdated` across all entities:

```javascript
function renderLastUpdated(entities) {
    const latest = entities
        .filter(e => e.lastUpdated)
        .map(e => new Date(e.lastUpdated))
        .sort((a, b) => b - a)[0];

    if (latest) {
        const el = document.getElementById('globalLastUpdated');
        const formatted = latest.toLocaleDateString('es-AR', {
            day: 'numeric', month: 'long', year: 'numeric'
        });
        el.textContent = `Datos actualizados: ${formatted}`;
        el.setAttribute('datetime', latest.toISOString());
    }
}
```

### Implementation notes

- The `<time datetime="...">` element is a semantic HTML element that Google parses for freshness signals.
- `es-AR` locale formatting produces "8 de febrero de 2026" which is natural Argentine Spanish.
- The global timestamp in the hero provides an immediately visible freshness signal above the fold.

### Acceptance criteria

- [ ] Each entity card shows its last-updated date
- [ ] Hero section shows the most recent update date
- [ ] `<time>` elements have valid `datetime` attributes in ISO 8601 format
- [ ] Dates display in Argentine Spanish format

---

## Task 2.5 — Display Official Source Links in UI

**File:** `index.html` — entity card rendering JavaScript and/or entity detail view

### Update entity cards

Add a "Ver fuente oficial" link to each entity card, using the existing `feeUrl` from `data.json`:

```javascript
// In the card template, add after the fee table:
`<a href="${entity.feeUrl}" rel="noopener" target="_blank"
    class="inline-flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800 mt-3">
    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
    </svg>
    Ver fuente oficial
</a>`
```

### Implementation notes

- **Do NOT use `rel="nofollow"`** on these links. Linking to authoritative bank/fintech domains without nofollow passes trust signals to Google and demonstrates E-E-A-T.
- `rel="noopener"` is included for security (prevents `window.opener` attacks).
- The external link icon provides visual affordance that this opens a new tab.

### Acceptance criteria

- [ ] Every entity card has a "Ver fuente oficial" link
- [ ] Links open in new tab with `rel="noopener"`
- [ ] No `rel="nofollow"` on outbound links to official sources
- [ ] All `feeUrl` values in `data.json` return 200 OK

---

## Task 2.6 — Create OG Image Asset (1200x630)

**File:** `og-image.png` (new, project root)

### Design specifications

| Property | Value |
|----------|-------|
| Dimensions | 1200 x 630 px |
| Format | PNG (or WebP with PNG fallback) |
| Max file size | 300KB (optimize with tinypng.com) |
| Background | Blue gradient (#2563eb → #1d4ed8) matching hero section |

### Content layout

```
┌──────────────────────────────────────────────────┐
│                                                  │
│    Cobro con Tarjeta Argentina                   │
│    ─────────────────────────                     │
│    Compará comisiones de cobro                   │
│    con tarjeta de débito y crédito               │
│                                                  │
│    ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐          │
│    │ MP  │  │ UA  │  │ BNA │  │BAPRO│          │
│    │3.25%│  │2.9% │  │0.8% │  │0.8% │          │
│    └─────┘  └─────┘  └─────┘  └─────┘          │
│                                                  │
│    cobrocontarjeta.com.ar                        │
└──────────────────────────────────────────────────┘
```

### Tools to generate

- **Figma/Canva:** Design manually with the brand colors
- **Programmatic:** Use a tool like `@vercel/og` or `satori` to generate from HTML
- **Simple approach:** Use an online OG image generator and customize

### Acceptance criteria

- [ ] Image is exactly 1200x630px
- [ ] File size under 300KB
- [ ] `https://cobrocontarjeta.com.ar/og-image.png` returns 200 OK
- [ ] Sharing URL on WhatsApp/Twitter/Slack shows the image correctly
- [ ] Text is readable at thumbnail size (no tiny fonts)

---

## Task 2.7 — Create Apple Touch Icon (180x180)

**File:** `apple-touch-icon.png` (new, project root)

### Design specifications

| Property | Value |
|----------|-------|
| Dimensions | 180 x 180 px |
| Format | PNG |
| Background | #2563eb (Blue 600) |
| Content | "CT" in white, bold, centered |
| Corner radius | None (iOS applies its own mask) |

### Add to `<head>` in `index.html`

```html
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

This icon appears when iOS users add the site to their home screen.

### Acceptance criteria

- [ ] Image is 180x180px PNG
- [ ] `<link rel="apple-touch-icon">` present in `<head>`
- [ ] Adding site to iOS home screen shows the icon

---

## Sprint 2 Commit Plan

```bash
# Commit 1: FAQ section + schema
git add index.html
git commit -m "feat(seo): add FAQ section with FAQPage structured data

7 questions targeting PAA boxes for high-intent queries about
payment processing fees in Argentina. Static HTML for guaranteed
crawlability. Includes FAQPage JSON-LD schema."

# Commit 2: Methodology section
git add index.html
git commit -m "feat(seo): add methodology section for E-E-A-T compliance

Explains data sources, update frequency, and open-source methodology.
Addresses YMYL trust requirements for financial content."

# Commit 3: lastUpdated in data pipeline
git add data.json internal/ cmd/
git commit -m "feat: add lastUpdated timestamp to entities

Track when each entity's fees were last verified/updated.
Updated by scrapers on each run."

# Commit 4: UI enhancements (timestamps + source links)
git add index.html
git commit -m "feat(ui): display update timestamps and official source links

Per-entity last-updated dates with <time> elements for freshness
signals. 'Ver fuente oficial' links on each card (no nofollow)."

# Commit 5: Brand assets
git add og-image.png apple-touch-icon.png index.html
git commit -m "feat(seo): add OG image and apple-touch-icon

1200x630 OG image for social sharing. 180x180 apple-touch-icon
for iOS home screen."
```

---

## Verification Checklist (Post-Deploy)

| Check | Tool | Expected Result |
|-------|------|-----------------|
| FAQ visible without JS | Disable JS in browser | FAQ section renders with all Q&A |
| FAQPage schema | Rich Results Test | 7 FAQ items detected |
| PAA format | Read first 60 words of each answer | Direct, concise response |
| Source links | Click each "Ver fuente oficial" | Official page loads |
| Timestamps | Check each entity card | Date in "X de mes de año" format |
| `<time>` elements | View source | Valid `datetime` attributes |
| OG image | https://www.opengraph.xyz/ | Image renders in preview |
| Methodology | Page inspection | Section visible without JS |
