"""Render the monitoring PRD: uv run --with markdown --with beautifulsoup4 python tools/render_tm_prd.py"""
from pathlib import Path
import html
import markdown
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'prd/交易监控/交易监控-PRD.md'
soup = BeautifulSoup(markdown.markdown(source.read_text(encoding='utf-8'), extensions=['tables', 'sane_lists', 'nl2br']), 'html.parser')
nav = []
for i, heading in enumerate(soup.select('h2, h3')):
    heading['id'] = f'section-{i}'
    nav.append(f'<a class="{heading.name}" href="#section-{i}">{html.escape(heading.get_text())}</a>')
for table in soup.select('table'):
    wrapper = soup.new_tag('div', attrs={'class': 'table-wrap', 'tabindex': '0', 'role': 'region', 'aria-label': '表格，可横向滚动'})
    table.wrap(wrapper)
css = '''
:root{color-scheme:light;--ink:#242832;--muted:#687080;--line:#e4e7ec;--accent:#986000}
*{box-sizing:border-box}html{scroll-padding-top:30px}body{margin:0;background:#f6f7f9;color:var(--ink);font:16px/1.85 -apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}a:focus-visible,button:focus-visible,[tabindex]:focus-visible{outline:2px solid #986000;outline-offset:3px}
.layout{max-width:1500px;margin:auto;display:grid;grid-template-columns:230px minmax(0,1fr);gap:36px;padding:40px 36px}
aside{position:sticky;top:32px;height:calc(100vh - 64px);overflow:auto;font-size:14px}.brand{font-size:13px;letter-spacing:1px;color:var(--muted);margin:0 12px 24px}.brand strong{color:#986000}nav a{display:block;color:#515867;padding:9px 12px;line-height:1.5;border-radius:5px}nav a:hover{background:#eceef2;text-decoration:none}nav .h3{padding-left:25px;font-size:13px}nav a.active{background:#fff3dd;color:#805100;font-weight:600}
main{min-width:0;background:white;border:1px solid var(--line);border-radius:8px;padding:44px 52px 64px}header{display:flex;gap:16px;justify-content:flex-end;border-bottom:1px solid var(--line);padding-bottom:20px;margin-bottom:30px;font-size:13px}button{font:inherit;color:var(--muted);border:0;background:none;padding:0;cursor:pointer}h1{font-size:32px;line-height:1.35;letter-spacing:-.5px;margin:0 0 20px}h2{font-size:23px;line-height:1.45;margin:48px 0 20px;padding-top:8px;border-top:1px solid var(--line)}h3{font-size:18px;margin:28px 0 14px}h3 a{color:inherit}p{margin:14px 0}li{margin:9px 0}ul,ol{padding-left:25px}code{font:13px/1.7 Consolas,monospace;background:#f3f4f6;border-radius:3px;padding:2px 4px;overflow-wrap:anywhere}.table-wrap{overflow-x:auto;margin:22px 0;border:1px solid var(--line);border-radius:6px}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.8;min-width:650px}th,td{text-align:left;vertical-align:top;padding:13px 15px;border-bottom:1px solid var(--line);overflow-wrap:anywhere}th{background:#f4f5f7;color:#414957;font-weight:600}tr:last-child td{border-bottom:0}tbody tr:nth-child(even){background:#fafbfc}td:first-child{min-width:100px}article>p:first-of-type{color:var(--muted);font-size:14px;background:#f8f9fb;padding:16px 20px;border-radius:5px}footer{margin-top:40px;color:var(--muted);font-size:12px}.mobile-toc{display:none}
@media(min-width:1500px){main{padding-left:64px;padding-right:64px}}
@media(max-width:900px){.layout{grid-template-columns:minmax(0,1fr);padding:20px;gap:16px}aside{position:static;height:auto}.brand{margin:0 0 12px}aside>nav{display:none}.mobile-toc{display:block;background:white;border:1px solid var(--line);border-radius:6px;padding:8px 14px}.mobile-toc summary{cursor:pointer;min-height:44px;display:flex;align-items:center}main{padding:28px 24px}h1{font-size:28px}}
@media(max-width:480px){.layout{padding:12px}main{padding:24px 18px}body{font-size:15px}header{justify-content:flex-start;flex-wrap:wrap}h2{font-size:21px}}
@media print{body{background:white;font-size:12pt}.layout{display:block;padding:0}aside,header,footer{display:none}main{border:0;padding:0}h2{break-after:avoid}.table-wrap{overflow:visible;border-radius:0}table{min-width:0;font-size:10pt}tr{break-inside:avoid}a{color:inherit}code{font-size:9pt}}
'''
nav_html = ''.join(nav)
page = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>交易监控 · 产品需求文档</title><style>'+css+'</style></head><body><div class="layout"><aside><div class="brand"><strong>YASBe</strong> / 产品需求文档</div><nav aria-label="章节目录">'+nav_html+'</nav><details class="mobile-toc"><summary>章节目录</summary><nav aria-label="移动端章节目录">'+nav_html+'</nav></details></aside><main><header><a href="../../prototypes/交易监控/index.html">查看原型</a><a href="交易监控-PRD.md">Markdown 源文件</a><button onclick="window.print()">打印 / 保存 PDF</button></header><article>'+str(soup)+'</article><footer>文档结束</footer></main></div><script>const observer=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting){document.querySelectorAll("nav a").forEach(a=>a.classList.toggle("active",a.hash==="#"+entry.target.id));}}},{rootMargin:"0px 0px -65% 0px"});document.querySelectorAll("article h2,article h3").forEach(h=>observer.observe(h));document.querySelectorAll(".mobile-toc a").forEach(a=>a.addEventListener("click",()=>document.querySelector(".mobile-toc").open=false));</script></body></html>'
target = source.with_suffix('.html')
target.write_text(page, encoding='utf-8')
assert BeautifulSoup(page, 'html.parser').article.get_text() == soup.get_text()
print('Generated HTML; all source content preserved:', target)
