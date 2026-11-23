---
slug: 2026-11-23-iphone-first-icloud
lang: en
title: "iPhone first, and what iCloud sync does"
description: "Tottertop is planned for iPhone only at first. Your progress can follow you between devices on one Apple ID through iCloud, while settings stay on each device."
excerpt: "iPhone only at first, and progress that follows you between phones. What syncs and what does not."
copy_review: iris 2026-11-19
published: 2026-11-23T17:30+09:00
---
Two small decisions that belong together: which devices come first, and how your progress moves between them.

## iPhone only, for now

The project could be built for both iPhone and iPad. On November 16 we decided to start with iPhone only. The iPad screenshots were already taken, and we are keeping them in case iPad comes later. One reason to wait: some screens, such as the block colors list, looked mostly empty on a large iPad display.

## What syncs

Your progress: best heights, stats, titles, streaks, achievements and the calendar. It moves between devices signed in to the same Apple ID, using iCloud key-value storage, a small store that Apple keeps for the app. It is not CloudKit, and we run no account system.

## What does not sync

Settings stay on each device, so changing sound or vibration on one phone does not change another. If a device is not signed in to iCloud, the game still works fully; its progress just stays on that device.

## What this does not say

Sync is not an account or a profile, and nothing here is a release date. The game is still in preparation.
