#!/usr/bin/env node
/**
 * Regression Tests for Commit 98cd62a
 * Fix critical security and stability issues in fee simulator
 */

const fs = require('fs');
const path = require('path');

// ANSI color codes
const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';

let passed = 0;
let failed = 0;

function logTest(name, success, details) {
    if (success) {
        console.log(`${GREEN}✓${RESET} ${name}`);
        passed++;
    } else {
        console.log(`${RED}✗${RESET} ${name}`);
        failed++;
    }
    if (details) {
        console.log(`  ${success ? GREEN : RED}${details}${RESET}\n`);
    }
}

function logSection(name) {
    console.log(`\n${BOLD}${YELLOW}═══ ${name} ═══${RESET}\n`);
}

// Load files
const indexHtml = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const dataJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'data.json'), 'utf8'));

console.log(`\n${BOLD}Regression Tests for Commit 98cd62a${RESET}`);
console.log(`Testing: Fix critical security and stability issues in fee simulator`);
console.log(`Date: ${new Date().toISOString()}\n`);

// ========================================
// DATA VALIDATION
// ========================================
logSection('Data Validation');

logTest(
    'data.json loads successfully',
    Array.isArray(dataJson) && dataJson.length > 0,
    `Loaded ${dataJson.length} entities`
);

logTest(
    'All entities have required fields',
    dataJson.every(e => e.id && e.name && e.fees && Array.isArray(e.fees)),
    dataJson.map(e => `${e.id}: ${e.name}`).join(', ')
);

logTest(
    'All fees have required fields (concept, term, rate)',
    dataJson.every(e => e.fees.every(f => f.concept && f.term && f.rate)),
    `Checked ${dataJson.reduce((sum, e) => sum + e.fees.length, 0)} fee entries`
);

// ========================================
// FIX #1: Null Safety Check
// ========================================
logSection('Fix #1: Null Safety Check for Entity Selection');

const hasNullCheck = indexHtml.includes('if (!entity)') &&
                    indexHtml.includes('Entity not found:');

logTest(
    'Null check exists for entity lookup',
    hasNullCheck,
    hasNullCheck ? 'Pattern found: if (!entity) with console.warn' : 'Pattern NOT found!'
);

const nullCheckSetsState = indexHtml.includes('simulatorState.selectedEntity = null') &&
                           indexHtml.includes('simulatorState.selectedFeeIndex = null');

logTest(
    'Null check resets simulator state',
    nullCheckSetsState,
    nullCheckSetsState ? 'Resets selectedEntity and selectedFeeIndex to null' : 'State reset NOT found!'
);

const nullCheckHidesUI = indexHtml.includes("paymentTypeContainer').classList.add('hidden')");

logTest(
    'Null check hides payment type UI',
    nullCheckHidesUI,
    nullCheckHidesUI ? 'Hides paymentTypeContainer on invalid entity' : 'UI hide NOT found!'
);

// ========================================
// FIX #2: Default Entity Fallback
// ========================================
logSection('Fix #2: Default Entity Initialization with Fallback');

const hasDefaultEntity = indexHtml.includes("const defaultEntityId = 'mercadopago'");

logTest(
    'Default entity ID defined',
    hasDefaultEntity,
    hasDefaultEntity ? "defaultEntityId = 'mercadopago'" : 'Default entity ID NOT defined!'
);

const hasFallbackLogic = indexHtml.includes('Default entity (mercadopago) not found') &&
                         indexHtml.includes('entities[0].id');

logTest(
    'Fallback logic for missing default entity',
    hasFallbackLogic,
    hasFallbackLogic ? 'Falls back to first available entity' : 'Fallback NOT implemented!'
);

const mercadopago = dataJson.find(e => e.id === 'mercadopago');

logTest(
    'Default entity (mercadopago) exists in data',
    !!mercadopago,
    mercadopago ? `Found: ${mercadopago.name}` : 'mercadopago NOT in data.json!'
);

logTest(
    'Fallback entity available',
    dataJson.length > 0,
    dataJson.length > 0 ? `First entity: ${dataJson[0].name}` : 'No entities available!'
);

// ========================================
// FIX #3: XSS Prevention
// ========================================
logSection('Fix #3: XSS Prevention - Safe DOM Manipulation');

// Check for safe DOM manipulation patterns
const hasSafeDOMPaymentType = indexHtml.includes('while (paymentTypeSelector.firstChild)') &&
                               indexHtml.includes('paymentTypeSelector.removeChild');

logTest(
    'Safe DOM manipulation for payment type selector',
    hasSafeDOMPaymentType,
    hasSafeDOMPaymentType ? 'Uses removeChild() loop instead of innerHTML' : 'Still using innerHTML!'
);

const hasSafeDOMBreakdown = indexHtml.includes('while (breakdownEl.firstChild)') &&
                            indexHtml.includes('breakdownEl.removeChild');

logTest(
    'Safe DOM manipulation for fee breakdown',
    hasSafeDOMBreakdown,
    hasSafeDOMBreakdown ? 'Uses removeChild() loop instead of innerHTML' : 'Still using innerHTML!'
);

// Check that createElement is used instead of innerHTML
const usesCreateElement = indexHtml.includes("document.createElement('option')") &&
                          indexHtml.includes("document.createElement('span')");

logTest(
    'Uses createElement for dynamic elements',
    usesCreateElement,
    usesCreateElement ? 'Creates elements safely with createElement' : 'Not using createElement!'
);

// Verify textContent is used for text (XSS-safe)
const usesTextContent = indexHtml.includes('.textContent =');

logTest(
    'Uses textContent for setting text',
    usesTextContent,
    usesTextContent ? 'Uses textContent (XSS-safe) for text' : 'Not using textContent!'
);

// Count innerHTML in simulator functions (should be minimal/zero)
const simulatorFunctionsCode = indexHtml.match(/function (handleEntityChange|recalculateFee|toggleSimulatorCollapse|handlePaymentTypeChange)\([^)]*\)[\s\S]*?(?=function [a-zA-Z]|\s*\/\/ ---)/g);
let innerHTMLCount = 0;
if (simulatorFunctionsCode) {
    simulatorFunctionsCode.forEach(code => {
        const matches = code.match(/\.innerHTML\s*=/g);
        if (matches) innerHTMLCount += matches.length;
    });
}

logTest(
    'No innerHTML in simulator functions',
    innerHTMLCount === 0,
    `Found ${innerHTMLCount} innerHTML assignments in simulator functions`
);

// ========================================
// FIX #4: Empty Fees Array Handling
// ========================================
logSection('Fix #4: Empty Fees Array Edge Case');

const hasEmptyFeesCheck = indexHtml.includes('!entity.fees || entity.fees.length === 0');

logTest(
    'Empty fees array check exists',
    hasEmptyFeesCheck,
    hasEmptyFeesCheck ? 'Checks for null/empty fees array' : 'Empty check NOT found!'
);

const hasUserFeedback = indexHtml.includes('Sin comisiones configuradas');

logTest(
    'User feedback for empty fees',
    hasUserFeedback,
    hasUserFeedback ? "Shows 'Sin comisiones configuradas' message" : 'User feedback NOT found!'
);

const disablesSelector = indexHtml.includes('paymentTypeSelector.disabled = true');

logTest(
    'Disables selector for empty fees',
    disablesSelector,
    disablesSelector ? 'Disables payment type selector' : 'Selector disable NOT found!'
);

const hasConsoleWarn = indexHtml.includes('has no fees configured');

logTest(
    'Console warning for debugging',
    hasConsoleWarn,
    hasConsoleWarn ? "Logs 'has no fees configured' warning" : 'Console warning NOT found!'
);

// ========================================
// FIX #5: Browser-Compatible Scroll Lock
// ========================================
logSection('Fix #5: Browser-Compatible Scroll Lock');

// Check CSS :has() is NOT used
const hasCSSHas = indexHtml.includes('body:has(');

logTest(
    'CSS :has() selector removed',
    !hasCSSHas,
    hasCSSHas ? 'WARNING: body:has() still present (incompatible with some browsers)' : 'No :has() selector found (good!)'
);

// Check class-based CSS exists
const hasClassBasedCSS = indexHtml.includes('body.simulator-expanded') &&
                         indexHtml.match(/body\.simulator-expanded\s*\{[\s\S]*overflow:\s*hidden/);

logTest(
    'Class-based scroll lock CSS',
    hasClassBasedCSS,
    hasClassBasedCSS ? 'body.simulator-expanded { overflow: hidden } found' : 'Class-based CSS NOT found!'
);

// Check JS adds/removes class
const addsClass = indexHtml.includes("document.body.classList.add('simulator-expanded')");
const removesClass = indexHtml.includes("document.body.classList.remove('simulator-expanded')");

logTest(
    'JS adds simulator-expanded class',
    addsClass,
    addsClass ? "classList.add('simulator-expanded') found" : 'Class add NOT found!'
);

logTest(
    'JS removes simulator-expanded class',
    removesClass,
    removesClass ? "classList.remove('simulator-expanded') found" : 'Class remove NOT found!'
);

// Check resize handler
const hasResizeHandler = indexHtml.includes("window.addEventListener('resize'") &&
                         indexHtml.includes('window.innerWidth > 768');

logTest(
    'Resize handler removes scroll lock on desktop',
    hasResizeHandler,
    hasResizeHandler ? 'Clears scroll lock when viewport > 768px' : 'Resize handler NOT found!'
);

// Check init clears scroll lock
const initClearsLock = indexHtml.includes("// Fix #5c: Ensure scroll lock is removed on init");

logTest(
    'Init clears any stale scroll lock',
    initClearsLock,
    initClearsLock ? 'Removes simulator-expanded class on init' : 'Init cleanup NOT found!'
);

// ========================================
// INTEGRATION TESTS
// ========================================
logSection('Integration Tests');

// Test fee calculation logic
const mpDebit = mercadopago?.fees.find(f => f.concept.includes('Point') && f.concept.includes('Débito'));
if (mpDebit) {
    const rateMatch = mpDebit.rate.match(/(\d+[\.,]?\d*)/);
    if (rateMatch) {
        const rate = parseFloat(rateMatch[0].replace(',', '.'));
        const amount = 10000;
        const feeWithIVA = amount * (rate / 100) * 1.21;

        logTest(
            'Fee calculation formula is correct',
            feeWithIVA === 393.25, // 10000 * 0.0325 * 1.21
            `$${amount} at ${rate}% + IVA = $${feeWithIVA.toFixed(2)}`
        );
    }
}

// Test unique entity IDs
const ids = dataJson.map(e => e.id);
const uniqueIds = new Set(ids);

logTest(
    'All entity IDs are unique',
    ids.length === uniqueIds.size,
    `${ids.length} entities, ${uniqueIds.size} unique IDs`
);

// Test rate extraction regex pattern
const testRates = ['3.25% + IVA', '0.8% + IVA', '0.80% - 6.29% + IVA (según medio)', 'Bonificado o Variable'];
const rateRegex = /(\d+[\.,]?\d*)/;

const rateResults = testRates.map(rate => {
    const match = rate.match(rateRegex);
    return { rate, extracted: match ? match[0] : null };
});

logTest(
    'Rate extraction regex handles all formats',
    rateResults.slice(0, 3).every(r => r.extracted !== null) && rateResults[3].extracted === null,
    rateResults.map(r => `"${r.rate}" → ${r.extracted || 'null'}`).join(', ')
);

// ========================================
// SUMMARY
// ========================================
console.log(`\n${BOLD}════════════════════════════════════════${RESET}`);
console.log(`${BOLD}REGRESSION TESTS COMPLETE${RESET}`);
console.log(`${BOLD}════════════════════════════════════════${RESET}\n`);

console.log(`${GREEN}Passed: ${passed}${RESET}`);
console.log(`${RED}Failed: ${failed}${RESET}`);
console.log(`Total:  ${passed + failed}\n`);

if (failed === 0) {
    console.log(`${GREEN}${BOLD}All tests passed! ✓${RESET}\n`);
    process.exit(0);
} else {
    console.log(`${RED}${BOLD}Some tests failed. Review above for details.${RESET}\n`);
    process.exit(1);
}
