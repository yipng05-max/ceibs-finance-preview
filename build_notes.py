#!/usr/bin/env python3
"""生成 notes.html:以 index.html 的章节内容(四段卡+精读区+互动组件+语音)为底稿,
每章在四段卡之后、精读区之前插入 notes_src/chN.html 里的课堂补充。"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'index.html')
OUT = os.path.join(ROOT, 'notes.html')
NOTES_DIR = os.path.join(ROOT, 'notes_src')
CHAPTERS = [1, 2, 3, 13, 14, 15, 16, 17, 18]
TITLES = {
    1: '会计：商业语言', 2: '财务报表导言', 3: '会计报表的关联和框架',
    13: '企业合并', 14: '利润表分析', 15: '资产负债表分析',
    16: '编制现金流量表', 17: '现金流量表分析和盈余质量',
    18: '财务比率分析、财务报表分析和ESG分析',
}

html = open(SRC, encoding='utf-8').read()

style = re.search(r'<style>.*?</style>', html, re.S).group(0)
chap_start = html.index('<div class="blockdiv"')
chap_end = html.rindex('</div>', 0, html.index('<footer>'))  # 去掉 .wrap 的闭合,模板里自己补
chapters = html[chap_start:chap_end]
script = html[html.index('<script>'):]

EXTRA_STYLE = '''<style>
.nb-table{width:100%;border-collapse:collapse;margin:8px 0;font-size:12.5px}
.nb-table th{background:#f6f1ff;color:#6f42c1;text-align:left;padding:8px 10px;border-bottom:2px solid #d9c9f2;font-weight:800}
.nb-table td{padding:8px 10px;border-bottom:1px solid #eef1f4;color:#42535f}
.nb-table tr:last-child td{border-bottom:none}
.nb-wrap{overflow-x:auto;margin:10px 0}
.nb-say{background:#f4eefb;border-left:3px solid #8156c9;border-radius:0 8px 8px 0;padding:8px 12px;margin:6px 0 10px;font-size:12.5px;color:#574769;line-height:1.7}
.nb-formula{background:#fff;border:1.5px solid #d9c9f2;border-radius:10px;padding:12px 14px;margin:8px 0;font-family:"SF Mono",Consolas,monospace;font-size:12.5px;color:#42535f;line-height:2}
.cls{background:#fffbea;border:2px solid #e0a800;border-radius:14px;padding:14px 16px;margin:14px 0 18px;box-shadow:0 2px 12px rgba(160,120,0,.10);scroll-margin-top:56px}
.clshd{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px}
.clstag{font-size:12px;font-weight:800;color:#fff;background:#e0a800;border-radius:12px;padding:3px 11px}
.clstitle{font-size:16px;font-weight:800;color:#5a4300}
.clsnote{font-size:12.5px;color:#8a7a3a;margin-left:auto}
.cls .dim .d{border-left-color:#e0a800}
.cls .stepmsg{background:#fff;border-color:#e6c76a}
.clsempty{font-size:13px;color:#8a7a3a;background:#fff;border:1px dashed #e6c76a;border-radius:9px;padding:9px 12px}
.pretag{display:inline-block;font-size:11.5px;font-weight:700;color:#2e6da4;background:#eaf1f7;border-radius:8px;padding:2px 9px;margin:2px 4px 6px 0}
.jinju{background:linear-gradient(135deg,#6f42c1,#8156c9);color:#fff;border-radius:12px;padding:14px 18px;margin:12px 0;font-size:17px;font-weight:800;text-align:center;letter-spacing:.5px;box-shadow:0 3px 12px rgba(111,66,193,.25)}
.jinju small{display:block;font-size:12px;font-weight:500;opacity:.85;margin-top:5px;letter-spacing:0}
</style>'''

def class_block(n):
    path = os.path.join(NOTES_DIR, f'ch{n}.html')
    body = open(path, encoding='utf-8').read().strip() if os.path.exists(path) else ''
    if not body:
        body = '<div class="clsempty">📖 本章课堂内容待老师讲到后补充。</div>'
    return (f'<div class="cls" id="ch{n}cls"><div class="clshd"><span class="clstag">🎓 课堂补充</span>'
            f'<span class="clstitle">第{n}章 · {TITLES[n]}</span>'
            f'<span class="clsnote">上面是预习四段卡，下面精读区是预习底稿</span></div>{body}</div>\n')

for n in CHAPTERS:
    anchor = f'<div class="section-t" id="ch{n}deep">'
    assert chapters.count(anchor) == 1, f'ch{n}deep anchor not unique'
    chapters = chapters.replace(anchor, class_block(n) + anchor)

nav = ''.join(f'<a href="#ch{n}cls" class="navlink">{n}. {TITLES[n]}</a>' for n in CHAPTERS)

page = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ACCT5002《财务报告》课堂笔记</title>
{style}
{EXTRA_STYLE}
</head><body>
<div class="hero">
  <h1>课堂笔记 · ACCT5002《财务报告》</h1>
  <div class="sub">以预习课件为脉络 · 每章先看四段卡，🎓黄框是老师课上补充，再往下是预习精读底稿</div>
  <div class="sub" style="font-size:12.5px"><a href="index.html" style="color:#fff;opacity:.85">← 返回预习站（含师资、路线图、案例五把尺子、概念速查）</a></div>
</div>
<div class="intro"><div class="introcard">
<b>这页怎么用：</b>章节顺序、四段卡、精读区、互动小组件和晓晓语音都跟预习站完全一致，是同一套底稿；不同的是每章多了一个<b style="color:#b98600">🎓 课堂补充</b>黄框，随堂把程林、丁远两位教授实际讲的内容填进去。想直接跳到某章的课堂补充，点下面导航。
</div></div>
<div class="nav">{nav}</div>
<div class="wrap">
{chapters}<footer>课堂笔记 · 随堂持续更新 · 学委制作 · <a href="index.html" style="color:#2e6da4">← 返回预习站</a></footer>
</div>
{script}'''

open(OUT, 'w', encoding='utf-8').write(page)
print(f'notes.html written: {len(page)} chars; div {page.count("<div")}/{page.count("</div>")}; '
      f'cls blocks {page.count("class=\"cls\"")}; audio {page.count("<audio")}')
