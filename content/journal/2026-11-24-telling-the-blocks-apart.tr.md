---
slug: 2026-11-24-telling-the-blocks-apart
lang: tr
title: "Blokları ayırt etmek: renk körlüğü testi"
description: "Tottertop'a blok renk setleri eklerken bir renk körlüğü simülasyonu, neredeyse aynı görünen iki varsayılan blok buldu. Neyi ölçtüğümüz ve neyi değiştirdiğimiz."
excerpt: "Yeşil renk körlüğü simülasyonunda mavi ve mor bloklar neredeyse aynıydı. Bir kontrast testinin bunu nasıl yakaladığı ve artık her renk setinin geçmesi gereken kural."
copy_review: iris 2026-11-20
published: 2026-11-24T14:45+09:00
---
Eğilen bir kulede rengin gerçek bir görevi vardır: bir bloğun nerede bitip sonrakinin nerede başladığını gösterir. Bu yüzden 15 Kasım'da blok renk setlerini eklerken, renk görme eksikliği olan oyuncuların da blokları kolayca ayırt edebildiğini kontrol eden bir test de ekledik.

## Oynayarak açılan dört set

Varsayılan set Şeker'dir. Pastel 12 katta, Okyanus 20 katta ve Gün batımı 30 katta açılır; bunlar unvan kazandığınız yüksekliklerle aynıdır. Serbest oyunda ya da Günün kulesinde ulaştığınız en yüksek kat sayılır, bu yüzden önceki rekorlarınız setleri hemen açar. Seti Ayarlar'dan seçersiniz; aynı renkler kulede, sonraki blok önizlemesinde ve ana ekranda kullanılır.

## Test ne yapıyor

Test her set için her blok rengini alır ve üç temel renk körlüğü türünde, yani kırmızıyı, yeşili ya da maviyi ayırt etmenin zor olduğu durumlarda, en güçlü derecede nasıl göründüğünü yayımlanmış bir modelle (Machado ve arkadaşları, 2009) canlandırır. Aynısını tipik renk görüşü için de yapar. Ardından renklerin birbirinden ne kadar uzak olduğunu renk farkı (CIELAB ΔE) olarak ölçer.

Blok yüzleri birbirinden en az 10 uzak olmalıdır. Her bloğun ayrıca daha koyu bir alt kenarı vardır; bu kenar yüzünden koyu kalmalı ve hem kendi yüzünden hem de alttaki bloğun yüzünden en az 9 uzak olmalıdır.

## Neyi yakaladı

İlk takılan bizim kendi varsayılan setimiz oldu. Yeşil renk körlüğü simülasyonunda mavi ve mor bloklar arasındaki fark yalnızca 0,8'di; pratikte aynı renk. Blok renklerinin her birini en fazla 12 kaydırdık ve Şeker setindeki en yakın çift 11,5 uzaklaşana kadar devam ettik. Yalnızca bloklar değişti; oyunun geri kalanındaki yazılar ve düğmeler renklerini korudu.

Her setteki en yakın çift, türü ne olursa olsun (yüz ya da kenar), şimdi şöyle: Şeker 11,5, Pastel 10,7, Okyanus 9,5 ve Gün batımı 12,3.

## Bunun bize söylemediği

Bu, bir görme modeli üzerinde yapılmış bir hesaptır; telefona bakan bir insan değil. Henüz renk körü oyuncularla kontrol etmedik; ekran parlaklığı ve gün ışığı da renklerin nasıl göründüğünü değiştirir. İnsanlar kontrol edene kadar bunu kontrol edilmemiş sayıyoruz.
