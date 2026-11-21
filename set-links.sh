#!/usr/bin/env bash
# Fill in the checkout URLs and publish.
#
#   ./set-links.sh "https://you.gumroad.com/l/pedalspec" \
#                  "https://you.gumroad.com/l/svcguard" \
#                  "https://you.gumroad.com/l/bundle" \
#                  "https://you.gumroad.com/l/promptforge"
#
# Any argument may be "" to leave that button on the contact fallback.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

PEDALSPEC="${1:-}"
SVCGUARD="${2:-}"
BUNDLE="${3:-}"
PROMPTFORGE="${4:-}"

python3 - "$PEDALSPEC" "$SVCGUARD" "$BUNDLE" "$PROMPTFORGE" <<'PY'
import re, sys, pathlib
pedalspec, svcguard, bundle, promptforge = sys.argv[1:5]
p = pathlib.Path("config.js")
src = p.read_text()
def setv(src, key, val):
    return re.sub(r'(%s:\s*)"[^"]*"' % re.escape(key), r'\g<1>"%s"' % val, src, count=1)
src = setv(src, "pedalspec", pedalspec)
src = setv(src, "svcguard", svcguard)
src = setv(src, "bundle", bundle)
src = setv(src, "promptforge", promptforge)
p.write_text(src)
print("config.js updated:")
for k, v in (("pedalspec", pedalspec), ("svcguard", svcguard),
             ("bundle", bundle), ("promptforge", promptforge)):
    print("  %-12s %s" % (k, v or "(contact fallback)"))
PY

git add config.js
git -c user.name="xhall-beep" -c user.email="xhall-beep@users.noreply.github.com" \
    commit -q -m "Wire checkout links"
git push -q origin main
echo "pushed — GitHub Pages rebuilds in about 30s"
echo "https://xhall-beep.github.io/small-tools/"
