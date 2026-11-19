---
slug: 2026-11-19-the-silent-switch
lang: de
title: "Ton an, nichts zu hören: der Stummschalter am iPhone"
description: "Der Ton in den Tottertop-Einstellungen blieb bei eingeschaltetem Stummschalter am iPhone aus. Was die Ursache war, was wir geändert haben und was auf echten Geräten noch ungeprüft ist."
excerpt: "Die Einstellung war an, der Codepfad in Ordnung, und das Spiel blieb trotzdem stumm. Schuld war ein einziger Audiomodus, der dem Stummschalter gehorcht."
copy_review: iris 2026-11-16
published: 2026-11-19T14:30+09:00
---
Beim Prüfen der Ton- und Vibrationseinstellungen sind wir auf ein Problem gestoßen, das wie ein Fehler in der Einstellung aussieht, aber keiner ist: Man konnte den Ton einschalten und hörte trotzdem nichts.

## Der Codepfad war in Ordnung

Wir haben jeden Schalter vom Einstellungsbildschirm bis zu dem Moment verfolgt, in dem ein Ton oder eine Vibration angefordert wird: den gespeicherten Wert, die Stelle, an der er wieder gelesen wird, die Schranke, die einen Ton überspringt, wenn die Einstellung aus ist, und jedes Spielereignis, das Rückmeldung verlangt. Alles hing zusammen. Die fünf Tondateien waren vorhanden, und die gespeicherten Schlüssel stimmten.

## Die Ursache: ein höflicher Audiomodus

Auf dem iPhone entscheidet die Art, wie eine App ihr Audio deklariert, ob sie dem Stummschalter gehorcht. Unser Spiel nutzte den höflichen Modus, der für Hintergrundklänge gedacht ist, und dieser Modus folgt dem Stummschalter und der Bildschirmsperre. Bei eingeschaltetem Schalter sagte die Einstellung also „an“, und das Telefon blieb leise.

## Was wir geändert haben

- Auf dem iPhone nutzt das Spiel jetzt den Wiedergabemodus, sodass der Stummschalter die Spieltöne nicht mehr stummschaltet. Es mischt sich weiterhin mit anderen Apps, die Musik, die du schon gehört hast, läuft also weiter.
- Auf Android werden Töne als Spieltöne gekennzeichnet und beanspruchen nicht den Audiofokus.
- Wenn du Vibration oder Ton einschaltest, gibt es jetzt sofort eine kurze Vibration bzw. einen kurzen Ton, damit du weißt, dass es funktioniert. Beim Ausschalten bleibt es still.
- Android bekommt die Vibrationsberechtigung ausdrücklich.
- Tests decken den Audiomodus, das einmalige Signal beim Einschalten und die Berechtigung ab.

## Was wir nicht geprüft haben

All das ist in Code und Tests belegt, aber noch nicht auf echten Telefonen. Wir müssen noch bestätigen, dass auf einem iPhone mit eingeschaltetem Stummschalter der Ton spielt, dass die Musik einer anderen App weiterläuft und dass die Vibration ankommt. Auch die systemeigene Haptik-Einstellung des Telefons oder der Energiesparmodus kann die Vibration unterdrücken, und darauf haben wir keinen Einfluss. Wir prüfen das im nächsten Testbuild und schreiben auf, was wir finden.
