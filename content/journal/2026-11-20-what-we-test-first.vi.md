---
slug: 2026-11-20-what-we-test-first
lang: vi
title: "Chúng tôi kiểm tra gì trước khi phát hành"
description: "Điểm qua các bước kiểm tra Tottertop phải qua trước khi một bản dựng rời bàn làm việc: kiểm thử đơn vị, kiểm tra bố cục 320 px ở 12 ngôn ngữ, bot chơi thử, và điều chỉ điện thoại thật mới cho biết."
excerpt: "Gần 700 bài kiểm tra tự động, kiểm tra bố cục ở mọi ngôn ngữ, và các bot chơi thử. Cùng danh sách những điều không bài kiểm tra nào quyết định được."
copy_review: iris 2026-11-16
published: 2026-11-20T14:30+09:00
---
Một trò chơi nhỏ vẫn cần rất nhiều bước kiểm tra tẻ nhạt. Đây là những gì nằm giữa một thay đổi và một bản dựng thử, và nơi việc kiểm tra dừng lại.

## Một cổng trước mỗi lần commit

Mỗi thay đổi đều phải qua một tập lệnh duy nhất: định dạng mã, phân tích mã và chạy kiểm thử. Nếu không xanh thì không commit và không tạo bản dựng. Tại thời điểm viết bài, ứng dụng có gần 700 bài kiểm tra tự động, bao gồm luật chơi, tháp hằng ngày, lưu và tải, cài đặt và ngôn ngữ.

## Mọi ngôn ngữ, màn hình hẹp

Từ tiếng Đức và tiếng Việt dài, còn tiếng Thái không có dấu cách để ngắt dòng. Vì vậy bài kiểm tra bố cục dựng mọi màn hình ở cả 12 ngôn ngữ với chiều rộng 320 px và thất bại nếu có chữ nào tràn ra. Trang web cũng qua kiểm tra tương tự ở 320 và 375 px, rồi lại ở chiều rộng máy tính bảng và máy tính để bàn.

## Bot chơi thay chúng tôi

Để chỉnh độ khó, chúng tôi không dựa vào ngón tay của mình. Những người chơi giả lập với nhiều mức kỹ năng chơi hàng trăm ván, và chúng tôi so sánh xem họ đi được bao xa. Nhờ vậy chúng tôi có thể nói rằng một lần sửa đã nâng mức trung bình của người chơi trình độ trung bình từ 12,4 lên 15,9 tầng, và giảm số ván kết thúc ở tầng bốn trở xuống từ 48 còn 11 trên 200. Bot cho chúng tôi biết về độ cân bằng. Chúng không cho biết trò chơi có vui hay không.

## Điều không bài kiểm tra nào quyết định được

Điện thoại thật vẫn có tiếng nói cuối cùng về âm thanh, rung, cảm giác chạm và diện mạo của trò chơi dưới ánh sáng ban ngày. Những bước kiểm tra này được làm thủ công trên thiết bị, và cho đến khi làm xong, chúng tôi ghi là chưa kiểm tra thay vì nói là ổn. Nếu nhật ký này nói điều gì đã được xác minh, thì đúng là đã xác minh. Nếu không nói, hãy hiểu là chưa.
