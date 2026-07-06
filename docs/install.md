# Install / setup — every platform

You don't install anything to *read* the tag. You only need a writer app when you want to change what it does. Pick your platform.

---

## iPhone (iOS 13+)

Every iPhone since the XS can write NFC. No jailbreak, no dev account.

1. App Store → install **NFC Tools** (free) or **NXP TagWriter**.
2. Open NFC Tools → **Write** → **Add a record**.
3. Pick a record type (URL, Text, Wi-Fi, Custom URL…).
4. Tap **Write** and hold the *top edge* of the phone to the tag.
5. Wait for the buzz + checkmark.

> iOS quirk: hold the tag near the **top** of the phone, not the back-center. The NFC coil lives up there.

---

## Android (Android 5+)

1. Settings → make sure **NFC** is toggled on.
2. Play Store → install **NFC Tools** or **TagWriter**.
3. **Write** → **Add a record** → choose type → **Write**.
4. Touch the tag to the back-center of the phone. Buzz = done.

Android will also auto-open whatever the tag currently points to the instant you touch it, so if you just want to *test* the default, unlock the phone and tap.

---

## Desktop — PN532 reader (Linux / macOS / Windows)

For batch-writing, scripting, or CI. Cheap PN532 USB/UART boards are ~€8.

```bash
# one-time deps (Debian/Ubuntu shown; use brew/choco elsewhere)
sudo apt install libnfc-bin libnfc-dev

# confirm the reader sees the tag
nfc-list

# write with our helper (see tools/write-tag.py)
python3 tools/write-tag.py --url "https://flowworld.xyz"
```

Full script + flags: [../tools/write-tag.py](../tools/write-tag.py).

---

## CLI — nfcpy (Python, any OS with a supported reader)

```bash
pip install nfcpy ndeflib

python3 - <<'PY'
import nfc, ndef
def on_connect(tag):
    tag.ndef.records = [ndef.UriRecord("https://flowworld.xyz")]
    print("written:", tag.ndef.records)
    return True
nfc.ContactlessFrontend('usb').connect(rdwr={'on-connect': on_connect})
PY
```

`nfcpy` supports most PN53x and RC-S380 readers. `nfc-list` / `lsusb` will tell you if yours is seen.

---

## Proxmark3 (for the people who already own one)

You know who you are.

```
hf mfu dump          # read current state
hf mfu wrbl -b 4 -d 03...   # write raw NDEF TLV, block by block
```

Overkill for a URL, perfect for poking at lock bytes and the config pages. Memory map in [../hardware/README.md](../hardware/README.md).

---

## Troubleshooting

| Symptom                        | Cause / fix                                              |
|--------------------------------|----------------------------------------------------------|
| Phone never detects the tag    | NFC off, or wrong spot on the phone. Try slow, top edge. |
| "Tag is read only"             | Someone set the lock bit. It's permanent — grab a new tag. |
| Write fails partway            | Payload too big for the chip. Shorten it / shorten the URL. |
| Reads but nothing happens      | Record type your OS doesn't auto-handle. Use URL or Text. |
| Works on Android, not iOS      | iOS ignores some record types in the background. Use a URI record. |
