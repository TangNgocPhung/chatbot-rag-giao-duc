# -*- coding: utf-8 -*-
"""Sửa nội dung, bố cục và hình thức tệp Word — phần 2.

Phần 2 bổ sung: danh mục hình, các mục còn thiếu, chú thích bảng, nội dung phụ
lục và toàn bộ hình minh hoạ mới.
"""
import sys; sys.path.insert(0, '.')
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from docx.shared import Cm, Pt
from docx.text.paragraph import Paragraph

from docx_helpers import (paragraphs, find, find_contains, set_text, replace_text,
                          insert_after, insert_before, insert_paragraphs_after,
                          iter_blocks, toc_field, add_figure_after, add_table_caption)

doc = docx.Document('out_part1.docx')
FIG = 'fig/'
log = []
def L(m): log.append(m); print('·', m)

def body(ref, text):
    return insert_after(ref, doc, text)

def h2(ref, text):
    return insert_after(ref, doc, text, style='Heading 2')

def h3(ref, text):
    return insert_after(ref, doc, text, style='Heading 3')

def bullet(ref, text):
    p = insert_after(ref, doc, text, style='List Paragraph')
    return p

# =========================================================================
# E. DANH MỤC HÌNH ẢNH (trước đây để trống)
# =========================================================================
h = find(doc, 'DANH MỤC HÌNH ẢNH', style='Heading 1')
fld = toc_field(doc, 'TOC \\h \\z \\c "Hình"',
                'Nhấn Ctrl+A rồi F9 trong Word để sinh danh mục hình.')
h._p.addnext(fld)
L('Chèn trường danh mục hình vào mục "DANH MỤC HÌNH ẢNH/BIỂU ĐỒ" (trước đây bỏ trống)')

# =========================================================================
# F. DANH MỤC CHỮ VIẾT TẮT: bổ sung các từ đã dùng trong bài nhưng chưa liệt kê
# =========================================================================
ABBR_NEW = [
    ('BERT', 'Bidirectional Encoder Representations from Transformers', 'Mô hình biểu diễn ngôn ngữ hai chiều dựa trên Transformer'),
    ('IDF', 'Inverse Document Frequency', 'Nghịch đảo tần suất tài liệu'),
    ('JSON', 'JavaScript Object Notation', 'Định dạng trao đổi dữ liệu JSON'),
    ('NDJSON', 'Newline Delimited JSON', 'Chuỗi JSON phân tách bằng ký tự xuống dòng'),
    ('RRF', 'Reciprocal Rank Fusion', 'Hợp nhất theo nghịch đảo thứ hạng'),
    ('SHA', 'Secure Hash Algorithm', 'Thuật toán băm an toàn'),
    ('SSRF', 'Server-Side Request Forgery', 'Giả mạo yêu cầu phía máy chủ'),
]
tbl = None
for b in iter_blocks(doc):
    if not isinstance(b, Paragraph) and len(b.columns) == 4 and 'Ký hiệu viết tắt' in b.rows[0].cells[1].text:
        tbl = b
        break
assert tbl is not None, 'Không tìm thấy bảng chữ viết tắt'
have = {r.cells[1].text.strip() for r in tbl.rows[1:]}
rows = [(r.cells[1].text.strip(), r.cells[2].text.strip(), r.cells[3].text.strip())
        for r in tbl.rows[1:]]
added = [a for a in ABBR_NEW if a[0] not in have]
rows.extend(added)
rows.sort(key=lambda r: r[0].lower())
for i, (k, en, vi) in enumerate(rows, 1):
    if i < len(tbl.rows):
        row = tbl.rows[i]
    else:
        row = tbl.add_row()
    for cell, val in zip(row.cells, (str(i), k, en, vi)):
        cell.text = val
        for p in cell.paragraphs:
            p.paragraph_format.first_line_indent = Cm(0)
L(f'Bổ sung {len(added)} mục vào danh mục chữ viết tắt ({", ".join(a[0] for a in added)}) và sắp xếp lại theo bảng chữ cái')

# =========================================================================
# G. CHƯƠNG 1 — hình minh hoạ và mục nghiên cứu liên quan
# =========================================================================
p = find_contains(doc, 'Các mô hình embedding hiện đại, trong đó có bge-m3')
add_figure_after(p, doc, FIG + 'f01_transformer.png',
                 'Kiến trúc khối Transformer và hai dòng mô hình kế thừa (encoder-only, decoder-only)',
                 chapter=1, number=1, width_cm=15.5)
L('Thêm hình minh hoạ kiến trúc Transformer vào mục 1.2')

p = find_contains(doc, 'Pha trực tuyến (querying) tiếp nhận câu hỏi')
add_figure_after(p, doc, FIG + 'f02_hai_pha_rag.png',
                 'Hai pha của một hệ thống RAG: pha ngoại tuyến dựng kho tri thức và pha trực tuyến phục vụ câu hỏi',
                 chapter=1, number=2, width_cm=15.5)
L('Thêm hình hai pha của hệ thống RAG vào mục 1.3.2')

p = find(doc, 'Để triển khai hệ thống chatbot RAG, nhóm tác giả sử dụng')
add_figure_after(p, doc, FIG + 'repo_cong_nghe_su_dung.png',
                 'Bản đồ công nghệ của hệ thống: bốn lớp chức năng và các thành phần mã nguồn mở tương ứng',
                 chapter=1, number=3, width_cm=15.0)
L('Thêm hình tổng quan các công nghệ sử dụng vào đầu mục 1.4')

# --- Mục mới: Một số nghiên cứu liên quan --------------------------------
anchor = find(doc, 'Các chỉ số đánh giá hiệu năng', style='Heading 2')
new_h = insert_before(anchor, doc, 'Một số nghiên cứu liên quan', style='Heading 2')
cur = new_h
for t in [
  'Kỹ thuật RAG được Lewis và cộng sự [4] đề xuất năm 2020 dưới dạng một kiến trúc hai thành phần: '
  'một bộ truy hồi dense và một mô hình sinh, huấn luyện phối hợp với nhau. Các hệ thống ứng dụng về '
  'sau hầu như không huấn luyện lại hai thành phần này mà ghép chúng ở mức suy luận, nhờ đó có thể '
  'thay mô hình sinh mà không đụng tới kho vector — đây cũng là cách hệ thống của đề tài được tổ chức.',

  'Khảo sát của Gao và cộng sự [5] hệ thống hoá các biến thể RAG thành ba nhóm. Naive RAG thực hiện '
  'tuần tự truy hồi rồi sinh. Advanced RAG bổ sung các bước tiền xử lý truy vấn (viết lại, mở rộng, '
  'định tuyến) và hậu xử lý kết quả truy hồi (xếp hạng lại, nén ngữ cảnh). Modular RAG tổ chức các '
  'bước thành những mô-đun có thể thay thế và lặp lại. Đối chiếu với phân loại này, hệ thống của đề '
  'tài thuộc nhóm Advanced RAG: có hậu xử lý bằng hợp nhất thứ hạng và xếp hạng lại, có định tuyến '
  'theo quy tắc, nhưng chưa có vòng lặp truy hồi – sinh – truy hồi lại như các kiến trúc Modular.',

  'Ở khâu truy hồi, hai hướng tiếp cận tồn tại song song. Hướng thưa (sparse) dựa trên thống kê từ '
  'khoá mà đại diện là BM25 [10], mạnh khi câu hỏi chứa thuật ngữ, số hiệu văn bản hoặc tên riêng '
  'xuất hiện nguyên văn trong tài liệu. Hướng dày (dense) dựa trên vector ngữ nghĩa, mạnh khi câu '
  'hỏi và tài liệu diễn đạt cùng một ý bằng những từ khác nhau. Nhiều công trình cho thấy hai hướng '
  'này bổ sung cho nhau hơn là thay thế nhau, nên các hệ thống thực tế thường kết hợp cả hai.',

  'Để kết hợp, Cormack và cộng sự [11] đề xuất Reciprocal Rank Fusion — một phương pháp chỉ dựa trên '
  'thứ hạng nên không cần chuẩn hoá điểm số giữa các nhánh và không cần huấn luyện trọng số. Đơn '
  'giản như vậy nhưng RRF vẫn vượt các phương pháp hợp nhất phức tạp hơn trong thực nghiệm của nhóm '
  'tác giả, và đó là lý do phương pháp này được chọn cho hệ thống của đề tài thay vì cộng điểm có '
  'trọng số.',

  'Về mô hình biểu diễn, bge-m3 [13] được thiết kế cho dữ liệu đa ngôn ngữ và hỗ trợ đồng thời ba '
  'chế độ biểu diễn (dense, sparse, multi-vector). Đề tài chỉ khai thác chế độ dense qua Ollama, '
  'phần truy hồi từ khoá được đảm nhiệm bằng BM25 chạy riêng — một lựa chọn đánh đổi giữa chất lượng '
  'và khả năng vận hành trên máy chỉ có CPU.',

  'Điểm khác biệt của đề tài so với các công trình trên nằm ở ràng buộc triển khai và ở miền dữ liệu. '
  'Các nghiên cứu được trích dẫn đánh giá trên tập chuẩn tiếng Anh và giả định có GPU; hệ thống ở đây '
  'phải chạy trọn vẹn trên một máy tính cá nhân không GPU, với kho văn bản quy phạm tiếng Việt nơi '
  'hai văn bản gần như trùng nghĩa (bản cũ và bản thay thế) tồn tại song song. Ràng buộc đó dẫn tới '
  'hai lựa chọn thiết kế riêng: xếp hạng lại bằng heuristic thay vì cross-encoder, và bổ sung tín '
  'hiệu hiệu lực văn bản vào điểm xếp hạng.',
]:
    cur = body(cur, t)
L('Bổ sung mục 1.5 "Một số nghiên cứu liên quan" — phần khảo sát công trình liên quan mà bản cũ chưa có')

p = find_contains(doc, 'nDCG@10 = 1: thứ hạng đạt mức lý tưởng')
add_figure_after(p, doc, FIG + 'f05_chi_so_ir.png',
                 'Cách đọc ba chỉ số Hit@K, MRR@10 và nDCG@10 trên cùng một danh sách kết quả truy hồi',
                 chapter=1, number=4, width_cm=15.5)
L('Thêm hình minh hoạ cách đọc ba chỉ số IR vào cuối Chương 1')

# =========================================================================
# H. CHƯƠNG 2 — hình minh hoạ và mục mới về định tuyến câu hỏi
# =========================================================================
p = find_contains(doc, 'Từ cách triển khai trên, có thể thấy hai điểm nhấn kỹ thuật')
add_figure_after(p, doc, FIG + 'repo_kien_truc.png',
                 'Sơ đồ chi tiết kiến trúc và luồng xử lý, dựng theo đúng các hằng số mặc định trong mã nguồn',
                 chapter=2, number=2, width_cm=15.5)
L('Thêm sơ đồ kiến trúc chi tiết (dựng từ mã nguồn) vào cuối mục 2.1')

p = find(doc, 'Ingestion là giai đoạn đầu tiên của pipeline RAG')
add_figure_after(p, doc, FIG + 'f06_ingestion.png',
                 'Luồng nạp dữ liệu: từ nguồn tài liệu tới chỉ mục FAISS và BM25',
                 chapter=2, number=3, width_cm=15.5)
L('Thêm hình luồng nạp dữ liệu và phân đoạn vào mục 2.2')

p = find_contains(doc, 'Đặc điểm này cũng được phản ánh trong cơ chế đánh giá của hệ thống')
add_figure_after(p, doc, FIG + 'f03_khong_gian_vector.png',
                 'Không gian biểu diễn dùng chung cho câu hỏi và đoạn tài liệu, cùng quy ước đọc khoảng cách Euclid',
                 chapter=2, number=4, width_cm=15.0)
L('Thêm hình minh hoạ không gian vector và độ đo khoảng cách vào mục 2.3')

p = find_contains(doc, 'Cách tiếp cận này cho phép kết hợp kết quả từ hai phương pháp')
add_figure_after(p, doc, FIG + 'f04_rrf.png',
                 'Ví dụ hợp nhất hai bảng xếp hạng bằng RRF với hằng số k = 60',
                 chapter=2, number=5, width_cm=15.5)
L('Thêm hình ví dụ tính điểm RRF vào mục 2.4.3')

p = find_contains(doc, 'Đa lượt hội thoại:')
add_figure_after(p, doc, FIG + 'f07_prompt_evidence.png',
                 'Cấu trúc prompt gửi tới mô hình ngôn ngữ và hai lớp hậu kiểm câu trả lời',
                 chapter=2, number=6, width_cm=15.5)
L('Thêm hình cấu trúc prompt và hậu kiểm vào mục 2.6')

# --- Mục mới 2.7: định tuyến câu hỏi và các lối tắt ----------------------
anchor = find(doc, 'Giao diện người dùng', style='Heading 2')
new_h = insert_before(anchor, doc, 'Định tuyến câu hỏi và các lối tắt trước dây chuyền RAG',
                      style='Heading 2')
cur = new_h
for t in [
  'Không phải câu hỏi nào gửi tới hệ thống cũng cần đi trọn dây chuyền truy hồi rồi sinh câu trả lời. '
  'Trên máy chỉ có CPU, mỗi lượt sinh tốn trung bình khoảng 150 giây, nên những câu trả lời được bằng '
  'cách khác — và trả lời chính xác hơn — được tách ra thành các nhánh riêng đặt trước khâu truy hồi. '
  'Mục này mô tả bốn nhóm lối tắt đó cùng thứ tự thử giữa chúng.',

  'Công cụ tính bằng Python. Hệ thống có bốn mô-đun trả lời trực tiếp mà không gọi mô hình ngôn ngữ: '
  'tinh_luong.py tính lương nhà giáo, dinh_muc_tiet_day.py tính định mức tiết dạy và các khoản giảm '
  'trừ, danh_gia_hoc_sinh.py tính điểm trung bình môn có trọng số và xếp loại học sinh, tinh_toan.py '
  'xử lý các biểu thức số học thuần tuý. Lý do tách khỏi RAG nằm ở chính ba lớp bảo vệ của hệ thống: '
  'prompt cấm ghép số liệu của hai khối bằng chứng khác nhau, trong khi tính lương đúng là lấy hệ số '
  'ở Thông tư nhân với mức lương cơ sở ở Nghị định; hậu kiểm gắn cờ mọi con số không xuất hiện nguyên '
  'văn trong đoạn trích, mà kết quả phép tính thì không văn bản nào chứa sẵn; và một mô hình bốn tỷ '
  'tham số chạy trên CPU không đáng tin ở số học nhiều bước. Nới ba lớp đó ra để mô hình được làm '
  'toán là một đánh đổi sai, nên phép tính được giao cho Python, còn căn cứ pháp lý của từng hằng số '
  'được mô-đun can_cu_van_ban.py gắn kèm dưới dạng chip nguồn bấm được.',

  'Thứ tự thử giữa các công cụ có ý nghĩa: ba công cụ gắn với văn bản quy phạm được thử trước, '
  'tinh_toan.py đứng sau cùng vì cổng nhận của nó rộng nhất và sẽ nuốt mất phần của ba công cụ kia '
  'nếu đảo thứ tự. Cổng nhận của mọi công cụ đều được đặt hẹp có chủ đích, bởi nhận nhầm một câu tra '
  'cứu khiến người dùng mất hẳn câu trả lời, trong khi bỏ sót một câu số học chỉ khiến họ phải chờ '
  'lâu như cũ.',

  'Bộ nhớ đệm ngữ nghĩa. Câu hỏi tra cứu văn bản giáo dục lặp lại rất nhiều giữa những người dùng '
  'khác nhau, nhưng hiếm khi lặp lại nguyên văn. Vì vậy cache_ngu_nghia.py không khoá bộ nhớ đệm theo '
  'chuỗi ký tự mà theo vector: câu hỏi được nhúng bằng chính mô hình bge-m3 đang chạy, và câu trả lời '
  'cũ chỉ được dùng lại khi độ tương đồng đạt ngưỡng cao cùng với điều kiện trùng mô hình sinh và '
  'trùng tập đoạn bằng chứng. Chi phí nhúng thêm khoảng 0,1 giây, đổi lại tiết kiệm trọn 150 giây '
  'sinh văn bản. Câu trả lời bị hậu kiểm gắn cảnh báo thì không được ghi vào bộ nhớ đệm.',

  'Hỏi đáp trên tệp đính kèm. Tệp người dùng thả vào khung chat là dữ liệu dùng một lần, nên hệ thống '
  'không nhúng vào FAISS chung — vừa mất hàng phút cho một tệp dày, vừa làm nhiễu chỉ mục chính. Thay '
  'vào đó tep_dinh_kem.py chỉ phân đoạn rồi dựng một chỉ mục BM25 riêng cho từng tệp; phạm vi tìm '
  'kiếm chỉ còn vài chục đoạn nên truy hồi từ khoá là đủ. Việc đọc tệp chạy nền vì một tệp PDF bản '
  'quét phải qua OCR còn video phải phiên âm; bản gốc sau đó được chép sang kho tài liệu chung để lần '
  'sau không phải đính kèm lại.',

  'Câu hỏi kèm URL. Khi người dùng dán một đường dẫn, web_loader.py tải trang qua trafilatura và dùng '
  'nội dung đó làm ngữ cảnh cho đúng lượt hỏi đáp tương ứng, không đưa vào kho vector nội bộ. Nhờ '
  'tách biệt như vậy, nội dung Internet không làm thay đổi kho tri thức chính thống của đơn vị.',
]:
    cur = body(cur, t)
for label in ('Công cụ tính bằng Python.', 'Bộ nhớ đệm ngữ nghĩa.',
              'Hỏi đáp trên tệp đính kèm.', 'Câu hỏi kèm URL.'):
    for q in paragraphs(doc):
        if q.text.startswith(label):
            full = q.text
            set_text(q, '')
            r1 = q.add_run(label); r1.bold = True
            q.add_run(full[len(label):])
            break
L('Bổ sung mục 2.7 "Định tuyến câu hỏi và các lối tắt trước dây chuyền RAG" — lớp công cụ tính, '
  'bộ nhớ đệm ngữ nghĩa, tệp đính kèm và URL đã có trong mã nguồn nhưng chưa được mô tả')

fig_p = add_figure_after(cur, doc, FIG + 'f08_dinh_tuyen.png',
                 'Thứ tự định tuyến câu hỏi: bốn lối tắt được thử trước khi vào dây chuyền RAG đầy đủ',
                 chapter=2, number=7, width_cm=15.5)
fig_p = add_figure_after(fig_p, doc, FIG + 'repo_so_do_quy_trinh.png',
                 'Tám bước xử lý một lượt hỏi – đáp, kể cả các nhánh thoát sớm và nhánh từ chối trả lời',
                 chapter=2, number=8, width_cm=15.5)
L('Thêm hai hình cho mục 2.7: sơ đồ định tuyến và sơ đồ tám bước hỏi – đáp')

# Giao diện: bổ sung ảnh bản dựng trên điện thoại
p = find_contains(doc, 'Nhìn chung, giao diện được thiết kế theo hướng tập trung vào ba nhóm chức năng')
add_figure_after(p, doc, '/home/user/chatbot-rag-giao-duc/ui-mobile.png',
                 'Giao diện trên màn hình điện thoại: thanh bên thu gọn, khung hội thoại và nguồn trích dẫn giữ nguyên',
                 chapter=2, number=9, width_cm=8.0)
L('Thêm ảnh giao diện trên điện thoại vào mục 2.8')

doc.save('out_part2.docx')
print(f'\nĐÃ GHI out_part2.docx — {len(log)} thay đổi')
