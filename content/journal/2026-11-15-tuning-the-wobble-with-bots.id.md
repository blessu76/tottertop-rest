---
slug: 2026-11-15-tuning-the-wobble-with-bots
lang: id
title: "Menyetel goyangan dengan bot, bukan dengan tangan"
description: "Bagaimana kami menentukan tingkat kesulitan Tottertop sebelum ada yang memainkannya: tiga bot dengan waktu ketukan berbeda, masing-masing 200 ronde, dan satu catatan jujur."
excerpt: "Sebelum ada yang bisa memainkan Tottertop, kami menyetel kesulitannya dengan tiga bot berkemampuan berbeda, masing-masing 200 ronde. Apa kata angkanya, dan apa yang tidak bisa dikatakannya."
copy_review: iris 2026-11-14
published: 2026-11-15T14:30+09:00
---
Gim susun berbasis fisika hidup-matinya ditentukan oleh seberapa sulit goyangannya terasa. Pada 11 November, ketika putaran ronde penuh pertama berhasil berjalan, belum ada yang memainkannya, jadi kami menyetelnya dengan bot.

## Idenya

Mesinnya ditulis sebagai kode Dart biasa yang berjalan pada jam tetap 120 langkah per detik, sehingga masukan yang sama selalu menghasilkan menara yang sama. Itu memudahkan kami mendudukkan bot di kursi pemain. Bot kami membidik saat terbaik untuk menjatuhkan blok, lalu mengetuk dengan kesalahan waktu acak yang diambil dari distribusi normal. Kesalahan yang lebih besar berarti tangan yang kurang mantap.

Kami membuat tiga bot dan menjalankan masing-masing 200 ronde:

| Bot | Kesalahan ketukan | Rata-rata lantai | Mencapai 30+ lantai |
|---|---|---|---|
| Ahli (juga memprediksi kemiringan) | 30 ms | 29,4 | 48% |
| Mahir | 50 ms | 18,1 | 1,5% |
| Biasa | 70 ms | 12,4 | 0% |

Untuk bot biasa, satu dari sepuluh ronde berakhir paling jauh di lantai 2, separuhnya mencapai lantai 14, dan sembilan dari sepuluh berakhir paling jauh di lantai 20.

## Apa yang kami incar

Target kami sederhana: pemain biasa rata-rata mencapai sekitar 10 sampai 15 lantai, dan pemain yang sangat mahir bisa melewati 30. Tabel di atas jatuh tepat di sana, jadi kami mempertahankan nilainya. Kami menyetel beberapa angka: seberapa kuat kemiringan menumpuk, seberapa keras setiap pendaratan menghentak menara, dan seberapa cepat goyangan mereda.

## Yang tidak ditunjukkan angka-angka ini

Bot bukan manusia. Ia tidak pernah lelah, tidak panik saat menara miring, dan tidak pernah tiba-tiba ingin mencoba hal yang aneh. Angka-angka ini menunjukkan bahwa kurva kesulitannya masuk akal di atas kertas, bukan bahwa gimnya terasa pas. Bagian itu butuh tangan sungguhan, dan kami akan memeriksanya lagi saat orang-orang memainkan versi uji coba.
