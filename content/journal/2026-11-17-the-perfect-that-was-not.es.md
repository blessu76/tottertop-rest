---
slug: 2026-11-17-the-perfect-that-was-not
lang: es
title: "El «Perfecto» que no lo era: tres arreglos del primer día"
description: "En la primera noche completa de pruebas de Tottertop aparecieron tres errores en torno al «Perfecto» y al récord. Qué eran y cómo los arreglamos."
excerpt: "Un «Perfecto» en un bloque que derriba la torre, un primer bloque que cayó en el piso uno, un récord perdido en pleno derrumbe: tres errores de una noche."
copy_review: iris 2026-11-14
published: 2026-11-17T14:45+09:00
---
El 11 de noviembre, cuando existió la primera versión jugable, dedicamos una noche a jugarla y a anotar todo lo que se sentía raro. Tres de esas cosas eran pequeñas, y cada una cambió cómo se siente el juego.

## Un «Perfecto» medido desde el sitio equivocado

Cuando un bloque cae casi en el centro exacto, el juego muestra «Perfecto» y mantiene tu racha. Nuestra primera comprobación medía el desvío desde el centro de la zona de contacto. Un bloque que descansa por completo sobre su base siempre tiene ahí un desvío de cero, así que el primer bloque era «Perfecto» cayera donde cayera. Peor aún: si caía a más de una quinta parte de bloque del centro, la torre se venía abajo, y la pantalla mostraba a la vez «¡Perfecto!» y «La torre se derrumbó en el piso 1». Ahora lo juzgamos desde el centro de la superficie sobre la que aterriza el bloque.

## «Perfecto» para una torre que se cae igualmente

Incluso con ese arreglo, un bloque colocado en el medio de la parte superior podía derribar toda la torre en el mismo instante, porque el peso combinado ya había pasado de la junta inferior. En 127 de 300 partidas simuladas con guion se mostraban «Perfecto» y derrumbe a la vez. Ahora, un aterrizaje que no puede sostenerse nunca recibe un «Perfecto».

También cambiamos el primer bloque: ahora se asienta sobre su base y se convierte en el punto de referencia de la inclinación, de modo que por sí solo no puede derribar la torre. En nuestras simulaciones con bots, el promedio de un jugador típico subió de 12,4 a 15,9 pisos, y las partidas que terminaban en el piso cuatro o antes bajaron de 48 a 11 de 200.

## El récord que no se guardaba

El derrumbe es lento a propósito: el primer segundo se reproduce a 0,45× para que veas qué pasó. Pero el récord solo se escribía en la pantalla de resultados, unos 1,6 segundos después, así que salir a mitad de la animación lo perdía. Ahora se guarda en el momento en que el derrumbe es seguro.

## Por qué lo escribimos

Ninguno de estos tres es ingenioso. Cada uno es un punto donde el juego le decía al jugador algo que no era cierto, y solo se encuentran jugando. Pensamos seguir haciéndolo.
