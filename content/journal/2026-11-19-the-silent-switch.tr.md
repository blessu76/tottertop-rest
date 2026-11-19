---
slug: 2026-11-19-the-silent-switch
lang: tr
title: "Ses açık ama sessizlik: iPhone'un sessiz anahtarı"
description: "Tottertop ayarlarında sesi açmak, sessiz anahtarı açık bir iPhone'da hiçbir şey değiştirmedi. Nedeni, ne değiştirdik ve gerçek cihazlarda hâlâ neyi denemedik."
excerpt: "Ayar açıktı, kod yolu sağlamdı, oyun yine de sessizdi. Sebep, sessiz anahtara uyan tek bir ses moduydu."
copy_review: iris 2026-11-16
published: 2026-11-19T14:30+09:00
---
Ses ve titreşim ayarlarını kontrol ederken, ayardaki bir hataya benzeyen ama öyle olmayan bir sorun bulduk: sesi açabiliyordunuz ve yine de hiçbir şey duymuyordunuz.

## Kod yolu sağlamdı

Her düğmeyi Ayarlar ekranından, bir ses ya da titreşimin istendiği ana kadar izledik: kaydedilen değer, geri okunduğu yer, ayar kapalıyken sesi atlayan kapı ve geri bildirim isteyen her oyun olayı. Hepsi birbirine bağlıydı. Beş ses dosyası yerindeydi ve kayıt anahtarları eşleşiyordu.

## Sebep: kibar bir ses modu

iPhone'da bir uygulamanın sesini nasıl tanımladığı, sessiz anahtara uyup uymayacağını belirler. Oyunumuz, arka plandaki ortam sesleri için tasarlanmış kibar modu kullanıyordu; bu mod sessiz anahtara ve ekran kilidine uyar. Yani anahtar açıkken ayar "açık" diyordu, telefon ise sessiz kalıyordu.

## Ne değiştirdik

- iPhone'da oyun artık oynatma modunu kullanıyor; böylece sessiz anahtar oyun seslerini kısmıyor. Yine de diğer uygulamalarla karışıyor, dolayısıyla çalmakta olan müziğiniz devam ediyor.
- Android'de sesler oyun sesi olarak işaretleniyor ve ses odağını almıyor.
- Titreşimi ya da sesi açtığınızda hemen kısa bir titreşim ya da ses geliyor; böylece çalıştığını anlıyorsunuz. Kapattığınızda ise sessiz kalıyor.
- Android'e titreşim izni açıkça verildi.
- Testler ses modunu, açılışta bir kez gelen sinyali ve izni kapsıyor.

## Neyi denemedik

Bunların hepsi kodda ve testlerde doğrulandı, henüz gerçek telefonlarda değil. Sessiz anahtarı açık bir iPhone'da sesin çaldığını, başka bir uygulamanın müziğinin çalmaya devam ettiğini ve titreşimin geldiğini hâlâ doğrulamamız gerekiyor. Telefonun kendi sistem dokunsal geri bildirim ayarı ya da düşük güç modu da titreşimi susturabilir; bu bizim elimizde değil. Bunları bir sonraki test sürümünde deneyip bulduklarımızı yazacağız.
