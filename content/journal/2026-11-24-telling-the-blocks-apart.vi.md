---
slug: 2026-11-24-telling-the-blocks-apart
lang: vi
title: "Phân biệt các khối: kiểm tra cho người mù màu"
description: "Khi thêm các bộ màu khối vào Tottertop, một mô phỏng mù màu phát hiện hai khối mặc định trông gần như giống hệt nhau. Chúng tôi đã đo gì và đổi gì."
excerpt: "Trong mô phỏng mù màu xanh lục, khối xanh dương và khối tím gần như y hệt. Bài kiểm tra độ tương phản đã bắt được điều đó ra sao, và quy tắc mọi bộ màu giờ phải vượt qua."
copy_review: iris 2026-11-20
published: 2026-11-24T14:45+09:00
---
Trên một tòa tháp đang nghiêng, màu sắc có việc thật để làm: cho thấy một khối kết thúc ở đâu và khối tiếp theo bắt đầu từ đâu. Vì vậy, khi thêm các bộ màu khối vào ngày 15 tháng 11, chúng tôi cũng thêm một bài kiểm tra để chắc rằng người chơi có khiếm khuyết về nhìn màu vẫn dễ phân biệt các khối.

## Bốn bộ màu, mở khóa bằng cách chơi

Kẹo ngọt là bộ mặc định. Màu phấn mở ở 12 tầng, Biển ở 20 tầng và Hoàng hôn ở 30 tầng, cũng là những độ cao bạn nhận danh hiệu. Trò chơi tính theo độ cao tốt nhất từ trước tới nay của bạn, ở Chơi tự do hoặc Tháp hôm nay, nên các kỷ lục cũ mở khóa ngay. Bạn chọn bộ màu trong Cài đặt, và cùng những màu đó sẽ hiện trên tháp, trong ô xem trước khối tiếp theo và ở màn hình chính.

## Bài kiểm tra làm gì

Với mỗi bộ, bài kiểm tra lấy từng màu khối và mô phỏng màu đó trông thế nào với ba dạng mù màu chính, khi khó phân biệt đỏ, lục hoặc lam, ở mức nặng nhất, dùng một mô hình đã được công bố (Machado và cộng sự, 2009). Nó cũng làm như vậy với thị lực màu thông thường. Sau đó đo khoảng cách giữa các màu bằng độ chênh lệch màu (CIELAB ΔE).

Các mặt khối phải cách nhau ít nhất 10. Mỗi khối còn có một viền dưới tối hơn; viền này phải luôn tối hơn mặt khối và cách ít nhất 9 so với chính mặt đó và với mặt của khối bên dưới.

## Những gì nó phát hiện

Chính bộ mặc định của chúng tôi không đạt. Trong mô phỏng mù màu xanh lục, khối xanh dương và khối tím chỉ cách nhau 0,8, gần như cùng một màu. Chúng tôi dịch các màu khối, mỗi màu tối đa 12, cho đến khi cặp gần nhất trong bộ Kẹo ngọt cách nhau 11,5. Chỉ các khối thay đổi; chữ và nút ở những phần khác của trò chơi vẫn giữ màu cũ.

Cặp gần nhất thuộc bất kỳ loại nào (mặt hoặc viền) trong mỗi bộ hiện là: Kẹo ngọt 11,5, Màu phấn 10,7, Biển 9,5 và Hoàng hôn 12,3.

## Điều bài kiểm tra này không cho biết

Đây là phép tính trên một mô hình thị giác, không phải một người nhìn vào điện thoại. Chúng tôi chưa kiểm tra cùng người chơi mù màu, và độ sáng màn hình hay ánh nắng ban ngày cũng làm màu trông khác đi. Cho đến khi có người thật kiểm tra, chúng tôi xem nó là chưa kiểm tra.
