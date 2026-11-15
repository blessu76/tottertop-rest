---
slug: 2026-11-15-tuning-the-wobble-with-bots
lang: en
title: "Tuning the wobble with bots instead of hands"
description: "How we set Tottertop's difficulty before anyone had played it: three bots with different tap timing, 200 rounds each, and an honest caveat."
excerpt: "Before a human could play Tottertop, we tuned its difficulty with three bots of different skill, 200 rounds each. What the numbers said, and what they cannot say."
copy_review: iris 2026-11-14
published: 2026-11-15T14:30+09:00
---
A physics stacker lives or dies on how hard the wobble feels. On 11 November, when the first full round loop worked, nobody had played it yet — so we tuned it with bots.

## The idea

The engine is written as plain Dart code that runs on a fixed 120-step-per-second clock, so the same inputs always produce the same tower. That makes it easy to put a bot in the player's seat. Our bot aims for the best moment to drop, then taps with a random timing error drawn from a normal distribution. A bigger error stands for a less steady hand.

We made three of them and ran 200 rounds each:

| Bot | Tap error | Average floors | Reached 30+ floors |
|---|---|---|---|
| Expert (also predicts the lean) | 30 ms | 29.4 | 48% |
| Good | 50 ms | 18.1 | 1.5% |
| Typical | 70 ms | 12.4 | 0% |

For the typical bot, a tenth of rounds ended by floor 2, half reached 14, and nine in ten ended by floor 20.

## What we were aiming for

Our target was simple: a typical player should average somewhere around 10 to 15 floors, and a very good player should be able to push past 30. The table above lands there, so we kept the values. We tuned a handful of numbers for how strongly the lean builds up, how hard each landing kicks the tower, and how quickly the wobble settles.

## What this does not tell us

A bot is not a person. It never gets tired, never panics when the tower tips, and never decides to try something silly. These numbers say the difficulty curve is sensible on paper — they do not say the game feels right. That part needs real hands, and we will check it again when people play the test builds.
