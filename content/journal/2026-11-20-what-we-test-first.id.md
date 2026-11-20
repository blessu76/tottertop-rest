---
slug: 2026-11-20-what-we-test-first
lang: id
title: "Apa yang kami uji sebelum apa pun dirilis"
description: "Tur singkat pemeriksaan yang dilalui Tottertop sebelum sebuah build keluar: tes unit, tes tata letak 320 px di 12 bahasa, uji coba bot, dan apa yang hanya bisa dijawab ponsel asli."
excerpt: "Hampir 700 tes otomatis, pemeriksaan tata letak di setiap bahasa, dan pemain bot. Serta daftar hal yang tidak bisa dituntaskan tes mana pun."
copy_review: iris 2026-11-16
published: 2026-11-20T14:30+09:00
---
Gim kecil pun tetap butuh banyak pemeriksaan yang membosankan. Inilah yang berdiri di antara sebuah perubahan dan build uji, dan di mana pemeriksaan itu berhenti.

## Gerbang sebelum setiap commit

Setiap perubahan melewati satu skrip yang merapikan kode, menganalisisnya, dan menjalankan tes. Jika tidak hijau, tidak ada yang di-commit dan tidak ada build yang dibuat. Saat ini aplikasi punya hampir 700 tes otomatis, yang mencakup aturan permainan, menara harian, penyimpanan dan pemuatan, pengaturan, dan bahasa.

## Setiap bahasa, layar sempit

Kata-kata dalam bahasa Jerman dan Vietnam panjang, dan bahasa Thai tidak punya spasi sebagai tempat memutus baris. Karena itu tes tata letak membangun setiap layar dalam semua 12 bahasa pada lebar 320 px dan gagal jika ada teks yang meluap. Situs web melewati pemeriksaan sejenis pada 320 dan 375 px, lalu lagi pada lebar tablet dan desktop.

## Bot yang bermain untuk kami

Untuk menyetel tingkat kesulitan, kami tidak mengandalkan jempol sendiri. Pemain simulasi dengan beberapa tingkat keterampilan memainkan ratusan ronde, lalu kami membandingkan seberapa jauh mereka sampai. Begitulah kami bisa mengatakan bahwa satu perbaikan menaikkan rata-rata pemain berkemampuan menengah dari 12,4 menjadi 15,9 lantai, dan menurunkan ronde yang berakhir di lantai empat atau lebih rendah dari 48 menjadi 11 dari 200. Bot memberi tahu kami soal keseimbangan. Bot tidak memberi tahu apakah gimnya seru.

## Yang tidak bisa dituntaskan tes

Ponsel asli tetap memegang kata akhir untuk suara, getaran, rasa sentuhan, dan tampilan gim di bawah cahaya siang. Pemeriksaan itu dilakukan manual di perangkat, dan selama belum dilakukan, kami menandainya belum diperiksa, bukan menyebutnya baik-baik saja. Jika jurnal ini menyebut sesuatu sudah diverifikasi, berarti memang sudah. Jika tidak disebut, anggap belum.
