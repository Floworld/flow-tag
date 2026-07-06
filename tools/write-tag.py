#!/usr/bin/env python3
"""
write-tag.py — flash a flow-tag from your laptop.

The tag is open. So is this. Point a PN532/PN53x or RC-S380 reader at a tag and
overwrite it with whatever record you want. No cloud, no account, no flow-tag
runtime — just NDEF onto an NTAG21x.

Dependencies:
    pip install nfcpy ndeflib

Examples:
    # open a URL on tap
    python3 write-tag.py --url "https://floworld.xyz"

    # plain text
    python3 write-tag.py --text "hack the planet"

    # trigger a Flow macro via custom scheme
    python3 write-tag.py --url "flow://macro/deep-work"

    # reset to the shipped default
    python3 write-tag.py --reset

    # read what's currently on the tag
    python3 write-tag.py --read

Tested with a €8 PN532 USB reader. See ../docs/install.md for setup.
"""

import argparse
import sys

DEFAULT_URL = "https://floworld.xyz"

try:
    import nfc
    import ndef
except ImportError:
    sys.exit("Missing deps. Run:  pip install nfcpy ndeflib")


def build_records(args):
    if args.reset:
        return [ndef.UriRecord(DEFAULT_URL)]
    if args.url:
        return [ndef.UriRecord(args.url)]
    if args.text:
        return [ndef.TextRecord(args.text)]
    return None


def main():
    p = argparse.ArgumentParser(description="Flash a flow-tag (NTAG21x) over NFC.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", help="write a URI record (http, https, flow://, tel:, mailto:, ...)")
    g.add_argument("--text", help="write a plain text record")
    g.add_argument("--reset", action="store_true", help="restore the shipped default")
    g.add_argument("--read", action="store_true", help="dump the tag's current records and exit")
    p.add_argument("--device", default="usb", help="nfcpy device path (default: usb)")
    args = p.parse_args()

    records = build_records(args)

    def on_connect(tag):
        if not tag.ndef:
            print("This tag isn't NDEF-formatted. Format it with your phone app first.")
            return True

        if args.read:
            if tag.ndef.records:
                for i, r in enumerate(tag.ndef.records):
                    print(f"[{i}] {r}")
            else:
                print("(tag is NDEF-formatted but empty)")
            return True

        if not tag.ndef.is_writeable:
            print("Tag is read-only (lock bit set). Nothing I can do — grab a fresh tag.")
            return True

        cap = tag.ndef.capacity
        payload_len = sum(len(bytes(r)) for r in records)
        if payload_len > cap:
            print(f"Payload {payload_len} B > tag capacity {cap} B. Shorten it or use a bigger NTAG.")
            return True

        tag.ndef.records = records
        print("written:")
        for r in tag.ndef.records:
            print("  ", r)
        return True

    print(f"Hold a tag to the reader ({args.device})…  Ctrl-C to quit.")
    try:
        clf = nfc.ContactlessFrontend(args.device)
    except IOError:
        sys.exit(f"No reader found at '{args.device}'. Check the connection / try --device usb:001:xxx")

    try:
        clf.connect(rdwr={"on-connect": on_connect})
    except KeyboardInterrupt:
        pass
    finally:
        clf.close()


if __name__ == "__main__":
    main()
