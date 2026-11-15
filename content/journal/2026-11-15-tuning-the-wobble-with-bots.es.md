---
slug: 2026-11-15-tuning-the-wobble-with-bots
lang: es
title: "Ajustar el bamboleo con bots en lugar de con las manos"
description: "Cómo fijamos la dificultad de Tottertop antes de que nadie lo hubiera jugado: tres bots con distinto timing al tocar, 200 rondas cada uno y una advertencia honesta."
excerpt: "Antes de que una persona pudiera jugar Tottertop, ajustamos su dificultad con tres bots de distinta habilidad, 200 rondas cada uno. Lo que dicen los números y lo que no pueden decir."
copy_review: iris 2026-11-14
published: 2026-11-15T14:30+09:00
---
Un juego de apilar con física vive o muere según lo difícil que se sienta el bamboleo. El 11 de noviembre, cuando funcionó por primera vez el bucle completo de una ronda, nadie lo había jugado todavía, así que lo ajustamos con bots.

## La idea

El motor está escrito en código Dart puro que corre con un reloj fijo de 120 pasos por segundo, de modo que las mismas entradas siempre dan la misma torre. Eso facilita sentar a un bot en el lugar del jugador. Nuestro bot apunta al mejor momento para soltar y luego toca con un error de timing aleatorio, tomado de una distribución normal. Un error mayor equivale a una mano menos firme.

Hicimos tres y corrimos 200 rondas con cada uno:

| Bot | Error al tocar | Pisos de media | Llegó a 30+ pisos |
|---|---|---|---|
| Experto (también predice la inclinación) | 30 ms | 29,4 | 48 % |
| Bueno | 50 ms | 18,1 | 1,5 % |
| Típico | 70 ms | 12,4 | 0 % |

Con el bot típico, una de cada diez rondas terminó antes del piso 2, la mitad llegó al 14 y nueve de cada diez acabaron antes del piso 20.

## Qué buscábamos

Nuestro objetivo era sencillo: que un jugador típico promedie entre 10 y 15 pisos y que uno muy bueno pueda pasar de 30. La tabla de arriba cae justo ahí, así que mantuvimos los valores. Ajustamos un puñado de números: con cuánta fuerza se acumula la inclinación, cuánto sacude a la torre cada aterrizaje y con qué rapidez se calma el bamboleo.

## Lo que esto no nos dice

Un bot no es una persona. Nunca se cansa, no se pone nervioso cuando la torre se inclina y jamás decide probar alguna tontería. Estos números dicen que la curva de dificultad tiene sentido sobre el papel, no que el juego se sienta bien. Para eso hacen falta manos de verdad, y lo volveremos a comprobar cuando la gente juegue las versiones de prueba.
