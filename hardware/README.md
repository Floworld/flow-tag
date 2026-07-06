# Hardware

Everything about the physical chip: what it is, how its memory is laid out, and where to buy more.

## What's in your tag

An **NXP NTAG21x** — the most common NFC Forum Type 2 tag on the planet. Passive (no battery), 13.56 MHz, ISO/IEC 14443A. Read range is a couple of centimetres by design; it's a tap, not a beacon.

We ship whichever of the three fits the run, all pin-and-protocol compatible:

| Chip    | Total EEPROM | Usable user memory | Password protect | Typical use            |
|---------|--------------|--------------------|------------------|------------------------|
| NTAG213 | 180 bytes    | **137 bytes**      | yes (PWD/PACK)   | a URL, short text      |
| NTAG215 | 540 bytes    | **504 bytes**      | yes              | vCard, Wi-Fi, Amiibo   |
| NTAG216 | 924 bytes    | **888 bytes**      | yes              | multi-record, big data |

Not sure which you got? Any reader app's **Read/Info** tab prints the chip model and capacity.

- **Endurance:** ~100,000 write cycles, ~10 year data retention. You will not wear it out.
- **UID:** 7-byte, factory-programmed, unique, read-only. Useful as an identity anchor (auth, access control) — but note UIDs can be cloned by determined attackers, so don't use the bare UID as your only security factor.

## Memory map (Type 2, simplified)

Memory is organized as **pages of 4 bytes**.

```
Page 0-2    UID + internal / lock bytes (mostly read-only)
Page 3      Capability Container (CC) — declares tag type & size
Page 4 ...  USER MEMORY  ← your NDEF TLV lives here
...
last pages  Dynamic lock bytes, CONFIG pages (AUTH0, ACCESS, PWD, PACK)
```

Your payload starts at **page 4**. The TLV wrapper (`03 <len> ... FE`) begins right there. Everything before page 4 is chip plumbing — leave it alone unless you know exactly what you're doing.

## Locking — the one irreversible action

NTAG21x has **static and dynamic lock bits**. Setting them makes pages **permanently read-only**. There is no unlock. No reflash. No warranty claim. The tag is frozen as-is until it's landfill.

Only lock a tag you're deploying somewhere you never want it altered (a product, a public poster). For anything on your own desk, **don't** — you'll want to rewrite it next week.

Softer alternative: the **password (PWD + PACK)** and **AUTH0** config gate *writes* behind a 32-bit password while still allowing reads. Reversible if you know the password. Set it via your writer app's **Other → Protect / Set password**, or by writing the CONFIG pages directly (see the NXP datasheet for the exact page numbers per chip).

## Sourcing more

- Search **"NTAG215 NFC sticker"** on any electronics marketplace — €0.30–1.00 each in packs.
- Want the round 25 mm white sticker like the one in your box? That's a bog-standard **NTAG215 25mm wet-inlay**.
- Or just [buy another Flow](https://flowworld.xyz) — one ships free in every box.

## Datasheets (authoritative byte-level truth)

- NXP NTAG213/215/216 datasheet (NT3H1x01) — the CONFIG page layout, lock semantics, and timing all live here.
- NFC Forum Type 2 Tag Operation Specification — the TLV + NDEF-on-tag rules.

If this repo and the datasheet ever disagree, the datasheet wins. Open a PR and we'll fix ours.
