---
slug: 2026-11-18-twelve-languages-one-order
lang: pt-BR
title: "Doze idiomas, uma ordem fixa"
description: "O Tottertop passou de onze para doze idiomas comuns, em ordem fixa. O que mudou, o que saiu e o teste de tela estreita que protege tudo isso."
excerpt: "Nosso primeiro post dizia onze idiomas. Agora são doze, em ordem fixa, com seletor de idioma e um teste que faz cada um caber numa tela de 320 px."
copy_review: iris 2026-11-16
published: 2026-11-18T16:15+09:00
---
Nosso primeiro post dizia que o Tottertop estaria disponível em 11 idiomas. Esse número ficou desatualizado: em 12 de novembro passamos para um conjunto de 12, e este post explica por que o conjunto, e a ordem dele, agora são fixos.

## O que mudou

A primeira versão cobria inglês, coreano, japonês, chinês, espanhol, francês, alemão, português, russo, árabe e híndi. O novo conjunto é, nesta ordem:

inglês · coreano · japonês · chinês tradicional · espanhol · português do Brasil · francês · alemão · indonésio · tailandês · vietnamita · turco

Russo, árabe e híndi saíram, indonésio, tailandês, vietnamita e turco chegaram, e os dois rótulos genéricos viraram específicos: chinês tradicional e português do Brasil. As traduções dos idiomas novos estão escritas por inteiro, e não deixadas como rascunhos vazios.

## Por que a ordem é fixa

A lista fica num kit compartilhado, então o app e o site usam os mesmos idiomas na mesma ordem. Fixar a ordem também permite que um teste a verifique, e assim ninguém embaralha a lista por acidente.

## Um seletor que lembra (13 de novembro)

No app, as Configurações agora têm uma opção de idioma: primeiro o idioma do próprio aparelho, depois os doze. Sua escolha fica salva, e um valor salvo errado ou desconhecido volta para o idioma do aparelho em vez de quebrar a tela.

## O teste que mais importa

Palavras em alemão e em vietnamita são longas, e o tailandês não tem espaços para quebrar a linha. Por isso o teste mais útil que temos é chato: cada tela, em cada um dos 12 idiomas, é montada com 320 px de largura, e o teste falha se algum texto transbordar. Um idioma que não cabe não é lançado.

O site segue os mesmos doze idiomas, e este diário também.
