---
slug: 2026-11-19-the-silent-switch
lang: en
title: "Sound switched on, nothing heard: the iPhone silent switch"
description: "Turning on sound in Tottertop's settings did nothing on an iPhone with the silent switch on. What caused it, what we changed, and what is still unchecked on real devices."
excerpt: "The setting was on, the code path was fine, and the game was still silent. The cause was one audio mode that obeys the silent switch."
copy_review: iris 2026-11-16
published: 2026-11-19T14:30+09:00
---
While checking the sound and vibration settings, we found a problem that looks like a bug in the setting but is not: you could switch sound on and still hear nothing.

## The code path was fine

We followed each toggle from the Settings screen to the moment a sound or a vibration is requested: the saved value, the place it is read back, the gate that skips a sound when the setting is off, and every game event that asks for feedback. All of it connected. The five sound files were present and the saved keys matched.

## The cause: a polite audio mode

On iPhone, the way an app declares its audio decides whether it obeys the silent switch. Our game used the polite mode meant for background ambience, and that mode follows the silent switch and the screen lock. So with the switch on, the setting said "on" and the phone stayed quiet.

## What we changed

- On iPhone the game now uses the playback mode, so the silent switch no longer mutes game sounds. It still mixes with other apps, so music you were already playing keeps going.
- On Android, sounds are marked as game sounds and do not grab audio focus.
- Turning vibration or sound on now gives you one short vibration or sound at once, so you know it works. Turning it off stays quiet.
- Android gets the vibration permission explicitly.
- Tests cover the audio mode, the one-time cue on switching on, and the permission.

## What we have not checked

All of this is verified in code and tests, not yet on real phones. We still need to confirm, on an iPhone with the silent switch on, that sound plays; that music from another app keeps playing; and that vibration arrives. The phone's own system haptics setting or low-power mode can also silence vibration, and that is outside our control. We will check these in the next test build and write down what we find.
