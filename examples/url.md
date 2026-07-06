# Example: open a URL

The simplest and most portable payload. Works on every phone, no app needed.

## App way (30 seconds)

1. NFC Tools → **Write → Add a record → URL / URI**.
2. Type your link, e.g. `https://floworld.xyz`.
3. **Write**, hold to tag.

## Raw NDEF

For `https://floworld.xyz` (see [../docs/ndef-spec.md](../docs/ndef-spec.md) for the breakdown):

```
03 11 D1 01 0D 55 04 66 6C 6F 77 6F 72 6C 64 2E 78 79 7A FE
```

## Scripted (nfcpy)

```python
import nfc, ndef
def w(tag):
    tag.ndef.records = [ndef.UriRecord("https://floworld.xyz")]
    return True
nfc.ContactlessFrontend('usb').connect(rdwr={'on-connect': w})
```

## Notes

- Use `https://` — iOS is pickier about plain `http`.
- Deep links work: `spotify://`, `mailto:you@x.com`, `tel:+49...`, `geo:52.5,13.4`.
- Long URL blowing past NTAG213's 137 bytes? Shorten it or move up to NTAG215.
