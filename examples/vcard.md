# Example: share your contact card

Tap to drop your details into someone's phone. The upgrade from paper business cards.

## The vCard

```vcf
BEGIN:VCARD
VERSION:3.0
FN:Ada Lovelace
ORG:Flow
TITLE:Firmware
EMAIL:ada@flowworld.xyz
URL:https://flowworld.xyz
END:VCARD
```

## Writing it

1. NFC Tools → **Write → Add a record → Contact** (or **Custom → MIME**, type `text/vcard`).
2. Paste the vCard above, edited for you.
3. **Write**, hold to tag.

Record type is TNF `0x2` (MIME), `text/vcard`. A full vCard runs 150-400 bytes, so use **NTAG215/216** — NTAG213 will overflow with anything beyond a name and email.

## Keep it lean

Every field costs bytes. Photos (`PHOTO;ENCODING=b`) will blow the budget instantly — link to an image URL instead. If you want the fancy card, put a URL record on the tag pointing at a hosted vCard or your site, and let the web do the heavy lifting.
