---
slug: 2026-11-17-the-perfect-that-was-not
lang: fr
title: "Le « Parfait » qui n’en était pas un : trois correctifs"
description: "Lors de la première vraie soirée de test de Tottertop, trois bugs sont apparus autour du « Parfait » et du record. Ce qu’ils étaient et comment nous les avons corrigés."
excerpt: "Un « Parfait » sur un bloc qui fait tomber la tour, un premier bloc tombé à l’étage 1, un record perdu en plein effondrement : trois bugs en une soirée."
copy_review: iris 2026-11-14
published: 2026-11-17T14:45+09:00
---
Le 11 novembre, dès que la première version jouable a existé, nous avons passé une soirée à y jouer en notant tout ce qui sonnait faux. Trois de ces points étaient petits, et chacun a changé la sensation du jeu.

## Un « Parfait » mesuré au mauvais endroit

Quand un bloc atterrit près du centre exact, le jeu affiche « Parfait » et prolonge votre série. Notre premier test mesurait l’écart par rapport au centre de la zone de contact. Un bloc entièrement posé sur sa base y a toujours un écart nul : le tout premier bloc était donc « Parfait » où qu’il tombe. Pire, s’il atterrissait à plus d’un cinquième de bloc du milieu, la tour basculait, et l’écran affichait en même temps « Parfait ! » et « La tour s’est effondrée à l’étage 1 ». Nous jugeons désormais depuis le centre de la surface sur laquelle le bloc se pose.

## « Parfait » pour une tour qui tombe quand même

Même avec ce correctif, un bloc posé au milieu du dessus pouvait encore faire s’effondrer toute la tour au même instant, car le poids cumulé avait dépassé le joint du dessous. Dans 127 parties simulées sur 300 (jouées par script), « Parfait » et effondrement s’affichaient ensemble. Un atterrissage qui ne peut pas tenir ne reçoit plus jamais de « Parfait ».

Le premier bloc a aussi changé : il se cale maintenant sur sa base et devient le point de référence de l’inclinaison, si bien qu’il ne peut plus renverser la tour à lui seul. Dans nos simulations avec des bots, la moyenne d’un joueur typique est passée de 12,4 à 15,9 étages, et les parties terminées à l’étage quatre ou avant sont tombées de 48 à 11 sur 200.

## Le record qui n’était pas enregistré

L’effondrement est lent exprès : la première seconde est jouée à 0,45× pour que l’on voie ce qui s’est passé. Mais le record n’était écrit qu’à l’écran de résultat, environ 1,6 seconde plus tard ; quitter en pleine animation le faisait donc perdre. Il est maintenant enregistré à l’instant où l’effondrement est certain.

## Pourquoi nous le notons

Aucun de ces trois bugs n’est brillant. Chacun est un endroit où le jeu disait au joueur quelque chose de faux, et on ne les trouve qu’en jouant. Nous comptons continuer.
