---
slug: 2026-11-20-what-we-test-first
lang: pt-BR
title: "O que testamos antes de qualquer lançamento"
description: "As verificações de uma versão do Tottertop antes de sair: testes unitários, layout a 320 px em 12 idiomas, partidas de bots e o que só um celular real mostra."
excerpt: "Quase 700 testes automáticos, uma checagem de layout em cada idioma e jogadores bots. E a lista do que nenhum teste resolve."
copy_review: iris 2026-11-16
published: 2026-11-20T14:30+09:00
---
Até um jogo pequeno precisa de muita checagem chata. Aqui está o que fica entre uma mudança e uma versão de teste, e onde essa checagem termina.

## Uma trava antes de cada commit

Toda mudança passa por um único script que formata o código, analisa e roda os testes. Se não estiver verde, nada é commitado e nenhuma versão é gerada. No momento em que escrevemos, o app tem quase 700 testes automáticos, que cobrem as regras do jogo, a torre diária, salvar e carregar, as configurações e os idiomas.

## Todos os idiomas, tela estreita

Palavras em alemão e em vietnamita são longas, e o tailandês não tem espaços para quebrar a linha. Por isso o teste de layout monta cada tela nos 12 idiomas com 320 px de largura e falha se algum texto transbordar. O site passa pelo mesmo tipo de checagem a 320 e 375 px, e de novo em larguras de tablet e de computador.

## Bots que jogam por nós

Para ajustar a dificuldade, não confiamos nos nossos próprios dedões. Jogadores simulados de vários níveis de habilidade jogam centenas de partidas, e comparamos até onde chegam. Foi assim que pudemos dizer que uma correção levou a média de um jogador de nível médio de 12,4 para 15,9 andares, e reduziu as partidas que terminavam no andar quatro ou antes de 48 em 200 para 11. Bots nos falam sobre equilíbrio. Não nos dizem se o jogo é divertido.

## O que nenhum teste resolve

Um celular de verdade ainda tem a última palavra sobre som, vibração, sensação ao toque e como o jogo aparece à luz do dia. Essas checagens são feitas à mão em aparelhos, e até serem feitas nós as marcamos como não verificadas, em vez de dizer que estão boas. Se este diário diz que algo foi verificado, foi. Se não diz nada, presuma que não foi.
