// News-image entry for 25 November 2026 (Node 22, standard library only).
// The image is drawn from code by draw.py and shipped as entry.png beside
// this file; the program just writes those exact bytes to the output dir.
// The grader runs it twice and both runs must produce identical bytes.
//
// Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const png = readFileSync(join(here, 'entry.png'));
writeFileSync(join(outDir, 'entry.png'), png);
