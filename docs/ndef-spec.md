# NDEF, at the byte level

You don't need this to use the tag. You need it if you want to write bytes by hand, script a batch, or understand *why* a tap does what it does. Here's the format with no hand-waving.

## The container: TLV

The chip's user memory doesn't start with NDEF directly — it starts with a **TLV** (Type-Length-Value) wrapper that says "an NDEF message lives here."

```
03 <LEN> <NDEF message ...> FE
│    │          │            └─ Terminator TLV
│    │          └─ the NDEF message itself
│    └─ length of the message in bytes
└─ 0x03 = "NDEF Message" TLV tag
```

If the message is ≥ 255 bytes, `<LEN>` becomes the 3-byte form `FF <hi> <lo>`.

## One NDEF record

```
┌────────┬────────┬───────────┬──────────┬──────────┬─────────┐
│ Header │ TypeLen│ PayloadLen│  [IDLen] │   Type   │ Payload │
│ 1 byte │ 1 byte │ 1 or 4 B  │  0/1 B   │  n bytes │  m bytes│
└────────┴────────┴───────────┴──────────┴──────────┴─────────┘
```

### The header byte (flags + TNF)

Bit by bit:

```
7   6   5   4   3   2 1 0
MB  ME  CF  SR  IL  └─TNF─┘
```

- **MB** Message Begin — 1 on the first record
- **ME** Message End — 1 on the last record
- **CF** Chunk Flag — 0 unless you're chunking (you're not)
- **SR** Short Record — 1 if payload < 256 bytes, so PayloadLen is 1 byte
- **IL** ID Length present — usually 0
- **TNF** Type Name Format — what kind of type string follows (below)

### TNF values you'll actually use

| TNF | Meaning              | Type field example              |
|-----|----------------------|---------------------------------|
| 0x1 | NFC Well-Known Type  | `U` (URI), `T` (Text)           |
| 0x2 | MIME media type      | `text/vcard`                    |
| 0x4 | External type        | `floworld.xyz:macro`           |

## Worked example: a URI record for https://floworld.xyz

Well-Known URI records shorten common prefixes with a one-byte code, so you don't waste memory on `https://`.

```
Prefix table (partial):
0x00 none      0x01 http://www.   0x02 https://www.
0x03 http://   0x04 https://      0x05 tel:  ...
```

`https://` is `0x04`, so we store `0x04` + `floworld.xyz`.

```
D1 01 0D 55 04 66 6C 6F 77 6F 72 6C 64 2E 78 79 7A
│  │  │  │  │  └──────────── "floworld.xyz" (ASCII) ──────────┘
│  │  │  │  └─ 0x04 = "https://" prefix
│  │  │  └─ 0x55 = 'U', the URI Well-Known type
│  │  └─ payload length = 0x0D = 13 bytes (1 prefix + 12 chars)
│  └─ type length = 0x01
└─ header: MB=1 ME=1 SR=1 TNF=1  → 0xD1
```

Wrapped in the TLV container, the full memory blob is:

```
03 11 D1 01 0D 55 04 66 6C 6F 77 6F 72 6C 64 2E 78 79 7A FE
```

That's a complete, valid tag. 20 bytes. Fits any NTAG variant with room to spare.

## Text record shape (TNF 0x1, type `T`)

```
payload = [status byte][language code][UTF-8 text]
status byte: bit7 = 0 (UTF-8), bits0-5 = length of language code
e.g. 0x02 "en" "hello"  →  02 65 6E 68 65 6C 6C 6F
```

## External / custom records (TNF 0x4)

This is the door for Flow triggers and anything bespoke:

```
TNF = 0x4, Type = "floworld.xyz:macro", Payload = your bytes
```

The OS won't auto-handle it — that's the point. Flow (or your own handler) claims the type and decides what it means. See [../examples/flow-macro.md](../examples/flow-macro.md).

## Verify your work

- `nfc-list` / NFC Tools' **Read** tab dumps the raw records.
- [`ndeflib`](https://ndeflib.readthedocs.io) (Python) parses and validates blobs offline.
- Proxmark `hf mfu dump` gives you the raw pages including lock/config bytes.

If the parser is happy, every phone will be too.
