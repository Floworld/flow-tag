# Example: join Wi-Fi on tap

Stick this on the fridge. Guests tap, phone offers to join, nobody reads a password off a Post-it again.

## App way

1. NFC Tools → **Write → Add a record → Wi-Fi network**.
2. Fill in **SSID**, **password**, **encryption** (usually WPA2-PSK).
3. **Write**, hold to tag.

Needs NTAG215 or 216 — the Wi-Fi record is bigger than NTAG213's 137 bytes once the SSID and key are in.

## What the record is

TNF `0x2` (MIME), type `application/vnd.wfa.wsc` — the Wi-Fi Simple Config blob. It packs SSID, auth type, encryption type and the pre-shared key into a nested TLV structure. Most writer apps build it for you; if you want to hand-roll it, `ndeflib` has a `WifiSimpleConfigRecord` helper.

## Platform reality check

- **Android:** full support, taps straight into "Connect to network?".
- **iOS:** Apple doesn't auto-join from a raw WSC record. Fallback that *does* work on both: encode a text/URI record with a QR-style string `WIFI:S:MySSID;T:WPA;P:mypassword;;` — some apps parse it, and it's trivially human-readable. For guaranteed iOS onboarding, pair the tag with a Wi-Fi QR code.

## Security note

The password sits on the tag in the clear. Anyone who can tap it can read it. That's fine for a guest network; don't put your main network's key on a sticker by the front door.
