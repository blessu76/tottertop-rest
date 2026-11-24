---
slug: 2026-11-24-telling-the-blocks-apart
lang: es
title: "Distinguir los bloques: una prueba de daltonismo"
description: "Al añadir conjuntos de colores de bloques a Tottertop, una simulación de daltonismo descubrió dos bloques por defecto casi iguales. Qué medimos y qué cambiamos."
excerpt: "Simulando la ceguera al verde, los bloques azul y morado eran casi idénticos. Cómo lo detectó una prueba de contraste y la regla que ahora debe cumplir cada conjunto."
copy_review: iris 2026-11-20
published: 2026-11-24T14:45+09:00
---
En una torre que se inclina, el color tiene un trabajo de verdad: muestra dónde termina un bloque y dónde empieza el siguiente. Por eso, cuando añadimos conjuntos de colores para los bloques el 15 de noviembre, añadimos también una prueba que comprueba que se sigan distinguiendo bien para quienes tienen alguna alteración en la visión del color.

## Cuatro conjuntos que se desbloquean jugando

Caramelo es el predeterminado. Pastel se abre a los 12 pisos, Océano a los 20 y Atardecer a los 30, las mismas alturas en las que ganas títulos. Cuenta tu mejor altura de siempre, en Juego libre o en la Torre del día, así que los récords anteriores los abren de inmediato. El conjunto se elige en Ajustes, y los mismos colores aparecen en la torre, en la vista previa del siguiente bloque y en la pantalla de inicio.

## Qué hace la prueba

Para cada conjunto, la prueba toma cada color de bloque y simula cómo se ve con los tres tipos principales de daltonismo, en los que cuesta distinguir el rojo, el verde o el azul, en su grado más fuerte, con un modelo publicado (Machado y colaboradores, 2009). Hace lo mismo con la visión típica. Después mide cuánto se separan los colores entre sí, como diferencia de color (CIELAB ΔE).

Las caras de los bloques deben estar al menos a 10 unas de otras. Cada bloque tiene además un borde inferior más oscuro, que debe seguir siendo más oscuro que su cara y estar al menos a 9 de ella y de la cara del bloque de abajo.

## Lo que encontró

Nuestro propio conjunto por defecto no pasó. En la simulación de ceguera al verde, los bloques azul y morado estaban a solo 0,8: prácticamente el mismo color. Movimos los colores de los bloques hasta 12 cada uno, hasta que el par más cercano de Caramelo quedó a 11,5. Solo cambiaron los bloques; los textos y botones del resto del juego conservan sus colores.

El par más cercano de cualquier tipo (caras o bordes) en cada conjunto queda así: Caramelo 11,5, Pastel 10,7, Océano 9,5 y Atardecer 12,3.

## Lo que esto no nos dice

Es un cálculo sobre un modelo de la visión, no una persona mirando un móvil. Todavía no lo hemos comprobado con jugadores daltónicos, y el brillo de la pantalla o la luz del día cambian cómo se ven los colores. Hasta que lo compruebe gente de verdad, lo contamos como no comprobado.
