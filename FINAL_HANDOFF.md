# Bàn giao lượt phản hồi USDA

Sponsor feedback pass: **FEEDBACK_PASS_COMPLETE_WITH_LIMITATIONS**.
Submission: **ON_HOLD / NOT_SUBMITTED; existing G4/G6 blockers unchanged by user choice.**

Lượt bổ sung đã xong trong timebox; không quay lại mission nộp bài. Feedback được lưu là lời bạn thuật lại, không phải policy/endorsement USDA hoặc chứng cứ đại diện đã test app. Bảng đầy đủ: SPONSOR_FEEDBACK_REVIEW.md; nguồn/ảnh/log/diff: FEEDBACK_MANIFEST.json và evidence/feedback.

Đã có từ trước: kiểm tra tọa độ request, strict snapshot/policy/evidence membership, agent read-only/bounded, human auth/approve/override, per-person drafts và frozen replay. Các bằng chứng LIVE/restore/Cloud Manager cũ được giữ đúng ngày/phiên bản; không gọi lại model hoặc mở điều tra ValueError lịch sử.

Khoảng trống mới được tái hiện offline: polygon ngoài facility vẫn được coi áp dụng; scope chưa xác minh có thể bị coi confirmed hoặc bỏ qua thành normal; ends kéo match vượt message expires; Cancel ngoài vị trí có thể xóa warning hợp lệ. Candidate sửa tại boundary hiện có: polygon coverage, outside khác unverified, metadata county/zone cho geometry null, interval giao với ca và supersession đúng scope. Null-geometry vẫn tin NWS point-filter, chưa có kiểm tra zone độc lập; nguồn sai nhưng metadata nhất quán vẫn có thể lọt. Không có sự cố Wisconsin/KC LIVE được quan sát.

Candidate source **656e8a0a5ee78d89064ddb47318bd2ec75e0b899**, image **sha256:84b3d897808d5ecd6aa81f9d1ea2f31f93dc5097309d444a375204bedda29a81**, tag closurecall-feedback:656e8a0a5ee78d89064ddb47318bd2ec75e0b899; **CHƯA DEPLOY**. Windows final 89 pass/12.67s; exact Linux image 89/6.43s; 24 cases mới, không phải 178 cases khác nhau. Một lần Windows bản chốt fail ở trace của test deadline 0,2 giây; testcase và full suite chạy lại nguyên trạng pass, nguyên nhân chưa xác minh, log fail còn nguyên. Không nới deadline hoặc sửa assertion.

Memo HTML mới đọc nguyên bundle đóng băng, tách recommendation/decision, có facility/ca/timezone, actor/time/reason đã ghi, evidence/basis/limits, decision ID/hash và drafts; renderer frozen-memo-v1 ghi riêng. Không sửa hash, nội dung drafts hay lý do cũ; thiếu actor/reason không tự suy ra. API/auth/escaping/time/call traps pass; nút UI download trong preview database riêng tải đúng bytes. File HTML chưa được agent xem trực quan/print do browser chặn file protocol; không tìm cách vòng qua. Ví dụ: evidence/feedback/example-decision-memo-final.html. **Nút memo chưa có ở 8081**; demo production vẫn dùng Replay/JSON export.

Production vẫn **e5f7801829aaa1f7cfd326e02e415f8389fa3dde**, image sha256:11bddbc767275d8af7d603511596cc432b5862fe07fd880d5404fac8d13f7184. SSH read lúc **2026-10-11T01:15:40Z** xác nhận healthy, cùng start 22:59:42 UTC ngày 10/10 và bind 127.0.0.1:8000. Giữ tunnel 8081/user tab. Không restart/redeploy, không thay DB/env/roster/rules production; original 33+3 artifacts kiểm lại đúng hash. Không giả rằng backup tám records chứa các quyết định bạn tạo sau đó.

Tài liệu demo/notes/QA/limitations đã chỉnh: hỗ trợ người trực/manager và quy trình thông báo hiện có, không thay OnSolve/đội emergency; không có API/import compatibility OnSolve hoặc nguồn LIVE điện/nước/cảnh sát. Tất cả notifications là drafts, deferred thủ công; giữ các mức operating posture, không biến cuộc trao đổi yes/no thành policy. Rehearsal lời nói vẫn bạn tự tập; UI times cũ không chứng minh đã tập nói.

Quyết định tiếp theo thuộc bạn: có áp dụng candidate hay giữ bản production đang ổn định. Nếu áp dụng cần bước deployment riêng, backup DB **hiện tại** trước, pin đúng tested image/build source và giữ mọi quyết định mới. Rollback code không restore backup sáu/tám records đè dữ liệu mới. Tôi chưa chạy bước này và chưa xin lại judge access/Submit. Git/private progress checkpoint cuối được xác minh sau commit tài liệu, độc lập với source/image đang chạy.

Không public/firewall/DNS/cấp quyền ngoài/tài nguyên trả phí/gửi thật/Submit. Kết thúc lượt feedback này; các giới hạn còn lại đã ghi rõ. Bàn giao V2 trước đó được giữ dưới đây như lịch sử.

# Bàn giao ClosureCall V2

Trạng thái: **READY_WITH_DISCLOSED_LIMITATIONS / NOT_SUBMITTED**. Phần kỹ thuật đã được kiểm tra trong phạm vi dưới đây. Bạn sẽ tự xử lý portal, team, quyền giám khảo và Submit sau khi chuẩn bị xong; chưa có bản nộp hay receipt. Goal đầy đủ chưa đạt bước nộp được xác nhận.

Goal bị chặn ở G4/G6: chưa có phương án judge/code access được BTC chấp nhận, thông tin portal/team/tracks và quyền Submit cho bản cụ thể. Điểm chặn này giữ nguyên qua ba lượt goal; các bước kỹ thuật độc lập đã xong. Dừng continuation tự động tại đây, giữ app/dữ liệu/backups. Khi bạn sẵn sàng xử lý phần nộp, dùng draft và bằng chứng hiện có; không cần khởi tạo lại hay chạy thêm model chỉ để làm báo cáo.

Tài liệu demo đã bổ sung `DEMO_PRESENTER_NOTES.md` bằng tiếng Việt để đi cùng lời nói tiếng Anh trong `DEMO_SCRIPT.md`; `ATTRIBUTIONS.md` lưu nguồn dữ liệu/SDK và metadata tám dependencies trực tiếp, chưa phải audit licensing đầy đủ. README/runbook đã sửa thông tin deployment cũ. Read-only SSH lúc 23:16:01 UTC xác nhận image/health/bind giữ nguyên; lần bổ sung này không chạy lại tests, gọi model hay redeploy.

Bản đang chạy private: source `e5f7801829aaa1f7cfd326e02e415f8389fa3dde`, image `sha256:11bddbc767275d8af7d603511596cc432b5862fe07fd880d5404fac8d13f7184`, container closurecall-app-1 trên Linode 172.234.201.174. Restart thực tế 2026-10-10T22:59:42.908771Z. Checkpoint bằng chứng gốc `2a98f48d40009beeec560e3c3da304755aeffd9c` và checkpoint tài liệu đã review được pin riêng trong RELEASE_MANIFEST.json; commit metadata sau đó không deploy lại app. HEAD cuối và remote được kiểm tra khi push.

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
