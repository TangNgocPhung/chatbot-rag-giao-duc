# -*- coding: utf-8 -*-
"""Phần 6: các chi tiết nhỏ còn lại ở trang bìa và trang ký tên."""
import sys; sys.path.insert(0, '.')
import docx
from docx_helpers import paragraphs, iter_blocks, replace_text, set_text
from docx.table import Table

doc = docx.Document('Thay_Minh_Hai_DA_SUA.docx')
log = []
def L(m): log.append(m); print('·', m)

n = 0
for p in paragraphs(doc):
    if replace_text(p, 'Chuyên đề các vấn đề hiện đại trong CNTT',
                    'Chuyên đề các vấn đề hiện đại trong Công nghệ thông tin'):
        n += 1
if n:
    L(f'Thống nhất tên học phần ở trang bìa ({n} chỗ viết tắt "CNTT" → viết đủ như bìa phụ)')

n = 0
for b in iter_blocks(doc):
    if isinstance(b, Table):
        for row in b.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if p.text.strip() == 'Tác giả':
                        set_text(p, 'Nhóm tác giả')
                        n += 1
if n:
    L(f'Sửa {n} ô ký tên "Tác giả" → "Nhóm tác giả" cho khớp với ba học viên thực hiện')

doc.save('Thay_Minh_Hai_DA_SUA.docx')
print('\nHOÀN TẤT')
