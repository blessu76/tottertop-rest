---
slug: 2026-11-15-tuning-the-wobble-with-bots
lang: fr
title: "Régler le tremblement avec des bots plutôt qu'à la main"
description: "Comment nous avons fixé la difficulté de Tottertop avant que quiconque y ait joué : trois bots au timing de tap différent, 200 parties chacun, et une réserve honnête."
excerpt: "Avant qu'un humain puisse jouer à Tottertop, nous avons réglé sa difficulté avec trois bots de niveaux différents, 200 parties chacun. Ce que disent les chiffres, et ce qu'ils ne peuvent pas dire."
copy_review: iris 2026-11-14
published: 2026-11-15T14:30+09:00
---
Un jeu d'empilement physique vit ou meurt selon la difficulté que l'on ressent dans le tremblement. Le 11 novembre, quand la première boucle de partie complète a fonctionné, personne n'y avait encore joué : nous l'avons donc réglé avec des bots.

## L'idée

Le moteur est écrit en code Dart pur, cadencé par une horloge fixe de 120 pas par seconde, si bien que les mêmes actions donnent toujours la même tour. Il est donc facile de mettre un bot à la place du joueur. Notre bot vise le meilleur moment pour lâcher, puis tape avec une erreur de timing aléatoire tirée d'une loi normale. Plus l'erreur est grande, moins la main est sûre.

Nous en avons fait trois et lancé 200 parties avec chacun :

| Bot | Erreur de tap | Étages en moyenne | A atteint 30+ étages |
|---|---|---|---|
| Expert (anticipe aussi l'inclinaison) | 30 ms | 29,4 | 48 % |
| Bon | 50 ms | 18,1 | 1,5 % |
| Moyen | 70 ms | 12,4 | 0 % |

Avec le bot moyen, une partie sur dix s'est arrêtée avant l'étage 2, la moitié a atteint le 14, et neuf sur dix se sont terminées avant l'étage 20.

## Ce que nous visions

Notre objectif était simple : un joueur moyen devrait faire environ 10 à 15 étages en moyenne, et un très bon joueur devrait pouvoir dépasser 30. Le tableau ci-dessus tombe là, nous avons donc gardé les valeurs. Nous avons ajusté quelques nombres : la force avec laquelle l'inclinaison s'accumule, la violence de chaque atterrissage sur la tour et la vitesse à laquelle le tremblement s'apaise.

## Ce que cela ne nous dit pas

Un bot n'est pas une personne. Il ne se fatigue jamais, ne panique pas quand la tour penche et ne décide jamais de tenter quelque chose d'absurde. Ces chiffres disent que la courbe de difficulté tient la route sur le papier, pas que le jeu est agréable à jouer. Cela demande de vraies mains, et nous le vérifierons à nouveau quand des gens joueront aux versions de test.
