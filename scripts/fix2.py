import re

BASE = r'C:\Users\xieyi\Desktop\YASBee-Interlace对接文档\prototypes-v2'
fpath = BASE + r'\12-卡片管理-v3.html'

with open(fpath, 'r', encoding='utf-8') as f:
    html = f.read()

# 用正则匹配并替换 ol() 函数（容忍空白和换行差异）
# 匹配从 function ol() 到下一个 function 或 script 结束
pattern = r'function ol\(\)\{[^}]*(?:\{[^}]*\}[^}]*)*\}'
replacement = '''function ol(){
  var c=cards[currentCard]; if(!c)return;
  var el=$('limitCardNum'); if(el)el.textContent='•••• '+c.num;
  el=$('limitLevel'); if(el)el.textContent=c.level;
  el=$('singleVal'); if(el)el.textContent='$'+c.single.toLocaleString();
  el=$('dailyVal'); if(el)el.textContent='$'+c.daily.toLocaleString();
  el=$('monthlyVal'); if(el)el.textContent='$'+c.monthly.toLocaleString();
  el=$('singleUsedBar'); if(el)el.style.width=Math.min(c.singleUsed/c.single*100,100).toFixed(1)+'%';
  el=$('dailyUsedBar'); if(el)el.style.width=Math.min(c.dailyUsed/c.daily*100,100).toFixed(1)+'%';
  el=$('monthlyUsedBar'); if(el)el.style.width=Math.min(c.monthlyUsed/c.monthly*100,100).toFixed(1)+'%';
  document.querySelectorAll('.level-row').forEach(function(r){r.classList.remove('highlight');});
  var lvs={'Lv1':0,'Lv2':1,'Lv3':2,'Lv4':3};
  var idx=c.level in lvs?lvs[c.level]:1;
  var rows=document.querySelectorAll('.level-row');
  if(rows[idx])rows[idx].classList.add('highlight');
  om('modalLimit');
}'''

new_html = re.sub(pattern, replacement, html, count=1)

if new_html == html:
    print('WARN: ol() regex did not match, trying harder...')
    # 更宽松的匹配
    pattern2 = r'function ol\(\)\{[^}]+\}'
    new_html = re.sub(pattern2, replacement, html, count=1)

if new_html != html:
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print('DONE: ol() replaced successfully')
else:
    print('ERROR: could not match ol() function')
