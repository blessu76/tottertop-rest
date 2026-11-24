---
slug: 2026-11-24-telling-the-blocks-apart
lang: pt-BR
title: "Distinguir os blocos: um teste de daltonismo"
description: "Ao adicionar conjuntos de cores de blocos ao Tottertop, uma simulação de daltonismo achou dois blocos padrão quase iguais. O que medimos e o que mudamos."
excerpt: "Numa simulação de daltonismo para o verde, os blocos azul e roxo eram quase idênticos. Como um teste de contraste pegou isso, e a regra que todo conjunto de cores precisa cumprir."
copy_review: iris 2026-11-20
published: 2026-11-24T14:45+09:00
---
Numa torre que se inclina, a cor tem um trabalho de verdade: mostra onde um bloco termina e onde começa o próximo. Por isso, quando adicionamos conjuntos de cores para os blocos em 15 de novembro, adicionamos também um teste que verifica se eles continuam fáceis de distinguir para quem tem alguma deficiência na visão de cores.

## Quatro conjuntos, liberados jogando

Doce é o padrão. Pastel é liberado com 12 andares, Oceano com 20 e Pôr do sol com 30, as mesmas alturas em que você ganha títulos. Vale a sua maior altura de todas, no Jogo livre ou na Torre do dia, então recordes anteriores já liberam os conjuntos na hora. Você escolhe o conjunto nas Configurações, e as mesmas cores aparecem na torre, na prévia do próximo bloco e na tela inicial.

## O que o teste faz

Para cada conjunto, o teste pega cada cor de bloco e simula como ela aparece nos três tipos comuns de daltonismo, em que fica difícil distinguir o vermelho, o verde ou o azul, no grau mais forte, usando um modelo publicado (Machado e colegas, 2009). Faz o mesmo para a visão típica. Depois mede a distância entre as cores como diferença de cor (CIELAB ΔE).

As faces dos blocos precisam estar a pelo menos 10 umas das outras. Cada bloco também tem uma borda inferior mais escura, que precisa continuar mais escura que a face e ficar a pelo menos 9 dela e da face do bloco de baixo.

## O que ele encontrou

O nosso próprio conjunto padrão falhou. Na simulação de daltonismo para o verde, os blocos azul e roxo estavam a apenas 0,8: praticamente a mesma cor. Movemos as cores dos blocos em até 12 cada, até que o par mais próximo do Doce ficasse a 11,5. Só os blocos mudaram; textos e botões no resto do jogo mantiveram as cores.

O par mais próximo de qualquer tipo (faces ou bordas) em cada conjunto agora é: Doce 11,5, Pastel 10,7, Oceano 9,5 e Pôr do sol 12,3.

## O que isto não nos diz

É um cálculo sobre um modelo de visão, não uma pessoa olhando para um celular. Ainda não verificamos com jogadores daltônicos, e o brilho da tela e a luz do dia mudam a forma como as cores aparecem. Até que pessoas confiram, contamos isso como não verificado.
