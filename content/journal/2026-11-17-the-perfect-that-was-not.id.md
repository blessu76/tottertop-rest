---
slug: 2026-11-17-the-perfect-that-was-not
lang: id
title: "“Perfect” yang Bukan Perfect: tiga perbaikan di hari pertama"
description: "Pada malam pertama Tottertop diuji penuh, muncul tiga bug seputar “Perfect” dan rekor. Apa saja bug itu dan bagaimana kami memperbaikinya."
excerpt: "“Perfect” pada blok yang justru merobohkan menara, blok pertama yang jatuh di lantai satu, rekor yang hilang saat runtuh: tiga bug dalam satu malam."
copy_review: iris 2026-11-14
published: 2026-11-17T14:45+09:00
---
Pada 11 November, begitu versi pertama yang bisa dimainkan jadi, kami menghabiskan satu malam memainkannya dan mencatat semua yang terasa janggal. Tiga di antaranya kecil, tetapi masing-masing mengubah rasa permainan ini.

## “Perfect” yang diukur dari tempat yang salah

Saat blok mendarat sangat dekat dengan titik tengah, gim menampilkan “Perfect” dan melanjutkan rentetan Anda. Pemeriksaan pertama kami mengukur selisihnya dari pusat area sentuh. Blok yang bertumpu penuh di alasnya selalu punya selisih nol di sana, jadi blok pertama selalu “Perfect” di mana pun ia mendarat. Lebih buruk lagi, jika ia mendarat lebih dari sekitar seperlima blok dari tengah, menara terguling, dan layar menampilkan “Perfect!” serta “Menara runtuh di lantai 1” sekaligus. Sekarang kami menilainya dari pusat permukaan tempat blok mendarat.

## “Perfect” untuk menara yang tetap roboh

Bahkan setelah perbaikan itu, blok yang diletakkan di tengah bagian atas masih bisa merobohkan seluruh menara pada saat yang sama, karena titik berat gabungannya sudah melewati sambungan di bawahnya. Dalam 127 dari 300 permainan simulasi berskrip, “Perfect” dan keruntuhan muncul bersamaan. Kini pendaratan yang tidak mungkin bertahan tidak pernah mendapat “Perfect”.

Blok pertama juga diubah: sekarang ia mengendap di alasnya dan menjadi titik acuan kemiringan, sehingga ia tidak bisa merobohkan menara sendirian. Dalam simulasi bot kami, rata-rata pemain biasa naik dari 12,4 menjadi 15,9 lantai, dan permainan yang berakhir di lantai empat atau lebih rendah turun dari 48 menjadi 11 dari 200.

## Rekor yang tidak tersimpan

Keruntuhan sengaja dibuat lambat: satu detik pertama diputar dengan kecepatan 0,45× agar Anda bisa melihat apa yang terjadi. Namun rekor baru ditulis di layar hasil, sekitar 1,6 detik kemudian, sehingga keluar di tengah animasi membuatnya hilang. Sekarang rekor disimpan begitu keruntuhan sudah pasti.

## Mengapa kami menuliskannya

Ketiganya bukan masalah yang cerdas. Masing-masing adalah tempat gim ini mengatakan sesuatu yang tidak benar kepada pemain, dan hanya bisa ditemukan dengan bermain. Kami berencana terus melakukannya.
