---
slug: 2026-11-19-the-silent-switch
lang: pt-BR
title: "Som ligado e nada se ouve: a chave de silêncio do iPhone"
description: "Ligar o som nas configurações do Tottertop não fazia nada num iPhone com a chave de silêncio ativada. A causa, o que mudamos e o que ainda falta verificar em aparelhos reais."
excerpt: "A configuração estava ligada, o código estava certo, e o jogo continuava mudo. A causa era um modo de áudio que obedece à chave de silêncio."
copy_review: iris 2026-11-16
published: 2026-11-19T14:30+09:00
---
Ao conferir as configurações de som e vibração, encontramos um problema que parece um bug da configuração, mas não é: dava para ligar o som e mesmo assim não ouvir nada.

## O caminho do código estava certo

Seguimos cada chave desde a tela de Configurações até o momento em que um som ou uma vibração é pedido: o valor salvo, o lugar onde ele é lido de volta, a trava que pula um som quando a configuração está desligada e cada evento do jogo que pede retorno. Tudo estava conectado. Os cinco arquivos de som estavam presentes e as chaves salvas batiam.

## A causa: um modo de áudio educado

No iPhone, a forma como um app declara o áudio decide se ele obedece à chave de silêncio. Nosso jogo usava o modo educado, pensado para ambiente de fundo, e esse modo segue a chave de silêncio e o bloqueio de tela. Então, com a chave ativada, a configuração dizia “ligado” e o celular continuava quieto.

## O que mudamos

- No iPhone, o jogo agora usa o modo de reprodução, então a chave de silêncio não cala mais os sons do jogo. Ele continua se misturando com outros apps, e a música que você já estava ouvindo segue tocando.
- No Android, os sons são marcados como sons de jogo e não pegam o foco de áudio.
- Ao ligar a vibração ou o som, você agora recebe na hora uma vibração ou um som curto, para saber que funciona. Ao desligar, fica em silêncio.
- O Android recebe a permissão de vibração de forma explícita.
- Testes cobrem o modo de áudio, o aviso único ao ligar e a permissão.

## O que não verificamos

Tudo isso está verificado no código e nos testes, mas ainda não em celulares de verdade. Ainda precisamos confirmar, num iPhone com a chave de silêncio ativada, que o som toca; que a música de outro app continua tocando; e que a vibração chega. A configuração de vibração do próprio sistema ou o modo de economia de bateria também pode silenciar a vibração, e isso foge do nosso controle. Vamos conferir tudo isso na próxima versão de teste e anotar o que encontrarmos.
