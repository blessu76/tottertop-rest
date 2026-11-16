---
slug: 2026-11-16-one-tower-for-everyone
lang: tr
title: "Herkes için tek kule: günlük tohum nasıl çalışıyor"
description: "Test sürümlerinde günlük kule, aynı gün tüm oyunculara aynı blok sırasını verir. Bir tarih nasıl kuleye dönüşür ve neden UTC."
excerpt: "Günlük kule ancak herkes gerçekten aynısını alırsa anlamlıdır. Bir tarihi, dünyadaki her telefonda birebir aynı olan bir blok sırasına nasıl çeviriyoruz."
copy_review: iris 2026-11-14
published: 2026-11-16T16:30+09:00
---
Baştan beri istediğimiz fikirlerden biri günlük kuleydi: bir gün boyunca herkes aynı blokları aynı sırayla alır, böylece kat sayısı herkes için aynı anlama gelir. Kulağa basit geliyor, ama ancak birkaç sıkıcı ayrıntı doğru olursa işe yarıyor.

## Bir tarih tohuma dönüşür

Blok dizisi bir tohumdan, tohum da tarihten gelir. Aynı tarihten başlayan iki telefon, aradaki hiçbir sunucu olmadan aynı diziyi kurar. Bilerek bir istisna yaptık: her kulenin ilk bloğu her zaman sade kare bloktur, böylece bir tur asla can sıkıcı bir şekille açılmaz.

## Neden UTC

Günlük kule her telefonun yerel tarihine uysaydı, Seul'deki bir oyuncu ile São Paulo'daki bir oyuncu günün büyük kısmında farklı kuleler üzerinde olurdu. Bu yüzden tarih UTC'den alınır. Yeni bir kule her yerde aynı anda belirir; Kore'de bu sabah saat 9'dur. UTC sınırı ve Kore saat dilimi için testler yazdık, çünkü "bugün günlerden ne?" hataları tam orada saklanır.

## Aynı girdi, aynı kule

Bu söz ancak oyunun kendisi deterministikse tutulur. Motor saniyede 120 adımlık sabit bir saatle çalışır ve kurallarını çizim kodundan ayrı tutar; böylece blok dizisi ve fizik telefonun ne kadar hızlı olduğuna bağlı değildir. Test sürümlerinde ana ekran cihazda iki en yüksek skoru ayrı tutar: biri serbest oyun, diğeri bugünün kulesi için; bugünün kulesinin skoru tarih değişince sıfırlanır.

## Henüz yapmadıklarımız

Henüz sunucu, sıralama tablosu ve başkalarıyla skor karşılaştırmanın bir yolu yok. Şimdilik günlük kule, tek başına oynadığınız ortak bir bulmaca. Bundan fazlasına dönüşüp dönüşmeyeceği henüz kararlaştırılmadı.
