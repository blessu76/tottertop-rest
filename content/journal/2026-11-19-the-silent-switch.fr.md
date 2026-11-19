---
slug: 2026-11-19-the-silent-switch
lang: fr
title: "Son activé, rien d’audible : le commutateur muet de l’iPhone"
description: "Activer le son dans les réglages de Tottertop ne faisait rien sur un iPhone en mode muet. La cause, ce que nous avons changé et ce qui reste à vérifier sur de vrais appareils."
excerpt: "Le réglage était activé, le code était correct, et le jeu restait muet. La cause : un mode audio qui obéit au commutateur muet."
copy_review: iris 2026-11-16
published: 2026-11-19T14:30+09:00
---
En vérifiant les réglages de son et de vibration, nous avons trouvé un problème qui ressemble à un bug du réglage sans en être un : on pouvait activer le son et ne rien entendre.

## Le chemin du code était correct

Nous avons suivi chaque interrupteur depuis l’écran des Réglages jusqu’au moment où un son ou une vibration est demandé : la valeur enregistrée, l’endroit où elle est relue, la barrière qui saute un son quand le réglage est désactivé, et chaque événement du jeu qui réclame un retour. Tout était relié. Les cinq fichiers de son étaient présents et les clés enregistrées correspondaient.

## La cause : un mode audio poli

Sur iPhone, la façon dont une appli déclare son audio décide si elle obéit au commutateur muet. Notre jeu utilisait le mode poli prévu pour l’ambiance de fond, et ce mode suit le commutateur muet et le verrouillage de l’écran. Commutateur enclenché, le réglage indiquait donc « activé » et le téléphone restait silencieux.

## Ce que nous avons changé

- Sur iPhone, le jeu utilise désormais le mode lecture, si bien que le commutateur muet ne coupe plus les sons du jeu. Il se mélange toujours aux autres applis, donc la musique que vous écoutiez déjà continue.
- Sur Android, les sons sont déclarés comme sons de jeu et ne prennent pas le focus audio.
- Activer la vibration ou le son déclenche maintenant tout de suite une courte vibration ou un court son, pour que vous sachiez que cela fonctionne. Le désactiver reste silencieux.
- Android reçoit explicitement la permission de vibration.
- Des tests couvrent le mode audio, le signal unique à l’activation et la permission.

## Ce que nous n’avons pas vérifié

Tout cela est vérifié dans le code et les tests, pas encore sur de vrais téléphones. Il nous reste à confirmer, sur un iPhone dont le commutateur muet est enclenché, que le son joue, que la musique d’une autre appli continue et que la vibration arrive. Le réglage haptique du système ou le mode économie d’énergie peut aussi couper la vibration, et cela échappe à notre contrôle. Nous le vérifierons dans la prochaine version de test et noterons ce que nous trouvons.
