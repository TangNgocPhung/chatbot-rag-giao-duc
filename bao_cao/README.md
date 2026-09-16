# Bài tiểu luận — bản đã rà soát và sửa

`Tieu_luan_RAG_giao_duc_ban_sua.docx` là bản sửa của tệp `Thay_Minh_Hai.docx`,
đối chiếu với mã nguồn trong kho này.

**Mở tệp lần đầu:** nhấn `Ctrl+A` rồi `F9` trong Word để cập nhật mục lục, danh
mục hình và danh mục bảng (tệp đã bật cờ tự cập nhật trường, nhưng làm thủ công
thì chắc chắn hơn).

## Nội dung sai đã sửa

| Vị trí | Bản cũ | Bản sửa |
|---|---|---|
| Mục Phạm vi nghiên cứu, mẫu `/etc/chatbot-rag.env` | `llama3.2:3b` | `qwen3.5:4b` — đúng mặc định trong `rag_service.py:467` và `main.py:54` |
| Mục 4.4 Kết quả | “74/87 câu nằm trong hai vị trí đầu” | 81/87 (72 hạng 1 + 9 hạng 2), bổ sung hạng 4, hạng 5 và hạng trung bình 1,29 |
| Mục 3.2 Tổng quan | 32 module · 11.500 dòng · 17 tệp kiểm thử | 36 module · ~13.700 dòng · 24 tệp kiểm thử · ~4.600 dòng |
| Mục 3.2 | “api.py khai báo khoảng 25 đầu cuối” | 24 đầu cuối |
| Mục 3.3 | “khoảng 60 tham số” | gần 80 tham số `RAG_*` |
| Mục 1.6 | công thức MRR dán lỗi: “hạng rr”, “1/r1/r” | “hạng r”, “1/r”, thêm quy ước RR = 0 khi trượt |
| Lời cảm ơn | “Công nghệ thông tins”, “Các thuật toán tối ưu” | sửa chính tả, sửa tên học phần bị chép nhầm |
| Lời cam đoan, ô ký tên | xưng “tôi”, “Tác giả” | “nhóm tác giả” — đề tài do ba học viên thực hiện |
| Mục Bố cục | “Ngoài phần … Kết luận … năm chương” rồi lại liệt kê Chương 5 là Kết luận | bỏ mâu thuẫn, sửa tên Chương 3 và Chương 4 cho khớp nội dung thật |
| Mục 2.1 Query Router | nói hệ thống không có định tuyến | mô tả đúng lớp định tuyến theo quy tắc và bốn công cụ tính |
| Chương 4 | lẫn lộn `0.806` và `0,806` | thống nhất dấu thập phân kiểu Việt Nam |

## Trích dẫn và tài liệu tham khảo

Mục **TÀI LIỆU THAM KHẢO** trong bản cũ để trống dù bài có 28 trích dẫn. Ngoài
ra, dữ liệu trường Mendeley bị lệch nguồn ở 7 chỗ: câu về Transformer gắn bài
LLaMA, câu về BERT gắn khảo sát ảo giác, câu về RAG gắn bài GPT-3, BM25 và RRF
gắn khảo sát RAG.

Bản sửa: gỡ trường Mendeley thành văn bản thường, gán lại số hiệu đúng với nội
dung từng câu, và dựng danh mục 26 tài liệu theo thứ tự xuất hiện lần đầu — bổ
sung Devlin (BERT), Robertson & Zaragoza (BM25), Cormack (RRF), FastAPI và thay
hai nguồn yếu (báo cáo seminar về Tesseract, blog về SSRF) bằng Smith 2007 và
OWASP.

> Nếu mở bằng Mendeley Cite và bấm làm mới, phần mềm sẽ ghi đè số hiệu theo thư
> viện cũ. Nên giữ nguyên dạng văn bản thường, hoặc chèn lại trích dẫn từ thư
> viện Mendeley đã dọn.

## Bố cục bổ sung

- **1.5 Một số nghiên cứu liên quan** — phần khảo sát công trình liên quan.
- **2.7 Định tuyến câu hỏi và các lối tắt trước dây chuyền RAG** — bốn công cụ
  tính bằng Python, bộ nhớ đệm ngữ nghĩa, tệp đính kèm, URL.
- **4.1 Kho tri thức dùng trong thử nghiệm** — 713 tệp, cơ cấu định dạng và thể loại.
- **4.5 Hạn chế của phương pháp đánh giá** — sáu giới hạn của cách đo hiện tại.
- **Phụ lục A, B, C, D** — trước đây chỉ có tiêu đề, nay có mã nguồn trích dẫn,
  ảnh chụp giao diện và câu dẫn cho hai bảng liên kết.

## Hình thức

- Lề trang đồng nhất: trên/dưới 2,5 cm, trái 3 cm, phải 2 cm (bản cũ phần thân
  bài dùng 2,54 cm bốn phía, khác phần đầu).
- Thêm đầu trang cho phần Tài liệu tham khảo và Phụ lục (trước đây mất số trang).
- Căn giữa ảnh, bỏ thụt dòng đầu ở đoạn chứa ảnh.
- Bỏ hai đề mục bị gán nhầm sang danh sách đánh số khác (nguồn gốc của “2.1.1”
  xuất hiện giữa Chương 3, “Hình 9.1”, “Bảng 9.1”).
- Hạ 7 mục con từ cấp 2 xuống cấp 3 cho đúng quan hệ bao hàm; đổi tên hai đề mục
  trùng tên.
- Danh mục hình: thêm trường mục lục (bản cũ để trống). Danh mục bảng: thêm chú
  thích cho 9 bảng (bản cũ chỉ 1 trong 12 bảng có chú thích).
- Bổ sung 5 mục vào danh mục chữ viết tắt và sắp xếp lại theo bảng chữ cái.

## Hình minh hoạ

Bản cũ có 9 hình, phần lớn là ảnh chụp giao diện. Bản sửa có 31 hình: thêm 20
hình cho lý thuyết, thiết kế, triển khai và kết quả thực nghiệm.

- `hinh/f01`–`f16`: hình mới dựng cho bài (HTML/CSS kết xuất bằng Chromium,
  biểu đồ bằng matplotlib).
- `hinh/repo_*`: kết xuất lại từ `kien_truc_rag.png`, `so_do_quy_trinh.svg`,
  `cong_nghe_su_dung.svg`, `bieu_do_co_cau_kho.svg` sẵn có trong kho, đã sửa tên
  model trong hình cho khớp mặc định hiện tại.

## Công cụ

`cong_cu/` chứa các script đã dùng, chạy tuần tự từ tệp gốc:

```
python3 fig_batch1.py && python3 fig_batch2.py && python3 fig_batch3.py && python3 fig_charts.py
python3 fix_part1.py && python3 fix_part2.py && python3 fix_part3.py
python3 fix_part4.py && python3 fix_part5.py && python3 fix_part6.py
```

Cần `python-docx`, `matplotlib`, `playwright` và một bản Chromium.
