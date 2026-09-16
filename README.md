# Chatbot RAG Giáo dục

Ứng dụng hỏi đáp tài liệu giáo dục chạy cục bộ bằng FastAPI, Ollama, FAISS và giao diện web tiếng Việt. Hệ thống hỗ trợ tìm kiếm lai FAISS + BM25, trích dẫn nguồn, cập nhật chỉ mục tăng dần, OCR PDF scan, đọc tài liệu Office, tệp đính kèm và đồng bộ thư mục Google Drive.
**Trường Đại học Sư phạm Thành phố Hồ Chí Minh**
**Khoa Công nghệ thông tin**

Học viên thực hiện:

1. Tăng Ngọc Phụng - KHMT836027
2. Hoàng Châu Ngọc Phương - KHMT836028
3. Lê Thị Mai Len - KHMT836015

Giảng viên hướng dẫn: TS. Nguyễn Minh Hải

---

Ứng dụng hỏi đáp tài liệu giáo dục chạy cục bộ bằng FastAPI, Ollama, FAISS và giao diện web tiếng Việt. Hệ thống hỗ trợ:

- Tìm kiếm lai FAISS + BM25, trích dẫn nguồn kèm vị trí trong tài liệu, chặn câu hỏi ngoài phạm vi kho
- Cập nhật chỉ mục tăng dần (chỉ xử lý tệp thêm, sửa hoặc xóa)
- Đọc PDF, Word (`.docx`, `.doc`), PowerPoint (`.pptx`), Excel/CSV, TXT, Markdown, HTML, EPUB
- OCR PDF scan và ảnh bằng Tesseract
- Phiên âm video/âm thanh offline bằng faster-whisper, đọc phụ đề `.srt`/`.vtt`
- Tệp đính kèm trong cuộc trò chuyện, lịch sử chat, cache ngữ nghĩa
- Đồng bộ thư mục Google Drive
- Chế độ chạy công khai có mật khẩu qua đường hầm Cloudflare, bộ script triển khai lên VPS

## Yêu cầu

- Windows 10/11 và Python 3.11
- [Ollama](https://ollama.com/) đang chạy
- Model embedding `bge-m3`
- Một model hội thoại, mặc định `llama3.2:3b`
- Tesseract OCR nếu cần đọc PDF scan
- Một model hội thoại, mặc định `qwen3.5:4b` (đổi bằng biến môi trường `RAG_LLM_MODEL` hoặc chọn trên giao diện)
- Tesseract OCR (kèm dữ liệu tiếng Việt `vie`) nếu cần đọc PDF scan hoặc ảnh
- Microsoft Word hoặc LibreOffice nếu cần đọc tệp `.doc` đời cũ

## Cài đặt

```powershell
py -3.11 -m venv .venv
