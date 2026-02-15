#!/usr/bin/env node
/**
 * Pre-render script for monitor-comisiones-bancarias
 *
 * Injects dynamic content into index.html at build time for SEO:
 * 1. Hero metrics (lowest debit/credit rates)
 * 2. Noscript fallback table with all fees
 * 3. JSON-LD feesAndCommissionsSpecification text
 * 4. Sitemap.xml lastmod date
 *
 * This script is idempotent - can be run multiple times safely.
 */

const fs = require('fs');
const path = require('path');

// --- Load data.json ---
const dataPath = path.join(__dirname, '..', 'data.json');
const entities = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

// --- Helper: Extract numeric rate from fee string ---
function extractRate(rateStr) {
    const match = rateStr.match(/(\d+[\.,]?\d*)/);
    return match ? parseFloat(match[0].replace(',', '.')) : null;
}

// --- 1. Calculate Hero Metrics ---
let minDebit = { rate: Infinity, entity: null };
let minCredit = { rate: Infinity, entity: null };

entities.forEach(entity => {
    entity.fees.forEach(fee => {
        const rate = extractRate(fee.rate);
        if (rate === null) return;

        if (fee.concept.includes('Débito') && rate < minDebit.rate) {
            minDebit = { rate, entity: entity.name };
        }
        if (fee.concept.includes('Crédito') && rate < minCredit.rate) {
            minCredit = { rate, entity: entity.name };
        }
    });
});

const metrics = {
    debit: minDebit.rate !== Infinity ? `${minDebit.rate}%` : 'Cargando...',
    debitEntity: minDebit.entity || '',
    credit: minCredit.rate !== Infinity ? `${minCredit.rate}%` : 'Cargando...',
    creditEntity: minCredit.entity || ''
};

console.log('✓ Calculated hero metrics:', metrics);

// --- 2. Build Noscript Fallback Table ---
const noscriptTable = `<noscript>
    <div style="max-width: 1280px; margin: 2rem auto; padding: 0 1rem;">
        <div style="background: white; border-radius: 12px; padding: 1.5rem; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h2 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem; color: #1e293b;">Comparación de Comisiones por Cobro con Tarjeta</h2>
            <p style="color: #64748b; margin-bottom: 1.5rem; font-size: 0.875rem;">Esta tabla muestra las comisiones actualizadas de cada procesador. Para ver la versión interactiva, habilite JavaScript.</p>

            ${entities.map(entity => `
            <div style="margin-bottom: 2rem; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;">
                <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: white; padding: 1rem; font-weight: bold; font-size: 1.125rem;">
                    ${entity.name}
                </div>
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: #f1f5f9; border-bottom: 1px solid #e2e8f0;">
                            <th style="padding: 0.75rem; text-align: left; font-size: 0.875rem; color: #475569;">Tipo de pago</th>
                            <th style="padding: 0.75rem; text-align: left; font-size: 0.875rem; color: #475569;">Cuándo cobrás</th>
                            <th style="padding: 0.75rem; text-align: right; font-size: 0.875rem; color: #475569;">Comisión</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${entity.fees.map((fee, idx) => `
                        <tr style="border-bottom: 1px solid #f1f5f9;">
                            <td style="padding: 0.75rem; font-size: 0.875rem; color: #334155;">${fee.concept}</td>
                            <td style="padding: 0.75rem; font-size: 0.875rem; color: #64748b;">${fee.term}</td>
                            <td style="padding: 0.75rem; text-align: right; font-family: monospace; font-weight: bold; font-size: 0.875rem; color: #1e293b;">${fee.rate}</td>
                        </tr>
                        `).join('')}
                    </tbody>
                </table>
                <div style="padding: 0.75rem; background: #fef3c7; border-top: 1px solid #fde68a; font-size: 0.75rem; color: #92400e;">
                    Las tasas no incluyen IVA ni retenciones. Verificá en la <a href="${entity.feeUrl}" style="color: #1d4ed8; text-decoration: underline;" target="_blank" rel="noopener">fuente oficial</a>.
                </div>
            </div>
            `).join('')}
        </div>
    </div>
</noscript>`;

console.log('✓ Built noscript table with', entities.length, 'entities');

// --- 3. Update index.html ---
const htmlPath = path.join(__dirname, '..', 'index.html');
let html = fs.readFileSync(htmlPath, 'utf8');

// Update hero metrics
html = html.replace(
    /(<p id="heroMinDebit"[^>]*>).*?(<\/p>)/,
    `$1${metrics.debit} <span class="text-sm font-normal text-blue-200">(${metrics.debitEntity})</span>$2`
);
html = html.replace(
    /(<p id="heroMinCredit"[^>]*>).*?(<\/p>)/,
    `$1${metrics.credit} <span class="text-sm font-normal text-blue-200">(${metrics.creditEntity})</span>$2`
);

console.log('✓ Updated hero metrics');

// Inject noscript (idempotent - replace if exists, insert if not)
if (html.includes('<noscript>')) {
    // Replace existing noscript block
    html = html.replace(/<noscript>[\s\S]*?<\/noscript>/, noscriptTable);
    console.log('✓ Replaced existing noscript block');
} else {
    // Insert after <body> tag
    html = html.replace(/(<body[^>]*>)/, `$1\n${noscriptTable}\n`);
    console.log('✓ Inserted new noscript block');
}

// Update JSON-LD feesAndCommissionsSpecification
const providerToId = {
    'Mercado Pago': 'mercadopago',
    'Ualá': 'uala',
    'Banco de la Nación Argentina': 'bna',
    'Banco de la Provincia de Buenos Aires': 'bapro',
};

// Extract ItemList from JSON-LD
const jsonLdMatch = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
if (jsonLdMatch) {
    const jsonLd = JSON.parse(jsonLdMatch[1]);
    const itemList = jsonLd['@graph'].find(item => item['@type'] === 'ItemList');

    if (itemList) {
        itemList.itemListElement.forEach(listItem => {
            const providerName = listItem.item.provider.name;
            const entityId = providerToId[providerName];
            const entity = entities.find(e => e.id === entityId);

            if (entity) {
                // Build fee summary text (debito: X%, credito: Y%)
                const debitFee = entity.fees.find(f => f.concept.includes('Débito'));
                const creditFee = entity.fees.find(f => f.concept.includes('Crédito'));

                let feeText = '';
                if (debitFee) {
                    feeText += `Debito: ${debitFee.rate} (${debitFee.term}).`;
                }
                if (creditFee) {
                    if (feeText) feeText += ' ';
                    feeText += `Credito: ${creditFee.rate} (${creditFee.term}).`;
                }

                // Update or add feesAndCommissionsSpecification
                if (typeof listItem.item.feesAndCommissionsSpecification === 'string') {
                    // Keep the URL, add description as separate field if needed
                    // For now, JSON-LD spec says this should be URL or text, so keep URL
                    // We'll skip modifying this to avoid breaking the schema
                } else {
                    // Already an object or missing - can add text
                    listItem.item.feesAndCommissionsSpecification = feeText || listItem.item.feesAndCommissionsSpecification;
                }
            }
        });

        // Serialize back to HTML
        const updatedJsonLd = JSON.stringify(jsonLd, null, 2);
        html = html.replace(
            /<script type="application\/ld\+json">[\s\S]*?<\/script>/,
            `<script type="application/ld+json">\n${updatedJsonLd}\n    </script>`
        );

        console.log('✓ Updated JSON-LD fee specifications');
    }
}

// Write updated HTML
fs.writeFileSync(htmlPath, html, 'utf8');
console.log('✓ Wrote updated index.html');

// --- 4. Update sitemap.xml lastmod ---
const sitemapPath = path.join(__dirname, '..', 'sitemap.xml');
if (fs.existsSync(sitemapPath)) {
    const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
    let sitemap = fs.readFileSync(sitemapPath, 'utf8');
    sitemap = sitemap.replace(/<lastmod>.*?<\/lastmod>/, `<lastmod>${today}</lastmod>`);
    fs.writeFileSync(sitemapPath, sitemap, 'utf8');
    console.log('✓ Updated sitemap.xml lastmod to', today);
}

console.log('\n✅ Pre-render complete!');
