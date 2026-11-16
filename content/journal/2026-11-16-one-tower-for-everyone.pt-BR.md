---
slug: 2026-11-16-one-tower-for-everyone
lang: pt-BR
title: "Uma torre para todos: como funciona a semente diária"
description: "Nas versões de teste, a torre diária entrega a todos os jogadores a mesma ordem de blocos no mesmo dia. Como uma data vira uma torre, e por que UTC."
excerpt: "Uma torre diária só funciona se todo mundo receber mesmo a mesma. Como transformamos uma data em uma ordem de blocos idêntica em todos os celulares do mundo."
copy_review: iris 2026-11-14
published: 2026-11-16T16:30+09:00
---
Uma das ideias que queríamos desde cedo era a torre diária: durante um dia, todos recebem os mesmos blocos na mesma ordem, e assim a contagem de andares significa a mesma coisa para todo mundo. Parece simples, e só funciona se alguns detalhes chatos estiverem certos.

## Uma data vira semente

A sequência de blocos vem de uma semente, e a semente vem da data. Dois celulares que partem da mesma data montam a mesma sequência, sem nenhum servidor no meio. Abrimos uma exceção de propósito: o primeiro bloco de toda torre é sempre o quadrado simples, para que uma partida nunca comece com algo desconfortável.

## Por que UTC

Se a torre diária seguisse a data local de cada celular, um jogador em Seul e outro em São Paulo ficariam em torres diferentes na maior parte do dia. Por isso a data vem do UTC. Uma torre nova aparece no mesmo instante em todo lugar, que na Coreia é 9h da manhã. Escrevemos testes para o limite do UTC e para o fuso horário da Coreia, porque é ali que os bugs de "que dia é hoje?" se escondem.

## Mesmas entradas, mesma torre

Isso só vale se o próprio jogo for determinístico. O motor roda em um relógio fixo de 120 passos por segundo e mantém suas regras separadas do código de desenho, então a sequência de blocos e a física não dependem da velocidade do celular. Nas versões de teste, a tela inicial guarda no aparelho duas melhores pontuações: uma para o jogo livre e outra para a torre de hoje, que é zerada quando a data muda.

## O que ainda não fizemos

Ainda não há servidor, ranking nem forma de comparar pontuações com outras pessoas. Por enquanto, a torre diária é um quebra-cabeça compartilhado que você joga sozinho. Se ela vai crescer para algo além disso, ainda não foi decidido.
