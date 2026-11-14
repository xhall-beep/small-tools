# Free editions

Two downloads. No email, no signup, no tracking.

## svcguard lite

A single file that names every broken service in a runit tree.

```bash
python3 svcguard-lite.py doctor
python3 svcguard-lite.py doctor --json
python3 svcguard-lite.py --svdir /path/to/service doctor
```

It reports five failure modes:

| Code | Meaning |
|---|---|
| `no-run-script` | service directory has no `run` file |
| `run-not-executable` | `run` exists but is not `chmod +x` |
| `stale-lock` | `supervise/lock` with no live `supervise/pid` |
| `dead-supervise-pid` | `supervise/pid` points at a process that is gone |
| `orphan` | service process reparented to PID 1, still using CPU/RAM |

Exit code is `1` when any `error` finding exists, so it drops straight into cron
or a monitoring check. `--json` gives the same report machine-readable.

Default service root is `$SVDIR`, falling back to the Termux path
`/data/data/com.termux/files/usr/var/service`.

**What is not here:** `ensure` (start supervisors for unmanaged services) and
`reap` (terminate orphaned processes). Those are in the paid edition, because
they are the commands that change system state and they need the safety model
that goes with them.

## PedalSpec v1 schema

`pedalspec.schema.json` is the JSON Schema 2020-12 document behind PedalSpec
Studio. It is the strict part of the product: ten required fields, numeric
ranges, enums, and a `source` field so a spec always says where its numbers
came from.

Use it for:

- validating a spreadsheet export before it reaches a listing
- a CI check on a public pedal database
- your own importer, so you reject bad data at the door

```python
import json, jsonschema
schema = json.load(open("pedalspec.schema.json"))
jsonschema.validate(record, schema)   # raises on the first violation
```

The schema is CC0. Take it, fork it, publish your own profile of it.

## Licence

- `svcguard-lite.py` — MIT. Use it, ship it, embed it.
- `pedalspec.schema.json` — CC0. Public domain.
- The paid editions are commercial single-user licences; see each archive.
