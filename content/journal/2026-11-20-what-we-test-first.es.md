---
slug: 2026-11-20-what-we-test-first
lang: es
title: "Qué probamos antes de que algo salga"
description: "Las comprobaciones de una versión de Tottertop antes de salir: pruebas unitarias, diseño a 320 px en 12 idiomas, bots y lo que solo un teléfono real puede decirnos."
excerpt: "Casi 700 pruebas automáticas, una comprobación de diseño en cada idioma y jugadores bot. Y la lista de lo que ninguna prueba puede resolver."
copy_review: iris 2026-11-16
published: 2026-11-20T14:30+09:00
---
Un juego pequeño también necesita mucha comprobación aburrida. Esto es lo que hay entre un cambio y una versión de prueba, y dónde se detiene esa comprobación.

## Una compuerta antes de cada commit

Todo cambio pasa por un único script que da formato al código, lo analiza y ejecuta las pruebas. Si no está en verde, no se hace commit ni se genera ninguna versión. En el momento de escribir esto, la app tiene cerca de 700 pruebas automáticas que cubren las reglas del juego, la torre diaria, guardar y cargar, los ajustes y los idiomas.

## Cada idioma, pantalla estrecha

Las palabras en alemán y en vietnamita son largas, y el tailandés no tiene espacios donde cortar. Por eso la prueba de diseño construye cada pantalla en los 12 idiomas con un ancho de 320 px y falla si algún texto se desborda. El sitio web pasa por el mismo tipo de comprobación a 320 y 375 px, y de nuevo en anchos de tableta y de escritorio.

## Bots que juegan por nosotros

Para ajustar la dificultad no confiamos en nuestros propios pulgares. Jugadores simulados de varios niveles de habilidad juegan cientos de partidas, y comparamos hasta dónde llegan. Así pudimos decir que una corrección subió el promedio de un jugador de nivel medio de 12,4 a 15,9 pisos, y redujo las partidas que terminaban en el piso cuatro o antes de 48 de 200 a 11. Los bots nos hablan del equilibrio. No nos dicen si el juego es divertido.

## Lo que ninguna prueba puede resolver

Un teléfono real sigue teniendo la última palabra sobre el sonido, la vibración, la sensación al tocar y cómo se ve el juego a la luz del día. Esas comprobaciones se hacen a mano en dispositivos, y hasta que se hacen las marcamos como no comprobadas en lugar de darlas por buenas. Si este diario dice que algo está verificado, lo está. Si no dice nada, da por hecho que no se verificó.
