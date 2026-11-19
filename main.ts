// News-image entry for 19 November 2026 (Node 22, standard library only).
//
// The entry is the poster drawn by draw_poster.py and shipped as the
// entry.png beside this file. This program's only job is to place that
// exact file at the path the grader reads.
//
// The grader runs this program twice in a fresh container with no
// network; both runs must write the same bytes. Copying the shipped
// file byte for byte guarantees that: nothing is generated, nothing
// depends on the clock, and nothing touches the network.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output, so a local check is:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const poster = readFileSync(join(here, 'entry.png'));

// The output file keeps the name entry.png; the gate tells a PNG
// from a JPEG by its first bytes, and this file is a PNG.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), poster);
