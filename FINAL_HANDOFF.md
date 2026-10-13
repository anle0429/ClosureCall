# Bàn giao ClosureCall — portfolio sau hackathon

## Cập nhật ngày 13/10/2026 — đánh giá sản phẩm

Đã review source và xác minh **93 tests Windows** từ checkout tách biệt không có env/DB local, **93 tests Linux** trên image candidate hiện có. Sửa duy nhất test provider từng có thể bỏ qua assertion khi máy đã có key; backend/UI/rules/dependencies không đổi.

Kết luận: phù hợp portfolio kỹ thuật và demo có người giám sát với dữ liệu giả lập; chưa đủ để vận hành với nhân viên thật. README có status/engineering controls rõ hơn, [PRODUCT_REVIEW.md](docs/PRODUCT_REVIEW.md) ghi điểm mạnh/giới hạn/priorities; GitHub workflow cũ được archive. Đã fast-forward/push lên master private và nhánh review, cùng checkpoint 2ba6096 được đối chiếu độc lập; đây không phải deployment.

SSH read mới xác nhận Linode a5681bc/image9ab42b0 healthy, cùng start/non-root/read-only/loopback. Candidate 3bc1ddd chưa deploy. Không có LIVE/model call mới, public/post/Submit hoặc sửa dữ liệu gốc. Phần bàn giao dưới đây giữ mốc 12/10; push/commit mới sẽ được xác minh riêng.

## Bàn giao ngày 12/10/2026

Trạng thái cuối: **PREP_COMPLETE_PENDING_EXTERNAL**, verdict kỹ thuật **ACCEPTABLE_WITH_LIMITATIONS**. Các gate nội bộ/link/secret/history/image/data đã kiểm tra; private branch đã push checkpoint e8bb341, master không đổi; submission vẫn **ON_HOLD / NOT_SUBMITTED**. Deadline thi cũ không được coi là gia hạn. Bạn đã yêu cầu hoàn thiện riêng cho GitHub/LinkedIn sau sự kiện.

Linode giữ nguyên source **a5681bc**, image **9ab42b0...**, healthy/private loopback, cùng start 11:45:50 UTC ngày 11/10. Candidate **3bc1ddd** / image **5fdf4901...** đã kiểm thử, **chưa deploy**. 8084 là bản QA local tách biệt; đánh giá mới có nhãn SYNTHETIC TEST và không gọi provider/model. 8081 cần mở tunnel bằng [hướng dẫn](docs/DEMO_RECOVERY.md); lượt này chưa mở lại.

Đã làm: README/docs có một mục lục hiện hành và archive giữ lịch sử; Python/JS/HTML/CSS được format bằng công cụ dev có pin và kiểm tra AST/control contracts; memo-v2 ưu tiên facility/ca trước hash; sửa badge draft bị kéo cao. Không thêm framework/agent, không đổi rules/auth/routing/API/history.

Đã chạy: **91 tests Windows (10.85s), 91 tests đúng image Linux (7.43s)**. Timeout test giữ 0.2s và thêm assertion process exit; timing startup cũ chưa biết chính xác. Test cuối tuần lộ lỗi gần nửa đêm: Start+10 phút đã sang Monday, production chấp nhận đúng; fixture giờ cố định kiểm tra cả hai phía. Log fail/initial verifier errors vẫn giữ, không nới budget/skip assertion để xanh.

QA approve/override có lý do, busy/double-click, drafts đủ người, Refresh giờ/lịch sử, download JSON/memo được kiểm tra. Chỉ hai run/hai quyết định mới trong QA. Bốn viewport không overflow; dữ liệu gốc production và QA cũ không đổi. Backup 9 records được mở bằng candidate trên volume riêng/network none, kiểm tra HTTP, đổi current rules/roster, restart QA thực rồi đối chiếu; không gọi nguồn/model/tính lại và không restore lên production.

Memo xem qua HTTP local và download đúng bytes; **Print/pagination và tập lời nói chưa xác minh**. Không có integration LIVE mới, không mô tả ảnh/replay là thời tiết bây giờ. Endpoint workshop sau sự kiện chưa được thử lại. Các nguồn sai nhưng metadata nhất quán và null geometry còn giới hạn.

Packet: [SUBMISSION.md](SUBMISSION.md). [Demo 180 giây](docs/DEMO_SCRIPT.md), [chú giải tiếng Việt](docs/DEMO_PRESENTER_NOTES.md), [LinkedIn draft](docs/LINKEDIN_DRAFT.md), [verification](docs/VERIFICATION.md), [limitations](docs/LIMITATIONS.md), [manifest](RELEASE_MANIFEST.json). Toàn bộ handoff cũ giữ nguyên tại docs/archive/hackathon/FINAL_HANDOFF_PRE_PORTFOLIO.md.

Phần bạn quyết định: license/team credits/quyền công bố, public GitHub hoặc đăng LinkedIn, có deploy candidate hay giữ Linode hiện tại, và kiểm tra print/tập nói nếu cần. Không post/share/public/restart/deploy/gửi thật/Submit trong lượt này; không có receipt. Private progress đã push vào maintenance/portfolio-readiness của repo đã có, independently matched tại checkpoint e8bb341; metadata follow-up giữ source/image riêng và không deploy. Không merge master trong lượt này.
