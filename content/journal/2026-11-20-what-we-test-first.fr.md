---
slug: 2026-11-20-what-we-test-first
lang: fr
title: "Ce que nous testons avant toute livraison"
description: "Les vérifications d’une version de Tottertop avant livraison : tests unitaires, mise en page à 320 px en 12 langues, parties de bots, et ce que seul un vrai téléphone peut dire."
excerpt: "Près de 700 tests automatiques, une vérification de mise en page dans chaque langue et des joueurs bots. Et la liste de ce qu’aucun test ne peut trancher."
copy_review: iris 2026-11-16
published: 2026-11-20T14:30+09:00
---
Même un petit jeu demande beaucoup de vérifications ennuyeuses. Voici ce qui sépare une modification d’une version de test, et où s’arrête cette vérification.

## Une barrière avant chaque commit

Chaque modification passe par un seul script qui met le code en forme, l’analyse et lance les tests. S’il n’est pas au vert, rien n’est commité et aucune version n’est produite. Au moment d’écrire ces lignes, l’appli compte près de 700 tests automatiques, qui couvrent les règles du jeu, la tour du jour, l’enregistrement et le chargement, les réglages et les langues.

## Chaque langue, écran étroit

Les mots allemands et vietnamiens sont longs, et le thaï n’a pas d’espaces où couper. Le test de mise en page construit donc chaque écran dans les 12 langues avec une largeur de 320 px et échoue si un texte déborde. Le site web passe par le même genre de vérification à 320 et 375 px, puis de nouveau en largeurs tablette et ordinateur.

## Des bots qui jouent à notre place

Pour régler la difficulté, nous ne nous fions pas à nos propres pouces. Des joueurs simulés de plusieurs niveaux jouent des centaines de parties, et nous comparons jusqu’où ils vont. C’est ainsi que nous avons pu dire qu’un correctif avait fait passer la moyenne d’un joueur de niveau moyen de 12,4 à 15,9 étages, et ramené les parties terminées à l’étage quatre ou moins de 48 sur 200 à 11. Les bots nous renseignent sur l’équilibre. Ils ne nous disent pas si le jeu est amusant.

## Ce qu’aucun test ne peut trancher

Un vrai téléphone a toujours le dernier mot sur le son, la vibration, la sensation au toucher et l’aspect du jeu en plein jour. Ces vérifications se font à la main sur des appareils, et tant qu’elles ne sont pas faites, nous les marquons comme non vérifiées au lieu de les déclarer correctes. Si ce journal dit que quelque chose est vérifié, c’est que cela l’a été. S’il ne dit rien, supposez que non.
