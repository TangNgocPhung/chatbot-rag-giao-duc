# -*- coding: utf-8 -*-
"""Nhóm hình 3: máy trạng thái, triển khai VPS, chuỗi sự kiện NDJSON."""
import sys; sys.path.insert(0, '.')
from style import page
from render import render_many

def bx(t, d, cls=""):
    return f'<div class="box {cls}"><div class="t">{t}</div><div class="d">{d}</div></div>'

# ---- F9: máy trạng thái --------------------------------------------------
f9 = page(
    "Máy trạng thái của dịch vụ RAG và ảnh hưởng tới giao diện",
    "Trạng thái được rag_service.py quản lý và giao diện hiển thị trực tiếp; khung nhập câu hỏi chỉ mở khoá khi đạt trạng thái ready.",
    f"""
<div class="row" style="align-items:center;margin-bottom:16px">
  {bx("starting","Tiến trình web đã lên, lifespan vừa kiểm tra xong cấu hình bảo mật. Máy chủ đáp ứng được ngay, kho tri thức chưa nạp.","slate")}
  <div class="ar">→</div>
  {bx("loading","Luồng nền lần lượt: kết nối Ollama → nạp FAISS từ đĩa → dựng BM25 trong RAM → đọc hồ sơ văn bản và bảng phân loại → làm nóng mô hình.","amber")}
  <div class="ar">→</div>
  {bx("ready","Đủ điều kiện trả lời. Giao diện mở khoá khung nhập câu hỏi, run_ui.py mới mở trình duyệt.","green")}
</div>
<div class="row">
  <div class="band" style="flex:1">
    <div class="cap">Hai nhánh rẽ khỏi ready</div>
    <div class="row">
      {bx("updating","Đang cập nhật chỉ mục. Việc gửi câu hỏi tạm bị khoá để không đọc chỉ mục ngay giữa lúc nó đang thay đổi. Xong thì quay lại ready.","amber")}
      {bx("error","Mất kết nối tới Ollama. Giao diện hiện thông báo kèm gợi ý; người dùng bấm thử lại để gọi /api/reinitialize mà không phải khởi động lại ứng dụng.","red")}
    </div>
  </div>
  <div class="band" style="flex:.88">
    <div class="cap">Vì sao tách sang luồng nền</div>
    {bx("Nạp chỉ mục mất vài chục giây","Nếu nạp đồng bộ trong lifespan thì cổng đã mở nhưng mọi yêu cầu HTTP đều treo, người dùng thấy trình duyệt trắng và không biết hệ thống đang làm gì. Đẩy sang luồng nền cho phép /api/status trả lời ngay từ giây đầu tiên.","blue")}
  </div>
</div>
""")

# ---- F10: triển khai VPS -------------------------------------------------
f10 = page(
    "Hai môi trường triển khai dùng chung một mã nguồn",
    "Khác biệt duy nhất giữa hai môi trường nằm ở tệp cấu hình môi trường, không nằm trong mã.",
    f"""
<div class="row" style="align-items:stretch">
  <div class="band" style="flex:1">
    <div class="cap">Máy cá nhân · Windows 11 · chỉ CPU</div>
    <div class="col">
      {bx("Người dùng","trình duyệt tại http://127.0.0.1:8010","slate")}
      <div class="ard">↓</div>
      {bx("start_ui.bat → run_ui.py","nạp khoa_api.bat nếu có, chiếm cổng, khởi động Uvicorn với api:app","blue")}
      <div class="ard">↓</div>
      {bx("Ollama cục bộ","http://localhost:11434 · bge-m3 + qwen3.5:4b · khoảng 26 token/giây nạp câu nhắc, 6 token/giây sinh chữ","violet")}
      <div class="ard">↓</div>
      {bx("Dữ liệu trên đĩa","data_giao_duc/ · faiss_index_data_giao_duc/ · ocr_cache/ · transcripts/ · lich_su_chat.db","green")}
    </div>
  </div>
  <div class="band" style="flex:1">
    <div class="cap">Máy chủ ảo · Debian 12 · 8 vCPU · 24 GB RAM · 200 GB đĩa</div>
    <div class="col">
      {bx("Người dùng trên Internet","truy cập qua tên miền, bắt buộc đăng nhập HTTP Basic cho mọi đường dẫn, kể cả /api/status","slate")}
      <div class="ard">↓</div>
      {bx("Máy chủ proxy","đảm nhiệm chứng chỉ HTTPS và chuyển tiếp về cổng nội bộ","amber")}
      <div class="ard">↓</div>
      {bx("Dịch vụ systemd chatbot-rag","chỉ lắng nghe 127.0.0.1:8010 · EnvironmentFile=/etc/chatbot-rag.env (quyền 640, sở hữu bởi root) · Restart=on-failure","blue")}
      <div class="ard">↓</div>
      {bx("Ollama trên cùng máy chủ","mô hình sinh cấu hình qua RAG_LLM_MODEL, ghi đè lựa chọn đã lưu trên giao diện","violet")}
    </div>
  </div>
</div>
<div style="height:14px"></div>
{bx("Ràng buộc an toàn khi khởi động","Nếu RAG_CONG_KHAI=1 mà RAG_MAT_KHAU để trống, bao_ve_truy_cap.kiem_tra_cau_hinh() được gọi ngay trong lifespan sẽ làm ứng dụng <b>từ chối khởi động</b>. Hệ thống vốn dành cho máy cá nhân nên mọi đầu cuối đều mở, kể cả đầu cuối tải tệp vào kho và xoá lịch sử — thà dừng hẳn còn hơn mở ra Internet rồi mới phát hiện chưa khoá cửa.","red")}
""")

# ---- F11: chuỗi sự kiện NDJSON -------------------------------------------
def ev(name, desc, cls):
    return f"""<div class="row" style="align-items:center;gap:12px">
      <div style="flex:0 0 132px"><span class="tag" style="background:#1f2933;color:#fff;font-family:'DejaVu Sans Mono',monospace">{name}</span></div>
      <div class="box {cls}" style="padding:8px 12px"><div class="d" style="margin:0">{desc}</div></div></div>"""
f11 = page(
    "Chuỗi sự kiện NDJSON của một lượt hỏi – đáp",
    "Máy chủ trả về một dòng JSON cho mỗi sự kiện; thứ tự các sự kiện quyết định điều người dùng nhìn thấy trước.",
    f"""
<div class="col" style="gap:9px">
  {ev("phase", "Giai đoạn đang chạy: “Đang tìm tài liệu liên quan”, rồi “Đang soạn câu trả lời”. Giữ cho giao diện không đứng im trong hàng chục giây đầu.", "slate")}
  {ev("sources", "Danh sách nguồn trích dẫn kèm số hiệu văn bản và vị trí (trang · slide · phút). <b>Xuất hiện trước khi câu trả lời bắt đầu hiện</b> — người đọc biết ngay hệ thống đang dựa vào tài liệu nào.", "blue")}
  {ev("hieu_luc", "Cảnh báo văn bản đã bị thay thế hoặc sửa đổi, dựng từ quan hệ hiệu lực đã trích xuất khi lập chỉ mục.", "amber")}
  {ev("token", "Từng mẩu chữ của câu trả lời, hiện dần trên màn hình thay vì đợi sinh xong toàn bộ.", "violet")}
  {ev("warning", "Cảnh báo hậu kiểm khi số trích dẫn hoặc con số trong câu trả lời không khớp khối bằng chứng.", "red")}
  {ev("goi_y", "Câu hỏi gợi ý tiếp theo, dựng từ chính nguồn vừa trích chứ không gọi thêm một lượt sinh.", "green")}
  {ev("done", "Kết thúc lượt, kèm thời gian xử lý; câu trả lời đạt hậu kiểm mới được ghi vào bộ nhớ đệm và lịch sử.", "slate")}
</div>
<div style="height:16px"></div>
<div class="row">
  {bx("Vì sao là NDJSON chứ không phải một phản hồi JSON duy nhất","Trên CPU, một câu trả lời đầy đủ mất trung bình khoảng 150 giây. Nếu chờ sinh xong mới trả về, người dùng nhìn màn hình trắng suốt thời gian đó và không phân biệt được hệ thống đang chạy với hệ thống đã treo.","blue")}
  {bx("Ràng buộc kiểm thử","Giao diện dựng câu trả lời theo đúng thứ tự sources → token → goi_y → done. Thiếu một sự kiện thì khung chat đứng im mà không báo lỗi, nên thứ tự này được khoá lại bằng kiểm thử tự động.","green")}
</div>
""")

render_many([
    (f9,  'fig/f09_may_trang_thai.png', 1560, 760),
    (f10, 'fig/f10_trien_khai.png',     1520, 1000),
    (f11, 'fig/f11_ndjson.png',         1520, 900),
], scale=2)
