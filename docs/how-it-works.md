# How it works

NFC sounds like magic. It isn't. Here's the whole thing in five minutes.

## The chip

Inside the sticker is an **NTAG21x** — a passive chip with a tiny antenna. Passive means it has no battery. When you hold a phone near it, the phone's NFC coil throws out a magnetic field, that field induces enough current in the tag's antenna to wake the chip up, and the chip talks back. Move the phone away, the chip goes dark. It's a parasite that only lives while you're looking at it.

Think of it like a QR code that you tap instead of aim — same job (hand a small blob of data to a device), different delivery.

## The data format: NDEF

The chip stores bytes. Left alone, bytes mean nothing. So the industry agreed on a wrapper called **NDEF** (NFC Data Exchange Format) that says "here is a record, here is its type, here is its payload." Your phone reads the type and knows what to do: a URL record opens a browser, a Wi-Fi record offers to join a network, a text record just shows text.

An NDEF message is one or more records glued together:

```
[ Record 1 ][ Record 2 ][ ... ]
     │
     ├─ type   → "U" (URI), "T" (text), "application/vnd.wfa.wsc" (Wi-Fi)...
     ├─ flags  → is this the first/last record? how long is it?
     └─ payload → the actual bytes (the URL, the SSID, the contact)
```

That's it. The tag doesn't run code. It doesn't decide anything. It hands your phone a labelled envelope and your phone opens it.

Byte-level detail lives in [ndef-spec.md](ndef-spec.md).

## Why this matters for hacking it

Because the format is open and the phone does the interpreting, **you never have to ask us for permission.** You write a new NDEF message onto the chip and every NFC device on earth already knows how to read it. There's no flow-tag runtime, no firmware, no API key. The "software" is a standard your phone shipped with.

The default we flash (the Kastanienhof demo) is just one NDEF URL record. Overwriting it is writing a different record into the same memory. Nothing sacred, nothing protected.

## The one gotcha: capacity

The chip is small. Depending on which NTAG variant you got, you have somewhere between ~137 and ~888 bytes of usable space:

| Chip      | Usable user memory | Roughly fits              |
|-----------|--------------------|---------------------------|
| NTAG213   | 137 bytes          | a URL, a short text       |
| NTAG215   | 504 bytes          | a vCard, a Wi-Fi config   |
| NTAG216   | 888 bytes          | several records at once   |

If a write fails, you probably overflowed. Shorten the payload or use a link shortener. That's the only real constraint.

## Where Flow comes in

A phone reads the tag and acts on the record itself. **Flow** can go further: point the tag at a custom scheme or a small local endpoint and a tap becomes a trigger for a Flow macro — launch an app, run a script, flip your lights, start a timer. The tag is dumb on purpose; Flow is the brain that makes a tap mean something. See [../examples/flow-macro.md](../examples/flow-macro.md) and [flowworld.xyz](https://flowworld.xyz).
