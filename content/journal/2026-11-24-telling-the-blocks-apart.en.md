---
slug: 2026-11-24-telling-the-blocks-apart
lang: en
title: "Telling the blocks apart: a color-blind check"
description: "When block color sets arrived in Tottertop, a color-blindness simulation found two default blocks that looked almost the same. What we measured and what we changed."
excerpt: "In a simulation of green color blindness, the blue and purple blocks were nearly identical. How a contrast test caught it, and the rule every block color set now has to pass."
copy_review: iris 2026-11-20
published: 2026-11-24T14:45+09:00
---
On a leaning tower, color does real work: it shows where one block ends and the next one begins. So when we added block color sets on November 15, we also added a test that checks the blocks stay easy to tell apart for players with color vision deficiency.

## Four sets, unlocked by playing

Candy is the default. Pastel opens at 12 floors, Ocean at 20 and Sunset at 30, the same heights at which you earn titles. What counts is your best height ever, in free play or today's tower, so earlier records open them straight away. You choose a set in Settings, and the same colors appear on the tower, in the next-block preview and on the home screen.

## What the test does

For every set, the test takes each block color and simulates how it looks with the three main kinds of color blindness, where red, green or blue is hard to tell apart, at full strength, using a published model (Machado and colleagues, 2009). It does the same for typical vision. Then it measures how far apart the colors are, as a color difference (CIELAB ΔE).

The block faces must be at least 10 apart from one another. Each block also has a darker lower edge, which must stay darker than its face and at least 9 away from it and from the face of the block below.

## What it caught

Our own default set failed. In the simulation of green color blindness, the blue and purple blocks were only 0.8 apart, which is practically the same color. We moved the block colors by up to 12 each, until the closest pair in Candy was 11.5 apart. Only the blocks changed; text and buttons in the rest of the game kept their colors.

The closest pair of any kind (faces or edges) in each set is now: Candy 11.5, Pastel 10.7, Ocean 9.5 and Sunset 12.3.

## What this does not tell us

This is a calculation on a model of vision, not a person looking at a phone. It has not been checked with color-blind players, and screen brightness and daylight change how colors look. Until people have checked it, we count it as not checked.
