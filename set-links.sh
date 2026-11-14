#!/usr/bin/env bash
# Fill in the three checkout URLs and publish.
#
#   ./set-links.sh "https://you.gumroad.com/l/pedalspec" \
#                  "https://you.gumroad.com/l/svcguard" \
#                  "https://you.gumroad.com/l/bundle"
#
# Any argument may be "" to leave that button on the contact fallback.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

PEDALSPEC="${1:-}"
SVCGUARD="${2:-}"
BUNDLE="${3:-}"

python3 - "$PEDALSPEC" "$SVCGUARD" "$BUNDLE" <<'PY'
import re, sys, pathlib
pedalspec, svcguard, bundle = sys.argv[1:4]
p = pathlib.Path("config.js")
src = p.read_text()
def setv(src, key, val):
    return re.sub(r'(%s:\s*)"[^"]*"' % re.escape(key), r'\g<1>"%s"' % val, src, count=1)
src = setv(src, "pedalspec", pedalspec)
src = setv(src, "svcguard", svcguard)
src = setv(src, "bundle", bundle)
p.write_text(src)
print("config.js updated:")
for k, v in (("pedalspec", pedalspec), ("svcguard", svcguard), ("bundle", bundle)):
    print("  %-10s %s" % (k, v or "(contact fallback)"))
PY

git add config.js
git -c user.name="xhall-beep" -c user.email="xhall-beep@users.noreply.github.com" \
    commit -q -m "Wire checkout links"
git push -q origin main
echo "pushed — GitHub Pages rebuilds in about 30s"
echo "https://xhall-beep.github.io/small-tools/"
