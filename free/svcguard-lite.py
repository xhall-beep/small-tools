#!/usr/bin/env python3
"""svcguard lite — find out why your runit service will not start.

Free edition. Detects the five failure modes that produce useless error
messages. The paid edition adds `ensure` (start supervisors) and `reap`
(terminate orphaned processes).

    python3 svcguard-lite.py doctor
    python3 svcguard-lite.py doctor --json
    python3 svcguard-lite.py --svdir /path/to/service doctor

Pure stdlib. Python 3.8+.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

DEFAULT_SVDIR = os.environ.get("SVDIR") or "/data/data/com.termux/files/usr/var/service"

PS_RE = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(.+?)\s*$")


def read_int(path):
    try:
        with open(path) as fh:
            return int(fh.read().strip() or 0) or None
    except (OSError, ValueError):
        return None


def ps_rows():
    ps = shutil.which("ps")
    if not ps:
        return []
    try:
        out = subprocess.run([ps, "-eo", "pid,ppid,pcpu,rss,comm"],
                             capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    rows = []
    for line in out.splitlines():
        m = PS_RE.match(line)
        if m:
            rows.append({"pid": int(m.group(1)), "ppid": int(m.group(2)),
                         "pcpu": float(m.group(3)), "rss_kb": int(m.group(4)),
                         "comm": m.group(5).strip()})
    return rows


def services(svdir):
    if not os.path.isdir(svdir):
        return []
    return [n for n in sorted(os.listdir(svdir))
            if os.path.isdir(os.path.join(svdir, n)) and not n.startswith(".") and n != "log"]


def diagnose(svdir):
    names = services(svdir)
    rows = ps_rows()
    findings = []
    orphans = []

    for name in names:
        path = os.path.join(svdir, name)
        run = os.path.join(path, "run")
        sup = os.path.join(path, "supervise")
        lock = os.path.join(sup, "lock")
        spid = read_int(os.path.join(sup, "pid"))

        if not os.path.isfile(run):
            findings.append({"severity": "error", "service": name, "code": "no-run-script",
                             "detail": "no run file; runsv can never start this service"})
        elif not os.access(run, os.X_OK):
            findings.append({"severity": "error", "service": name, "code": "run-not-executable",
                             "detail": "run exists but is not executable (chmod +x)"})

        if os.path.exists(lock) and not spid:
            findings.append({"severity": "error", "service": name, "code": "stale-lock",
                             "detail": "supervise/lock with no supervise/pid; restart will fail until removed"})

        if spid and rows and not any(r["pid"] == spid for r in rows):
            findings.append({"severity": "warn", "service": name, "code": "dead-supervise-pid",
                             "detail": "supervise/pid %d is not running" % spid})

    if rows:
        wanted = set(names)
        for r in rows:
            if r["ppid"] == 1 and r["pid"] != 1 and os.path.basename(r["comm"]) in wanted:
                orphans.append(r)
                findings.append({"severity": "warn", "service": os.path.basename(r["comm"]),
                                 "code": "orphan",
                                 "detail": "pid %d reparented to init, %.1f%% CPU, %d MB"
                                           % (r["pid"], r["pcpu"], r["rss_kb"] // 1024)})

    return {"svdir": os.path.abspath(svdir), "service_count": len(names),
            "findings": findings, "orphans": orphans,
            "ok": not any(f["severity"] == "error" for f in findings)}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="svcguard-lite",
                                 description="Diagnose runit supervision failures (free edition).")
    ap.add_argument("--svdir", default=DEFAULT_SVDIR)
    ap.add_argument("command", nargs="?", default="doctor", choices=["doctor"])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    rep = diagnose(args.svdir)

    if args.json:
        print(json.dumps(rep, indent=2))
        return 0 if rep["ok"] else 1

    print("svcguard lite — %s" % rep["svdir"])
    print("services: %d" % rep["service_count"])
    if not rep["findings"]:
        print("  no problems found")
    for f in rep["findings"]:
        print("  [%-5s] %-20s %-18s %s" % (f["severity"].upper(), f["service"],
                                           f["code"], f["detail"]))
    print()
    print("Paid edition adds `ensure` (start supervisors) and `reap` (kill orphans).")
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
