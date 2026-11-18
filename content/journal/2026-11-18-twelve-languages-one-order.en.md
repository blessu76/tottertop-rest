---
slug: 2026-11-18-twelve-languages-one-order
lang: en
title: "Twelve languages, one fixed order"
description: "Tottertop moved from eleven languages to twelve common ones in a fixed order. What changed, what we dropped, and the narrow-screen test that guards it."
excerpt: "Our first post said eleven languages. It is twelve now, in a fixed order, with a language picker and a test that makes every one fit a 320 px screen."
copy_review: iris 2026-11-16
published: 2026-11-18T16:15+09:00
---
Our first post said Tottertop would be available in 11 languages. That number is out of date: on 12 November we moved to a set of 12, and this post explains why the set, and its order, are now fixed.

## What changed

The first version covered English, Korean, Japanese, Chinese, Spanish, French, German, Portuguese, Russian, Arabic and Hindi. The new set is, in this order:

English · Korean · Japanese · Traditional Chinese · Spanish · Brazilian Portuguese · French · German · Indonesian · Thai · Vietnamese · Turkish

Russian, Arabic and Hindi left, Indonesian, Thai, Vietnamese and Turkish arrived, and the two broad labels became specific ones: Traditional Chinese and Brazilian Portuguese. The translations for the new languages are written out in full rather than left as stubs.

## Why the order is fixed

The list lives in a shared kit, so the app and the site use the same languages in the same order. Fixing the order also lets a test check it, so nobody can reshuffle the list by accident.

## A picker that remembers (13 November)

In the app, Settings now has a language option: the device's own language, followed by the twelve. Your choice is saved, and a wrong or unknown saved value falls back to the device language instead of breaking the screen.

## The test that matters most

German and Vietnamese words are long, and Thai has no spaces to break on. So the most useful test we have is dull: every screen, in every one of the 12 languages, is built at a 320 px width, and the test fails if any text overflows. A language that does not fit does not ship.

The site follows the same twelve languages, and so does this journal.
