# Example: trigger a Flow macro

This is the one that makes the tag more than a fancy QR code. A tap becomes an action on your machine — launch an app, run a script, flip lights, start a pomodoro — routed through your [Flow](https://flowworld.xyz) device.

## The idea

The tag carries a **custom URI** that means nothing to a stock phone but everything to a handler you control. You register the handler once; after that, every tap fires the macro.

```
tap tag  →  phone reads URI  →  handler catches scheme  →  Flow runs macro
```

## Option A — custom URI scheme (phone-driven)

Write a URI record with your own scheme:

```
flow://macro/deep-work
```

- **Android:** register an intent filter for the `flow://` scheme (or use an automation app like Tasker/Macrodroid to catch it and hit Flow's local endpoint).
- **iOS:** register a URL scheme in a companion Shortcut; the Shortcut calls Flow.

Write it: NFC Tools → **Add a record → Custom URL/URI** → `flow://macro/deep-work` → **Write**.

## Option B — external NDEF type (handler-driven)

Cleaner if you own the handler end-to-end. Use TNF `0x4`, type `flowworld.xyz:macro`, payload = the macro id:

```
Type:    flowworld.xyz:macro
Payload: deep-work
```

Stock phones ignore it; your Flow-aware handler claims the type and dispatches. Raw byte format is in [../docs/ndef-spec.md](../docs/ndef-spec.md) under "External / custom records."

## Option C — local HTTP endpoint (no scheme registration)

If Flow exposes a small HTTP endpoint on your LAN, skip schemes entirely and write a plain URL:

```
http://flow.local:8080/macro/deep-work
```

Tap → phone opens the URL → Flow's endpoint runs the macro → returns 200. Dead simple, works on every phone, no handler install. Downside: only fires when you're on the same network as your Flow.

## Macro ideas people actually run

- `deep-work` → mute Slack, open editor, start 50-min timer
- `standup` → open the call, set status, dim the desk lamp
- `leaving` → lock the machine, pause music, arm the camera
- `demo` → launch the exact app + window layout for a screen-share

The tag is dumb and cheap on purpose. Flow is where the logic lives. Build your macros at [flowworld.xyz](https://flowworld.xyz).
