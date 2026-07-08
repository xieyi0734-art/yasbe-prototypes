import re

fpath = r'C:\Users\xieyi\Desktop\YASBee-Interlace对接文档\prototypes-v2\12-卡片管理-v3.html'

with open(fpath, 'r', encoding='utf-8') as f:
    html = f.read()

# 用非贪婪匹配整个 ol() 函数体（从 function ol() 到下一个 function 前）
# 匹配策略：找到 "function ol()" 开始，到 "}\n\nfunction " 或 "}\n\n//" 结束
pattern = r'function ol\(\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}'

new_ol = '''function ol(){
  var c=cards[currentCard]; if(!c)return;
  var el,F=$('limitCardNum');if(F)F.textContent='•••• '+c.num;
  el=$('limitLevel');if(el)el.textContent=c.level;
  el=$('singleVal');if(el)el.textContent='$'+c.single.toLocaleString();
  el=$('dailyVal');if(el)el.textContent='$'+c.daily.toLocaleString();
  el=$('monthlyVal');if(el)el.textContent='$'+c.monthly.toLocaleString();
  el=$('singleUsedBar');if(el)el.style.width=Math.min(c.singleUsed/c.single*100,100).toFixed(1)+'%;';
  el=$('dailyUsedBar');if(el)el.style.width=Math.min(c.dailyUsed/c.daily*100,100).toFixed(1)+'%;';
  el=$('monthlyUsedBar');if(el)el.style.width=Math.min(c.monthlyUsed/c.monthly*100,100).toFixed(1)+'%;';
  document.querySelectorAll('.level-row').forEach(function(r){r.classList.remove('highlight');});
  var lvs={'Lv1':0,'Lv2':1,'Lv3':2,'Lv4':3};
  var idx=c.level in lvs?lvs[c.level]:1;
  var rows=document.querySelectorAll('.level-row');
  if(rows[idx])rows[idx].classList.add('highlight');
  om('modalLimit');
}'''

count = 0
def repl(m):
    global count
    count += 1
    return new_ol

html2 = re.sub(pattern, repl, html, count=1)

if count == 0:
    # 更宽松的匹配：匹配到第一个  "}\nfunction " 为止
    pattern2 = r'function ol\(\)[\s\S]*?\n}\n\nfunction '
    html2 = re.sub(pattern2, new_ol + '\n\nfunction ', html, count=1)
    if html2 == html:
        print('ERROR: could not match ol()')
    else:
        print('DONE: ol() replaced via pattern2')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html2)
else:
    print('DONE: ol() replaced via pattern1')
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html2)
