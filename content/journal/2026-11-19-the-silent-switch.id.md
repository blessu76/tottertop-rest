---
slug: 2026-11-19-the-silent-switch
lang: id
title: "Suara menyala, tak terdengar: tombol senyap iPhone"
description: "Menyalakan suara di pengaturan Tottertop tidak berefek pada iPhone dengan tombol senyap aktif. Penyebabnya, apa yang kami ubah, dan apa yang belum diperiksa di perangkat asli."
excerpt: "Pengaturannya aktif, jalur kodenya benar, tetapi gim tetap senyap. Penyebabnya satu mode audio yang menuruti tombol senyap."
copy_review: iris 2026-11-16
published: 2026-11-19T14:30+09:00
---
Saat memeriksa pengaturan suara dan getaran, kami menemukan masalah yang tampak seperti bug pada pengaturan tetapi bukan: Anda bisa menyalakan suara dan tetap tidak mendengar apa pun.

## Jalur kodenya baik-baik saja

Kami menelusuri setiap tombol dari layar Pengaturan hingga saat suara atau getaran diminta: nilai yang tersimpan, tempat nilai itu dibaca kembali, gerbang yang melewati suara bila pengaturan mati, dan setiap kejadian dalam gim yang meminta umpan balik. Semuanya tersambung. Kelima berkas suara ada dan kunci simpanannya cocok.

## Penyebabnya: mode audio yang sopan

Di iPhone, cara sebuah aplikasi mendeklarasikan audionya menentukan apakah ia menuruti tombol senyap. Gim kami memakai mode sopan yang dibuat untuk suasana latar, dan mode itu mengikuti tombol senyap serta kunci layar. Jadi dengan tombol aktif, pengaturan menunjukkan "nyala" dan ponsel tetap sunyi.

## Apa yang kami ubah

- Di iPhone, gim kini memakai mode pemutaran, sehingga tombol senyap tidak lagi membisukan suara gim. Suara tetap bercampur dengan aplikasi lain, jadi musik yang sudah Anda putar terus berjalan.
- Di Android, suara ditandai sebagai suara gim dan tidak merebut fokus audio.
- Menyalakan getaran atau suara kini langsung memberi satu getaran atau suara singkat, supaya Anda tahu fungsinya bekerja. Mematikannya tetap sunyi.
- Android mendapat izin getar secara eksplisit.
- Tes mencakup mode audio, isyarat sekali saat dinyalakan, dan izinnya.

## Yang belum kami periksa

Semua ini terverifikasi di kode dan tes, belum di ponsel sungguhan. Kami masih perlu memastikan, pada iPhone dengan tombol senyap aktif, bahwa suara terdengar; bahwa musik dari aplikasi lain tetap berputar; dan bahwa getaran terasa. Pengaturan haptik sistem atau mode hemat daya pada ponsel juga bisa membungkam getaran, dan itu di luar kendali kami. Kami akan memeriksanya di build uji berikutnya dan menuliskan hasilnya.
