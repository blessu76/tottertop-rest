---
slug: 2026-11-16-one-tower-for-everyone
lang: es
title: "Una torre para todos: cómo funciona la semilla diaria"
description: "En las versiones de prueba, la torre diaria da a todos los jugadores el mismo orden de bloques el mismo día. Cómo una fecha se convierte en una torre, y por qué UTC."
excerpt: "Una torre diaria solo funciona si todos reciben de verdad la misma. Cómo convertimos una fecha en un orden de bloques idéntico en todos los teléfonos del mundo."
copy_review: iris 2026-11-14
published: 2026-11-16T16:30+09:00
---
Una de las ideas que quisimos desde el principio fue la torre diaria: durante un día, todos reciben los mismos bloques en el mismo orden, así que el número de pisos significa lo mismo para todos. Suena sencillo, y solo funciona si unos cuantos detalles aburridos están bien resueltos.

## Una fecha se convierte en semilla

La secuencia de bloques sale de una semilla, y la semilla sale de la fecha. Dos teléfonos que parten de la misma fecha construyen la misma secuencia, sin ningún servidor de por medio. Hicimos una excepción a propósito: el primer bloque de cada torre es siempre el cuadrado simple, para que una partida nunca empiece con algo incómodo.

## Por qué UTC

Si la torre diaria siguiera la fecha local de cada teléfono, un jugador en Seúl y otro en São Paulo estarían en torres distintas durante la mayor parte del día. Por eso la fecha se toma de UTC. Una torre nueva aparece en el mismo instante en todas partes, que en Corea son las 9 de la mañana. Escribimos pruebas para el límite de UTC y para la zona horaria de Corea, porque ahí se esconden los errores del tipo «¿qué día es hoy?».

## Mismas entradas, misma torre

Esto solo se cumple si el propio juego es determinista. El motor funciona con un reloj fijo de 120 pasos por segundo y mantiene sus reglas separadas del código de dibujo, de modo que la secuencia de bloques y la física no dependen de lo rápido que sea el teléfono. En las versiones de prueba, la pantalla de inicio guarda en el dispositivo dos mejores puntuaciones: una para el juego libre y otra para la torre de hoy, que se reinicia cuando cambia la fecha.

## Lo que aún no hemos hecho

No hay servidor, ni clasificación, ni forma de comparar puntuaciones con otras personas todavía. Por ahora la torre diaria es un puzle compartido que se juega en solitario. Si llegará a ser algo más, aún no está decidido.
