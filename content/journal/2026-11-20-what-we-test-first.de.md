---
slug: 2026-11-20-what-we-test-first
lang: de
title: "Was wir testen, bevor irgendetwas erscheint"
description: "Die Prüfungen, die ein Tottertop-Build durchläuft: Unit-Tests, ein 320-px-Layouttest in 12 Sprachen, Bot-Läufe und was nur ein echtes Telefon verrät."
excerpt: "Fast 700 automatische Tests, eine Layoutprüfung in jeder Sprache und Bot-Spieler. Dazu die Liste dessen, was kein Test klären kann."
copy_review: iris 2026-11-16
published: 2026-11-20T14:30+09:00
---
Auch ein kleines Spiel braucht viel langweiliges Prüfen. Hier steht, was zwischen einer Änderung und einem Testbuild liegt und wo dieses Prüfen endet.

## Eine Schranke vor jedem Commit

Jede Änderung durchläuft ein einziges Skript, das den Code formatiert, analysiert und die Tests ausführt. Ist es nicht grün, wird nichts committet und kein Build erstellt. Zum Zeitpunkt dieses Beitrags hat die App fast 700 automatische Tests, die die Spielregeln, den täglichen Turm, Speichern und Laden, die Einstellungen und die Sprachen abdecken.

## Jede Sprache, schmaler Bildschirm

Deutsche und vietnamesische Wörter sind lang, und Thai hat keine Leerzeichen, an denen man umbrechen könnte. Darum baut der Layouttest jeden Bildschirm in allen 12 Sprachen mit 320 px Breite auf und schlägt fehl, sobald ein Text überläuft. Die Website durchläuft dieselbe Art von Prüfung bei 320 und 375 px, danach noch einmal bei Tablet- und Desktop-Breiten.

## Bots, die für uns spielen

Um den Schwierigkeitsgrad abzustimmen, verlassen wir uns nicht auf unsere eigenen Daumen. Simulierte Spieler mit verschiedenen Fähigkeitsstufen spielen Hunderte Runden, und wir vergleichen, wie weit sie kommen. So konnten wir sagen, dass eine Korrektur den Durchschnitt eines Spielers mittlerer Stärke von 12,4 auf 15,9 Etagen angehoben hat und die Runden, die in Etage vier oder darunter endeten, von 48 von 200 auf 11 gesenkt hat. Bots sagen uns etwas über die Balance. Ob das Spiel Spaß macht, sagen sie uns nicht.

## Was kein Test klären kann

Bei Ton, Vibration, Gefühl beim Berühren und beim Aussehen des Spiels im Tageslicht hat weiterhin ein echtes Telefon das letzte Wort. Diese Prüfungen machen wir von Hand auf Geräten, und solange sie nicht erledigt sind, markieren wir sie als ungeprüft, statt sie für in Ordnung zu erklären. Wenn dieses Journal sagt, etwas sei geprüft, dann war es das. Wenn es nichts sagt, geh davon aus, dass es nicht geprüft wurde.
