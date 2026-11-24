---
slug: 2026-11-24-telling-the-blocks-apart
lang: fr
title: "Distinguer les blocs : un test pour le daltonisme"
description: "En ajoutant des jeux de couleurs de blocs à Tottertop, une simulation du daltonisme a révélé deux blocs par défaut presque identiques. Ce que nous avons mesuré et changé."
excerpt: "En simulant un daltonisme du vert, les blocs bleu et violet étaient presque identiques. Comment un test de contraste l'a repéré, et la règle que chaque jeu de couleurs doit suivre."
copy_review: iris 2026-11-20
published: 2026-11-24T14:45+09:00
---
Sur une tour qui penche, la couleur a un vrai rôle : elle montre où un bloc s'arrête et où commence le suivant. Alors, quand nous avons ajouté des jeux de couleurs pour les blocs le 15 novembre, nous avons aussi ajouté un test qui vérifie qu'ils restent faciles à distinguer pour les personnes qui perçoivent mal certaines couleurs.

## Quatre jeux, débloqués en jouant

Bonbon est le jeu par défaut. Pastel s'ouvre à 12 étages, Océan à 20 et Coucher de soleil à 30, les mêmes hauteurs que les titres. C'est votre meilleure hauteur de tous les temps, en Partie libre ou sur la Tour du jour, qui compte : vos records précédents les ouvrent donc tout de suite. Le jeu se choisit dans les Réglages, et les mêmes couleurs s'affichent sur la tour, dans l'aperçu du bloc suivant et sur l'écran d'accueil.

## Ce que fait le test

Pour chaque jeu, le test prend chaque couleur de bloc et simule son apparence avec les trois principales formes de daltonisme, où le rouge, le vert ou le bleu est difficile à distinguer, à leur degré le plus fort, à l'aide d'un modèle publié (Machado et coll., 2009). Il fait de même pour une vision typique. Puis il mesure l'écart entre les couleurs, sous forme de différence de couleur (CIELAB ΔE).

Les faces des blocs doivent être à au moins 10 les unes des autres. Chaque bloc a aussi un bord inférieur plus sombre, qui doit rester plus sombre que sa face et se tenir à au moins 9 d'elle et de la face du bloc du dessous.

## Ce qu'il a trouvé

Notre propre jeu par défaut a échoué. Avec la simulation du daltonisme du vert, les blocs bleu et violet n'étaient qu'à 0,8 : pratiquement la même couleur. Nous avons déplacé les couleurs des blocs de 12 au maximum chacune, jusqu'à ce que la paire la plus proche de Bonbon soit à 11,5. Seuls les blocs ont changé ; les textes et les boutons du reste du jeu ont gardé leurs couleurs.

La paire la plus proche, toutes catégories confondues (faces ou bords), est maintenant de : Bonbon 11,5, Pastel 10,7, Océan 9,5 et Coucher de soleil 12,3.

## Ce que cela ne nous dit pas

C'est un calcul sur un modèle de la vision, pas une personne qui regarde un téléphone. Nous ne l'avons pas encore vérifié avec des joueurs daltoniens, et la luminosité de l'écran comme la lumière du jour changent la façon dont les couleurs apparaissent. Tant que des personnes ne l'ont pas vérifié, nous le comptons comme non vérifié.
