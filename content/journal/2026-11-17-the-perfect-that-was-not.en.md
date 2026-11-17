---
slug: 2026-11-17-the-perfect-that-was-not
lang: en
title: "The “Perfect” that was not: three fixes from day one"
description: "On the first full evening of testing Tottertop, three bugs showed up around the “Perfect” landing and the record. What they were and how we fixed them."
excerpt: "A “Perfect” on a block that topples the tower, a first block that fell on floor one, a best score lost mid-collapse: three bugs from one evening."
copy_review: iris 2026-11-14
published: 2026-11-17T14:45+09:00
---
On 11 November, once the first playable version existed, we spent an evening playing it and writing down everything that felt wrong. Three of the items were small, and each one changed how the game feels.

## “Perfect” measured from the wrong place

When a block lands close to dead centre, the game shows “Perfect” and keeps your streak going. Our first check measured the offset from the centre of the contact area. A block resting fully on its base always has an offset of zero there, so the very first block was “Perfect” wherever it landed. Worse, if it landed more than about a fifth of a block from the middle, the tower tipped over — and the screen showed “Perfect!” and “The tower collapsed on floor 1” at the same time. We now judge it from the centre of the surface the block lands on.

## “Perfect” for a tower that falls anyway

Even with the fix, a block placed in the middle of the top could still bring the whole tower down in the same instant, because the combined weight had moved past the joint below. In 127 of 300 simulated scripted games it showed “Perfect” and a collapse together. A landing that cannot hold now never earns a “Perfect”.

The first block was also changed: it now settles onto its base and becomes the reference point for the tilt, so it cannot topple the tower by itself. In our bot simulations, a typical player's average rose from 12.4 to 15.9 floors, and games that ended on floor four or earlier dropped from 48 to 11 out of 200.

## The best score that did not get saved

The collapse is slow on purpose: the first second plays at 0.45× speed so you can see what happened. But the best score was only written on the result screen, about 1.6 seconds later, so leaving mid-animation lost it. Now it is saved the moment the collapse is certain.

## Why we write this down

None of these three are clever. Each is a place where the game told the player something that was not true, and you only find them by playing. We plan to keep doing that.
