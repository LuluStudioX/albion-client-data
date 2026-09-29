# albion-client-data

Albion Online's static game data, decoded from the official game client. XML, one directory,
one commit per client build, tagged so you can pin an exact one.

**Unofficial.** Not affiliated with, endorsed by, or operated by Sandbox Interactive GmbH.
Read [NOTICE.md](NOTICE.md) before you use any of this - it covers ownership, why there is no
licence file, and how to ask for it to come down.

```
VERSION          the client build this data came from, e.g. 1.32.020.344269
manifest.json    every file with its sha256 and byte count
gamedata/        the XML, byte-for-byte as the decoder produced it
```

## Getting a file

```bash
# the current build
curl -sO https://raw.githubusercontent.com/LuluStudioX/albion-client-data/main/gamedata/items.xml

# a specific build, pinned - tags are immutable, main moves
curl -sO https://raw.githubusercontent.com/LuluStudioX/albion-client-data/v1.32.020.344269/gamedata/items.xml

# which build is current, without cloning
curl -s https://raw.githubusercontent.com/LuluStudioX/albion-client-data/main/VERSION
```

A full clone is about 15 MB. Each patch adds well under 1 MB of history, so there is no LFS,
no shallow-clone advice and nothing to prune.

## Checking what you got

`manifest.json` holds the sha256 of every file, and it is recomputed from the bytes on every
publish rather than carried forward:

```bash
python3 - <<'PY'
import hashlib, json, pathlib
man = json.load(open("manifest.json"))
bad = [n for n, m in man["files"].items()
       if hashlib.sha256(pathlib.Path("gamedata", n).read_bytes()).hexdigest() != m["sha256"]]
print(f'{man["version"]}: {len(man["files"]) - len(bad)}/{len(man["files"])} verified')
PY
```

## Diffing two builds

Every publish is a single commit and a tag, so:

```bash
git diff v1.32.010.343282 v1.32.020.344269 -- gamedata/items.xml
git diff --stat v1.32.010.343282 v1.32.020.344269
```

The GitHub Release for each tag lists what changed.

## Where it comes from

The Linux client is fetched from Albion's own patch server and every file is verified against
the md5 in the server's own table of contents. `GameData/*.bin` is then decoded to XML. The
client ships 164 `.bin`; 145 of them are markup and are what you see here. The other 19 are
not, and are skipped rather than guessed at.

## What this is not

**It is not a mirror of [ao-bin-dumps](https://github.com/ao-data/ao-bin-dumps)**, and should
not be used as a drop-in replacement for it. Measured 2026-09-29:

|                                              | files |
| -------------------------------------------- | ----- |
| ao-bin-dumps                                  | 203   |
| here                                          | 145   |
| in ao-bin-dumps, not here                     | 59    |
| ...of those, present in the client download   | 0     |
| here, not in ao-bin-dumps                     | 1     |

Those 59 are all `_asia` / `_europe` / `_patch` variants, and none of them has a `.bin` in the
downloadable client - they come off the live servers, which this pipeline never touches. The
one file here that ao-bin-dumps does not carry is `profanity.xml`.

So: if you need the regional and patch variants, use ao-bin-dumps. If you want the client's
own data tied to an exact build number and verifiable against its hashes, use this.

There is no JSON here yet. It may come later; the layout leaves room for it without moving a
file.

## How it is published

Unattended, on patch day. A script on the maintainer's box decodes the new build, runs six
refusal checks over it, and pushes an `updates-<version>` branch. A workflow in this
repository validates the committed bytes independently, opens a pull request and turns on
auto-merge, so a green build lands with nobody acting and a red one lands never.

The checks that can refuse a publish: every XML parses; the version strictly advanced; the
file count is within 10% of the last release; no file lost more than half its size; the
manifest matches the bytes; the checkout was clean to begin with.
