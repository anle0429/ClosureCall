# Chú giải cho người trình bày

Dùng với [script tiếng Anh](DEMO_SCRIPT.md). Candidate **3bc1ddd** ở 8084 là QA tách biệt: đánh giá mới là SYNTHETIC TEST, không gọi thời tiết/model. Linode vẫn chạy **a5681bc**, chưa nhận candidate; tunnel 8081 chưa mở lại trong lượt này. Đây là chuẩn bị portfolio sau hackathon, chưa đăng LinkedIn/public/nộp bài.

1. Chỉ tên facility, tọa độ, timezone và khoảng giờ làm việc. **Refresh time (+15 min)** đặt Start bằng bây giờ +15 phút, End giữ độ dài ca; sau đó phải bấm **Check conditions & recommendation** mới đánh giá. Refresh không làm mới dữ liệu lịch sử.
2. Phân biệt nguồn rỗng hợp lệ với thiếu nguồn. Trên 8084 nói rõ dữ liệu test; khi mở lịch sử nói “This is historical replay, not current weather.” AQ là mô hình, không phải cảm biến trong tòa nhà.
3. Đọc recommendation tự nhiên trước khi manager quyết định. Model đọc năm tools; rules đề xuất, người quản lý approve/override. Override cần lý do rõ; demo closure ở Watch là test, không phải xác minh an toàn.
4. Xem drafts: essential cần chỉ dẫn supervisor; telework deferred phải xử lý thủ công; offsite/no-shift có lý do loại; accessible voice là draft, chưa gọi ai.
5. Mở Saved decisions/Replay rồi download JSON hoặc memo. Giải thích evidence/rules/roster/actor/time/reason/drafts được giữ nguyên; không lấy nguồn/model mới.
6. Kết thúc bằng giới hạn thực: không phải USDA/OPM policy, không thay đội trực/OnSolve, chưa kiểm tra điện/nước/an ninh hay gửi thật.

Nếu quá mốc 65 giây vẫn chờ, nói đúng trạng thái rồi dùng lịch sử có timestamp. Không bấm Evaluate nhiều lần. Reload cần đăng nhập lại, có thể tiếp tục run ID đang lưu trong session.

Agent đã thao tác approve 153.088s/override 59.332s với overhead công cụ; đây không phải thời gian bạn tập nói hoặc latency model. Bạn cần tự tập 180 giây và kiểm tra Print nếu muốn in memo. Preview HTTP/download đã kiểm tra; print pagination chưa xác minh. [Q&A](PITCH_QA.md), [recovery](DEMO_RECOVERY.md).
