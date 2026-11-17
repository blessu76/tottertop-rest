---
slug: 2026-11-17-the-perfect-that-was-not
lang: pt-BR
title: "O “Perfeito” que não era: três correções do primeiro dia"
description: "Na primeira noite inteira de testes do Tottertop, três bugs apareceram em torno do “Perfeito” e do recorde. O que eram e como corrigimos."
excerpt: "Um “Perfeito” num bloco que derruba a torre, um primeiro bloco que caiu no andar um, um recorde perdido em pleno desabamento: três bugs de uma noite."
copy_review: iris 2026-11-14
published: 2026-11-17T14:45+09:00
---
Em 11 de novembro, quando a primeira versão jogável ficou pronta, passamos uma noite jogando e anotando tudo o que parecia estranho. Três desses itens eram pequenos, e cada um mudou a sensação do jogo.

## “Perfeito” medido do lugar errado

Quando um bloco cai bem perto do centro, o jogo mostra “Perfeito” e mantém a sua sequência. Nossa primeira verificação media o desvio a partir do centro da área de contato. Um bloco totalmente apoiado na base sempre tem desvio zero ali, então o primeiro bloco era “Perfeito” onde quer que caísse. Pior: se ele caísse a mais ou menos um quinto de bloco do meio, a torre tombava — e a tela mostrava “Perfeito!” e “A torre desabou no andar 1” ao mesmo tempo. Agora o julgamento parte do centro da superfície em que o bloco pousa.

## “Perfeito” para uma torre que cai de qualquer jeito

Mesmo com a correção, um bloco colocado no meio do topo ainda podia derrubar a torre inteira no mesmo instante, porque o peso combinado já tinha passado da junta de baixo. Em 127 de 300 partidas simuladas com roteiro, apareciam “Perfeito” e desabamento juntos. Agora, um pouso que não se sustenta nunca ganha um “Perfeito”.

O primeiro bloco também mudou: ele agora assenta na base e vira o ponto de referência da inclinação, então não consegue derrubar a torre sozinho. Nas simulações com bots, a média de um jogador típico subiu de 12,4 para 15,9 andares, e as partidas que terminavam no andar quatro ou antes caíram de 48 para 11 em 200.

## O recorde que não era salvo

O desabamento é lento de propósito: o primeiro segundo roda a 0,45× para você ver o que aconteceu. Mas o recorde só era gravado na tela de resultado, cerca de 1,6 segundo depois, então sair no meio da animação o perdia. Agora ele é salvo no instante em que o desabamento é certo.

## Por que registramos isso

Nenhum dos três é genial. Cada um é um ponto em que o jogo dizia ao jogador algo que não era verdade, e só se descobre jogando. Pretendemos continuar fazendo isso.
