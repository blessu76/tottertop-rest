---
slug: 2026-11-16-one-tower-for-everyone
lang: en
title: "One tower for everyone: how the daily seed works"
description: "In the test builds, the daily tower hands every player the same block order on the same day. How a date becomes a tower, and why UTC."
excerpt: "A daily tower only works if everyone really gets the same one. How we turn a date into a block order that is identical on every phone in the world."
copy_review: iris 2026-11-14
published: 2026-11-16T16:30+09:00
---
One idea we wanted early was a daily tower: everyone gets the same blocks in the same order for a day, so a floor count means the same thing for everybody. It sounds simple, and it only works if a few boring details are right.

## A date becomes a seed

The sequence of blocks comes from a seed, and the seed comes from the date. Two phones that start from the same date build the same sequence, with no server in between. We made one exception on purpose: the first block of every tower is always the plain square one, so a round never opens with something awkward.

## Why UTC

If the daily tower followed each phone's local date, a player in Seoul and a player in São Paulo would be on different towers for most of the day. So the date comes from UTC. A new tower appears at the same instant everywhere, which is 9 a.m. in Korea. We wrote tests for the UTC boundary and for the Korean time zone, because that is where "which day is it?" bugs hide.

## Same inputs, same tower

This only holds if the game itself is deterministic. The engine runs on a fixed 120-step-per-second clock and keeps its rules separate from the drawing code, so the sequence of blocks and the physics do not depend on how fast a phone is. In the test builds, the home screen keeps two best scores on the device — one for free play and one for today's tower, which resets when the date changes.

## What we have not done

There is no server, no leaderboard and no way to compare scores with other people yet. For now the daily tower is a shared puzzle you play alone. Whether it grows into more than that is not decided.
