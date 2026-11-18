---
slug: 2026-11-18-twelve-languages-one-order
lang: tr
title: "On iki dil, sabit bir sıra"
description: "Tottertop on bir dilden, sabit bir sırayla sık kullanılan on iki dile geçti. Ne değişti, neyi çıkardık ve bunu koruyan dar ekran testi."
excerpt: "İlk yazımızda on bir dil demiştik. Artık on iki, sabit bir sırada; bir dil seçici ve her dilin 320 px'lik ekrana sığmasını sağlayan bir test var."
copy_review: iris 2026-11-16
published: 2026-11-18T16:15+09:00
---
İlk yazımızda Tottertop'un 11 dilde sunulacağını söylemiştik. Bu sayı eskidi: 12 Kasım'da 12 dillik bir kümeye geçtik. Bu yazıda kümenin ve sırasının neden artık sabit olduğunu anlatıyoruz.

## Ne değişti

İlk sürüm İngilizce, Korece, Japonca, Çince, İspanyolca, Fransızca, Almanca, Portekizce, Rusça, Arapça ve Hintçeyi kapsıyordu. Yeni küme şu sırayla:

İngilizce · Korece · Japonca · Geleneksel Çince · İspanyolca · Brezilya Portekizcesi · Fransızca · Almanca · Endonezce · Tayca · Vietnamca · Türkçe

Rusça, Arapça ve Hintçe ayrıldı; Endonezce, Tayca, Vietnamca ve Türkçe geldi. İki geniş etiket de daha belirli hâle geldi: Geleneksel Çince ve Brezilya Portekizcesi. Yeni dillerin çevirileri yarım bırakılmadı, baştan sona yazıldı.

## Sıra neden sabit

Liste ortak bir pakette duruyor; böylece uygulama ve site aynı dilleri aynı sırayla kullanıyor. Sırayı sabitlemek bir testle denetlemeyi de mümkün kılıyor, yani kimse listeyi yanlışlıkla karıştıramıyor.

## Hatırlayan bir seçici (13 Kasım)

Uygulamada Ayarlar'da artık bir dil seçeneği var: önce cihazın kendi dili, ardından on iki dil. Seçiminiz kaydediliyor; kayıtlı değer yanlış ya da bilinmiyorsa ekran bozulmuyor, cihaz diline dönülüyor.

## En önemli test

Almanca ve Vietnamca kelimeler uzundur, Tayca'da ise satır bölünecek boşluk yoktur. Bu yüzden elimizdeki en işe yarar test sıkıcı bir test: 12 dilin her birinde her ekran 320 px genişlikte kuruluyor ve herhangi bir metin taşarsa test başarısız oluyor. Sığmayan bir dil yayına çıkmaz.

Site de aynı on iki dili izliyor, bu günlük de öyle.
