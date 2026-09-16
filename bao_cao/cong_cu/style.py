CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fff;font-family:'Liberation Sans','DejaVu Sans',sans-serif;color:#1f2933}
#fig{background:#fff;padding:26px 30px 22px}
.h{font-size:23px;font-weight:700;letter-spacing:-.2px}
.sub{font-size:14.5px;color:#64748b;margin-top:4px}
.rule{height:2px;background:#e2e8f0;margin:14px 0 18px}
.row{display:flex;align-items:stretch;gap:10px}
.col{display:flex;flex-direction:column;gap:10px}
.box{border:1.6px solid #cbd5e1;border-radius:10px;padding:11px 13px;background:#fff;flex:1}
.box .t{font-size:16px;font-weight:700;line-height:1.25}
.box .d{font-size:13.5px;color:#475569;margin-top:5px;line-height:1.45}
.box code,.mono{font-family:'DejaVu Sans Mono',monospace;font-size:12.5px;color:#334155}
.blue{border-color:#2563eb;background:#eff6ff}
.green{border-color:#059669;background:#ecfdf5}
.amber{border-color:#d97706;background:#fffbeb}
.red{border-color:#dc2626;background:#fef2f2}
.violet{border-color:#7c3aed;background:#f5f3ff}
.slate{border-color:#94a3b8;background:#f8fafc}
.dash{border-style:dashed}
.ar{display:flex;align-items:center;justify-content:center;font-size:24px;color:#64748b;flex:0 0 26px}
.ard{display:flex;align-items:center;justify-content:center;font-size:22px;color:#64748b;height:22px}
.band{border:1.6px solid #e2e8f0;border-radius:12px;padding:13px;background:#f8fafc}
.band>.cap{font-size:13px;font-weight:700;letter-spacing:.8px;color:#475569;text-transform:uppercase;margin-bottom:10px}
.tag{display:inline-block;font-size:12px;font-weight:700;padding:2px 8px;border-radius:20px;background:#e2e8f0;color:#475569;margin-right:5px}
.note{font-size:13px;color:#64748b;margin-top:14px;line-height:1.5}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{border:1px solid #cbd5e1;padding:6px 9px;text-align:left}
th{background:#f1f5f9;font-weight:700;font-size:13.5px}
td.n{text-align:center;font-family:'DejaVu Sans Mono',monospace}
.hi{background:#ecfdf5;font-weight:700}
"""
def page(title, sub, body, note=""):
    n = f'<div class="note">{note}</div>' if note else ''
    return f"""<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div id="fig"><div class="h">{title}</div><div class="sub">{sub}</div><div class="rule"></div>
{body}{n}</div></body></html>"""
