# -*- coding: utf-8 -*-
"""Sửa nội dung, bố cục và hình thức tệp Word — phần 1.

Phần 1 xử lý: hình thức trang, cấu trúc đề mục, các lỗi nội dung và số liệu,
đánh số lại trích dẫn và dựng danh mục tài liệu tham khảo.
"""
import sys; sys.path.insert(0, '.')
import re
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from docx.shared import Cm, Pt
from docx.text.paragraph import Paragraph

from docx_helpers import (paragraphs, find, find_contains, set_text, replace_text,
                          insert_after, insert_before, insert_paragraphs_after,
                          center_image_paragraphs, set_page_margins,
                          enable_update_fields, toc_field, iter_blocks)

doc = docx.Document('docx/orig.docx')
log = []
def L(msg): log.append(msg); print('·', msg)

# =========================================================================
# A. HÌNH THỨC TRÌNH BÀY
# =========================================================================
n = set_page_margins(doc)               # trên 2,5 · dưới 2,5 · trái 3 · phải 2 (cm)
L(f'Đồng nhất lề trang cho {n} phân đoạn: trên/dưới 2,5 cm, trái 3 cm, phải 2 cm')

# Phân đoạn cuối (Tài liệu tham khảo + Phụ lục) chưa có đầu trang nên mất số trang
sects = list(doc.element.body.iter(qn('w:sectPr')))
last = sects[-1]
if last.find(qn('w:headerReference')) is None:
    ref = parse_xml(
        '<w:headerReference %s xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        ' w:type="default" r:id="rId19"/>' % nsdecls('w'))
    last.insert(0, ref)
    L('Thêm đầu trang (số trang) cho phần Tài liệu tham khảo và Phụ lục')

n = center_image_paragraphs(doc)
L(f'Căn giữa và bỏ thụt dòng đầu cho {n} đoạn chứa ảnh')

# Kiểu Caption: căn giữa, không thụt dòng đầu, có khoảng cách trên/dưới
cap = doc.styles['Caption']
cap.paragraph_format.alignment = AL.CENTER
cap.paragraph_format.first_line_indent = Cm(0)
cap.paragraph_format.space_before = Pt(4)
cap.paragraph_format.space_after = Pt(10)
L('Chuẩn hoá kiểu "Caption": căn giữa, không thụt dòng đầu')

enable_update_fields(doc)
L('Bật cờ cập nhật trường khi mở tệp (mục lục, số hình, số bảng tự tính lại)')

core = doc.core_properties
core.title = 'Xây dựng chatbot RAG chuyên ngành giáo dục'
core.subject = 'Chuyên đề các vấn đề hiện đại trong Công nghệ thông tin'
core.keywords = 'RAG; chatbot; giáo dục; FAISS; BM25; Ollama; truy hồi thông tin'
L('Điền thuộc tính tài liệu (tiêu đề, học phần, từ khoá)')

# =========================================================================
# B. CẤU TRÚC ĐỀ MỤC
# =========================================================================
# B1. Bỏ hai đề mục bị gán thủ công sang danh sách đánh số khác (numId 31)
for title in ('Cấu hình phần cứng', 'Phần mềm nền'):
    p = find(doc, title, style='Heading 3')
    pPr = p._p.find(qn('w:pPr'))
    numPr = pPr.find(qn('w:numPr'))
    if numPr is not None:
        pPr.remove(numPr)
        L(f'Trả đề mục "{title}" về đúng mạch đánh số của Chương 3')

# B2. Hạ cấp các mục con bị để nhầm ở cấp 2
demote = ['Độ đo khoảng cách', 'Số lượng ứng viên trong truy hồi', 'Truy hồi câu hỏi',
          'Triển khai mô hình', 'Kết luận', 'Truy hồi ngữ nghĩa', 'Truy hồi theo từ khóa']
for title in demote:
    for p in paragraphs(doc):
        if p.style.name == 'Heading 2' and p.text.strip() == title:
            p.style = doc.styles['Heading 3']
            L(f'Hạ "{title}" từ cấp 2 xuống cấp 3 cho đúng quan hệ bao hàm')
            break

# "Kết luận" trong Chương 2 trùng tên với Chương 5 → đổi thành tiểu kết
for p in paragraphs(doc):
    if p.style.name == 'Heading 3' and p.text.strip() == 'Kết luận':
        set_text(p, 'Tiểu kết về lớp vector embedding')
        L('Đổi tên mục "Kết luận" trong Chương 2 thành "Tiểu kết về lớp vector embedding"')
        break

# Mục cấp 3 "Xếp hạng lại kết quả" trùng tên với mục cấp 2 ngay sau đó
for p in paragraphs(doc):
    if p.style.name == 'Heading 3' and p.text.strip() == 'Xếp hạng lại kết quả':
        set_text(p, 'Chuyển sang bước xếp hạng lại')
        L('Đổi tên mục cấp 3 "Xếp hạng lại kết quả" để không trùng mục cấp 2')
        break

# =========================================================================
# C. SỬA NỘI DUNG SAI
# =========================================================================
# C1 – Lời cam đoan: đề tài do ba học viên thực hiện, không phải cá nhân
p = find(doc, 'Tôi cam đoan đây là công trình nghiên cứu')
set_text(p, 'Nhóm tác giả cam đoan đây là công trình nghiên cứu của nhóm, được thực hiện dưới '
            'sự hướng dẫn của giảng viên TS. Nguyễn Minh Hải. Các số liệu, tài liệu và kết quả '
            'trình bày trong bài là trung thực, được đo trực tiếp trên hệ thống do nhóm xây dựng, '
            'chưa từng được công bố trong bất kỳ công trình nào khác và có nguồn gốc trích dẫn rõ '
            'ràng. Nhóm tác giả xin hoàn toàn chịu trách nhiệm về lời cam đoan này.')
L('Viết lại Lời cam đoan cho đúng chủ thể (nhóm ba học viên, không phải cá nhân)')

# C2 – Lời cảm ơn: lỗi chính tả và sai tên học phần
p = find(doc, 'Trong quá trình học tập và hoàn thành học phần')
set_text(p, 'Trong quá trình học tập và hoàn thành học phần Chuyên đề các vấn đề hiện đại trong '
            'Công nghệ thông tin, nhóm tác giả đã nhận được sự quan tâm, hướng dẫn và giúp đỡ tận '
            'tình của giảng viên cùng nhà trường.')
L('Sửa lỗi chính tả "Công nghệ thông tins" trong Lời cảm ơn')

p = find(doc, 'Trước hết, tôi xin bày tỏ lòng biết ơn')
set_text(p, 'Trước hết, nhóm tác giả xin bày tỏ lòng biết ơn sâu sắc tới TS. Nguyễn Minh Hải – '
            'giảng viên giảng dạy học phần Chuyên đề các vấn đề hiện đại trong Công nghệ thông tin, '
            'người đã tận tâm truyền đạt kiến thức, định hướng tư duy khoa học và tạo điều kiện '
            'thuận lợi để nhóm hoàn thành bài tiểu luận này. Những bài giảng sâu sắc và các ý kiến '
            'góp ý quý báu của thầy đã giúp nhóm hiểu rõ hơn những nội dung cốt lõi của các kỹ '
            'thuật hiện đại trong xử lý ngôn ngữ tự nhiên và mô hình ngôn ngữ lớn, từ đó vận dụng '
            'vào quá trình học tập và nghiên cứu.')
L('Sửa tên môn học bị chép nhầm ("Các thuật toán tối ưu") trong Lời cảm ơn')

p = find(doc, 'Tôi cũng xin chân thành cảm ơn nhà trường')
set_text(p, 'Nhóm tác giả cũng xin chân thành cảm ơn nhà trường đã tạo môi trường học tập nghiêm '
            'túc, thuận lợi để học viên có điều kiện rèn luyện và nâng cao kiến thức. Do thời gian '
            'và năng lực còn hạn chế, bài tiểu luận không tránh khỏi những thiếu sót. Nhóm rất mong '
            'nhận được sự góp ý của giảng viên để bài làm được hoàn thiện hơn.')
L('Chuẩn hoá xưng hô trong Lời cảm ơn (sinh viên → học viên cao học)')

# C3 – Mô hình sinh mặc định thực tế là qwen3.5:4b
p = find_contains(doc, 'mô hình ngôn ngữ llama3.2:3b')
replace_text(p, 'mô hình ngôn ngữ llama3.2:3b', 'mô hình ngôn ngữ qwen3.5:4b')
L('Sửa mô hình sinh trong Phạm vi nghiên cứu: llama3.2:3b → qwen3.5:4b (đúng mã nguồn)')

p = find(doc, 'RAG_LLM_MODEL=llama3.2:3b')
set_text(p, 'RAG_LLM_MODEL=qwen3.5:4b')
L('Sửa mẫu tệp /etc/chatbot-rag.env cho khớp mô hình mặc định')

# C4 – Bố cục: mâu thuẫn "ngoài phần Kết luận … năm chương" và sai tên chương
p = find(doc, 'Ngoài phần Mở đầu, Kết luận, Tài liệu tham khảo')
set_text(p, 'Ngoài phần Mở đầu, Tài liệu tham khảo và Phụ lục, nội dung chính của bài tiểu luận '
            'được tổ chức thành năm chương:')
chap = {
    'Chương 1: Cơ sở lý thuyết': 'Chương 1: Cơ sở lý thuyết – trình bày tổng quan về xử lý ngôn ngữ tự nhiên, kiến trúc Transformer, kỹ thuật RAG, các mô hình và công cụ mã nguồn mở được sử dụng, một số nghiên cứu liên quan và các chỉ số đánh giá.',
    'Chương 2: Thiết kế hệ thống': 'Chương 2: Thiết kế hệ thống – trình bày kiến trúc tổng thể, quy trình nạp dữ liệu, cơ chế truy hồi lai, xếp hạng lại, sinh câu trả lời có kiểm soát và giao diện người dùng.',
    'Chương 3: Xây dựng và triển khai hệ thống': 'Chương 3: Cài đặt và triển khai – mô tả môi trường thử nghiệm, cấu trúc mã nguồn, cấu hình vận hành và quy trình đưa hệ thống vào hoạt động.',
    'Chương 4: Kết quả thử nghiệm và đánh giá': 'Chương 4: Đánh giá thử nghiệm – trình bày bộ dữ liệu kiểm thử, các chế độ đo, kết quả định lượng và hạn chế của phương pháp đánh giá.',
    'Chương 5: Kết luận và hướng phát triển': 'Chương 5: Kết luận và hướng phát triển – tổng kết kết quả đạt được, nêu hạn chế còn tồn tại và đề xuất hướng phát triển tiếp theo.',
}
for old, new in chap.items():
    for q in paragraphs(doc):
        if q.text.strip().startswith(old):
            set_text(q, new)
            break
L('Viết lại mục "Bố cục bài tiểu luận": bỏ mâu thuẫn về số chương, sửa tên Chương 3 và Chương 4 cho khớp nội dung thật')

# C5 – xưng hô trong Chương 1
p = find(doc, 'Để triển khai hệ thống chatbot RAG, tôi sử dụng')
replace_text(p, 'tôi sử dụng', 'nhóm tác giả sử dụng')
L('Chuẩn hoá xưng hô ở mục 1.4')

# C6 – lỗi công thức MRR bị lặp ký tự khi dán từ trình soạn thảo công thức
p = find(doc, 'MRR@10 (Mean Reciprocal Rank at 10)')
txt = p.text.replace('ở hạng rr,', 'ở hạng r,').replace('là 1/r1/r;', 'là 1/r;')
for r in p.runs:
    if 'hạng rr' in r.text or '1/r1/r' in r.text:
        r.text = r.text.replace('ở hạng rr,', 'ở hạng r,').replace('là 1/r1/r;', 'là 1/r;')
L('Sửa công thức MRR bị lặp ký tự: "hạng rr" → "hạng r", "1/r1/r" → "1/r"')

p = find(doc, 'Trong đó N là tổng số câu hỏi được đánh giá')
set_text(p, 'Trong đó N là tổng số câu hỏi được đánh giá, rᵢ là vị trí (hạng) đầu tiên mà nguồn '
            'mong đợi xuất hiện đối với câu hỏi thứ i, và RRᵢ = 1/rᵢ là nghịch đảo của hạng đó '
            '(Reciprocal Rank); quy ước RRᵢ = 0 khi nguồn mong đợi không xuất hiện trong 10 kết '
            'quả đầu.')
L('Bổ sung quy ước RRᵢ = 0 khi trượt, và viết chỉ số dưới cho rᵢ, RRᵢ')

# C7 – số liệu thống kê mã nguồn đã cũ so với kho hiện tại
p = find(doc, 'Dự án gồm 32 module Python')
set_text(p, 'Dự án gồm 36 module Python ở thư mục gốc với khoảng 13.700 dòng mã, phần giao diện '
            'web tĩnh khoảng 3.270 dòng, cùng 24 tệp kiểm thử tự động khoảng 4.600 dòng.')
L('Cập nhật số liệu quy mô mã nguồn theo kho hiện tại (36 module · ~13.700 dòng · 24 tệp kiểm thử)')

p = find(doc, 'api.py khai báo khoảng 25 đầu cuối')
replace_text(p, 'api.py khai báo khoảng 25 đầu cuối', 'api.py khai báo 24 đầu cuối')
L('Sửa số đầu cuối API: khoảng 25 → 24 (đếm trực tiếp trong api.py)')

p = find_contains(doc, 'Toàn bộ khoảng 60 tham số được đọc từ biến môi trường')
replace_text(p, 'Toàn bộ khoảng 60 tham số', 'Toàn bộ gần 80 tham số')
L('Sửa số tham số môi trường: khoảng 60 → gần 80')

p = find_contains(doc, 'Thư mục tests/ chứa 17 tệp kiểm thử tự động')
replace_text(p, 'Thư mục tests/ chứa 17 tệp kiểm thử tự động bao phủ truy hồi, phân loại, bộ nhớ đệm, lịch sử, bảo vệ truy cập và trích dẫn theo vị trí.',
             'Thư mục tests/ chứa 24 tệp kiểm thử tự động bao phủ truy hồi, phân loại, bộ nhớ đệm, '
             'lịch sử hội thoại, bảo vệ truy cập, trích dẫn theo vị trí, chặn câu hỏi lạc đề và '
             'định tuyến sang các công cụ tính.')
L('Cập nhật mô tả bộ kiểm thử tự động (24 tệp, bổ sung nhóm chặn lạc đề và định tuyến công cụ)')

# C8 – phân bố thứ hạng bị cộng sai
p = find_contains(doc, 'tổng cộng 74/87 câu được truy hồi đúng')
set_text(p, 'Trên toàn bộ 97 câu hỏi, hệ thống đạt MRR@10 = 0,806, với khoảng tin cậy bootstrap '
            '95% là [0,735; 0,875]. Kết quả cho thấy khả năng xếp hạng nguồn nhìn chung ở mức khá '
            'tốt: khi nguồn đúng được truy hồi, nguồn này thường xuất hiện ở vị trí rất cao trong '
            'danh sách kết quả, với hạng trung bình khi trúng là 1,29. Phân bố thứ hạng của nguồn '
            'đúng đầu tiên gồm 72 câu ở hạng 1, 9 câu ở hạng 2, 3 câu ở hạng 3, 2 câu ở hạng 4 và '
            '1 câu ở hạng 5; như vậy 81 trong số 87 câu được truy hồi đúng – tức 83,5% toàn bộ bộ '
            'đo – có nguồn đúng nằm ở một trong hai vị trí đầu tiên. Điều này cho thấy vấn đề chủ '
            'yếu không nằm ở việc nguồn đúng bị xếp quá thấp, mà ở 10 trường hợp nguồn cần tìm '
            'hoàn toàn không xuất hiện trong nhóm kết quả.')
L('Sửa lỗi số liệu: "74/87 câu nằm trong hai vị trí đầu" → đúng là 81/87 (72 hạng 1 + 9 hạng 2); '
  'bổ sung đầy đủ phân bố hạng 4, hạng 5 và hạng trung bình khi trúng')

# C9 – bổ sung ghi chú về giới hạn cấu trúc của Hit@10
p = find_contains(doc, 'Vì vậy, Hit@10 = 90% không thể được hiểu trực tiếp')
insert_after(p, doc,
    'Một điểm nữa cần lưu ý khi đọc Hit@10: sau bước khử trùng lặp nội dung và ràng buộc mỗi '
    'tài liệu nguồn chỉ đóng góp tối đa hai đoạn, mỗi lượt truy hồi chỉ còn trung bình 9,5 tài '
    'liệu riêng biệt. Hit@10 vì thế đã gần chạm trần cấu trúc của rổ ứng viên chứ không phải '
    'trần chất lượng xếp hạng; muốn cải thiện chỉ số này phải nới rổ ứng viên hoặc thay đổi '
    'chiến lược phân đoạn, chứ không chỉ tinh chỉnh trọng số xếp hạng lại.')
L('Bổ sung diễn giải: Hit@10 đã chạm trần cấu trúc rổ ứng viên (9,5 tài liệu riêng biệt mỗi lượt)')

# C10 – mô tả Query Router chưa phản ánh lớp công cụ tính đã có trong mã nguồn
p = find(doc, 'Query Router.')
set_text(p, 'Query Router. Hệ thống không có Query Router theo nghĩa dùng một mô hình phân loại ý '
            'định để quyết định giữa việc sử dụng RAG và trả lời bằng kiến thức nội tại của LLM. '
            'Thay vào đó, việc định tuyến được thực hiện bằng quy tắc tường minh và đặt trước dây '
            'chuyền truy hồi: bốn công cụ tính bằng Python (tinh_luong, dinh_muc_tiet_day, '
            'danh_gia_hoc_sinh, tinh_toan), nhánh xử lý tệp đính kèm, nhánh xử lý URL và bộ nhớ '
            'đệm ngữ nghĩa. Câu hỏi không khớp nhánh nào mới đi tiếp vào quá trình truy hồi. Cơ '
            'chế này được trình bày chi tiết ở mục 2.7.')
p.runs[0].bold = True
L('Cập nhật mô tả Query Router: nêu rõ lớp định tuyến theo quy tắc và bốn công cụ tính đã có trong mã nguồn')

# =========================================================================
# D. TRÍCH DẪN VÀ TÀI LIỆU THAM KHẢO
# =========================================================================
# Các trường trích dẫn Mendeley trong tệp gốc bị lệch nguồn: câu nói về
# Transformer lại gắn bài LLaMA, câu về BERT gắn khảo sát ảo giác, câu về RAG
# gắn bài GPT-3, BM25 và RRF gắn khảo sát RAG… Ngoài ra hai mục Mendeley trùng
# nhau cùng trỏ về một khảo sát ([5] và [9]) nên danh mục sẽ có mục lặp.
# Cách xử lý: gỡ trường Mendeley thành văn bản thường và gán lại số hiệu đúng
# với nội dung từng câu, theo thứ tự xuất hiện lần đầu trong bài.
CITES = [
    ('[1], [2]', 'GPT, Llama, Gemini'),
    ('[3]',      'hiện tượng ảo giác'),
    ('[4], [5]', 'nguyên lý RAG'),
    ('[6]',      'kiến trúc Transformer 2017'),
    ('[6]',      'Vaswani giới thiệu Transformer — trước đây gắn nhầm bài LLaMA'),
    ('[7]',      'BERT — trước đây gắn nhầm khảo sát ảo giác'),
    ('[2], [8]', 'LLaMA và Llama 3'),
    ('[9]',      'Qwen'),
    ('[3]',      'hạn chế ảo giác của LLM — trước đây gắn nhầm bài RAG của Lewis'),
    ('[4]',      'Lewis đề xuất RAG 2020 — trước đây gắn nhầm bài GPT-3'),
    ('[10]',     'BM25 — trước đây gắn nhầm khảo sát RAG'),
    ('[11]',     'RRF — trước đây gắn nhầm bài Attention Is All You Need'),
    ('[5]',      'nguồn của Hình 1.1'),
    ('[12]',     'Ollama'),
    ('[13]',     'bge-m3'),
    ('[9]',      'Qwen'),
    ('[14]',     'FAISS'),
    ('[10]',     'BM25 khớp từ khoá — trước đây gắn nhầm khảo sát RAG'),
    ('[15]',     'LangChain'),
    ('[17]',     'Tesseract OCR'),
    ('[18]',     'faster-whisper'),
    ('[19]',     'Google Drive API'),
    ('[20]',     'Trafilatura'),
    ('[21]',     'SSRF'),
    ('[22]',     'SQLite'),
    ('[23], [24]', 'pypdf và pypdfium2'),
    ('[25]',     'MRR / TREC-8'),
    ('[26]',     'nDCG'),
]

sdts = [s for s in doc.element.body.iter(qn('w:sdt'))
        if any('MENDELEY_CITATION' in (t.get(qn('w:val')) or '')
               for t in s.iter(qn('w:tag')))]
assert len(sdts) == len(CITES), f'{len(sdts)} trường trích dẫn, cần {len(CITES)} giá trị'
sua_nguon = 0
for sdt, (num, what) in zip(sdts, CITES):
    par = sdt.getparent()
    prev = sdt.getprevious()
    before = ''
    if prev is not None and prev.tag == qn('w:r'):
        before = ''.join(t.text or '' for t in prev.iter(qn('w:t')))
    # IEEE: luôn có một khoảng trắng trước dấu ngoặc vuông
    lead = '' if (not before or before[-1] in ' \u00a0([') else ' '
    run = parse_xml(f'<w:r {nsdecls("w")}><w:t xml:space="preserve">{lead}{num}</w:t></w:r>')
    par.replace(sdt, run)
    if 'trước đây gắn nhầm' in what:
        sua_nguon += 1
        L(f'Sửa trích dẫn gắn sai nguồn: {what}')
L(f'Chuyển {len(sdts)} trích dẫn Mendeley thành văn bản thường và đánh số lại '
  f'theo thứ tự xuất hiện ({sua_nguon} trích dẫn vốn trỏ sai nguồn)')

# Dọn khoảng trắng thừa còn lại quanh vị trí trích dẫn cũ
for p in paragraphs(doc):
    runs = p.runs
    for i, r in enumerate(runs[:-1]):
        if r.text == ' ' and runs[i + 1].text[:1] in (',', '.', ';', ':'):
            r.text = ''
        if r.text == ' ' and runs[i + 1].text[:1] == ' ':
            r.text = ''

# Chú thích Hình 1.1 lấy lại từ khảo sát RAG: ghi rõ nguồn cho đúng thông lệ
p = find_contains(doc, 'Ba mô hình RAG: Naive, Advanced và Modular')
replace_text(p, 'Modular [5]', 'Modular (nguồn: Gao và cộng sự [5])')
L('Ghi rõ nguồn của Hình 1.1 trong chú thích hình')

# Bổ sung trích dẫn còn thiếu cho FastAPI (mục 1.4.7)
p = find(doc, 'FastAPI được sử dụng để xây dựng lớp API')
replace_text(p, 'FastAPI được sử dụng để xây dựng lớp API',
             'FastAPI [16] được sử dụng để xây dựng lớp API')
L('Bổ sung trích dẫn [16] cho FastAPI ở mục 1.4.7')

# --- Danh mục tài liệu tham khảo -----------------------------------------
REFS = [
 'T. B. Brown và cộng sự, “Language models are few-shot learners,” trong Advances in Neural Information Processing Systems (NeurIPS), tập 33, 2020, tr. 1877–1901.',
 'H. Touvron và cộng sự, “LLaMA: Open and efficient foundation language models,” arXiv:2302.13971, 2023.',
 'Z. Ji và cộng sự, “Survey of hallucination in natural language generation,” ACM Computing Surveys, tập 55, số 12, tr. 1–38, 2023.',
 'P. Lewis và cộng sự, “Retrieval-augmented generation for knowledge-intensive NLP tasks,” trong NeurIPS, tập 33, 2020, tr. 9459–9474.',
 'Y. Gao và cộng sự, “Retrieval-augmented generation for large language models: A survey,” arXiv:2312.10997, 2023.',
 'A. Vaswani và cộng sự, “Attention is all you need,” trong NeurIPS, tập 30, 2017, tr. 5998–6008.',
 'J. Devlin, M.-W. Chang, K. Lee và K. Toutanova, “BERT: Pre-training of deep bidirectional transformers for language understanding,” trong NAACL-HLT, 2019, tr. 4171–4186.',
 'Llama Team, AI @ Meta, “The Llama 3 herd of models,” arXiv:2407.21783, 2024.',
 'Qwen Team, “Qwen2.5 technical report,” arXiv:2412.15115, 2024.',
 'S. Robertson và H. Zaragoza, “The probabilistic relevance framework: BM25 and beyond,” Foundations and Trends in Information Retrieval, tập 3, số 4, tr. 333–389, 2009.',
 'G. V. Cormack, C. L. A. Clarke và S. Buettcher, “Reciprocal rank fusion outperforms Condorcet and individual rank learning methods,” trong SIGIR, 2009, tr. 758–759.',
 'Ollama, “Ollama – Get up and running with large language models locally.” https://github.com/ollama/ollama (truy cập ngày 15/9/2026).',
 'J. Chen, S. Xiao, P. Zhang, K. Luo, D. Lian và Z. Liu, “BGE M3-Embedding: Multi-lingual, multi-functionality, multi-granularity text embeddings through self-knowledge distillation,” arXiv:2402.03216, 2024.',
 'J. Johnson, M. Douze và H. Jégou, “Billion-scale similarity search with GPUs,” IEEE Transactions on Big Data, tập 7, số 3, tr. 535–547, 2021.',
 'LangChain, “LangChain overview.” https://docs.langchain.com/oss/python/langchain/overview (truy cập ngày 15/9/2026).',
 'S. Ramírez, “FastAPI documentation.” https://fastapi.tiangolo.com (truy cập ngày 15/9/2026).',
 'R. Smith, “An overview of the Tesseract OCR engine,” trong ICDAR, 2007, tr. 629–633.',
 'A. Radford, J. W. Kim, T. Xu, G. Brockman, C. McLeavey và I. Sutskever, “Robust speech recognition via large-scale weak supervision,” trong ICML, 2023, tr. 28492–28518.',
 'Google, “Google Drive API v3 reference.” https://developers.google.com/workspace/drive/api/reference/rest/v3 (truy cập ngày 15/9/2026).',
 'A. Barbaresi, “Trafilatura: A web scraping library and command-line tool for text discovery and extraction,” trong ACL-IJCNLP 2021: System Demonstrations, 2021, tr. 122–131.',
 'OWASP Foundation, “Server side request forgery.” https://owasp.org/www-community/attacks/Server_Side_Request_Forgery (truy cập ngày 15/9/2026).',
 'SQLite Consortium, “SQLite documentation.” https://www.sqlite.org/docs.html (truy cập ngày 15/9/2026).',
 'pypdf, “pypdf documentation.” https://pypdf.readthedocs.io/en/stable/ (truy cập ngày 15/9/2026).',
 'pypdfium2 Team, “pypdfium2.” https://github.com/pypdfium2-team/pypdfium2 (truy cập ngày 15/9/2026).',
 'E. M. Voorhees, “The TREC-8 question answering track report,” trong Proceedings of the 8th Text REtrieval Conference (TREC-8), 1999, tr. 77–82.',
 'K. Järvelin và J. Kekäläinen, “Cumulated gain-based evaluation of IR techniques,” ACM Transactions on Information Systems, tập 20, số 4, tr. 422–446, 2002.',
]
h = find(doc, 'TÀI LIỆU THAM KHẢO', style='Heading 1')
cur = h
for i, ref in enumerate(REFS, 1):
    p = insert_after(cur, doc, f'[{i}]\t{ref}', style='Bibliography')
    pf = p.paragraph_format
    pf.first_line_indent = Cm(-1.0)
    pf.left_indent = Cm(1.0)
    pf.space_after = Pt(6)
    cur = p
L(f'Dựng danh mục {len(REFS)} tài liệu tham khảo (trước đây mục này để trống dù bài có 28 trích dẫn)')

doc.save('out_part1.docx')
print('\n'.join(['', 'ĐÃ GHI out_part1.docx', f'{len(log)} thay đổi']))
