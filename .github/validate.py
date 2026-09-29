#!/usr/bin/env python3
"""Validate a publish from the committed bytes. Run by CI; no dependencies.

    python3 .github/validate.py [--base-version <v>]

This is deliberately a SECOND OPINION. The box-side publisher runs its own checks before it
pushes, and a check that is wrong passes itself - so this one re-derives everything from what
actually landed in the commit rather than trusting any of it:

  - every file in gamedata/ parses as XML
  - manifest.json names exactly those files, with the right sha256 and byte count
  - VERSION is dotted digits and agrees with manifest.version
  - VERSION strictly advances on the base branch's (when --base-version is given)

Exits non-zero with the reason on the first failure. `main` requires this check to pass, so a
red run means the pull request sits there and nothing is published.
"""
import argparse
import hashlib
import json
import os
import sys
import xml.etree.ElementTree as ET

SUBDIR = "gamedata"


def fail(msg):
    print("FAIL " + msg)
    sys.exit(1)


def version_key(v):
    parts = []
    for piece in str(v).strip().split("."):
        if not piece.isdigit():
            fail(f"version {v!r} is not dotted digits")
        parts.append(int(piece))
    return tuple(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-version", help="the VERSION on the branch being merged into")
    a = ap.parse_args()

    if not os.path.isdir(SUBDIR):
        fail(f"no {SUBDIR}/ directory")
    if not os.path.exists("VERSION"):
        fail("no VERSION file")
    if not os.path.exists("manifest.json"):
        fail("no manifest.json")

    version = open("VERSION", encoding="utf-8").read().strip()
    version_key(version)

    man = json.load(open("manifest.json", encoding="utf-8"))
    if man.get("version") != version:
        fail(f"VERSION says {version!r}, manifest says {man.get('version')!r}")

    on_disk = sorted(f for f in os.listdir(SUBDIR) if f.endswith(".xml"))
    if not on_disk:
        fail(f"{SUBDIR}/ holds no .xml files")

    listed = sorted(man.get("files") or {})
    if on_disk != listed:
        missing = sorted(set(on_disk) - set(listed))
        extra = sorted(set(listed) - set(on_disk))
        fail(f"manifest does not match the directory - unlisted: {missing[:5]}, "
             f"listed but absent: {extra[:5]}")

    for fn in on_disk:
        path = os.path.join(SUBDIR, fn)
        try:
            ET.parse(path)
        except Exception as e:                             # noqa: BLE001 - the reason is the point
            fail(f"{fn} does not parse: {type(e).__name__}: {e}")
        raw = open(path, "rb").read()
        entry = man["files"][fn]
        if len(raw) != entry.get("bytes"):
            fail(f"{fn} is {len(raw)} bytes, manifest says {entry.get('bytes')}")
        got = hashlib.sha256(raw).hexdigest()
        if got != entry.get("sha256"):
            fail(f"{fn} hashes to {got[:12]}..., manifest says {str(entry.get('sha256'))[:12]}...")

    if a.base_version:
        base = a.base_version.strip()
        if base and version_key(version) <= version_key(base):
            fail(f"version {version} does not advance on the published {base}")

    print(f"ok   {version}: {len(on_disk)} files parsed, hashed and matched against the manifest")
    if a.base_version:
        print(f"ok   advances on {a.base_version.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
