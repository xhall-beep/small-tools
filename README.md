# Small Tools

Software that fixes one expensive problem, with tests you can run yourself.

This repository is the storefront and the free editions. The paid editions are
separate archives and are not published here.

## Free

| File | What it does | Licence |
|---|---|---|
| [`free/svcguard-lite.py`](free/svcguard-lite.py) | Names every broken service in a runit tree: stale lock, dead supervise pid, missing run script, orphan | MIT |
| [`free/pedalspec.schema.json`](free/pedalspec.schema.json) | JSON Schema 2020-12 for guitar pedal specifications | CC0 |

```bash
python3 free/svcguard-lite.py doctor
python3 free/svcguard-lite.py doctor --json
```

## Paid

| Product | What it is | Price |
|---|---|---|
| **svcguard** | Full supervisor diagnosis and repair: `ensure`, `reap`, dry-run safety, 18 tests | $9 |
| **PedalSpec Studio** | Local-first pedal spec catalog with validation, comparison, CSV/Markdown/print export, 20 tests | $19 |

Checkout links live in [`config.js`](config.js).

## Why the free editions are real

They are not timers or crippled demos. `svcguard-lite` is the entire diagnosis
half of the paid tool and will keep working forever. The schema is the actual
schema the app enforces.

## Hosting

Static site. No build step, no framework, no analytics. Open `index.html` or
serve the directory:

```bash
python3 -m http.server 8000
```

## Licence

Site and free tools: see [`free/LICENSE.txt`](free/LICENSE.txt). Paid archives
carry a commercial single-user licence.
