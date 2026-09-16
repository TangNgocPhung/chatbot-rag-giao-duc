# -*- coding: utf-8 -*-
"""Phần 5: sắp xếp lại vị trí một hình và đồng bộ số hiệu hình/bảng đã lưu sẵn.

Số hiệu hình và bảng trong tệp là kết quả của trường STYLEREF + SEQ nên Word sẽ
tự tính lại khi mở. Tuy vậy giá trị lưu sẵn vẫn cần đúng, để bản in hoặc các
trình đọc không cập nhật trường (Google Docs, trình xem nhanh) hiển thị chính xác.
"""
import sys; sys.path.insert(0, '.')
import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx_helpers import paragraphs, find, find_contains, iter_blocks

doc = docx.Document('out_part4.docx')
log = []
def L(m): log.append(m); print('·', m)

# --- 1. Đưa ảnh giao diện điện thoại xuống cuối mục 2.8 ------------------
mob_cap = find_contains(doc, 'Giao diện trên màn hình điện thoại')
mob_img = Paragraph(mob_cap._p.getprevious(), doc)
last_cap = find_contains(doc, 'Hộp thoại "Kho tài liệu"')
last_cap._p.addnext(mob_cap._p)
last_cap._p.addnext(mob_img._p)
L('Chuyển ảnh giao diện điện thoại xuống cuối mục 2.8 để các ảnh giao diện đứng liền mạch')

# --- 2. Đồng bộ số hiệu hình và bảng ------------------------------------
def field_results(par):
    """Trả về các run là kết quả lưu sẵn của trường (nằm giữa 'separate' và 'end')."""
    out, inside = [], False
    for r in par._p.findall(qn('w:r')):
        fld = r.find(qn('w:fldChar'))
        if fld is not None:
            t = fld.get(qn('w:fldCharType'))
            if t == 'separate':
                inside = True
            elif t == 'end':
                inside = False
            continue
        if inside:
            out.append(r)
    return out

chuong = 0
dem = {'Hình': 0, 'Bảng': 0}
sua = 0
for b in iter_blocks(doc):
    if not isinstance(b, Paragraph):
        continue
    if b.style.name == 'Heading 1':
        pPr = b._p.find(qn('w:pPr'))
        numPr = pPr.find(qn('w:numPr')) if pPr is not None else None
        so_id = None
        if numPr is not None:
            nid = numPr.find(qn('w:numId'))
            so_id = nid.get(qn('w:val')) if nid is not None else None
        if so_id != '0':                       # numId = 0 nghĩa là đề mục không đánh số
            chuong += 1
            dem = {'Hình': 0, 'Bảng': 0}
        continue
    if b.style.name != 'Caption':
        continue
    kind = b.text.strip().split(' ')[0]
    if kind not in dem:
        continue
    res = field_results(b)
    if len(res) < 2:
        continue
    dem[kind] += 1
    for run, val in zip(res[:2], (chuong, dem[kind])):
        t = run.find(qn('w:t'))
        if t is not None and t.text != str(val):
            t.text = str(val)
            sua += 1
L(f'Cập nhật {sua} số hiệu hình/bảng lưu sẵn cho khớp vị trí thực tế '
  '(ví dụ "Hình 9.1" và "Bảng 9.1" trong Chương 4 trở lại đúng là 4.3 và 4.1)')

doc.save('Thay_Minh_Hai_DA_SUA.docx')
print(f'\nĐÃ GHI Thay_Minh_Hai_DA_SUA.docx')
