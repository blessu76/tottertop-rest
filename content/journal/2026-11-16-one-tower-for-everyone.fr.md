---
slug: 2026-11-16-one-tower-for-everyone
lang: fr
title: "Une tour pour tous : comment fonctionne la graine du jour"
description: "Dans les versions de test, la tour du jour donne à tous les joueurs le même ordre de blocs le même jour. Comment une date devient une tour, et pourquoi l'UTC."
excerpt: "Une tour du jour n'a de sens que si tout le monde reçoit vraiment la même. Comment nous transformons une date en un ordre de blocs identique sur tous les téléphones du monde."
copy_review: iris 2026-11-14
published: 2026-11-16T16:30+09:00
---
Une des idées que nous voulions dès le début était la tour du jour : pendant une journée, tout le monde reçoit les mêmes blocs dans le même ordre, si bien que le nombre d'étages veut dire la même chose pour tous. Cela paraît simple, et cela ne fonctionne que si quelques détails ennuyeux sont justes.

## Une date devient une graine

La suite de blocs vient d'une graine, et la graine vient de la date. Deux téléphones qui partent de la même date construisent la même suite, sans aucun serveur entre les deux. Nous avons fait une exception volontaire : le premier bloc de chaque tour est toujours le carré simple, pour qu'une partie ne commence jamais par quelque chose de gênant.

## Pourquoi l'UTC

Si la tour du jour suivait la date locale de chaque téléphone, un joueur à Séoul et un joueur à São Paulo seraient sur des tours différentes la plupart de la journée. La date est donc prise en UTC. Une nouvelle tour apparaît au même instant partout, soit 9 h du matin en Corée. Nous avons écrit des tests pour la frontière de l'UTC et pour le fuseau horaire coréen, car c'est là que se cachent les bugs du type « quel jour sommes-nous ? ».

## Mêmes entrées, même tour

Cela ne tient que si le jeu lui-même est déterministe. Le moteur tourne sur une horloge fixe de 120 pas par seconde et sépare ses règles du code de dessin, de sorte que la suite de blocs et la physique ne dépendent pas de la vitesse du téléphone. Dans les versions de test, l'écran d'accueil garde sur l'appareil deux meilleurs scores : un pour le jeu libre et un pour la tour du jour, qui est remis à zéro quand la date change.

## Ce que nous n'avons pas fait

Il n'y a pas de serveur, pas de classement et pas encore de moyen de comparer ses scores avec d'autres personnes. Pour l'instant, la tour du jour est un puzzle partagé auquel on joue seul. Qu'elle devienne autre chose, ce n'est pas décidé.
