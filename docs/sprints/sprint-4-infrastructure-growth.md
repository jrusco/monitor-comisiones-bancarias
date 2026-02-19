# Sprint 4: Infrastructure & Growth

**Goal:** Establish the monitoring, analytics, and growth infrastructure needed to measure progress, iterate on SEO strategy, and begin building external authority through link building.

**Depends on:** Sprints 1–3 complete (domain configured, content ready, pre-rendering working).

---

## Task 4.1 — Google Analytics 4 Setup

**File:** `index.html` — `<head>` section

Add after the AdSense script, before `</head>`:

```html
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-XXXXXXXXXX');
    </script>
```

**Setup steps:**
1. Go to https://analytics.google.com/
2. Create a new GA4 property for `cobrocontarjeta.com.ar`
3. Create a "Web" data stream
4. Copy the Measurement ID (`G-XXXXXXXXXX`)
5. Replace the placeholder in the code above
6. Enable Enhanced Measurement (scrolls, outbound clicks, site search)

### Custom event tracking

Track key user interactions to understand engagement:

Add to `index.html` at the bottom of `<body>`, after the existing script initialization block (after the `DOMContentLoaded` listener or after `renderEntityGrid()` is called).

```javascript
// Track fee simulator usage
function trackSimulatorUse(entityName, amount) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'simulator_use', {
            entity: entityName,
            amount: amount,
        });
    }
}

// Track entity card clicks
function trackEntityClick(entityId) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'entity_view', {
            entity_id: entityId,
        });
    }
}

// Track FAQ expansion
document.querySelectorAll('details').forEach(d => {
    d.addEventListener('toggle', () => {
        if (d.open && typeof gtag !== 'undefined') {
            const question = d.querySelector('h3')?.textContent?.substring(0, 50);
            gtag('event', 'faq_open', { question });
        }
    });
});

// Track outbound link clicks (official sources)
document.querySelectorAll('a[target="_blank"]').forEach(a => {
    a.addEventListener('click', () => {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'outbound_click', {
                url: a.href,
                // Requires data-entity-id="${entity.id}" on the entity detail wrapper element
                entity: a.closest('[data-entity-id]')?.dataset.entityId || 'unknown',
            });
        }
    });
});
```

**Implementation note:** For the `outbound_click` entity tracking to work, add `data-entity-id="${entity.id}"` to the entity detail modal or container element when implementing. Entity cards currently use `id="${entity.id}"` only.

### Link GA4 to Search Console

1. In GA4: Admin → Product Links → Search Console Links
2. Select the verified `cobrocontarjeta.com.ar` property
3. This enables combined reporting: see which search queries drive traffic AND what users do after landing

### Acceptance criteria

- [ ] Analytics script loads on the page (verify in DevTools Network tab)
- [ ] Real-time view shows your own visit
- [ ] Custom events fire when interacting with simulator, FAQ, entity cards
- [ ] Search Console linked to GA4 property

---

## Task 4.2 — Submit to Google Search Console

**Note:** Google Search Console registration was initiated in Sprint 1 (Task 1.10). This task covers verification and sitemap submission.

### Google Search Console post-verification steps

1. **Submit sitemap:**
   - Go to Sitemaps section
   - Enter `sitemap.xml`
   - Status should show "Success" within minutes

2. **Request initial indexing:**
   - Go to URL Inspection
   - Enter `https://cobrocontarjeta.com.ar/`
   - Click "Request Indexing"
   - Google will queue the page for priority crawling

3. **Verify JavaScript rendering:**
   - In URL Inspection, click "View Crawled Page" → "Screenshot"
   - Verify Google sees the full rendered content (entity cards, chart, FAQ)
   - If content is missing, this confirms the pre-rendering (Sprint 3) is critical

4. **Set up email alerts:**
   - Settings → Email preferences → Enable all notifications
   - You'll be alerted to coverage issues, manual actions, and Core Web Vitals problems

5. **International Targeting:**
   - Legacy tools → International Targeting → Country tab
   - Select "Argentina"

### Acceptance criteria

- [ ] Google Search Console: Sitemap shows "Success"
- [ ] Google Search Console: URL Inspection shows "URL is on Google" (may take days)
- [ ] Google Search Console: JavaScript-rendered screenshot shows full content

---

## Task 4.3 — Build Automated Changelog (Fee Change Detection)

**Files:** `scripts/detect-changes.js` (new), `changelog.json` (new), CI/CD workflow

### Goal

When scrapers detect a fee change, record the change with before/after values and a timestamp. This data can power:
- A "Recent changes" section on the site
- Future blog posts about fee trends
- Historical tracking for trend charts (nice-to-have from strategy)

### 4.3.1 Changelog data structure

**File:** `changelog.json` (new, project root)

```json
[]
```

Initial empty array. Entries will be appended by the script:

```json
[
    {
        "date": "2026-02-15T03:00:00Z",
        "entity": "mercadopago",
        "entityName": "Mercado Pago",
        "changes": [
            {
                "concept": "Point - Débito",
                "field": "rate",
                "from": "3.25% + IVA",
                "to": "3.15% + IVA"
            }
        ]
    }
]
```

### 4.3.2 Change detection script

**File:** `scripts/detect-changes.js` (new)

```javascript
#!/usr/bin/env node

/**
 * Detects changes between old and new data.json versions.
 * Run AFTER scrapers update data.json, BEFORE git commit.
 *
 * Usage: node scripts/detect-changes.js
 * Compares data.json in working tree vs last committed version.
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const CHANGELOG_PATH = path.join(__dirname, '..', 'changelog.json');
const DATA_PATH = path.join(__dirname, '..', 'data.json');

function getOldData() {
    try {
        const raw = execSync('git show HEAD:data.json', { encoding: 'utf-8' });
        return JSON.parse(raw);
    } catch {
        return [];
    }
}

function getNewData() {
    return JSON.parse(fs.readFileSync(DATA_PATH, 'utf-8'));
}

function detectChanges(oldEntities, newEntities) {
    const changes = [];
    const now = new Date().toISOString();

    for (const newEntity of newEntities) {
        const oldEntity = oldEntities.find(e => e.id === newEntity.id);
        if (!oldEntity) {
            changes.push({
                date: now,
                entity: newEntity.id,
                entityName: newEntity.name,
                changes: [{ concept: 'Nueva entidad', field: 'entity', from: null, to: newEntity.name }],
            });
            continue;
        }

        const feeChanges = [];
        for (const newFee of newEntity.fees) {
            const oldFee = oldEntity.fees.find(f => f.concept === newFee.concept);
            if (!oldFee) {
                feeChanges.push({ concept: newFee.concept, field: 'fee', from: null, to: newFee.rate });
                continue;
            }
            if (oldFee.rate !== newFee.rate) {
                feeChanges.push({ concept: newFee.concept, field: 'rate', from: oldFee.rate, to: newFee.rate });
            }
            if (oldFee.term !== newFee.term) {
                feeChanges.push({ concept: newFee.concept, field: 'term', from: oldFee.term, to: newFee.term });
            }
        }

        if (feeChanges.length > 0) {
            changes.push({
                date: now,
                entity: newEntity.id,
                entityName: newEntity.name,
                changes: feeChanges,
            });
        }
    }

    return changes;
}

function appendChangelog(newChanges) {
    let changelog = [];
    if (fs.existsSync(CHANGELOG_PATH)) {
        changelog = JSON.parse(fs.readFileSync(CHANGELOG_PATH, 'utf-8'));
    }
    changelog.push(...newChanges);

    // Keep last 100 entries to prevent unbounded growth
    if (changelog.length > 100) {
        changelog = changelog.slice(-100);
    }

    fs.writeFileSync(CHANGELOG_PATH, JSON.stringify(changelog, null, 2), 'utf-8');
}

function main() {
    const oldData = getOldData();
    const newData = getNewData();
    const changes = detectChanges(oldData, newData);

    if (changes.length === 0) {
        console.log('No fee changes detected.');
        return;
    }

    console.log(`Detected ${changes.length} entity change(s):`);
    for (const change of changes) {
        for (const c of change.changes) {
            console.log(`  ${change.entityName}: ${c.concept} ${c.field} ${c.from} → ${c.to}`);
        }
    }

    appendChangelog(changes);
    console.log('Changelog updated.');
}

main();
```

### 4.3.3 Add to CI/CD workflow

**Note:** Node.js 20 is already available in the workflow via the existing `actions/setup-node@v4` step used by `scripts/prerender.js`. No new setup step is needed.

Add **after** scrapers run but **before** commit:

```yaml
      - name: Detect fee changes
        run: node scripts/detect-changes.js

      # ... existing validate, build, prerender steps ...

      - name: Commit and push if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data.json index.html sitemap.xml tailwind.min.css changelog.json
          git diff --staged --quiet || git commit -m "chore: update fees [automated]"
          git push
```

### Acceptance criteria

- [ ] Running `node scripts/detect-changes.js` after modifying `data.json` detects changes
- [ ] `changelog.json` is appended with before/after values
- [ ] Changelog entries have ISO 8601 timestamps
- [ ] Changelog is capped at 100 entries

---

## Task 4.4 — Community Outreach and Link Building

This is an ongoing, non-code task. Document the strategy and track progress.

### Target communities (prioritized by ROI)

| Channel | Approach | Expected Backlinks | Effort |
|---------|----------|-------------------|--------|
| **r/argentina** | Share as useful tool in commerce/fintech threads | 0 (nofollow) but drives traffic | Low |
| **r/merval** | Share in relevant financial discussions | 0 (nofollow) but drives traffic | Low |
| **Argentine monotributista forums** | Share as free resource for small business owners | 1-3 | Low |
| **iProup / iProUP** | Pitch as a unique open-source fintech tool | 1 (high authority) | Medium |
| **El Cronista fintech section** | Press pitch about automated fee monitoring | 1 (high authority) | Medium |
| **InfoKioscos** | Share as relevant tool for kiosk owners | 1 | Low |
| **GitHub Awesome Argentina lists** | PR to add to curated lists | 1-2 | Low |
| **FreeCodeCamp BA / MeetupJS** | Present as open-source project | 2-3 | Medium |
| **Accounting/PYME blogs** | Guest post or tool recommendation | 2-5 | High |
| **NIC Argentina blog** | Showcase as example .com.ar project | 1 (very high authority) | Medium |

### Outreach template (Spanish)

```
Asunto: Herramienta gratuita para comparar comisiones de cobro con tarjeta

Hola [nombre],

Creé una herramienta open-source que compara automáticamente las comisiones
de cobro con tarjeta en Argentina (Mercado Pago, Ualá, Banco Nación,
Banco Provincia). Se actualiza sola cada semana desde las fuentes oficiales.

🔗 https://cobrocontarjeta.com.ar

La pueden usar sus lectores/miembros para elegir el procesador de pagos
más conveniente. Es 100% gratuita y sin registro.

¿Les interesaría compartirla o hacer una reseña? Puedo darles más info
sobre cómo funciona la automatización.

Saludos,
[nombre]
```

### Track outreach results

_Create this file as `docs/outreach-log.md`. Replace the example rows with your own tracking data as outreach progresses._

| Date | Target | Contact | Status | Link Acquired | Notes |
|------|--------|---------|--------|---------------|-------|

### Acceptance criteria

- [ ] At least 5 outreach attempts made within first 2 weeks
- [ ] At least 1 backlink acquired within first month
- [ ] Reddit posts submitted (r/argentina, r/merval)
- [ ] GitHub project has a clear, linkable README with the tool URL

---

## Sprint 4 Commit Plan

```bash
# Commit 1: Analytics
git add index.html
git commit -m "feat: add Google Analytics 4 with custom event tracking

Track simulator usage, entity clicks, FAQ interactions, and outbound
link clicks for SEO performance monitoring."

# Commit 2: Changelog system
git add scripts/detect-changes.js changelog.json .github/workflows/update-fees.yml
git commit -m "feat: add automated fee change detection and changelog

Compare data.json before/after scraper runs, record changes with
before/after values and timestamps. Capped at 100 entries."
```

---

## Verification Checklist (Post-Deploy)

| Check | Tool | Expected Result |
|-------|------|-----------------|
| Analytics collecting data | GA4 Real-time view | Your visit visible |
| Custom events firing | GA4 → Events | simulator_use, entity_view, faq_open events |
| Search Console sitemap | GSC → Sitemaps | Status: "Success" |
| Search Console rendering | GSC → URL Inspection → Screenshot | Full content visible |
| Changelog after manual data change | Modify `data.json`, run `node scripts/detect-changes.js` | `changelog.json` updated |

---

## Post-Sprint 4: Ongoing SEO Monitoring

After all four sprints are complete, establish a weekly review cadence:

### Weekly (5 minutes)

- Check Google Search Console → Performance for impressions/clicks trends
- Check Core Web Vitals report for regressions
- Review any new "Coverage" issues

### Monthly (30 minutes)

- Review top queries and positions — identify new keyword opportunities
- Check if FAQ snippets are appearing in SERPs
- Review changelog.json for fee change patterns
- Assess backlink progress (use Search Console → Links)

### Quarterly (1 hour)

- Comprehensive keyword analysis — new competitors, new queries
- Content gap assessment — are users searching for things not covered?
- Competitor check — have iKiwi, Taca Taca, or others improved?
- Plan next phase of features (embeddable widget, historical tracking, etc.)
