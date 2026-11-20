---
slug: 2026-11-20-what-we-test-first
lang: en
title: "What we test before anything ships"
description: "A short tour of the checks Tottertop goes through before a build leaves the desk: unit tests, a 320 px layout test in 12 languages, bot runs, and what only a real phone can tell us."
excerpt: "Nearly 700 automated tests, a layout check in every language, and bot players. And the list of things no test can settle."
copy_review: iris 2026-11-16
published: 2026-11-20T14:30+09:00
---
A small game still needs a lot of dull checking. Here is what stands between a change and a test build, and where that checking stops.

## A gate before every commit

Every change passes one script that formats the code, analyzes it and runs the tests. If it is not green, nothing is committed and no build is made. At the time of writing the app has close to 700 automated tests, covering the rules of the game, the daily tower, saving and loading, the settings and the languages.

## Every language, narrow screen

German and Vietnamese words are long, and Thai has no spaces to break on. So the layout test builds every screen in all 12 languages at a width of 320 px and fails if any text overflows. The website goes through the same kind of check at 320 and 375 px, and again at tablet and desktop widths.

## Bots that play for us

To tune difficulty we do not rely on our own thumbs. Simulated players of several skill levels play hundreds of rounds, and we compare how far they get. That is how we could say that one fix raised the average of a mid-skill player from 12.4 to 15.9 floors, and cut rounds that ended at floor four or below from 48 out of 200 to 11. Bots tell us about balance. They do not tell us whether the game is fun.

## What no test can settle

A real phone still has the last word on sound, vibration, touch feel and how the game looks in daylight. Those checks are done by hand on devices, and until they are done we mark them as unchecked instead of calling them fine. If this journal says something is verified, it was. If it does not say, assume it was not.
