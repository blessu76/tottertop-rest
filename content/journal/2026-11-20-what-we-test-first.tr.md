---
slug: 2026-11-20-what-we-test-first
lang: tr
title: "Bir şey yayına çıkmadan önce neyi test ediyoruz"
description: "Bir sürüm masamızdan çıkmadan önce Tottertop'un geçtiği kontrollere kısa bir bakış: birim testleri, 12 dilde 320 px düzen testi, bot oyunları ve yalnızca gerçek bir telefonun söyleyebildikleri."
excerpt: "Yaklaşık 700 otomatik test, her dilde bir düzen kontrolü ve bot oyuncular. Bir de hiçbir testin çözemediği şeylerin listesi."
copy_review: iris 2026-11-16
published: 2026-11-20T14:30+09:00
---
Küçük bir oyun bile çok sıkıcı kontrol ister. Bir değişiklikle bir test sürümü arasında neler olduğunu ve bu kontrolün nerede bittiğini anlatıyoruz.

## Her commit'ten önce bir kapı

Her değişiklik tek bir betikten geçer: kodu biçimlendirir, analiz eder ve testleri çalıştırır. Yeşil değilse hiçbir şey commit edilmez ve sürüm üretilmez. Bu yazıyı yazdığımız sırada uygulamada yaklaşık 700 otomatik test var; oyunun kurallarını, günlük kuleyi, kaydetme ve yüklemeyi, ayarları ve dilleri kapsıyorlar.

## Her dil, dar ekran

Almanca ve Vietnamca kelimeler uzundur, Tayca'da ise satır bölünecek boşluk yoktur. Bu yüzden düzen testi her ekranı 12 dilin hepsinde 320 px genişlikte kurar ve herhangi bir metin taşarsa başarısız olur. Web sitesi de benzer bir kontrolden 320 ve 375 px'te, ardından tablet ve masaüstü genişliklerinde geçer.

## Bizim yerimize oynayan botlar

Zorluğu ayarlarken kendi parmaklarımıza güvenmiyoruz. Çeşitli beceri düzeylerindeki sanal oyuncular yüzlerce tur oynuyor ve ne kadar ilerlediklerini karşılaştırıyoruz. Bu sayede, tek bir düzeltmenin orta düzey bir oyuncunun ortalamasını 12,4 kattan 15,9 kata çıkardığını ve dördüncü katta ya da daha aşağıda biten turları 200'de 48'den 11'e düşürdüğünü söyleyebildik. Botlar dengeyi anlatır. Oyunun eğlenceli olup olmadığını anlatmazlar.

## Hiçbir testin çözemediği şeyler

Ses, titreşim, dokunma hissi ve oyunun gün ışığında nasıl göründüğü konusunda son sözü hâlâ gerçek bir telefon söyler. Bu kontroller cihazlarda elle yapılır; yapılana kadar da bunları "iyi" demek yerine denenmedi diye işaretleriz. Bu günlük bir şeyin doğrulandığını söylüyorsa, doğrulanmıştır. Söylemiyorsa, doğrulanmadığını varsayın.
