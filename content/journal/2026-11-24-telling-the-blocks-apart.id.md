---
slug: 2026-11-24-telling-the-blocks-apart
lang: id
title: "Membedakan balok: uji untuk buta warna"
description: "Saat set warna balok ditambahkan ke Tottertop, simulasi buta warna menemukan dua balok bawaan yang terlihat hampir sama. Apa yang kami ukur dan apa yang kami ubah."
excerpt: "Dalam simulasi buta warna hijau, balok biru dan ungu nyaris sama. Bagaimana uji kontras menangkapnya, dan aturan yang kini harus dipenuhi setiap set warna."
copy_review: iris 2026-11-20
published: 2026-11-24T14:45+09:00
---
Di menara yang miring, warna punya tugas nyata: menunjukkan di mana satu balok berakhir dan balok berikutnya dimulai. Karena itu, saat kami menambahkan set warna balok pada 15 November, kami juga menambahkan uji yang memeriksa apakah balok tetap mudah dibedakan oleh pemain dengan gangguan penglihatan warna.

## Empat set, dibuka dengan bermain

Permen adalah set bawaan. Pastel terbuka di 12 lantai, Laut di 20, dan Senja di 30, ketinggian yang sama dengan saat kamu mendapat gelar. Yang dihitung adalah ketinggian terbaikmu sepanjang masa, di Main bebas atau Menara hari ini, jadi rekor lama langsung membukanya. Set dipilih di Pengaturan, dan warna yang sama dipakai di menara, di pratinjau balok berikutnya, dan di layar beranda.

## Apa yang dilakukan uji ini

Untuk setiap set, uji ini mengambil tiap warna balok dan menyimulasikan tampilannya pada tiga jenis utama buta warna, yaitu saat merah, hijau, atau biru sulit dibedakan, pada tingkat terkuat, dengan model yang sudah diterbitkan (Machado dkk., 2009). Hal yang sama dilakukan untuk penglihatan warna biasa. Lalu uji mengukur seberapa jauh jarak antarwarna, sebagai selisih warna (CIELAB ΔE).

Permukaan balok harus berjarak minimal 10 satu sama lain. Setiap balok juga punya tepi bawah yang lebih gelap, yang harus tetap lebih gelap dari permukaannya dan berjarak minimal 9 darinya serta dari permukaan balok di bawahnya.

## Yang ditemukannya

Set bawaan kami sendiri gagal. Dalam simulasi buta warna hijau, balok biru dan ungu hanya berjarak 0,8, praktis warna yang sama. Kami menggeser warna balok masing-masing paling banyak 12, sampai pasangan terdekat di Permen berjarak 11,5. Yang berubah hanya baloknya; teks dan tombol di bagian lain game tetap dengan warnanya.

Pasangan terdekat dari jenis apa pun (permukaan atau tepi) di tiap set kini: Permen 11,5, Pastel 10,7, Laut 9,5, dan Senja 12,3.

## Yang tidak bisa diberitahukan uji ini

Ini perhitungan dengan model penglihatan, bukan orang yang melihat ponsel. Kami belum memeriksanya bersama pemain buta warna, dan kecerahan layar serta cahaya siang juga mengubah cara warna terlihat. Sampai orang sungguhan memeriksanya, kami menganggapnya belum diperiksa.
