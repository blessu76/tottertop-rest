---
slug: 2026-11-15-tuning-the-wobble-with-bots
lang: de
title: "Das Wackeln mit Bots statt mit den Händen abstimmen"
description: "Wie wir den Schwierigkeitsgrad von Tottertop festgelegt haben, bevor es jemand gespielt hatte: drei Bots mit unterschiedlichem Tipp-Timing, je 200 Runden und ein ehrlicher Vorbehalt."
excerpt: "Bevor ein Mensch Tottertop spielen konnte, haben wir den Schwierigkeitsgrad mit drei unterschiedlich geschickten Bots abgestimmt, je 200 Runden. Was die Zahlen sagen und was sie nicht sagen können."
copy_review: iris 2026-11-14
published: 2026-11-15T14:30+09:00
---
Ein Physik-Stapelspiel steht und fällt damit, wie schwer sich das Wackeln anfühlt. Am 11. November, als die erste komplette Rundenschleife lief, hatte es noch niemand gespielt, also haben wir es mit Bots abgestimmt.

## Die Idee

Die Engine ist als reiner Dart-Code geschrieben und läuft mit einem festen Takt von 120 Schritten pro Sekunde, sodass dieselben Eingaben immer denselben Turm ergeben. Dadurch lässt sich leicht ein Bot auf den Platz des Spielers setzen. Unser Bot zielt auf den besten Moment zum Fallenlassen und tippt dann mit einem zufälligen Timing-Fehler, der aus einer Normalverteilung gezogen wird. Ein größerer Fehler steht für eine weniger ruhige Hand.

Wir haben drei gebaut und mit jedem 200 Runden gespielt:

| Bot | Tipp-Fehler | Etagen im Schnitt | 30+ Etagen erreicht |
|---|---|---|---|
| Experte (sagt auch die Neigung voraus) | 30 ms | 29,4 | 48 % |
| Gut | 50 ms | 18,1 | 1,5 % |
| Durchschnittlich | 70 ms | 12,4 | 0 % |

Beim durchschnittlichen Bot endete jede zehnte Runde bis Etage 2, die Hälfte erreichte Etage 14, und neun von zehn endeten bis Etage 20.

## Was wir erreichen wollten

Unser Ziel war einfach: Ein durchschnittlicher Spieler sollte im Schnitt etwa 10 bis 15 Etagen schaffen, und ein sehr guter Spieler sollte über 30 kommen können. Die Tabelle oben liegt genau dort, also haben wir die Werte beibehalten. Wir haben eine Handvoll Zahlen abgestimmt: wie stark sich die Neigung aufbaut, wie hart jede Landung den Turm anstößt und wie schnell das Wackeln abklingt.

## Was uns das nicht verrät

Ein Bot ist kein Mensch. Er wird nie müde, gerät nicht in Panik, wenn der Turm kippt, und kommt nie auf die Idee, etwas Alberes auszuprobieren. Diese Zahlen sagen, dass die Schwierigkeitskurve auf dem Papier sinnvoll ist, nicht, dass sich das Spiel richtig anfühlt. Dafür braucht es echte Hände, und wir prüfen es erneut, wenn Leute die Testversionen spielen.
