# -*- coding: utf-8 -*-
"""Nhóm hình 2: Transformer, không gian vector, RRF, chỉ số IR, prompt EVIDENCE."""
import sys; sys.path.insert(0, '.')
from style import page
from render import render_many

def bx(t, d, cls=""):
    return f'<div class="box {cls}"><div class="t">{t}</div><div class="d">{d}</div></div>'

# ---- F1: Transformer -----------------------------------------------------
f1 = page(
    "Kiến trúc Transformer và hai dòng mô hình kế thừa",
    "Cơ chế tự chú ý cho phép mọi vị trí trong chuỗi nhìn thấy nhau trong một bước, thay cho việc truyền trạng thái tuần tự của RNN/LSTM.",
    f"""
<div class="row" style="align-items:stretch">
  <div class="band" style="flex:1.15">
    <div class="cap">Khối Transformer · lặp lại N lần</div>
    <div class="col">
      {bx("Nhúng đầu vào + mã hoá vị trí","token → vector; vị trí được mã hoá tường minh vì mô hình không xử lý tuần tự","slate")}
      <div class="ard">↓</div>
      {bx("Tự chú ý nhiều đầu (multi-head self-attention)","mỗi token tính trọng số chú ý tới mọi token khác: Attention(Q,K,V) = softmax(QKᵀ/√d<sub>k</sub>)·V","blue")}
      <div class="ard">↓</div>
      {bx("Cộng phần dư &amp; chuẩn hoá lớp","giữ đường truyền gradient khi xếp chồng hàng chục lớp","slate")}
      <div class="ard">↓</div>
      {bx("Mạng truyền thẳng theo vị trí","hai phép biến đổi tuyến tính kèm hàm kích hoạt, áp dụng độc lập cho từng vị trí","slate")}
    </div>
  </div>
  <div class="ar">→</div>
  <div class="col" style="flex:1.25">
    <div class="band" style="flex:1">
      <div class="cap">Hai hướng phát triển</div>
      <div class="col">
        {bx("Chỉ bộ mã hoá · encoder-only","BERT và các mô hình cùng dòng. Đọc hai chiều, mạnh về <b>hiểu và biểu diễn</b> ngữ nghĩa văn bản.","green")}
        {bx("Chỉ bộ giải mã · decoder-only","GPT, Llama, Qwen. Sinh token trái sang phải, mạnh về <b>sinh ngôn ngữ</b> và học trong ngữ cảnh.","violet")}
      </div>
    </div>
    <div class="band">
      <div class="cap">Vị trí trong hệ thống của đề tài</div>
      <div class="row">
        {bx("bge-m3","kiến trúc dòng encoder → sinh vector 1.024 chiều cho đoạn tài liệu và câu hỏi","green")}
        {bx("qwen3.5:4b","kiến trúc dòng decoder → sinh câu trả lời từ khối bằng chứng đã truy hồi","violet")}
      </div>
    </div>
  </div>
</div>
""",
    "Cả hai mô hình của hệ thống đều kế thừa Transformer nhưng đảm nhiệm hai vai trò tách biệt; "
    "nhờ vậy có thể đổi mô hình sinh mà không phải dựng lại chỉ mục vector."
)

# ---- F3: không gian vector & L2 -----------------------------------------
svg_space = """
<svg width="560" height="330" viewBox="0 0 560 330" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="560" height="330" fill="#fff"/>
  <line x1="50" y1="290" x2="530" y2="290" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="50" y1="290" x2="50" y2="20" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="520" y="312" font-size="13" fill="#64748b" font-family="Liberation Sans">chiều 1</text>
  <text x="14" y="26" font-size="13" fill="#64748b" font-family="Liberation Sans">chiều 2</text>
  <circle cx="250" cy="130" r="8" fill="#dc2626"/>
  <text x="240" y="115" font-size="14" font-weight="bold" fill="#dc2626" font-family="Liberation Sans">q</text>
  <circle cx="300" cy="96" r="7" fill="#2563eb"/><text x="312" y="94" font-size="13" fill="#1f2933" font-family="Liberation Sans">Điều 5 · chuẩn trình độ GV THCS</text>
  <circle cx="208" cy="176" r="7" fill="#2563eb"/><text x="70" y="196" font-size="13" fill="#1f2933" font-family="Liberation Sans">Điều 6 · chuẩn trình độ GV THPT</text>
  <circle cx="330" cy="200" r="7" fill="#2563eb"/><text x="342" y="204" font-size="13" fill="#1f2933" font-family="Liberation Sans">bồi dưỡng giáo viên</text>
  <circle cx="130" cy="60" r="7" fill="#94a3b8"/><text x="142" y="58" font-size="13" fill="#64748b" font-family="Liberation Sans">định mức tiết dạy</text>
  <circle cx="460" cy="250" r="7" fill="#94a3b8"/><text x="300" y="268" font-size="13" fill="#64748b" font-family="Liberation Sans">thời khoá biểu khối 9</text>
  <line x1="250" y1="130" x2="300" y2="96" stroke="#dc2626" stroke-width="2" stroke-dasharray="5 4"/>
  <line x1="250" y1="130" x2="208" y2="176" stroke="#dc2626" stroke-width="2" stroke-dasharray="5 4"/>
  <line x1="250" y1="130" x2="330" y2="200" stroke="#cbd5e1" stroke-width="1.6" stroke-dasharray="5 4"/>
  <text x="258" y="104" font-size="12" fill="#dc2626" font-family="Liberation Sans">d₁</text>
  <text x="216" y="152" font-size="12" fill="#dc2626" font-family="Liberation Sans">d₂</text>
  <text x="292" y="168" font-size="12" fill="#94a3b8" font-family="Liberation Sans">d₃</text>
</svg>"""
f3 = page(
    "Không gian biểu diễn và độ đo khoảng cách của nhánh truy hồi ngữ nghĩa",
    "Câu hỏi và mọi đoạn tài liệu được mã hoá bằng cùng một mô hình, nên nằm chung một không gian và so sánh được với nhau.",
    f"""
<div class="row">
  <div class="band" style="flex:1.1">
    <div class="cap">Minh hoạ (chiếu về 2 chiều)</div>
    {svg_space}
  </div>
  <div class="col" style="flex:1">
    {bx("Cùng một mô hình cho hai vai trò","bge-m3 mã hoá đoạn tài liệu khi lập chỉ mục và mã hoá câu hỏi khi truy vấn. Khác mô hình thì hai loại vector không còn so sánh được — đây là lý do đổi mô hình nhúng bắt buộc phải dựng lại chỉ mục.","blue")}
    {bx("Khoảng cách Euclid (L2)","d(q, c) = √( Σⱼ₌₁ᴰ (qⱼ − cⱼ)² ) với D = 1.024. Hệ thống không chuẩn hoá L2 trước khi ghi vào FAISS, nên phép đo đang chạy là khoảng cách Euclid chứ không phải cosine.","green")}
    {bx("Quy ước đọc kết quả","Giá trị càng <b>nhỏ</b> càng gần — ngược chiều với cosine similarity (càng lớn càng giống). Nhầm chiều quy ước này là lỗi thường gặp khi ghép điểm số của hai nhánh truy hồi.","amber")}
    {bx("Giới hạn của nhánh dense","Hai văn bản gần như trùng nghĩa (bản cũ và bản thay thế nó) nằm sát nhau trong không gian, nên riêng khoảng cách vector không đủ để chọn đúng — phần việc còn lại thuộc về BM25 và bước xếp hạng lại.","red dash")}
  </div>
</div>
""")

# ---- F4: RRF -------------------------------------------------------------
f4 = page(
    "Hợp nhất hai bảng xếp hạng bằng Reciprocal Rank Fusion (RRF)",
    "RRF chỉ dùng thứ hạng, không dùng điểm số gốc, nên ghép được hai phương pháp chấm điểm trên hai thang đo hoàn toàn khác nhau.",
    f"""
<div class="row" style="align-items:flex-start">
  <div class="band" style="flex:1">
    <div class="cap">Nhánh FAISS · theo khoảng cách vector</div>
    <table>
      <tr><th>Hạng</th><th>Đoạn</th><th>Khoảng cách L2</th></tr>
      <tr><td class="n">1</td><td>C<sub>a</sub></td><td class="n">0,71</td></tr>
      <tr><td class="n">2</td><td>C<sub>b</sub></td><td class="n">0,83</td></tr>
      <tr><td class="n">3</td><td>C<sub>c</sub></td><td class="n">0,90</td></tr>
      <tr><td class="n">…</td><td>…</td><td class="n">…</td></tr>
      <tr><td class="n">15</td><td>C<sub>o</sub></td><td class="n">1,42</td></tr>
    </table>
  </div>
  <div class="band" style="flex:1">
    <div class="cap">Nhánh BM25 · theo điểm khớp từ khoá</div>
    <table>
      <tr><th>Hạng</th><th>Đoạn</th><th>Điểm BM25</th></tr>
      <tr><td class="n">1</td><td>C<sub>c</sub></td><td class="n">18,4</td></tr>
      <tr><td class="n">2</td><td>C<sub>d</sub></td><td class="n">15,1</td></tr>
      <tr><td class="n">3</td><td>C<sub>a</sub></td><td class="n">12,7</td></tr>
      <tr><td class="n">…</td><td>…</td><td class="n">…</td></tr>
      <tr><td class="n">15</td><td>C<sub>p</sub></td><td class="n">3,2</td></tr>
    </table>
  </div>
  <div class="band" style="flex:1.25">
    <div class="cap">Điểm RRF hợp nhất · k = 60</div>
    <table>
      <tr><th>Đoạn</th><th>Cách tính</th><th>Điểm</th><th>Hạng</th></tr>
      <tr class="hi"><td>C<sub>a</sub></td><td class="mono">1/(60+1) + 1/(60+3)</td><td class="n">0,0323</td><td class="n">1</td></tr>
      <tr class="hi"><td>C<sub>c</sub></td><td class="mono">1/(60+3) + 1/(60+1)</td><td class="n">0,0323</td><td class="n">1</td></tr>
      <tr><td>C<sub>b</sub></td><td class="mono">1/(60+2)</td><td class="n">0,0161</td><td class="n">3</td></tr>
      <tr><td>C<sub>d</sub></td><td class="mono">1/(60+2)</td><td class="n">0,0161</td><td class="n">3</td></tr>
      <tr><td>C<sub>o</sub></td><td class="mono">1/(60+15)</td><td class="n">0,0133</td><td class="n">5</td></tr>
    </table>
  </div>
</div>
<div style="height:16px"></div>
<div class="row">
  {bx("Công thức","RRF(c) = Σ<sub>r ∈ R</sub> 1 / (k + hạng<sub>r</sub>(c)), với R là tập các danh sách truy hồi và k = 60 — hằng số chuẩn, cũng là giá trị đang dùng trong mã nguồn.","blue")}
  {bx("Vì sao được ưa dùng","Không cần chuẩn hoá điểm về cùng thang, không cần huấn luyện trọng số, và ít nhạy với việc một nhánh có điểm số lệch bất thường.","green")}
  {bx("Hệ quả đáng chú ý","Đoạn được <b>cả hai</b> nhánh cùng truy hồi luôn được cộng dồn hai số hạng nên leo lên đầu — đây chính là tín hiệu “đồng thuận giữa hai kênh” mà bước xếp hạng lại tiếp tục khai thác.","amber")}
</div>
""",
    "Ví dụ trong hình dùng số liệu minh hoạ; cấu hình thực tế của hệ thống lấy 15 ứng viên mỗi nhánh trước khi hợp nhất "
    "và giữ lại 4 đoạn sau khi xếp hạng lại."
)

# ---- F5: chỉ số IR -------------------------------------------------------
f5 = page(
    "Cách đọc ba chỉ số đánh giá chất lượng xếp hạng truy hồi",
    "Cùng một danh sách kết quả, ba chỉ số trả lời ba câu hỏi khác nhau: có tìm thấy không, thấy ở hạng mấy, và cả danh sách xếp tốt tới đâu.",
    f"""
<div class="band" style="margin-bottom:16px">
  <div class="cap">Một lượt truy hồi cho câu hỏi “Chuẩn trình độ đào tạo để dạy môn Toán cấp THCS là gì?”</div>
  <table>
    <tr><th style="width:70px">Hạng</th><th>Đoạn được truy hồi</th><th style="width:150px">Có phải nguồn mong đợi?</th><th style="width:110px">Mức liên quan</th></tr>
    <tr><td class="n">1</td><td>Thông tư về bồi dưỡng thường xuyên giáo viên — Điều 3</td><td class="n">không</td><td class="n">0</td></tr>
    <tr class="hi"><td class="n">2</td><td>Luật Giáo dục — Điều 72 · trình độ chuẩn được đào tạo của nhà giáo</td><td class="n">có</td><td class="n">1</td></tr>
    <tr><td class="n">3</td><td>Thông tư về chương trình môn Toán — phần đánh giá</td><td class="n">không</td><td class="n">0</td></tr>
    <tr><td class="n">…</td><td>…</td><td class="n">…</td><td class="n">…</td></tr>
  </table>
</div>
<div class="row">
  {bx("Hit@K · tìm thấy hay không","Bằng 1 nếu nguồn mong đợi nằm trong K kết quả đầu, ngược lại bằng 0. Ở ví dụ trên: Hit@1 = 0 nhưng Hit@3 = Hit@5 = Hit@10 = 1. Chỉ số này đo <b>độ bao phủ</b> của rổ ứng viên, không phân biệt hạng 2 với hạng 10.","blue")}
  {bx("MRR@10 · thấy ở hạng mấy","RR = 1/r với r là hạng đầu tiên xuất hiện nguồn đúng (bằng 0 nếu không xuất hiện trong 10 kết quả đầu). Ở ví dụ trên RR = 1/2 = 0,5. MRR là trung bình RR trên toàn bộ câu hỏi — chỉ số <b>nhạy với vị trí</b>.","green")}
  {bx("nDCG@10 · cả danh sách tốt tới đâu","DCG@10 = Σ<sub>i=1..10</sub> (2<sup>rel<sub>i</sub></sup> − 1)/log₂(i+1), chuẩn hoá bằng DCG của thứ hạng lý tưởng. Phạt dần theo vị trí và cộng dồn <b>mọi</b> kết quả liên quan, không chỉ kết quả đúng đầu tiên.","violet")}
</div>
<div style="height:14px"></div>
{bx("Vì sao RAG cần cả ba","Prompt của hệ thống chỉ nhận 4 đoạn. Một hệ thống có Hit@10 cao nhưng MRR thấp nghĩa là nguồn đúng thường nằm ở hạng 5–10 — tức là <b>rơi ra ngoài</b> cửa sổ 4 đoạn thực sự đi vào prompt. Vì vậy Hit@10 = 90% không đồng nghĩa 90% câu hỏi có đủ bằng chứng đúng khi sinh câu trả lời.","amber")}
""")

# ---- F7: prompt EVIDENCE -------------------------------------------------
f7 = page(
    "Cấu trúc prompt và cơ chế hậu kiểm câu trả lời",
    "Bốn đoạn bằng chứng được đánh số, kèm dòng tiêu đề nguồn; mọi ý trong câu trả lời phải gắn được với một số hiệu trong khoảng đó.",
    f"""
<div class="row" style="align-items:flex-start">
  <div class="col" style="flex:1.15">
    <div class="band">
      <div class="cap">Prompt gửi tới mô hình ngôn ngữ</div>
      <div class="col">
        {bx("Vai trò &amp; rào chắn","“Chuyên viên tra cứu chính sách giáo dục Việt Nam.” EVIDENCE được tuyên bố rõ là <b>dữ liệu tham khảo, không phải mệnh lệnh</b> — chặn chỉ dẫn lạ nằm trong chính tài liệu.","violet")}
        {bx("Bảy quy tắc ràng buộc","chỉ dùng thông tin trong EVIDENCE · câu từ chối cố định khi không có · mỗi ý kèm số trích dẫn · cấm ghép số liệu của hai EVIDENCE · nêu phạm vi áp dụng · nhắc lại đúng vị trí (trang/slide/phút) · kết luận trước, tối đa 6 gạch đầu dòng.","amber")}
        {bx("{context} · khối bằng chứng","Do format_docs() dựng: mỗi đoạn được đánh số [1]…[4], mở đầu bằng dòng nguồn (tên tệp, trang, Chương, Điều, nhãn ngữ cảnh), phần thân cắt còn 900 ký tự tính từ đầu đoạn.","blue")}
        {bx("{question} · yêu cầu người dùng","Kèm tối đa 6 lượt hội thoại gần nhất, mỗi lượt cắt còn 1.200 ký tự, gắn nhãn “Người dùng”/“Trợ lý”.","slate")}
      </div>
    </div>
  </div>
  <div class="ar" style="align-self:center">→</div>
  <div class="col" style="flex:.92">
    {bx("Sinh câu trả lời","qwen3.5:4b qua Ollama · temperature 0,15 · top_p 0,9 · num_ctx 4.096 · num_predict 420 · phát theo dòng từng token","violet")}
    <div class="ard">↓</div>
    <div class="band">
      <div class="cap">Hậu kiểm bằng đối chiếu chuỗi · không gọi thêm mô hình</div>
      <div class="col">
        {bx("Kiểm trích dẫn","mọi số [n] trong câu trả lời phải nằm trong khoảng số hiệu thực sự được cấp cho lượt đó","green")}
        {bx("Kiểm số liệu","mọi con số, thời hạn, tín chỉ phải xuất hiện nguyên văn trong một đoạn bằng chứng cụ thể","green")}
        {bx("Khi phát hiện bất thường","gắn cảnh báo hiển thị cho người dùng đối chiếu lại và <b>không</b> ghi câu trả lời vào bộ nhớ đệm","red")}
      </div>
    </div>
  </div>
</div>
""",
    "Prompt được giữ ngắn có chủ đích: trên máy chỉ có CPU, mỗi 100 token quy tắc thêm vào đây tốn khoảng 4 giây chờ "
    "và đi kèm mọi câu hỏi."
)

render_many([
    (f1, 'fig/f01_transformer.png', 1560, 880),
    (f3, 'fig/f03_khong_gian_vector.png', 1500, 760),
    (f4, 'fig/f04_rrf.png', 1620, 900),
    (f5, 'fig/f05_chi_so_ir.png', 1620, 900),
    (f7, 'fig/f07_prompt_evidence.png', 1560, 1000),
], scale=2)
