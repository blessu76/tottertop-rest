---
slug: 2026-11-18-twelve-languages-one-order
lang: es
title: "Doce idiomas, un orden fijo"
description: "Tottertop pasó de once idiomas a doce de uso común, en un orden fijo. Qué cambió, qué dejamos y la prueba de pantalla estrecha que lo protege."
excerpt: "Nuestra primera entrada decía once idiomas. Ahora son doce, en un orden fijo, con selector de idioma y una prueba que hace que cada uno quepa en una pantalla de 320 px."
copy_review: iris 2026-11-16
published: 2026-11-18T16:15+09:00
---
Nuestra primera entrada decía que Tottertop estaría disponible en 11 idiomas. Esa cifra ya no es válida: el 12 de noviembre pasamos a un conjunto de 12, y esta entrada explica por qué el conjunto y su orden ahora son fijos.

## Qué cambió

La primera versión cubría inglés, coreano, japonés, chino, español, francés, alemán, portugués, ruso, árabe y hindi. El nuevo conjunto es, en este orden:

inglés · coreano · japonés · chino tradicional · español · portugués de Brasil · francés · alemán · indonesio · tailandés · vietnamita · turco

Salieron el ruso, el árabe y el hindi, llegaron el indonesio, el tailandés, el vietnamita y el turco, y las dos etiquetas generales pasaron a ser específicas: chino tradicional y portugués de Brasil. Las traducciones de los idiomas nuevos están escritas completas, no como borradores vacíos.

## Por qué el orden es fijo

La lista vive en un kit compartido, así que la app y el sitio usan los mismos idiomas en el mismo orden. Fijar el orden también permite que una prueba lo verifique, de modo que nadie pueda reordenar la lista por accidente.

## Un selector que recuerda (13 de noviembre)

En la app, los Ajustes ahora tienen una opción de idioma: primero el idioma del propio dispositivo y después los doce. Tu elección se guarda, y si el valor guardado es incorrecto o desconocido, se vuelve al idioma del dispositivo en lugar de romper la pantalla.

## La prueba que más importa

Las palabras en alemán y en vietnamita son largas, y el tailandés no tiene espacios donde cortar. Por eso la prueba más útil que tenemos es aburrida: cada pantalla, en cada uno de los 12 idiomas, se construye con un ancho de 320 px, y la prueba falla si algún texto se desborda. Un idioma que no cabe no se publica.

El sitio sigue los mismos doce idiomas, y este diario también.
