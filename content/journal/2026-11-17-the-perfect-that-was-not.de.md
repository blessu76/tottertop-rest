---
slug: 2026-11-17-the-perfect-that-was-not
lang: de
title: "Das „Perfekt“, das keins war: drei Fixes vom ersten Tag"
description: "Am ersten vollen Testabend mit Tottertop tauchten drei Bugs rund um „Perfekt“ und den Rekord auf. Was sie waren und wie wir sie behoben haben."
excerpt: "Ein „Perfekt“ für einen Block, der den Turm umwirft, ein erster Block, der in Etage eins fiel, ein Rekord, der im Einsturz verloren ging: drei Bugs eines Abends."
copy_review: iris 2026-11-14
published: 2026-11-17T14:45+09:00
---
Am 11. November, als es die erste spielbare Version gab, haben wir einen Abend lang gespielt und alles notiert, was sich falsch anfühlte. Drei dieser Punkte waren klein, und jeder hat verändert, wie sich das Spiel anfühlt.

## „Perfekt“, vom falschen Ort aus gemessen

Landet ein Block fast genau in der Mitte, zeigt das Spiel „Perfekt“ und führt deine Serie fort. Unsere erste Prüfung maß die Abweichung von der Mitte der Kontaktfläche. Ein Block, der vollständig auf seiner Basis aufliegt, hat dort immer die Abweichung null, also war der allererste Block „Perfekt“, egal wo er landete. Schlimmer noch: Landete er mehr als etwa ein Fünftel Blockbreite neben der Mitte, kippte der Turm, und der Bildschirm zeigte gleichzeitig „Perfekt!“ und „Der Turm ist in Etage 1 eingestürzt“. Jetzt beurteilen wir es von der Mitte der Fläche aus, auf der der Block landet.

## „Perfekt“ für einen Turm, der trotzdem fällt

Auch nach dem Fix konnte ein Block in der Mitte der Oberseite im selben Augenblick den ganzen Turm zum Einsturz bringen, weil der gemeinsame Schwerpunkt über die untere Fuge hinausgewandert war. In 127 von 300 simulierten Skriptspielen erschienen „Perfekt“ und Einsturz zusammen. Eine Landung, die nicht halten kann, bekommt jetzt nie mehr ein „Perfekt“.

Auch der erste Block wurde geändert: Er setzt sich jetzt auf seine Basis und wird zum Bezugspunkt für die Neigung, sodass er den Turm nicht allein umwerfen kann. In unseren Bot-Simulationen stieg der Durchschnitt eines typischen Spielers von 12,4 auf 15,9 Etagen, und Spiele, die in Etage vier oder früher endeten, sanken von 48 auf 11 von 200.

## Der Rekord, der nicht gespeichert wurde

Der Einsturz ist absichtlich langsam: Die erste Sekunde läuft mit 0,45-facher Geschwindigkeit, damit man sieht, was passiert ist. Der Rekord wurde aber erst im Ergebnisbildschirm geschrieben, etwa 1,6 Sekunden später; wer mitten in der Animation ging, verlor ihn. Jetzt wird er gespeichert, sobald der Einsturz feststeht.

## Warum wir das aufschreiben

Keiner dieser drei Fehler ist raffiniert. Jeder ist eine Stelle, an der das Spiel dem Spieler etwas Unwahres sagte, und man findet sie nur durchs Spielen. Das wollen wir weiter tun.
