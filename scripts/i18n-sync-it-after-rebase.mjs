#!/usr/bin/env node
// One-off: align the Italian pack with current English after a rebase.
// Keeps existing it strings; fills missing keys from es (upstream-synced); drops keys removed from en.
import { existsSync, unlinkSync } from 'node:fs'
import path from 'node:path'
import {
    flatten,
    MESSAGES_DIR,
    namespaces,
    readNamespace,
    unflattenLike,
    writeNamespace,
} from './i18n/catalog.mjs'

const IT_DIR = path.join(MESSAGES_DIR, 'it')
const rewindPath = path.join(IT_DIR, 'rewind.json')
if (existsSync(rewindPath)) unlinkSync(rewindPath)

for (const ns of namespaces('en')) {
    const enTree = readNamespace('en', ns)
    const en = flatten(enTree)
    const es = flatten(readNamespace('es', ns))
    const it = existsSync(path.join(IT_DIR, `${ns}.json`)) ? flatten(readNamespace('it', ns)) : {}
  const out = {}
    for (const [key, value] of Object.entries(en)) {
        if (it[key] !== undefined) out[key] = it[key]
        else if (es[key] !== undefined) out[key] = es[key]
        else out[key] = value
    }
    writeNamespace('it', ns, unflattenLike(enTree, out))
}

console.log('i18n: it pack structure synced with en (missing keys bootstrapped from es).')