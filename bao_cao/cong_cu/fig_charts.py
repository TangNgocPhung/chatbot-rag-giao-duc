# -*- coding: utf-8 -*-
"""Biểu đồ kết quả thực nghiệm (Chương 4)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.edgecolor': '#94a3b8', 'axes.labelcolor': '#1f2933',
    'text.color': '#1f2933', 'xtick.color': '#475569', 'ytick.color': '#475569',
    'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 200,
})
BLUE, GREEN, VIOLET, AMBER, SLATE = '#2563eb', '#059669', '#7c3aed', '#d97706', '#94a3b8'

groups = ['video', 'trinh_chieu', 'bang_excel', 'tai_lieu_docx', 'van_ban_doc', 'chinh_sach_pdf']
n      = [5, 14, 8, 14, 6, 50]
mrr    = [0.467, 0.631, 0.713, 0.821, 0.889, 0.890]
ndcg   = [0.423, 0.655, 0.712, 0.794, 0.917, 0.893]
mapk   = [0.367, 0.595, 0.634, 0.750, 0.889, 0.890]
hit1   = [40, 43, 62, 71, 83, 88]
hit3   = [60, 86, 62, 93, 100, 90]
hit5   = [60, 86, 100, 93, 100, 90]
hit10  = [60, 86, 100, 93, 100, 90]
labels = [f'{g}\n(n = {c})' for g, c in zip(groups, n)]

# --- Biểu đồ 1: MRR@10 / nDCG@10 / MAP@10 theo nhóm ----------------------
fig, ax = plt.subplots(figsize=(10.2, 4.6))
x = np.arange(len(groups)); w = 0.26
ax.bar(x - w, mrr,  w, label='MRR@10',  color=BLUE)
ax.bar(x,     ndcg, w, label='nDCG@10', color=GREEN)
ax.bar(x + w, mapk, w, label='MAP@10',  color=VIOLET)
for xi, (a, b, c) in enumerate(zip(mrr, ndcg, mapk)):
    for off, v in ((-w, a), (0, b), (w, c)):
        ax.text(xi + off, v + 0.015, f'{v:.3f}'.replace('.', ','), ha='center', fontsize=8.5, color='#334155')
ax.axhline(0.806, color=AMBER, ls='--', lw=1.4)
ax.text(0.02, 0.812, 'MRR@10 toàn bộ = 0,806', color=AMBER, fontsize=9.5, ha='left')
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=10)
ax.set_ylim(0, 1.12); ax.set_ylabel('Giá trị chỉ số')
ax.set_title('Chất lượng xếp hạng truy hồi theo từng nhóm tài liệu (97 câu hỏi có nhãn nguồn)',
             fontsize=12.5, fontweight='bold', pad=12)
ax.legend(frameon=False, ncol=3, loc='upper center', fontsize=10, bbox_to_anchor=(0.5,1.02))
ax.grid(axis='y', color='#e2e8f0', lw=.8); ax.set_axisbelow(True)
from matplotlib.ticker import FuncFormatter
ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p: f'{v:.1f}'.replace('.',',')))
fig.tight_layout(); fig.savefig('fig/f13_chi_so_theo_nhom.png', bbox_inches='tight'); plt.close(fig)

# --- Biểu đồ 2: Hit@K ----------------------------------------------------
fig, ax = plt.subplots(figsize=(10.2, 4.4))
w = 0.2
ax.bar(x - 1.5*w, hit1,  w, label='Hit@1',  color='#bfdbfe')
ax.bar(x - 0.5*w, hit3,  w, label='Hit@3',  color='#60a5fa')
ax.bar(x + 0.5*w, hit5,  w, label='Hit@5',  color='#2563eb')
ax.bar(x + 1.5*w, hit10, w, label='Hit@10', color='#1e3a8a')
for xi, vals in enumerate(zip(hit1, hit3, hit5, hit10)):
    for off, v in zip((-1.5*w, -0.5*w, 0.5*w, 1.5*w), vals):
        ax.text(xi + off, v + 1.6, f'{v}', ha='center', fontsize=8.5, color='#334155')
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=10)
ax.set_ylim(0, 116); ax.set_ylabel('Tỷ lệ câu hỏi tìm thấy nguồn đúng (%)')
ax.set_title('Độ bao phủ Hit@K theo độ sâu danh sách kết quả', fontsize=12.5, fontweight='bold', pad=12)
ax.legend(frameon=False, ncol=4, loc='upper left', fontsize=10)
ax.grid(axis='y', color='#e2e8f0', lw=.8); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig('fig/f14_hit_at_k.png', bbox_inches='tight'); plt.close(fig)

# --- Biểu đồ 3: phân bố hạng của nguồn đúng đầu tiên ---------------------
fig, ax = plt.subplots(figsize=(8.6, 4.2))
ranks = ['Hạng 1', 'Hạng 2', 'Hạng 3', 'Hạng 4', 'Hạng 5', 'Không có\ntrong top 10']
cnt   = [72, 9, 3, 2, 1, 10]
cols  = [GREEN, '#34d399', '#6ee7b7', '#a7f3d0', '#d1fae5', '#fca5a5']
bars = ax.bar(ranks, cnt, color=cols, edgecolor='#94a3b8', lw=.7)
for b, c in zip(bars, cnt):
    ax.text(b.get_x() + b.get_width()/2, c + 1.2, f'{c} câu\n' + f'{c/97*100:.1f}%'.replace('.', ','),
            ha='center', fontsize=9.5, color='#334155')
ax.axvspan(-0.5, 1.5, color='#ecfdf5', zorder=0)
ax.annotate('81/97 câu · 83,5% — nguồn đúng\nnằm ở một trong hai vị trí đầu',
            xy=(1.45, 12), xytext=(2.35, 52), fontsize=10.5, color=GREEN, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.4))
ax.annotate('10 câu còn lại là giới hạn\nhiện tại của khâu truy hồi',
            xy=(5, 13), xytext=(3.55, 34), fontsize=10.5, color='#b91c1c',
            arrowprops=dict(arrowstyle='->', color='#b91c1c', lw=1.4))
ax.set_ylim(0, 86); ax.set_ylabel('Số câu hỏi')
ax.set_title('Phân bố thứ hạng của nguồn đúng đầu tiên (97 câu hỏi có nhãn nguồn)',
             fontsize=12.5, fontweight='bold', pad=12)
ax.grid(axis='y', color='#e2e8f0', lw=.8); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig('fig/f15_phan_bo_hang.png', bbox_inches='tight'); plt.close(fig)

# --- Biểu đồ 4: cơ cấu bộ câu hỏi kiểm thử -------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.3),
                               gridspec_kw={'width_ratios': [1.15, 1]})
g2 = ['chinh_sach_pdf', 'ngoai_pham_vi', 'tai_lieu_docx', 'trinh_chieu', 'bang_excel', 'van_ban_doc', 'video']
c2 = [50, 30, 14, 14, 8, 6, 5]
col2 = [BLUE, '#dc2626', GREEN, VIOLET, AMBER, '#0891b2', '#db2777']
bars = ax1.barh(range(len(g2))[::-1], c2, color=col2, height=.62)
for i, v in enumerate(c2):
    ax1.text(v + .8, len(g2) - 1 - i, f'{v} câu · ' + f'{v/127*100:.1f}%'.replace('.', ','), va='center', fontsize=9.5, color='#334155')
ax1.set_yticks(range(len(g2))[::-1]); ax1.set_yticklabels(g2, fontsize=10)
ax1.set_xlim(0, 62); ax1.set_xlabel('Số câu hỏi')
ax1.set_title('Bảy nhóm của bộ 127 câu hỏi kiểm thử', fontsize=12, fontweight='bold', pad=10)
ax1.grid(axis='x', color='#e2e8f0', lw=.8); ax1.set_axisbelow(True)

ax2.pie([97, 30], labels=['97 câu có nhãn nguồn\n(đo chỉ số IR)', '30 câu ngoài phạm vi\n(đo khả năng từ chối)'],
        colors=[BLUE, '#dc2626'], autopct=lambda p: f'{p:.1f}%'.replace('.', ','), startangle=110,
        textprops={'fontsize': 10, 'color': '#1f2933'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax2.set_title('Hai mục đích đánh giá khác nhau', fontsize=12, fontweight='bold', pad=10)
fig.tight_layout(); fig.savefig('fig/f16_bo_cau_hoi.png', bbox_inches='tight'); plt.close(fig)
print('charts ok')
