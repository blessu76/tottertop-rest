---
slug: 2026-11-19-the-silent-switch
lang: vi
title: "Bật âm thanh mà không nghe gì: công tắc im lặng của iPhone"
description: "Bật âm thanh trong phần cài đặt của Tottertop không có tác dụng trên iPhone đang bật công tắc im lặng. Nguyên nhân, điều chúng tôi đã đổi và điều chưa kiểm tra trên máy thật."
excerpt: "Cài đặt đã bật, luồng mã vẫn đúng, vậy mà trò chơi vẫn im lặng. Nguyên nhân là một chế độ âm thanh tuân theo công tắc im lặng."
copy_review: iris 2026-11-16
published: 2026-11-19T14:30+09:00
---
Khi kiểm tra các cài đặt âm thanh và rung, chúng tôi phát hiện một vấn đề trông như lỗi của cài đặt nhưng thật ra không phải: bạn có thể bật âm thanh mà vẫn không nghe thấy gì.

## Luồng mã không có vấn đề

Chúng tôi lần theo từng công tắc từ màn hình Cài đặt đến lúc âm thanh hoặc rung được yêu cầu: giá trị đã lưu, nơi đọc lại giá trị đó, cổng bỏ qua âm thanh khi cài đặt tắt, và mọi sự kiện trong trò chơi yêu cầu phản hồi. Tất cả đều khớp nhau. Năm tệp âm thanh đều có đủ và các khóa lưu trữ trùng khớp.

## Nguyên nhân: một chế độ âm thanh quá lịch sự

Trên iPhone, cách một ứng dụng khai báo âm thanh của mình quyết định việc nó có tuân theo công tắc im lặng hay không. Trò chơi của chúng tôi dùng chế độ lịch sự dành cho âm thanh nền, và chế độ đó làm theo công tắc im lặng cùng khóa màn hình. Vì vậy khi công tắc bật, cài đặt báo "bật" mà điện thoại vẫn im lặng.

## Điều chúng tôi đã đổi

- Trên iPhone, trò chơi giờ dùng chế độ phát, nên công tắc im lặng không còn tắt tiếng trò chơi. Âm thanh vẫn hòa cùng các ứng dụng khác, nên nhạc bạn đang nghe vẫn tiếp tục.
- Trên Android, âm thanh được đánh dấu là âm thanh trò chơi và không giành quyền ưu tiên âm thanh.
- Bật rung hoặc âm thanh giờ sẽ cho một lần rung hoặc một tiếng ngắn ngay lập tức, để bạn biết nó hoạt động. Khi tắt thì vẫn im lặng.
- Android được cấp quyền rung một cách tường minh.
- Các bài kiểm tra bao phủ chế độ âm thanh, tín hiệu một lần khi bật, và quyền đó.

## Điều chúng tôi chưa kiểm tra

Tất cả những điều này mới được xác minh trong mã và bài kiểm tra, chưa phải trên điện thoại thật. Chúng tôi vẫn cần xác nhận, trên iPhone đang bật công tắc im lặng, rằng âm thanh phát ra; rằng nhạc từ ứng dụng khác vẫn tiếp tục; và rằng rung hoạt động. Cài đặt phản hồi xúc giác của hệ thống hoặc chế độ tiết kiệm pin cũng có thể làm tắt rung, và việc đó nằm ngoài tầm kiểm soát của chúng tôi. Chúng tôi sẽ kiểm tra ở bản thử nghiệm tiếp theo và ghi lại những gì tìm thấy.
