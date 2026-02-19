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
