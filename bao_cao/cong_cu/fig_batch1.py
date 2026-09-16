# -*- coding: utf-8 -*-
"""Nhóm hình 1: hai pha RAG, nạp dữ liệu, định tuyến câu hỏi, cập nhật gia tăng."""
import sys; sys.path.insert(0, '.')
from style import page
from render import render_many

def bx(t, d, cls=""):
    return f'<div class="box {cls}"><div class="t">{t}</div><div class="d">{d}</div></div>'

# ---- F2: hai pha của RAG -------------------------------------------------
f2 = page(
    "Hai pha của một hệ thống RAG",
    "Pha ngoại tuyến dựng kho tri thức; pha trực tuyến phục vụ từng câu hỏi. Hai pha chạy độc lập, chỉ gặp nhau ở chỉ mục.",
    f"""
<div class="band" style="margin-bottom:16px">
  <div class="cap">Pha ngoại tuyến · indexing · chạy trước, không có người dùng chờ</div>
  <div class="row">
    {bx("Thu thập tài liệu","PDF · DOCX · PPTX · XLSX<br>video · âm thanh · trang web","slate")}
    <div class="ar">→</div>
    {bx("Trích xuất nội dung","bộ nạp theo định dạng<br>OCR và phiên âm khi cần","slate")}
    <div class="ar">→</div>
    {bx("Phân đoạn","chunking theo cấu trúc<br>gắn metadata nguồn","slate")}
    <div class="ar">→</div>
    {bx("Vector hoá","mô hình embedding<br>một vector cho mỗi đoạn","blue")}
    <div class="ar">→</div>
    {bx("Lập chỉ mục","cơ sở dữ liệu vector<br>+ chỉ mục từ khoá","green")}
  </div>
</div>
<div class="band">
  <div class="cap">Pha trực tuyến · querying · người dùng đang chờ câu trả lời</div>
  <div class="row">
    {bx("Câu hỏi","người dùng nhập<br>bằng ngôn ngữ tự nhiên","slate")}
    <div class="ar">→</div>
    {bx("Mã hoá câu hỏi","cùng mô hình embedding<br>đã dùng khi lập chỉ mục","blue")}
    <div class="ar">→</div>
    {bx("Truy hồi","tìm k đoạn gần nhất<br>trong kho tri thức","green")}
    <div class="ar">→</div>
    {bx("Ghép prompt","đoạn bằng chứng + câu hỏi<br>+ ràng buộc trả lời","amber")}
    <div class="ar">→</div>
    {bx("Sinh câu trả lời","mô hình ngôn ngữ<br>kèm trích dẫn nguồn","violet")}
  </div>
</div>
""",
    "Điểm gặp nhau duy nhất của hai pha là chỉ mục: thêm tài liệu mới chỉ chạy lại pha ngoại tuyến, "
    "không phải huấn luyện lại mô hình ngôn ngữ."
)

# ---- F6: ingestion & chunking -------------------------------------------
f6 = page(
    "Luồng nạp dữ liệu và phân đoạn tài liệu",
    "Mỗi định dạng đi qua một bộ nạp riêng đã được kiểm chứng trên kho thật, thay vì một bộ nạp tổng quát tự đoán.",
    f"""
<div class="row" style="align-items:flex-start">
  <div class="col" style="flex:1.05">
    <div class="band">
      <div class="cap">Nguồn dữ liệu</div>
      <div class="col">
        {bx("Thư mục kho","ollama-rag-desktop/data_giao_duc","slate")}
        {bx("Google Drive","đồng bộ theo chu kỳ 15 phút<br>so sánh md5Checksum","slate")}
        {bx("Tải lên từ giao diện","POST /api/kho/tep","slate")}
        {bx("Tệp đính kèm trong chat","POST /api/tep · chỉ dựng BM25 riêng","slate dash")}
      </div>
    </div>
  </div>
  <div class="ar" style="align-self:center">→</div>
  <div class="col" style="flex:1.35">
    <div class="band">
      <div class="cap">Trích xuất theo định dạng</div>
      <div class="col">
        {bx("PDF","PyPDFLoader đọc lớp văn bản sẵn có","blue")}
        {bx("PDF bản quét","pypdf phát hiện thiếu chữ → pypdfium2 kết xuất ảnh → Tesseract OCR (vie)","amber")}
        {bx("DOCX · DOC · PPTX · XLSX · CSV","Docx2txtLoader · chuyển DOC sang DOCX · tách theo slide · pandas theo từng sheet","blue")}
        {bx("Video · âm thanh","faster-whisper, giữ mốc thời gian từng đoạn","violet")}
      </div>
    </div>
  </div>
  <div class="ar" style="align-self:center">→</div>
  <div class="col" style="flex:1.05">
    <div class="band">
      <div class="cap">Phân đoạn &amp; gắn nhãn</div>
      <div class="col">
        {bx("Văn bản quy phạm","giữ trọn một Điều làm một đoạn; quá dài mới cắt tiếp","green")}
        {bx("Văn bản thường","RecursiveCharacterTextSplitter<br>1.200 ký tự · chồng lấn 150","green")}
        {bx("Dữ liệu có ranh giới sẵn","slide · khối dòng bảng · đoạn phiên âm giữ nguyên ranh giới","green")}
        {bx("Gắn metadata","tên tệp · trang · Chương · Điều · slide · sheet · mốc thời gian","slate")}
      </div>
    </div>
  </div>
  <div class="ar" style="align-self:center">→</div>
  <div class="col" style="flex:.82">
    <div class="band" style="height:100%">
      <div class="cap">Lập chỉ mục</div>
      <div class="col">
        {bx("Embedding bge-m3","vector 1.024 chiều<br>thêm vào FAISS theo lô 20 đoạn","blue")}
        {bx("FAISS trên đĩa","save_local() · điểm kiểm tra định kỳ","green")}
        {bx("BM25 trong RAM","dựng lại mỗi lần khởi động","green")}
        {bx("Sổ ghi chép","SHA-256 + chunk_id của từng tệp","slate")}
      </div>
    </div>
  </div>
</div>
""",
    "Kết quả OCR và phiên âm được lưu đệm theo mã băm nội dung, nên một tài liệu không đổi chỉ phải xử lý một lần "
    "dù chỉ mục được dựng lại nhiều lần."
)

# ---- F8: định tuyến câu hỏi ---------------------------------------------
f8 = page(
    "Định tuyến câu hỏi: bốn lối tắt đặt trước dây chuyền RAG",
    "Thứ tự thử đi từ công cụ có phạm vi nhận hẹp nhất tới rộng nhất; câu nào không khớp lối tắt nào mới đi tiếp vào truy hồi.",
    f"""
<div class="row" style="align-items:center">
  {bx("Câu hỏi của người dùng","POST /api/chat/stream<br>question · history · tep_ids · pham_vi","slate")}
  <div class="ar">→</div>
  <div class="col" style="flex:2.6">
    <div class="band">
      <div class="cap">Lối tắt · trả lời xong là thoát, không gọi mô hình ngôn ngữ</div>
      <div class="row">
        {bx("1 · tinh_luong","lương nhà giáo: hệ số ở Thông tư nhân lương cơ sở ở Nghị định","green")}
        {bx("2 · dinh_muc_tiet_day","định mức tiết dạy, các khoản giảm trừ theo Điều 9, Điều 10","green")}
        {bx("3 · danh_gia_hoc_sinh","ĐTBmhk có trọng số và xếp loại theo ngưỡng từng môn","green")}
        {bx("4 · tinh_toan","biểu thức số học thuần tuý: phần trăm, nhân chia, tăng giảm","green")}
      </div>
      <div style="height:10px"></div>
      <div class="row">
        {bx("Tệp đính kèm được chọn","chỉ tìm trong BM25 của chính tệp đó, bỏ qua kho chung","amber")}
        {bx("Câu hỏi kèm URL","trafilatura tải trang, dùng làm ngữ cảnh một lượt, không ghi vào FAISS","amber")}
        {bx("Cache ngữ nghĩa","nhúng câu hỏi bằng bge-m3, tương đồng ≥ 0,96 thì phát lại câu đã soạn","violet")}
      </div>
    </div>
  </div>
  <div class="ar">→</div>
  {bx("Dây chuyền RAG đầy đủ","truy hồi lai → chặn lạc đề → sinh câu trả lời → hậu kiểm trích dẫn","blue")}
</div>
<div style="height:14px"></div>
<div class="band">
  <div class="cap">Vì sao tách khỏi RAG thay vì dạy prompt cách tính</div>
  <div class="row">
    {bx("Prompt cấm ghép số liệu","quy tắc 4 cấm gộp số của hai EVIDENCE khác nhau — mà tính lương chính là việc đó","red dash")}
    {bx("Hậu kiểm gắn cờ","kiem_tra_tra_loi.py đánh dấu mọi con số không có nguyên văn trong đoạn trích","red dash")}
    {bx("Mô hình nhỏ chạy CPU","số học nhiều bước không đáng tin, lại tốn trọn thời gian sinh văn bản","red dash")}
    {bx("Công cụ Python trả lời","con số do Python tính, kèm chip nguồn dẫn đúng điều khoản quy định nó","green")}
  </div>
</div>
""",
    "Cổng nhận của mỗi công cụ được đặt hẹp có chủ đích: nhận nhầm một câu tra cứu thì người dùng mất hẳn câu trả lời, "
    "còn bỏ sót một câu số học thì họ chỉ phải chờ lâu như cũ."
)

# ---- F12: cập nhật gia tăng ---------------------------------------------
f12 = page(
    "Cập nhật gia tăng chỉ mục theo mã băm nội dung",
    "Sổ ghi chép data_giao_duc_da_xu_ly.json lưu SHA-256 và danh sách chunk_id của từng tệp, làm căn cứ so sánh giữa hai lần chạy.",
    f"""
<div class="row" style="align-items:center;margin-bottom:16px">
  {bx("Quét kho tài liệu","liệt kê tệp hiện có, tính SHA-256 từng tệp","slate")}
  <div class="ar">→</div>
  {bx("Đối chiếu sổ ghi chép","so mã băm, kích thước và thời điểm sửa","slate")}
  <div class="ar">→</div>
  {bx("Phân loại thay đổi","bốn trạng thái loại trừ nhau","blue")}
</div>
<div class="row">
  <div class="col" style="flex:1">
    <div class="box green"><div class="t">NEW · tệp mới</div>
    <div class="d">Chunk → embedding → thêm vector vào FAISS → ghi chunk_id vào sổ.</div></div>
  </div>
  <div class="col" style="flex:1">
    <div class="box amber"><div class="t">MODIFIED · nội dung đã đổi</div>
    <div class="d">Xoá các vector cũ theo chunk_id đã lưu, rồi xử lý lại tệp từ đầu như tệp mới.</div></div>
  </div>
  <div class="col" style="flex:1">
    <div class="box red"><div class="t">DELETED · tệp đã bị xoá</div>
    <div class="d">Xoá vector tương ứng khỏi FAISS và xoá bản ghi khỏi sổ ghi chép.</div></div>
  </div>
  <div class="col" style="flex:1">
    <div class="box slate"><div class="t">UNCHANGED · không đổi</div>
    <div class="d">Bỏ qua hoàn toàn: không đọc lại, không OCR, không sinh lại vector.</div></div>
  </div>
</div>
<div style="height:16px"></div>
<div class="band">
  <div class="cap">Ba cách kích hoạt cập nhật</div>
  <div class="row">
    {bx("Từ giao diện","nút “Cập nhật kho tri thức” hiện trên thẻ trạng thái khi hệ thống phát hiện kho đã đổi","blue")}
    {bx("Từ dòng lệnh","chạy capnhat_tailieu_moi.py","blue")}
    {bx("Tự động từ Google Drive","kéo tài liệu mới theo chu kỳ mặc định 15 phút","blue")}
  </div>
  <div style="height:10px"></div>
  {bx("Trong lúc cập nhật","trạng thái dịch vụ chuyển sang <b>updating</b> và việc gửi câu hỏi tạm bị khoá, tránh đọc chỉ mục ngay giữa lúc nó đang thay đổi","amber")}
</div>
""",
    "Nhờ cơ chế này, bổ sung vài tài liệu vào kho 713 tệp chỉ tốn thời gian xử lý đúng phần thay đổi, "
    "thay vì dựng lại toàn bộ 25.761 vector."
)

render_many([
    (f2,  'fig/f02_hai_pha_rag.png',    1560, 900),
    (f6,  'fig/f06_ingestion.png',      1680, 1000),
    (f8,  'fig/f08_dinh_tuyen.png',     1700, 1000),
    (f12, 'fig/f12_cap_nhat.png',       1600, 1000),
], scale=2)
