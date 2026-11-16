---
slug: 2026-11-16-one-tower-for-everyone
lang: de
title: "Ein Turm für alle: So funktioniert der tägliche Seed"
description: "In den Testversionen gibt der tägliche Turm allen Spielern am selben Tag dieselbe Blockreihenfolge. Wie aus einem Datum ein Turm wird und warum UTC."
excerpt: "Ein täglicher Turm funktioniert nur, wenn wirklich alle denselben bekommen. Wie wir ein Datum in eine Blockreihenfolge verwandeln, die auf jedem Handy der Welt identisch ist."
copy_review: iris 2026-11-14
published: 2026-11-16T16:30+09:00
---
Eine Idee, die wir früh haben wollten, war der tägliche Turm: Einen Tag lang bekommen alle dieselben Blöcke in derselben Reihenfolge, sodass eine Stockwerkzahl für alle dasselbe bedeutet. Das klingt einfach, und es funktioniert nur, wenn ein paar langweilige Details stimmen.

## Aus einem Datum wird ein Seed

Die Blockfolge stammt aus einem Seed, und der Seed stammt aus dem Datum. Zwei Handys, die vom selben Datum ausgehen, bauen dieselbe Folge, ganz ohne Server dazwischen. Eine Ausnahme haben wir bewusst gemacht: Der erste Block jedes Turms ist immer der schlichte quadratische, damit eine Runde nie mit etwas Unbequemem beginnt.

## Warum UTC

Würde der tägliche Turm dem lokalen Datum jedes Handys folgen, wären ein Spieler in Seoul und ein Spieler in São Paulo den größten Teil des Tages auf verschiedenen Türmen. Deshalb kommt das Datum aus UTC. Ein neuer Turm erscheint überall im selben Moment, in Korea um 9 Uhr morgens. Wir haben Tests für die UTC-Grenze und für die koreanische Zeitzone geschrieben, denn dort verstecken sich die „Welcher Tag ist heute?“-Fehler.

## Gleiche Eingaben, gleicher Turm

Das gilt nur, wenn das Spiel selbst deterministisch ist. Die Engine läuft mit einem festen Takt von 120 Schritten pro Sekunde und hält ihre Regeln vom Zeichencode getrennt, sodass Blockfolge und Physik nicht davon abhängen, wie schnell ein Handy ist. In den Testversionen speichert der Startbildschirm zwei Bestwerte auf dem Gerät: einen für das freie Spiel und einen für den heutigen Turm, der zurückgesetzt wird, wenn sich das Datum ändert.

## Was wir noch nicht getan haben

Es gibt noch keinen Server, keine Bestenliste und keine Möglichkeit, Punktzahlen mit anderen zu vergleichen. Vorerst ist der tägliche Turm ein gemeinsames Rätsel, das man allein spielt. Ob daraus mehr wird, ist nicht entschieden.
