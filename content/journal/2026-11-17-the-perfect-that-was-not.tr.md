---
slug: 2026-11-17-the-perfect-that-was-not
lang: tr
title: "“Mükemmel” olmayan “Mükemmel”: ilk günden üç düzeltme"
description: "Tottertop’u ilk kez akşam boyu denediğimizde “Mükemmel” iniş ve rekor çevresinde üç hata çıktı. Neydiler ve nasıl düzelttik."
excerpt: "Kuleyi deviren blokta “Mükemmel”, birinci katta düşen ilk blok, çöküş sırasında kaybolan en yüksek skor: tek bir akşamdan üç hata."
copy_review: iris 2026-11-14
published: 2026-11-17T14:45+09:00
---
11 Kasım’da ilk oynanabilir sürüm hazır olunca bir akşam boyunca oynadık ve tuhaf gelen her şeyi not aldık. Bunlardan üçü küçüktü ama her biri oyunun hissini değiştirdi.

## Yanlış yerden ölçülen “Mükemmel”

Bir blok tam ortaya yakın düştüğünde oyun “Mükemmel” gösterir ve serinizi sürdürür. İlk kontrolümüz sapmayı temas alanının merkezinden ölçüyordu. Tabanına tamamen oturan bir bloğun orada sapması hep sıfırdır; bu yüzden ilk blok nereye düşerse düşsün “Mükemmel” oluyordu. Daha kötüsü, ortadan yaklaşık bir blok beşte birinden fazla uzağa düşerse kule devriliyordu ve ekranda aynı anda “Mükemmel!” ile “Kule 1. katta çöktü” yazıyordu. Artık değerlendirmeyi bloğun üzerine indiği yüzeyin merkezinden yapıyoruz.

## Zaten yıkılan kule için “Mükemmel”

Bu düzeltmeden sonra bile üst yüzün ortasına konan bir blok, aynı anda tüm kuleyi yıkabiliyordu; çünkü toplam ağırlık merkezi alttaki birleşim yerini aşmıştı. Senaryolu 300 simüle oyunun 127’sinde “Mükemmel” ve çöküş birlikte görünüyordu. Taşıyamayacak bir iniş artık asla “Mükemmel” almıyor.

İlk blok da değişti: artık tabanına oturuyor ve eğimin referans noktası oluyor, yani tek başına kuleyi deviremiyor. Bot simülasyonlarımızda tipik bir oyuncunun ortalaması 12,4’ten 15,9 kata çıktı; dördüncü katta veya daha önce biten oyunlar 200’de 48’den 11’e düştü.

## Kaydedilmeyen en yüksek skor

Çöküş bilerek yavaştır: ilk saniye 0,45× hızda oynar, ne olduğunu görebilesiniz diye. Ama en yüksek skor ancak sonuç ekranında, yaklaşık 1,6 saniye sonra yazılıyordu; animasyonun ortasında çıkmak onu kaybettiriyordu. Artık çöküş kesinleştiği anda kaydediliyor.

## Bunu neden yazıyoruz

Bu üçü de zekice şeyler değil. Her biri oyunun oyuncuya doğru olmayan bir şey söylediği bir yer ve bunları ancak oynayarak bulursunuz. Bunu sürdürmeyi planlıyoruz.
