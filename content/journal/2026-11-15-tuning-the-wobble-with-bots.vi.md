---
slug: 2026-11-15-tuning-the-wobble-with-bots
lang: vi
title: "Chỉnh độ lắc bằng bot thay vì bằng tay"
description: "Cách chúng tôi đặt độ khó cho Tottertop trước khi có ai chơi: ba bot với nhịp chạm khác nhau, mỗi bot 200 ván, kèm một lưu ý thẳng thắn."
excerpt: "Trước khi có người chơi được Tottertop, chúng tôi chỉnh độ khó bằng ba bot với trình độ khác nhau, mỗi bot 200 ván. Những con số nói lên điều gì, và điều gì chúng không thể nói."
copy_review: iris 2026-11-14
published: 2026-11-15T14:30+09:00
---
Một game xếp chồng vật lý sống hay chết là do cảm giác lắc khó đến mức nào. Ngày 11 tháng 11, khi vòng lặp một ván đầy đủ đầu tiên chạy được, chưa ai chơi thử cả, nên chúng tôi chỉnh bằng bot.

## Ý tưởng

Engine được viết bằng mã Dart thuần, chạy theo nhịp cố định 120 bước mỗi giây, nên cùng một đầu vào luôn cho ra cùng một tòa tháp. Nhờ vậy rất dễ đặt một bot vào chỗ người chơi. Bot của chúng tôi nhắm vào thời điểm thả tốt nhất, rồi chạm với một sai số nhịp ngẫu nhiên lấy từ phân phối chuẩn. Sai số càng lớn thì tay càng kém vững.

Chúng tôi làm ba bot và chạy mỗi bot 200 ván:

| Bot | Sai số chạm | Số tầng trung bình | Đạt 30+ tầng |
|---|---|---|---|
| Chuyên gia (còn dự đoán độ nghiêng) | 30 ms | 29,4 | 48% |
| Giỏi | 50 ms | 18,1 | 1,5% |
| Bình thường | 70 ms | 12,4 | 0% |

Với bot bình thường, một ván trong mười kết thúc trước tầng 2, một nửa đạt tới tầng 14, và chín ván trong mười kết thúc trước tầng 20.

## Mục tiêu của chúng tôi

Mục tiêu rất đơn giản: người chơi bình thường nên đạt trung bình khoảng 10 đến 15 tầng, còn người chơi rất giỏi có thể vượt 30 tầng. Bảng trên rơi đúng vào khoảng đó, nên chúng tôi giữ nguyên các giá trị. Chúng tôi chỉnh một vài con số: độ nghiêng tích tụ mạnh đến đâu, mỗi lần tiếp đất làm tháp rung mạnh ra sao, và độ lắc dịu lại nhanh thế nào.

## Điều này không cho chúng tôi biết

Bot không phải con người. Nó không bao giờ mệt, không hoảng khi tháp nghiêng, và không bao giờ nảy ra ý thử một điều ngớ ngẩn. Những con số này chỉ cho thấy đường cong độ khó hợp lý trên giấy, chứ không nói rằng game cho cảm giác đúng. Phần đó cần đến đôi tay thật, và chúng tôi sẽ kiểm tra lại khi mọi người chơi các bản thử nghiệm.
