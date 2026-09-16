# Chatbot RAG Giáo dục

Ứng dụng hỏi đáp tài liệu giáo dục chạy cục bộ bằng FastAPI, Ollama, FAISS và giao diện web tiếng Việt. Hệ thống hỗ trợ tìm kiếm lai FAISS + BM25, trích dẫn nguồn, cập nhật chỉ mục tăng dần, OCR PDF scan, đọc tài liệu Office, tệp đính kèm và đồng bộ thư mục Google Drive.

## Yêu cầu

- Windows 10/11 và Python 3.11
- [Ollama](https://ollama.com/) đang chạy
- Model embedding `bge-m3`
- Một model hội thoại, mặc định `llama3.2:3b`
- Tesseract OCR nếu cần đọc PDF scan

## Cài đặt

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull bge-m3
ollama pull llama3.2:3b
```

Đặt tài liệu vào thư mục:

```text
ollama-rag-desktop/data_giao_duc
```

Tạo chỉ mục lần đầu:

```powershell
.\.venv\Scripts\python.exe main.py
```

Khởi động giao diện:

```powershell
.\start_ui.bat
```

Ứng dụng sẽ chọn một cổng trống từ `8000` đến `8020` và mở trình duyệt tự động.

## Cập nhật tài liệu

Sau khi thêm, sửa hoặc xóa tài liệu trong kho, có thể cập nhật chỉ mục từ giao diện hoặc chạy:

```powershell
.\.venv\Scripts\python.exe capnhat_tailieu_moi.py
```

Kết quả OCR và sổ theo dõi giúp lần chạy tiếp theo tiếp tục mà không xử lý lại toàn bộ kho.

## Câu hỏi tính toán

Những câu cần một con số tính ra được rẽ sang công cụ Python chạy trước cả cache và khâu truy hồi, thay vì để mô hình làm toán. Lý do nằm ở chính ba lớp chống bịa của hệ thống: prompt cấm ghép số liệu giữa hai đoạn trích, hậu kiểm gắn cờ mọi con số không có nguyên văn trong đoạn trích, và model 3B chạy CPU không đáng tin ở số học nhiều bước. Mỗi công cụ in kèm công thức đã thay số để người đọc kiểm lại bằng máy tính bỏ túi.

| Công cụ | Nhận câu hỏi dạng | Căn cứ |
|---|---|---|
| `tinh_luong.py` | lương, phụ cấp của nhà giáo theo chức danh, hạng, bậc | Nghị định 73/2024, Thông tư 31/2026, Nghị định phụ cấp ưu đãi |
| `dinh_muc_tiet_day.py` | định mức tiết dạy, mức giảm khi kiêm nhiệm, số tiết dạy vượt | Thông tư 04/2026/TT-BGDĐT |
| `danh_gia_hoc_sinh.py` | điểm trung bình môn, xếp loại kết quả học tập, danh hiệu cuối năm | Thông tư 22/2021/TT-BGDĐT |
| `tinh_toan.py` | số học thuần: phần trăm, tăng giảm theo tỉ lệ, biểu thức | không dùng văn bản nào, nên không gắn chip nguồn |

```powershell
.\.venv\Scripts\python.exe tinh_luong.py "tính lương giáo viên THPT hạng III bậc 1"
.\.venv\Scripts\python.exe dinh_muc_tiet_day.py "giáo viên GDTX chủ nhiệm 1 lớp dạy bao nhiêu tiết"
.\.venv\Scripts\python.exe danh_gia_hoc_sinh.py "điểm thường xuyên 8, 9, giữa kì 7, cuối kì 8"
.\.venv\Scripts\python.exe tinh_toan.py "12% của 2.340.000"
```

Gõ có dấu hay không dấu đều được: câu hỏi đi qua một bước bỏ dấu trước khi so mẫu, nên "tinh luong giao vien THPT hang III bac 1" và bản gõ đủ dấu đi chung một đường.

Hằng số nào chưa có văn bản trong kho chứng minh thì kết quả nói rõ "chưa có trong kho tài liệu" và không gắn chip nguồn, thay vì im lặng đưa ra một con số trông như đã được kiểm chứng. Cổng nhận câu của cả ba công cụ nghiêng hẳn về phía bỏ sót: chúng đứng trước RAG nên nhận nhầm một câu tra cứu thì người dùng mất hẳn câu trả lời từ kho.

## Đo chất lượng hệ thống

Bộ câu hỏi chuẩn nằm ở `bo_cau_hoi_benchmark.json` (127 câu, trong đó 97 câu có nhãn nguồn đúng và 30 câu cố tình lạc đề).

```powershell
.\.venv\Scripts\python.exe benchmark_chatbot.py --ir
```

Chế độ `--ir` đo chất lượng **xếp hạng** của khối truy hồi bằng bộ chỉ số IR/QA kinh điển — MRR, Hit@K, Recall@K, nDCG@K, MAP (công thức nằm trong `chi_so_ir.py`). Không gọi LLM nên chạy vài phút, kết quả ghi ra `ket_qua_chi_so_ir.json` và bảng markdown `bang_chi_so_ir.md` để dán thẳng vào báo cáo.

Hai chế độ còn lại: `--nhanh` đo truy hồi kèm cổng chặn lạc đề, `--bo` gọi đủ LLM để đo thêm trích dẫn và số liệu (chậm, khoảng 150 giây/câu trên CPU).

## Cấu hình Google Drive

Sao chép `khoa_api.mau.bat` thành `khoa_api.bat`, sau đó điền khóa API của riêng bạn. `khoa_api.bat` đã được loại khỏi Git để tránh công khai khóa.

## Dữ liệu không nằm trong repository

Repository chỉ chứa mã nguồn. Tài liệu gốc, chỉ mục FAISS, cache OCR, bản phiên âm, lịch sử chat, khóa API và cấu hình riêng của máy không được commit vì có thể chứa dữ liệu riêng tư hoặc tệp dung lượng lớn.

Xem thêm [hướng dẫn chạy giao diện](HUONG_DAN_CHAY_GIAO_DIEN.md) và [tài liệu bàn giao](HUONG_DAN_BAN_GIAO_UI.md).
