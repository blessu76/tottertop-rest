---
slug: 2026-11-16-one-tower-for-everyone
lang: id
title: "Satu menara untuk semua orang: cara kerja seed harian"
description: "Di versi uji coba, menara harian memberi semua pemain urutan blok yang sama pada hari yang sama. Bagaimana tanggal menjadi menara, dan mengapa UTC."
excerpt: "Menara harian hanya berarti jika semua orang benar-benar mendapat menara yang sama. Begini cara kami mengubah satu tanggal menjadi urutan blok yang identik di setiap ponsel di dunia."
copy_review: iris 2026-11-14
published: 2026-11-16T16:30+09:00
---
Salah satu ide yang kami inginkan sejak awal adalah menara harian: selama satu hari, semua orang mendapat blok yang sama dalam urutan yang sama, sehingga jumlah lantai berarti hal yang sama bagi semua orang. Kedengarannya sederhana, dan hanya berhasil jika beberapa detail membosankan sudah benar.

## Tanggal menjadi seed

Urutan blok berasal dari sebuah seed, dan seed berasal dari tanggal. Dua ponsel yang berangkat dari tanggal yang sama menyusun urutan yang sama, tanpa server di antaranya. Kami sengaja membuat satu pengecualian: blok pertama di setiap menara selalu blok persegi polos, supaya satu ronde tidak pernah dibuka dengan sesuatu yang canggung.

## Mengapa UTC

Kalau menara harian mengikuti tanggal lokal tiap ponsel, pemain di Seoul dan pemain di São Paulo akan berada di menara yang berbeda hampir sepanjang hari. Karena itu tanggalnya diambil dari UTC. Menara baru muncul pada saat yang sama di mana-mana, yaitu pukul 9 pagi di Korea. Kami menulis pengujian untuk batas UTC dan untuk zona waktu Korea, karena di situlah bug "hari ini tanggal berapa?" bersembunyi.

## Masukan sama, menara sama

Ini hanya berlaku jika gamenya sendiri deterministik. Mesinnya berjalan dengan jam tetap 120 langkah per detik dan memisahkan aturannya dari kode penggambaran, sehingga urutan blok dan fisikanya tidak bergantung pada seberapa cepat ponsel. Di versi uji coba, layar beranda menyimpan dua skor terbaik di perangkat: satu untuk permainan bebas dan satu untuk menara hari ini, yang direset saat tanggal berganti.

## Yang belum kami kerjakan

Belum ada server, papan peringkat, maupun cara membandingkan skor dengan orang lain. Untuk saat ini, menara harian adalah teka-teki bersama yang dimainkan sendirian. Apakah nanti akan berkembang lebih jauh, belum diputuskan.
