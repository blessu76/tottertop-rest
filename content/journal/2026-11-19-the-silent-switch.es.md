---
slug: 2026-11-19-the-silent-switch
lang: es
title: "Sonido activado y silencio: el interruptor del iPhone"
description: "Activar el sonido en los ajustes de Tottertop no hacía nada en un iPhone con el interruptor de silencio puesto. Qué lo causaba, qué cambiamos y qué falta por comprobar en dispositivos reales."
excerpt: "El ajuste estaba activado, el código estaba bien y el juego seguía en silencio. La causa era un modo de audio que obedece al interruptor de silencio."
copy_review: iris 2026-11-16
published: 2026-11-19T14:30+09:00
---
Mientras revisábamos los ajustes de sonido y vibración, encontramos un problema que parece un error del ajuste pero no lo es: podías activar el sonido y aun así no oír nada.

## El camino del código estaba bien

Seguimos cada interruptor desde la pantalla de Ajustes hasta el momento en que se pide un sonido o una vibración: el valor guardado, el lugar donde se vuelve a leer, la compuerta que omite un sonido cuando el ajuste está desactivado y cada evento del juego que pide respuesta. Todo estaba conectado. Los cinco archivos de sonido estaban presentes y las claves guardadas coincidían.

## La causa: un modo de audio educado

En el iPhone, la forma en que una app declara su audio decide si obedece al interruptor de silencio. Nuestro juego usaba el modo educado pensado para ambientación de fondo, y ese modo sigue al interruptor de silencio y al bloqueo de pantalla. Así que, con el interruptor puesto, el ajuste decía «activado» y el teléfono seguía callado.

## Qué cambiamos

- En iPhone, el juego ahora usa el modo de reproducción, de modo que el interruptor de silencio ya no silencia los sonidos del juego. Sigue mezclándose con otras apps, así que la música que ya estabas escuchando continúa.
- En Android, los sonidos se marcan como sonidos de juego y no toman el foco de audio.
- Al activar la vibración o el sonido, ahora recibes de inmediato una vibración o un sonido breve, para que sepas que funciona. Al desactivarlos, no pasa nada.
- Android recibe el permiso de vibración de forma explícita.
- Hay pruebas para el modo de audio, la señal única al activar y el permiso.

## Qué no hemos comprobado

Todo esto está verificado en el código y en pruebas, pero todavía no en teléfonos reales. Aún tenemos que confirmar, en un iPhone con el interruptor de silencio puesto, que el sonido suena; que la música de otra app sigue sonando; y que la vibración llega. El ajuste háptico del propio sistema o el modo de bajo consumo también pueden silenciar la vibración, y eso queda fuera de nuestro control. Lo comprobaremos en la próxima versión de prueba y anotaremos lo que encontremos.
