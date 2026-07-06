# Customize it

The tag ships doing one thing. Here's how to make it do your thing. None of this asks permission from us — you're writing an open standard onto a chip you own.

## The 60-second version

1. Open a writer app (see [install.md](install.md)).
2. **Write → Add a record.**
3. Pick a type, fill it in, hold to the tag.

Done. The old default is gone, your record is live.

## Pick a record type

Every recipe below has a ready-made file in [`../examples/`](../examples/).

| I want the tap to…            | Record type        | Example                                   |
|-------------------------------|--------------------|-------------------------------------------|
| Open a website / link         | URI                | [url.md](../examples/url.md)              |
| Join my Wi-Fi                  | Wi-Fi (WSC)        | [wifi.md](../examples/wifi.md)            |
| Share my contact card          | vCard / MIME       | [vcard.md](../examples/vcard.md)          |
| Trigger a Flow macro           | Custom URI scheme  | [flow-macro.md](../examples/flow-macro.md)|
| Show plain text                | Text               | inline below                              |
| Launch an app                  | Android App / URI  | inline below                              |

### Text record (inline)

In NFC Tools: **Add a record → Text → type it → Write.** Good for notes, codes, a message on a package.

### Launch an app

- **Android:** **Add a record → Application** → paste the package name (e.g. `com.spotify.music`).
- **iOS:** apps can't be force-launched by tag; instead write a **URI** with the app's universal link or custom scheme (e.g. `spotify://`).

## Multi-record tags

You can stack records — e.g. a URL *and* a text note. Order matters: the OS usually acts on the **first** actionable record and shows the rest. Watch your [capacity](../hardware/README.md); NTAG213 fills up fast.

## Make a change permanent (careful)

NTAG21x has a **lock bit**. Set it and the tag is read-only *forever* — no take-backs, no reflash. Only do this for tags you're handing out in the wild and never want tampered with. How-to and the exact config bytes: [../hardware/README.md](../hardware/README.md).

## Password-protect instead of hard-locking

NTAG215/216 support a 32-bit password (PWD/PACK) that gates writes but still allows reads. Softer than the lock bit — you can still rewrite it if you know the password. Set it via the app's **Other → Set password** or the config pages directly.

## Reset to the shipped default

Want the shipped default back? Re-write it from source:

- Human-readable definition: [`../payloads/default.json`](../payloads/default.json)
- Raw NDEF file: [`../examples/default.ndef`](../examples/default.ndef)
- Or just: write a URI record pointing at the default URL listed in `default.json`.

## Going deeper

If "write a record" is too abstract and you want to know exactly which bytes land where, read [ndef-spec.md](ndef-spec.md) and then script it with [`../tools/write-tag.py`](../tools/write-tag.py). That's the rabbit hole. Enjoy it.
