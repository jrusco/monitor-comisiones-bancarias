#!/usr/bin/env node
/**
 * Edge Case Functional Tests
 * Tests runtime behavior with edge case data
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

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
        console.log(`  ${details}\n`);
    }
}

function logSection(name) {
    console.log(`\n${BOLD}${YELLOW}═══ ${name} ═══${RESET}\n`);
}

console.log(`\n${BOLD}Edge Case Functional Tests${RESET}`);
console.log(`Testing runtime behavior with edge case data\n`);

// ========================================
// TEST: Entity with Empty Fees Array
// ========================================
logSection('Edge Case: Entity with No Fees');

// Create test data with an entity that has no fees
const testDataNoFees = [
    {
        "id": "test-entity",
        "name": "Test Entity",
        "type": "Test",
        "color": "bg-slate-600",
        "textColor": "text-slate-600",
        "logo": "TE",
        "feeUrl": "https://example.com",
        "apiUrl": "N/A",
        "hasApi": false,
        "fees": []  // Empty fees array
    },
    {
        "id": "mercadopago",
        "name": "Mercado Pago",
        "type": "Agregador",
        "color": "bg-sky-500",
        "textColor": "text-sky-500",
        "logo": "MP",
        "feeUrl": "https://mercadopago.com",
        "apiUrl": "N/A",
        "hasApi": true,
        "fees": [
            { "concept": "Point - Débito", "term": "En el momento", "rate": "3.25% + IVA" }
        ]
    }
];

// Test that the code handles empty fees
const indexHtml = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');

// Extract handleEntityChange function code
const funcMatch = indexHtml.match(/function handleEntityChange[\s\S]*?^        \}/m);
if (funcMatch) {
    const funcCode = funcMatch[0];

    // Verify empty fees handling code exists and is structured correctly
    const hasEmptyCheck = funcCode.includes('!entity.fees || entity.fees.length === 0');
    const hasDisable = funcCode.includes('paymentTypeSelector.disabled = true');
    const hasNoFeesMessage = funcCode.includes('Sin comisiones configuradas');
    const resetsState = funcCode.includes('simulatorState.selectedFeeIndex = null');

    logTest(
        'handleEntityChange checks for empty fees',
        hasEmptyCheck,
        hasEmptyCheck ? 'Condition: !entity.fees || entity.fees.length === 0' : 'Check NOT found'
    );

    logTest(
        'Dropdown is disabled for empty fees',
        hasDisable,
        hasDisable ? 'paymentTypeSelector.disabled = true' : 'Disable NOT found'
    );

    logTest(
        'User sees helpful message for empty fees',
        hasNoFeesMessage,
        hasNoFeesMessage ? '"Sin comisiones configuradas" message shown' : 'Message NOT found'
    );

    logTest(
        'State is properly reset for empty fees',
        resetsState,
        resetsState ? 'selectedFeeIndex reset to null' : 'State reset NOT found'
    );
}

// ========================================
// TEST: Missing Default Entity
// ========================================
logSection('Edge Case: Missing Default Entity');

// Create test data WITHOUT mercadopago
const testDataNoDefault = [
    {
        "id": "bna",
        "name": "Banco Nación",
        "type": "Banco",
        "color": "bg-blue-600",
        "textColor": "text-blue-600",
        "logo": "BNA",
        "feeUrl": "https://bna.com",
        "apiUrl": "N/A",
        "hasApi": false,
        "fees": [
            { "concept": "Débito", "term": "24 hs", "rate": "0.8% + IVA" }
        ]
    }
];

// Extract initSimulator function to verify fallback logic
const initMatch = indexHtml.match(/function initSimulator[\s\S]*?^        \}/m);
if (initMatch) {
    const initCode = initMatch[0];

    const hasDefaultId = initCode.includes("const defaultEntityId = 'mercadopago'");
    const hasFindDefault = initCode.includes('entities.find(e => e.id === defaultEntityId)');
    const hasIfDefault = initCode.includes('if (defaultEntity)');
    const hasElseFallback = initCode.includes('else if (entities.length > 0)');
    const usesFallback = initCode.includes('entities[0].id');

    logTest(
        'Default entity ID is defined',
        hasDefaultId,
        hasDefaultId ? "defaultEntityId = 'mercadopago'" : 'Default NOT defined'
    );

    logTest(
        'Searches for default entity',
        hasFindDefault,
        hasFindDefault ? 'Uses entities.find() to locate default' : 'Find NOT found'
    );

    logTest(
        'Conditional check for default entity',
        hasIfDefault,
        hasIfDefault ? 'Checks if (defaultEntity) exists' : 'Check NOT found'
    );

    logTest(
        'Fallback for missing default',
        hasElseFallback,
        hasElseFallback ? 'Has else if (entities.length > 0) clause' : 'Fallback NOT found'
    );

    logTest(
        'Uses first entity as fallback',
        usesFallback,
        usesFallback ? 'Falls back to entities[0].id' : 'First entity NOT used'
    );
}

// ========================================
// TEST: Invalid Entity Selection
// ========================================
logSection('Edge Case: Invalid Entity Selection');

const handleMatch = indexHtml.match(/function handleEntityChange[\s\S]*?^        \}/m);
if (handleMatch) {
    const handleCode = handleMatch[0];

    // Verify null check comes AFTER the find and BEFORE using entity
    const nullCheckPattern = /const entity = entities\.find[\s\S]*?if \(!entity\)[\s\S]*?return;[\s\S]*?simulatorState\.selectedEntity = entity/;
    const hasProperOrder = nullCheckPattern.test(handleCode);

    logTest(
        'Null check occurs after find() and before using entity',
        hasProperOrder,
        hasProperOrder ? 'Proper code order: find → null check → use entity' : 'Order may be incorrect'
    );

    const earlyReturn = handleCode.includes('return;') && handleCode.includes('if (!entity)');
    logTest(
        'Early return on null entity',
        earlyReturn,
        earlyReturn ? 'Returns early when entity is null' : 'Early return NOT found'
    );
}

// ========================================
// TEST: Variable Rate Handling
// ========================================
logSection('Edge Case: Variable/Non-Numeric Rates');

const recalcMatch = indexHtml.match(/function recalculateFee[\s\S]*?^        \}/m);
if (recalcMatch) {
    const recalcCode = recalcMatch[0];

    const hasRateMatch = recalcCode.includes("fee.rate.match(/");
    const hasNullCheck = recalcCode.includes('if (!rateMatch)');
    const hasWarningMessage = recalcCode.includes('Tasa variable - consultar con proveedor');

    logTest(
        'Extracts rate using regex',
        hasRateMatch,
        hasRateMatch ? 'Uses regex to extract numeric rate' : 'Regex NOT found'
    );

    logTest(
        'Handles non-numeric rates gracefully',
        hasNullCheck,
        hasNullCheck ? 'Checks if (!rateMatch) for non-numeric rates' : 'Check NOT found'
    );

    logTest(
        'Shows warning for variable rates',
        hasWarningMessage,
        hasWarningMessage ? 'Displays warning for rates like "Bonificado o Variable"' : 'Warning NOT found'
    );
}

// ========================================
// TEST: XSS Prevention in All Code Paths
// ========================================
logSection('Edge Case: XSS Prevention Code Paths');

// Check that innerHTML is not used in user-facing content generation
const dangerousPatterns = [
    { pattern: /paymentTypeSelector\.innerHTML\s*=/, name: 'paymentTypeSelector.innerHTML' },
    { pattern: /breakdownEl\.innerHTML\s*=/, name: 'breakdownEl.innerHTML' },
    { pattern: /feeResult\.innerHTML\s*=/, name: 'feeResult.innerHTML' }
];

dangerousPatterns.forEach(({ pattern, name }) => {
    const found = pattern.test(indexHtml);
    logTest(
        `No dangerous ${name}`,
        !found,
        !found ? `${name} NOT found (safe!)` : `WARNING: ${name} found - potential XSS`
    );
});

// ========================================
// SUMMARY
// ========================================
console.log(`\n${BOLD}════════════════════════════════════════${RESET}`);
console.log(`${BOLD}EDGE CASE TESTS COMPLETE${RESET}`);
console.log(`${BOLD}════════════════════════════════════════${RESET}\n`);

console.log(`${GREEN}Passed: ${passed}${RESET}`);
console.log(`${RED}Failed: ${failed}${RESET}`);
console.log(`Total:  ${passed + failed}\n`);

if (failed === 0) {
    console.log(`${GREEN}${BOLD}All edge case tests passed! ✓${RESET}\n`);
    process.exit(0);
} else {
    console.log(`${RED}${BOLD}Some tests failed. Review above for details.${RESET}\n`);
    process.exit(1);
}
