---
slug: 2026-11-15-tuning-the-wobble-with-bots
lang: pt-BR
title: "Ajustando o balanço com bots em vez de com as mãos"
description: "Como definimos a dificuldade do Tottertop antes de alguém jogá-lo: três bots com tempos de toque diferentes, 200 rodadas cada um e um aviso honesto."
excerpt: "Antes de uma pessoa poder jogar o Tottertop, ajustamos a dificuldade com três bots de habilidades diferentes, 200 rodadas cada. O que os números dizem e o que eles não conseguem dizer."
copy_review: iris 2026-11-14
published: 2026-11-15T14:30+09:00
---
Um jogo de empilhar com física vive ou morre pelo quanto o balanço parece difícil. Em 11 de novembro, quando o primeiro ciclo completo de uma rodada funcionou, ninguém tinha jogado ainda, então ajustamos com bots.

## A ideia

O motor é escrito em código Dart puro que roda em um relógio fixo de 120 passos por segundo, então as mesmas entradas sempre geram a mesma torre. Isso facilita colocar um bot no lugar do jogador. Nosso bot mira o melhor momento para soltar e depois toca com um erro de tempo aleatório, sorteado de uma distribuição normal. Quanto maior o erro, menos firme é a mão.

Criamos três e rodamos 200 rodadas com cada um:

| Bot | Erro de toque | Média de andares | Chegou a 30+ andares |
|---|---|---|---|
| Especialista (também prevê a inclinação) | 30 ms | 29,4 | 48% |
| Bom | 50 ms | 18,1 | 1,5% |
| Típico | 70 ms | 12,4 | 0% |

Com o bot típico, uma em cada dez rodadas terminou até o andar 2, metade chegou ao 14 e nove em cada dez terminaram até o andar 20.

## O que queríamos alcançar

Nossa meta era simples: um jogador típico deve fazer em média de 10 a 15 andares, e um jogador muito bom deve conseguir passar de 30. A tabela acima cai bem aí, então mantivemos os valores. Ajustamos alguns números: a força com que a inclinação se acumula, o quanto cada pouso sacode a torre e a rapidez com que o balanço se acalma.

## O que isso não nos diz

Um bot não é uma pessoa. Ele nunca se cansa, não entra em pânico quando a torre pende e nunca resolve tentar alguma coisa maluca. Esses números dizem que a curva de dificuldade faz sentido no papel, não que o jogo é bom de jogar. Isso exige mãos de verdade, e vamos conferir de novo quando as pessoas jogarem as versões de teste.
