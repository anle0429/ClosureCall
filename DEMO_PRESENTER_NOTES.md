# Chú giải cho người trình bày ClosureCall

Dùng cùng `DEMO_SCRIPT.md`: lời nói trước giám khảo bằng tiếng Anh; tài liệu này giúp bạn hiểu ý, chuyển nhánh và tránh mô tả sai. Đây không phải bằng chứng bạn đã tập nói. Hai lần agent thao tác UI mất 86.005/123.789 giây, có overhead công cụ; thời gian lời nói chưa được đo.

Sau lượt feedback: bản 8081 vẫn chạy e5f7801. Candidate 656e8a0 có kiểm tra phòng vệ polygon/thời gian và nút tải memo HTML, chưa deploy. Khi demo production, dùng Replay và JSON export đang có; không chỉ người xem tới nút memo chưa tồn tại tại đó. Feedback là lời người dùng thuật lại cuộc trao đổi, không phải USDA phê duyệt hay đại diện đã test app.

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

Các câu hỏi bạn cần tự trả lời khi trình bày:

| Câu hỏi | Cách trả lời đúng với bản hiện tại |
|---|---|
| Dữ liệu áp dụng ở đâu, lúc nào? | Chỉ facility/tọa độ, timezone, Start–End, fetched time và hiệu lực alert. REPLAY là thời điểm lịch sử. Candidate kiểm thử fixture Wisconsin ngoài KC; đó không phải sự cố LIVE hay bảo đảm chặn mọi dữ liệu sai. |
| Model có quyền gì? | Đọc năm tools của snapshot hiện tại, chọn references/focus hợp lệ. Rules tạo đề xuất; manager ghi quyết định. Model không approve/send. |
| Nếu dữ liệu sai hoặc thiếu? | Phân biệt nguồn rỗng hợp lệ, nguồn lỗi và phần chưa xác minh. Kiểm tra kỹ thuật không phát hiện mọi thông tin sai có metadata nhất quán. Manager/đội trực cần xem điều kiện thực địa; weather/AQ chưa kiểm tra điện, nước hay an ninh. |
| Thông báo đã gửi chưa? | Chưa. Included/queued_demo là draft; channel là nhãn dự kiến; deferred cần supervisor xử lý thủ công. Package có thể hỗ trợ quy trình hiện có, chưa có OnSolve integration/import schema được thử. |
| Memo chứa gì? | Facility/ca/timezone, đề xuất gốc, quyết định cuối, actor/time/reason đã ghi, nguồn/hiệu lực/giới hạn và drafts. Candidate tạo cách trình bày mới từ bundle cũ với renderer version riêng; không sửa lịch sử, không gọi model lại. HTML tải được trong preview; agent browser chưa mở file để kiểm tra trực quan do chặn file protocol. |
| Có thay đội emergency/security không? | Không có bằng chứng cho điều đó. App hỗ trợ người trực/manager đọc dữ liệu và lưu quyết định; không có giám sát 24/7 hoặc nguồn cảnh sát/điện/nước. |

Câu Anh khi cần: “This supports the existing duty team and notification process. It does not establish local safety, replace a staffed emergency team, or integrate with OnSolve.” Giữ các mức operating posture của challenge; mô tả yes/no trong cuộc trao đổi không biến thành policy mới hoặc quyền xóa các mức đó.
