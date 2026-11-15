---
slug: 2026-11-15-tuning-the-wobble-with-bots
lang: tr
title: "Sallanmayı eller yerine botlarla ayarlamak"
description: "Tottertop'un zorluğunu kimse oynamadan önce nasıl belirledik: dokunuş zamanlaması farklı üç bot, her biri 200 tur ve dürüst bir not."
excerpt: "Bir insan Tottertop'u oynayabilmeden önce zorluğunu, becerisi farklı üç botla, her biri 200 tur olarak ayarladık. Rakamların söylediği ve söyleyemediği şeyler."
copy_review: iris 2026-11-14
published: 2026-11-15T14:30+09:00
---
Fizik tabanlı bir istifleme oyunu, sallanmanın ne kadar zor hissettirdiğine bağlı olarak yaşar ya da ölür. 11 Kasım'da ilk tam tur döngüsü çalıştığında henüz kimse oynamamıştı, biz de onu botlarla ayarladık.

## Fikir

Motor, saniyede 120 adımlık sabit bir saatle çalışan düz Dart koduyla yazıldı; bu yüzden aynı girdiler her zaman aynı kuleyi ortaya çıkarır. Bu da oyuncunun yerine bir bot oturtmayı kolaylaştırır. Botumuz bırakmak için en iyi anı hedefler, sonra normal dağılımdan çekilen rastgele bir zamanlama hatasıyla dokunur. Hata ne kadar büyükse el o kadar az sabittir.

Üç bot yaptık ve her biriyle 200 tur oynattık:

| Bot | Dokunuş hatası | Ortalama kat | 30+ kata ulaşan |
|---|---|---|---|
| Uzman (eğimi de öngörür) | 30 ms | 29,4 | %48 |
| İyi | 50 ms | 18,1 | %1,5 |
| Tipik | 70 ms | 12,4 | %0 |

Tipik bot için turların onda biri 2. kata kadar bitti, yarısı 14. kata ulaştı ve onda dokuzu 20. kata kadar bitti.

## Neyi hedefliyorduk

Hedefimiz basitti: tipik bir oyuncu ortalama 10 ila 15 kat civarında yapmalı, çok iyi bir oyuncu ise 30'u geçebilmeli. Yukarıdaki tablo tam bu aralığa düşüyor, biz de değerleri koruduk. Birkaç sayıyı ayarladık: eğimin ne kadar güçlü biriktiği, her inişin kuleyi ne kadar sert sarstığı ve sallanmanın ne kadar çabuk yatıştığı.

## Bunun bize söylemedikleri

Bot bir insan değildir. Hiç yorulmaz, kule yattığında paniğe kapılmaz ve saçma bir şey denemeye asla karar vermez. Bu rakamlar zorluk eğrisinin kâğıt üzerinde makul olduğunu söylüyor; oyunun doğru hissettirdiğini değil. Bunun için gerçek eller gerekiyor ve insanlar test sürümlerini oynadığında bunu yeniden kontrol edeceğiz.
