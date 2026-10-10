# Chú giải cho người trình bày ClosureCall

Dùng cùng `DEMO_SCRIPT.md`: lời nói trước giám khảo bằng tiếng Anh; tài liệu này giúp bạn hiểu ý, chuyển nhánh và tránh mô tả sai. Đây không phải bằng chứng bạn đã tập nói. Hai lần agent thao tác UI mất 86.005/123.789 giây, có overhead công cụ; thời gian lời nói chưa được đo.

| Mốc | Ý chính cần truyền đạt | Điểm cần nhìn trên UI |
|---|---|---|
| 0–20 giây | Vấn đề là giúp người quản lý có dữ liệu và lưu được quyết định. Facility, ca và nhân viên giả lập; ngưỡng hành động là prototype. | Tên facility, tọa độ/timezone, checkbox special shift. Chọn ca mới có giờ kết thúc trong tương lai; cuối tuần phải ghi rõ ca giả lập. |
| 20–75 giây | Nút Evaluate thực sự gọi NWS/AQ cho điểm đó. HTTP 200/0 alerts là feed rỗng hợp lệ; unavailable là thiếu dữ liệu. AQ là mô hình grid, không phải cảm biến trong tòa nhà. | Fetched UTC, source URL, valid time, alert validity và phần giao với ca. Trong lúc AI chạy, nói về dữ liệu vừa hiển thị; không giả rằng brief đã xong. |
| 75–110 giây | Rules tạo candidate khi đủ cơ sở; model chọn references/focus, không quyết định đóng cửa. Human manager approve hoặc override có lý do. | Recommendation tự nhiên trước override; policy/rule version, confidence và What would change this. `unsupported_hazard`/low/no candidate phải được giải thích, không đổi thành normal cho dễ demo. |
| 110–140 giây | Mỗi người có route, lý do, chỉ dẫn và channel. Essential cần supervisor; telework có informational draft/manual follow-up; offsite/no-shift không nhận chỉ dẫn khẩn tại site. | Harper Quinn, Jordan Lake, Casey Brook. `queued_demo` vẫn là draft; voice_accessible là nhãn kênh dự kiến, không có cuộc gọi. |
| 140–165 giây | Replay dựng lại đúng dữ liệu và quyết định tại thời điểm lưu, không lấy thời tiết/model mới. Export là gói lịch sử. | Badge REPLAY, collection/decision timestamps, Export frozen decision package. Timeline giữ provenance nguồn LIVE ban đầu, không có nghĩa đang fetch lại. |
| 165–180 giây | Strands có năm tools riêng biệt; app/SQLite chạy trên Linode. Nêu một giới hạn rõ rồi kết thúc. | Tool timeline, deployment footer. Không đọc secrets, không chiếu `.env` hoặc Cloud Manager account/billing. |

Ba câu chuyển nhánh có thể dùng nguyên văn:

- Khi chờ: **“The model is still running. The source evidence and deterministic assessment are already visible; I won't present an unfinished brief as complete.”** Đừng đứng im hoặc hứa thời gian phản hồi cố định.
- Khi degrade: **“AI is degraded for this run. The stored source evidence and deterministic assessment remain available, and the manager retains the decision.”** Chỉ nói khi trạng thái của run đang mở thực sự degraded; không dùng model success cũ thay vào.
- Khi replay: **“This is historical replay, collected at the timestamp shown. It is not current weather, and replay makes no source or model calls.”** Luôn nói rõ trước khi chuyển sang record đã lưu.

Nếu quá 75 giây vẫn chờ inference, mở historical Replay và nói rõ timestamp. Thao tác này dừng polling UI; job backend vẫn chạy. Muốn quay lại đúng run sau demo: reload, đăng nhập lại; session storage giữ run ID. Không bấm Evaluate nhiều lần để thử “làm nhanh”.

Các mốc đã ghi, không phải dữ liệu LIVE mới:

- KC normal/AI active: collected 22:54:46 UTC ngày 10/10; approve 22:55:50; record `a9cfe7dc-2336-4cde-8f55-694defe160ad`.
- Fixed site Watch: NWS fetched 22:56:35.991537 UTC, ca 23:11–01:11 UTC, America/New_York; no candidate/unsupported/low. Closure record `16a170c1-af9b-4950-86b2-a3eecf1ad26b` là **controlled synthetic test override**, không phải kết luận an toàn thực địa.
- Flash Flood Warning cũ hết hạn **22:30 UTC ngày 10/10**. Tên facility giữ lại từ lịch sử, không chứng minh có Warning hiện tại. Chỉ mở record này dưới nhãn REPLAY.
- Old KC degraded record `fc569eb8-54bd-4989-b9b7-fedcc46b3896` cho thấy ValueError đã lưu; đừng mô tả đó là một failure mới vừa xảy ra.

Tập với đồng hồ một lần trước khi pitch, dùng browser đã đăng nhập và đọc lời Anh trong DEMO_SCRIPT.md. Mục tiêu nói khoảng 150–165 giây là kế hoạch nội bộ, không phải SLA. Nếu chưa tập, giữ trạng thái human rehearsal NOT VERIFIED. Không khẳng định USDA phê duyệt ngưỡng, đã gửi thông báo, tự động follow-up, impact/latency thống kê hay đã Submit.
