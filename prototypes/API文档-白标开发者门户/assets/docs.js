/* YASBe 白标开发者文档 — 通用交互
   1) 环境切换 pill  2) 代码语言 tab（多条 <pre data-lang>）  3) 复制按钮  4) TOC 高亮 */
(function(){
  /* ---------- 环境切换 ---------- */
  document.querySelectorAll('.env-switch button').forEach(function(b){
    b.addEventListener('click', function(){
      document.querySelectorAll('.env-switch button').forEach(function(x){ x.classList.remove('on'); });
      b.classList.add('on');
      var isTest = b.textContent.indexOf('Sandbox') > -1;
      document.querySelectorAll('[data-env-url]').forEach(function(el){
        var v = isTest ? el.getAttribute('data-env-url-test') : el.getAttribute('data-env-url-live');
        if(v){ el.textContent = v; }
      });
      document.querySelectorAll('[data-env-key]').forEach(function(el){
        var v = isTest ? el.getAttribute('data-env-key-test') : el.getAttribute('data-env-key-live');
        if(v){ el.textContent = v; }
      });
      document.querySelectorAll('.env-note').forEach(function(el){
        el.textContent = isTest
          ? '当前展示沙盒环境：api-sandbox.yasbee.com，示例密钥为 sk_test_ 前缀。'
          : '当前展示生产环境：api.yasbee.com，示例密钥为 sk_live_ 前缀，生产无需模拟端点。';
      });
    });
  });

  /* ---------- 代码语言 tab ---------- */
  document.querySelectorAll('.code').forEach(function(box){
    var tabs = box.querySelectorAll('.code-head .tab');
    var pres = box.querySelectorAll('pre[data-lang]');
    if(tabs.length < 2 || pres.length < 2) return;
    var show = function(lang){
      pres.forEach(function(p){
        p.style.display = (p.getAttribute('data-lang') === lang) ? 'block' : 'none';
      });
    };
    var first = tabs[0] ? tabs[0].getAttribute('data-l') : null;
    if(first) show(first);
    tabs.forEach(function(t){
      t.addEventListener('click', function(){
        tabs.forEach(function(x){ x.classList.remove('on'); });
        t.classList.add('on');
        show(t.getAttribute('data-l'));
      });
    });
  });

  /* ---------- 复制按钮 ---------- */
  document.querySelectorAll('.code-head .cp').forEach(function(cp){
    cp.addEventListener('click', function(){
      var box = cp.closest('.code');
      if(!box) return;
      var pres = box.querySelectorAll('pre');
      var src = null;
      pres.forEach(function(p){ if(!src && (!p.style.display || p.style.display === 'block')) src = p; });
      if(!src && pres.length) src = pres[0];
      if(!src) return;
      var txt = src.innerText;
      var done = function(){
        var old = cp.textContent;
        cp.textContent = '已复制';
        setTimeout(function(){ cp.textContent = old; }, 1400);
      };
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(txt).then(done, done);
      } else {
        var ta = document.createElement('textarea');
        ta.value = txt; document.body.appendChild(ta); ta.select();
        try{ document.execCommand('copy'); }catch(e){}
        document.body.removeChild(ta); done();
      }
    });
  });

  /* ---------- TOC 滚动高亮 ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.toc a[href^="#"]'));
  if(links.length){
    var targets = links.map(function(a){ return document.querySelector(a.getAttribute('href')); });
    var onScroll = function(){
      var y = window.scrollY + 150, idx = 0;
      targets.forEach(function(t, i){ if(t && t.offsetTop <= y) idx = i; });
      links.forEach(function(a, i){ a.classList.toggle('on', i === idx); });
    };
    window.addEventListener('scroll', onScroll, {passive:true});
    onScroll();
  }

  /* ---------- 侧栏锚点视觉标记 ---------- */
  document.querySelectorAll('.side a[href^="#"]').forEach(function(a){
    a.addEventListener('click', function(){ a.classList.add('on'); });
  });
})();
