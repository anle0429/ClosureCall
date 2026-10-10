# Bàn giao ClosureCall V2

Trạng thái: **READY_WITH_DISCLOSED_LIMITATIONS / NOT_SUBMITTED**. Phần kỹ thuật đã được kiểm tra trong phạm vi dưới đây. Bạn sẽ tự xử lý portal, team, quyền giám khảo và Submit sau khi chuẩn bị xong; chưa có bản nộp hay receipt. Goal đầy đủ chưa đạt bước nộp được xác nhận.

Bản đang chạy private: source `e5f7801829aaa1f7cfd326e02e415f8389fa3dde`, image `sha256:11bddbc767275d8af7d603511596cc432b5862fe07fd880d5404fac8d13f7184`, container closurecall-app-1 trên Linode 172.234.201.174. Restart thực tế 2026-10-10T22:59:42.908771Z. SHA tài liệu được theo dõi riêng trong RELEASE_MANIFEST.json và Git; push tài liệu không deploy lại app.

Đã xác minh:

- 65 tests Windows; 65 tests trong đúng image Linux deploy. Giữ nguyên validator/authority/budgets; sửa tối thiểu prompt để model dùng đúng mã bằng chứng của feed NWS rỗng.
- Ba KC evaluation mới liên tiếp có nguồn thật/AI active; natural normal, approve qua UI. Một run có sáu tool events/ba model calls; hai run có năm/hai. Trace đủ năm tools riêng biệt.
- Site cố định có Flood Watch thật đang áp dụng lúc thu thập; không còn Flash Flood Warning cũ. Kết quả giữ unsupported_hazard/low confidence/no candidate. Override closure chỉ là test giả lập có lý do rõ, không xác minh an toàn địa phương.
- Hai package kiểm tra đủ 12 người, essential/accessibility/telework/offsite/no-shift và manual deferred follow-up. Tất cả là drafts. Browser export khớp API/replay; counters không có decision/batch trùng sau double-click.
- Sáu lịch sử gốc và hai quyết định demo mới giữ nguyên sau restart. Backup sáu records đã restore trên container/volume riêng; actual HTTP, integrity, outbox/export/replay và thay roster/rules đều khớp, không gọi nguồn/model/tính lại. Container thử đã dừng; production không bị thay dữ liệu.
- Cloud Manager VM closurecall-hackmidwest RUNNING, Chicago; ảnh crop không chứa account/billing/key. Diễn tập UI của agent: 86.005 và 123.789 giây; chưa phải rehearsal lời nói của bạn.

Truy cập: http://127.0.0.1:8081/ qua tunnel đang mở. Khi cần mở lại, chạy `scripts/open_tunnel.ps1` trong PowerShell tại repo, nhập passphrase trực tiếp vào terminal. Đăng nhập bằng manager credentials trong `.env`, không chiếu secrets. `DEMO_RECOVERY.md` có đường dẫn/key pin/backup/restart/rollback cụ thể. Operator URL và private GitHub chưa cho phép giám khảo truy cập.

Backup mới: `/app/data/backups/closurecall-20261010T225942Z.sqlite3` chứa tám quyết định; backup đã drill là `closurecall-20261010T225050Z.sqlite3` chứa sáu. Không restore bản cũ đè các quyết định mới để rollback code. Code rollback chưa được chạy trong production; cần tuân thủ freeze của BTC.

Rủi ro còn lại theo ảnh hưởng: (1) chưa nộp/chưa xác nhận judge access/team eligibility; (2) thời tiết ngày demo có thể đổi, cảnh báo cũ phải là REPLAY; (3) AI có thể degrade dù ba KC smokes mới pass; (4) chưa tập lời nói bấm giờ; (5) không có ngưỡng USDA chính thức, thông báo thật, scheduler hay kiểm chứng local safety. High-wind/high-AQ LIVE chưa xác minh. Backend duration chỉ là bốn quan sát riêng lẻ, không phải SLA.

Cần bạn thực hiện khi sẵn sàng: xác nhận team/tracks/portal/access với BTC; tập `DEMO_SCRIPT.md`; dùng `SUBMISSION.md` làm draft trung thực, kiểm tra các trường/điều khoản rồi nộp đúng một project và lưu receipt/trạng thái Submitted. Hạn vận hành 08:00 ngày 11/10/2026 America/Chicago, trừ cập nhật BTC đã xác minh. Không coi file draft, private repo hay upload đơn thuần là đã nộp.

Không mở public/firewall/DNS, cấp quyền người ngoài, tạo tài nguyên trả phí, gửi email/SMS/voice hay Submit. VM và dữ liệu giữ lại để chấm; không tự xóa sau demo. Sau sự kiện, bạn quyết định thu hồi quyền/tunnel/credentials và tài nguyên. Bằng chứng/tests/report nằm trong evidence/release và các tài liệu gốc của repo.
