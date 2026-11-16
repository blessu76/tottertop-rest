---
slug: 2026-11-16-one-tower-for-everyone
lang: vi
title: "Một tháp cho mọi người: hạt giống hằng ngày hoạt động ra sao"
description: "Trong các bản thử nghiệm, tòa tháp hằng ngày đưa cho mọi người chơi cùng một thứ tự khối trong cùng một ngày. Ngày tháng trở thành tòa tháp như thế nào, và vì sao dùng UTC."
excerpt: "Tòa tháp hằng ngày chỉ có ý nghĩa nếu mọi người thật sự nhận được cùng một tòa. Cách chúng tôi biến một ngày thành thứ tự khối giống hệt nhau trên mọi chiếc điện thoại trên thế giới."
copy_review: iris 2026-11-14
published: 2026-11-16T16:30+09:00
---
Một ý tưởng chúng tôi muốn có từ sớm là tòa tháp hằng ngày: trong một ngày, mọi người nhận cùng các khối theo cùng thứ tự, nên số tầng có ý nghĩa như nhau với tất cả. Nghe thì đơn giản, và nó chỉ hoạt động khi một vài chi tiết nhàm chán được làm đúng.

## Ngày tháng trở thành hạt giống

Chuỗi khối đến từ một hạt giống, và hạt giống đến từ ngày tháng. Hai chiếc điện thoại xuất phát từ cùng một ngày sẽ dựng cùng một chuỗi, không cần máy chủ ở giữa. Chúng tôi cố ý tạo một ngoại lệ: khối đầu tiên của mọi tòa tháp luôn là khối vuông trơn, để một ván không bao giờ mở đầu bằng thứ gì đó khó chịu.

## Vì sao dùng UTC

Nếu tòa tháp hằng ngày theo ngày địa phương của từng điện thoại, người chơi ở Seoul và người chơi ở São Paulo sẽ ở trên hai tòa tháp khác nhau trong phần lớn thời gian của ngày. Vì vậy ngày được lấy theo UTC. Một tòa tháp mới xuất hiện cùng một khoảnh khắc ở mọi nơi, tức là 9 giờ sáng ở Hàn Quốc. Chúng tôi đã viết các bài kiểm thử cho ranh giới UTC và cho múi giờ Hàn Quốc, vì đó là nơi các lỗi kiểu "hôm nay là ngày mấy?" ẩn nấp.

## Cùng đầu vào, cùng một tòa tháp

Điều này chỉ đúng nếu bản thân trò chơi mang tính xác định. Engine chạy trên một đồng hồ cố định 120 bước mỗi giây và tách các quy tắc khỏi mã vẽ, nên chuỗi khối và vật lý không phụ thuộc vào tốc độ của điện thoại. Trong các bản thử nghiệm, màn hình chính lưu hai điểm cao nhất ngay trên thiết bị: một cho chế độ chơi tự do và một cho tòa tháp hôm nay, được đặt lại khi ngày thay đổi.

## Những gì chúng tôi chưa làm

Hiện chưa có máy chủ, chưa có bảng xếp hạng và chưa có cách nào để so điểm với người khác. Hiện tại, tòa tháp hằng ngày là một câu đố chung mà bạn chơi một mình. Liệu nó có phát triển thành thứ gì hơn thế hay không, chúng tôi chưa quyết định.
