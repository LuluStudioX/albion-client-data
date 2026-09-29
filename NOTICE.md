# NOTICE

## What these files are

The XML files in `gamedata/` are Albion Online's static game data - items, mobs,
buildings, spells, loot tables and so on. They were not written here. They are
produced by decoding `GameData/*.bin` from the official Albion Online game client,
which Sandbox Interactive GmbH distributes publicly and which any player already
has on disk.

The decoding is a format conversion and nothing else. No file is edited, filtered,
enriched or reformatted: what is committed is byte-for-byte what the decoder
produced, and `manifest.json` records the sha256 of every file so that can be
checked rather than trusted.

## Who owns it

Sandbox Interactive GmbH. Not us.

We claim no ownership of the data and grant no licence to it, because neither is
ours to give. This repository carries no software licence for that reason - an
absent licence here is a deliberate statement, not an oversight. If you use these
files, your position is between you and the rights holder.

## Why it exists

To make the game's own data readable and diffable for the tools the community
builds around Albion Online, and to give those tools a stable, versioned,
verifiable copy to pin against instead of each one shipping its own scrape. Every
publish is tagged with the exact client build it came from.

## What is deliberately NOT here

The client's **art** - textures, icons, banners - is not published here and will
not be. The same pipeline extracts it for internal use; redistributing it is a
different question with no precedent behind it, and the answer we have chosen is
no.

Also absent: the game client itself, the raw `.bin` files, and anything that is
inferred rather than decoded.

## Affiliation

This repository is an independent, fan-made project. It is **not affiliated with,
endorsed by, or operated by Sandbox Interactive GmbH**. "Albion Online" is a
trademark of its respective owner.

It is maintained by Lulu Studio, the operator of AO-SAGE
(<https://ao-sage.com>), a sole independent operator based in Denmark (EU).
Automated traffic from that project identifies itself as
`ao-sage/1.0 (+https://ao-sage.com; <component>)`, so requests seen in a server
log and this repository lead to the same place.

## Contact, including to ask us to stop

Open an issue on this repository. For anything better kept out of public view, the
operator's contact details are published at <https://ao-sage.com/imprint>.

If Sandbox Interactive would prefer this data not be published, say so by either
route and it comes down. No argument, no delay, no process. That offer is the
point of this section.

Last updated: 2026-09-29
