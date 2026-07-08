import re

with open('12-卡片管理-v3.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 修复 cards 数据：加入 wallet 字段
old_cards = """var cards = {
  std: {name:'标准卡',num:'4821',bal:12458.60,status:'active',type:'VIRTUAL',bin:'BB-BIN（加拿大）',level:'Lv3',issue:'2026-05-15',expire:'2029-05-15',fee:'$0.25/月',fx:'1.5%',single:5000,daily:15000,monthly:50000,dailyUsed:1080,monthlyUsed:3245,singleUsed:4200,cvv:'123'},
  biz: {name:'企业卡',num:'6732',bal:5425.90,status:'active',type:'VIRTUAL',bin:'BB-BIN（加拿大）',level:'Lv3',issue:'2026-05-10',expire:'2029-06-27',fee:'$0.25/月',fx:'1.5%',single:5000,daily:15000,monthly:50000,dailyUsed:500,monthlyUsed:1200,singleUsed:0,cvv:'456'},
  sub: {name:'副卡',num:'1094',bal:350.00,status:'frozen',type:'VIRTUAL',bin:'BZ-BIN（美国）',level:'Lv2',issue:'2026-04-20',expire:'2028-03-15',fee:'$0.25/月',fx:'Pass through + 5bps',single:2000,daily:5000,monthly:20000,dailyUsed:0,monthlyUsed:0,singleUsed:0,cvv:'789'}
};"""
new_cards = """var cards = {
  std: {name:'标准卡',num:'4821',bal:12458.60,status:'active',type:'VIRTUAL',bin:'BB-BIN（加拿大）',level:'Lv3',issue:'2026-05-15',expire:'2029-05-15',fee:'$0.25/月',fx:'1.5%',single:5000,daily:15000,monthly:50000,dailyUsed:1080,monthlyUsed:3245,singleUsed:4200,cvv:'123',wallet:'✅ GPW + Apple Pay'},
  biz: {name:'企业卡',num:'6732',bal:5425.90,status:'active',type:'VIRTUAL',bin:'BB-BIN（加拿大）',level:'Lv3',issue:'2026-05-10',expire:'2029-06-27',fee:'$0.25/月',fx:'1.5%',single:5000,daily:15000,monthly:50000,dailyUsed:500,monthlyUsed:1200,singleUsed:0,cvv:'456',wallet:'✅ GPW + Apple Pay'},
  sub: {name:'副卡',num:'1094',bal:350.00,status:'frozen',type:'VIRTUAL',bin:'BZ-BIN（美国）',level:'Lv2',issue:'2026-04-20',expire:'2028-03-15',fee:'$0.25/月',fx:'Pass through + 5bps',single:2000,daily:5000,monthly:20000,dailyUsed:0,monthlyUsed:0,singleUsed:0,cvv:'789',wallet:'❌ 不支持'}
};"""
html = html.replace(old_cards, new_cards)

# 2. 重写整个 script 块（从 // ===== Data ===== 到 </script>）
# 找到 script 开始和结束
script_start = html.find('// ===== Data =====')
script_end = html.find('</script>')
if script_start == -1 or script_end == -1:
    print("ERROR: cannot find script markers")
else:
    before = html[:script_start]
    after = html[script_end + len('</script>'):]
    
    new_script = """// ===== Data =====
var cards = {
  std: {name:'标准卡',num:'4821',bal:12458.60,status:'active',type:'VIRTUAL',bin:'BB-BIN（加拿大）',level:'Lv3',issue:'2026-05-15',expire:'2029-05-15',fee:'$0.25/月',fx:'1.5%',single:5000,daily:15000,monthly:50000,dailyUsed:1080,monthlyUsed:3245,singleUsed:4200,cvv:'123',wallet:'✅ GPW + Apple Pay'},
  biz: {name:'企业卡',num:'6732',bal:5425.90,status:'active',type:'VIRTUAL',bin:'BB-BIN（加拿大）',level:'Lv3',issue:'2026-05-10',expire:'2029-06-27',fee:'$0.25/月',fx:'1.5%',single:5000,daily:15000,monthly:50000,dailyUsed:500,monthlyUsed:1200,singleUsed:0,cvv:'456',wallet:'✅ GPW + Apple Pay'},
  sub: {name:'副卡',num:'1094',bal:350.00,status:'frozen',type:'VIRTUAL',bin:'BZ-BIN（美国）',level:'Lv2',issue:'2026-04-20',expire:'2028-03-15',fee:'$0.25/月',fx:'Pass through + 5bps',single:2000,daily:5000,monthly:20000,dailyUsed:0,monthlyUsed:0,singleUsed:0,cvv:'789',wallet:'❌ 不支持'}
};
var currentCard='std', cardNumVis=false;
var kycStep=1, kycBin='bb';
var kybStep=1, kybBin='bb';

// ===== Utils =====
function $(id){return document.getElementById(id);}
function om(id){var el=$(id);if(!el)return;el.classList.add('show');document.body.classList.add('modal-open');}
function cm(id){var el=$(id);if(!el)return;el.classList.remove('show');document.body.classList.remove('modal-open');}
document.querySelectorAll('.modal-overlay').forEach(function(o){o.addEventListener('click',function(e){if(e.target===this)cm(this.id);});});
document.addEventListener('keydown',function(e){if(e.key==='Escape')document.querySelectorAll('.modal-overlay.show').forEach(function(m){cm(m.id);});});
function st(el,t){document.querySelectorAll(t).forEach(function(x){x.classList.remove('active');});el.classList.add('active');}
function sr(el){var g=el.closest('.radio-group');if(g)g.querySelectorAll('.radio-item').forEach(function(r){r.classList.remove('selected');});el.classList.add('selected');var r=el.querySelector('input[type=radio]');if(r)r.checked=true;}

function showToast(msg,type){
  var t=$('toast');if(!t)return;
  t.textContent=msg;t.className='toast show '+(type||'');
  setTimeout(function(){t.classList.remove('show');},3000);
}

// ===== Card Detail =====
function od(k){
  currentCard=k;var c=cards[k],f=c.status==='frozen';
  var cf=$('detailCardFace');if(!cf)return;
  cf.className='detail-card-face '+(f?'frozen':'active');
  $('detailAmount').textContent='$'+c.bal.toLocaleString('en-US',{minimumFractionDigits:2});
  $('detailNumText').textContent=cardNumVis?'4001 2345 6789 '+c.num:'•••• •••• •••• '+c.num;
  $('detailName').textContent='JOHN DOE';
  $('detailCvv').textContent='•••';
  $('detailTypeBadge').textContent=c.type;
  $('detailLevelBadge').textContent=c.level;
  $('detailStatus').textContent=f?'● 已冻结':'● 使用中';
  $('detailStatus').className='r '+(f?'warn':'green');
  $('detailBin').textContent=c.bin;
  $('detailIssue').textContent=c.issue;
  $('detailExpire').textContent=c.expire;
  $('detailFee').textContent=c.fee;
  $('detailFx').textContent=c.fx;
  if($('detailWallet'))$('detailWallet').textContent=c.wallet||'';
  $('detailSingle').textContent='$'+c.singleUsed.toLocaleString()+' / $'+c.single.toLocaleString();
  $('detailSingleBar').style.width=Math.min(c.singleUsed/c.single*100,100).toFixed(1)+'%';
  $('detailDaily').textContent='$'+c.dailyUsed.toLocaleString()+' / $'+c.daily.toLocaleString();
  $('detailDailyBar').style.width=Math.min(c.dailyUsed/c.daily*100,100).toFixed(1)+'%';
  $('detailMonthly').textContent='$'+c.monthlyUsed.toLocaleString()+' / $'+c.monthly.toLocaleString();
  $('detailMonthlyBar').style.width=Math.min(c.monthlyUsed/c.monthly*100,100).toFixed(1)+'%';
  $('freezeLabel').textContent=f?'解冻':'冻结';
  om('modalDetail');
}
function tcn(){
  cardNumVis=!cardNumVis;
  $('detailNumText').textContent=cardNumVis?'4001 2345 6789 4821':'•••• •••• •••• 4821';
  $('toggleVisBtn').textContent=cardNumVis?'隐藏':'显示';
}

// ===== Freeze =====
function of(){
  var c=cards[currentCard],f=c.status==='frozen';
  $('freezeTitle').textContent=f?'解冻卡片':'冻结卡片';
  $('freezeCardNum').textContent='•••• '+c.num;
  $('freezeDesc').innerHTML=f
    ?'确定要解冻卡片 <b>•••• '+c.num+'</b> 吗？'
    :'确定要冻结卡片 <b>•••• '+c.num+'</b> 吗？冻结期间无法进行任何交易。';
  $('btnConfirmFreeze').textContent=f?'确认解冻':'确认冻结';
  $('btnConfirmFreeze').className='btn '+(f?'btn-dark':'btn-danger');
  if($('freezeNotice'))$('freezeNotice').style.display='none';
  if($('expireNotice'))$('expireNotice').style.display='none';
  if(f && currentCard==='sub' && $('freezeNotice'))$('freezeNotice').style.display='flex';
  om('modalFreeze');
}
function cf(){
  var c=cards[currentCard],f=c.status==='frozen';
  if(f && currentCard==='sub'){
    cm('modalFreeze');
    om('modalUnfreezeVerify');
    return;
  }
  c.status=f?'active':'frozen';
  cm('modalFreeze');
  showToast(f?'✅ 卡片已解冻':'✅ 卡片已冻结');
  od(currentCard);
}
function doUnfreezeVerify(){
  cards[currentCard].status='active';
  cm('modalUnfreezeVerify');
  showToast('✅ 身份验证通过，卡片已解冻');
  od(currentCard);
}
function verify3DS(){
  cm('modal3DS');
  showToast('✅ 3DS 验证通过，交易继续','success');
}
function tcvv(){
  var v=$('detailCvv').textContent==='•••';
  $('detailCvv').textContent=v?cards[currentCard].cvv:'•••';
  $('cvvToggleBtn').textContent=v?'隐藏':'显示';
}

// ===== Limit =====
function ol(){
  var c=cards[currentCard];
  if(!c)return;
  if($('limitCardNum'))$('limitCardNum').textContent='•••• '+c.num;
  if($('limitLevel'))$('limitLevel').textContent=c.level;
  if($('singleVal'))$('singleVal').textContent='$'+c.single.toLocaleString();
  if($('dailyVal'))$('dailyVal').textContent='$'+c.daily.toLocaleString();
  if($('monthlyVal'))$('monthlyVal').textContent='$'+c.monthly.toLocaleString();
  if($('singleUsedBar'))$('singleUsedBar').style.width=Math.min(c.singleUsed/c.single*100,100).toFixed(1)+'%';
  if($('dailyUsedBar'))$('dailyUsedBar').style.width=Math.min(c.dailyUsed/c.daily*100,100).toFixed(1)+'%';
  if($('monthlyUsedBar'))$('monthlyUsedBar').style.width=Math.min(c.monthlyUsed/c.monthly*100,100).toFixed(1)+'%';
  if($('singleUsedText'))$('singleUsedText').textContent='已用 $'+c.singleUsed.toLocaleString();
  if($('dailyUsedText'))$('dailyUsedText').textContent='已用 $'+c.dailyUsed.toLocaleString();
  if($('monthlyUsedText'))$('monthlyUsedText').textContent='已用 $'+c.monthlyUsed.toLocaleString();
  document.querySelectorAll('.level-row').forEach(function(r){r.classList.remove('highlight');});
  var lvs={'Lv1':0,'Lv2':1,'Lv3':2,'Lv4':3};
  var idx=lvs[c.level]!==undefined?lvs[c.level]:1;
  var rows=document.querySelectorAll('.level-row');
  if(rows[idx])rows[idx].classList.add('highlight');
  om('modalLimit');
}
function sl(){
  var c=cards[currentCard];
  if(!c)return;
  var selected=document.querySelector('input[name=ld]:checked');
  if(selected && selected.value==='half'){
    c.single=Math.round(c.single*0.5);
    c.daily=Math.round(c.daily*0.5);
    c.monthly=Math.round(c.monthly*0.5);
  }
  cm('modalLimit');
  showToast('✅ 限额已更新');
  od(currentCard);
}

// ===== Cancel =====
function oc(){
  var c=cards[currentCard];if(!c)return;
  $('cancelCardNum').textContent='•••• '+c.num;
  $('cancelBalance').textContent='$'+c.bal.toLocaleString('en-US',{minimumFractionDigits:2});
  $('cancelRefund').textContent='$'+c.bal.toLocaleString('en-US',{minimumFractionDigits:2});
  $('cancelConfirmInput').value='';
  $('btnConfirmCancel').disabled=true;
  om('modalCancel');
}
function ccc(){$('btnConfirmCancel').disabled=$('cancelConfirmInput').value!=='注销';}
function cxc(){cm('modalCancel');showToast('✅ 卡片已注销，余额已退回账户','success');}

// ===== Topup =====
function ot(){
  if($('topupCrypto'))$('topupCrypto').style.display='block';
  if($('topupFiat'))$('topupFiat').style.display='none';
  if($('topupInternal'))$('topupInternal').style.display='none';
  if($('tabCrypto'))$('tabCrypto').classList.add('active');
  if($('tabFiat'))$('tabFiat').classList.remove('active');
  if($('tabInternal'))$('tabInternal').classList.remove('active');
  uc();
  om('modalTopup');
}
function stt(el,t){
  document.querySelectorAll('#modalTopup .tx-tab').forEach(function(x){x.classList.remove('active');});
  el.classList.add('active');
  if($('topupCrypto'))$('topupCrypto').style.display=t==='crypto'?'block':'none';
  if($('topupFiat'))$('topupFiat').style.display=t==='fiat'?'block':'none';
  if($('topupInternal'))$('topupInternal').style.display=t==='internal'?'block':'none';
}
function uc(){
  var coin=$('cryptoCoin').value,amt=parseFloat($('cryptoAmount').value)||0;
  if($('cryptoPay'))$('cryptoPay').textContent='约 '+amt.toFixed(2)+' '+coin;
  if($('cryptoRate'))$('cryptoRate').textContent='1 '+coin+' ≈ $1.00（实时）';
}
function ct(){cm('modalTopup');showToast('✅ 充值请求已提交，区块链确认后 ≤ 10 秒到账','success');}

// ===== New Card KYC =====
function onc(type){if(type==='kyc'){kycStep=1;kycBin='bb';kycShowStep();om('modalKYC');}else{kybStep=1;kybBin='bb';kybShowStep();om('modalKYB');}}
function kycShowStep(){
  for(var i=1;i<=3;i++){
    var stepEl=$('kyc-step-'+i);if(stepEl)stepEl.style.display=i===kycStep?'block':'none';
    var d=$('kyc-dot-'+i);if(d)d.className='step-dot '+(i<kycStep?'done':i===kycStep?'current':'pending');
  }
  var backBtn=$('kyc-back');if(backBtn)backBtn.style.display=kycStep>1?'inline-flex':'none';
  var nextBtn=$('kyc-next');if(nextBtn)nextBtn.style.display=kycStep<3?'inline-flex':'none';
  var goBtn=$('kyc-go');if(goBtn)goBtn.style.display=kycStep===3?'inline-flex':'none';
  if(kycStep===3){
    var confBin=$('kyc-conf-bin');if(confBin)confBin.textContent=kycBin==='bb'?'BB-BIN 🇨🇦 加拿大':'BZ-BIN 🇺🇸 美国';
    var confFx=$('kyc-conf-fx');if(confFx)confFx.textContent=kycBin==='bb'?'1.5%':'Pass through + 5bps';
    var confWallet=$('kyc-conf-wallet');if(confWallet)confWallet.textContent=kycBin==='bb'?'✅ GPW + Apple Pay':'❌ 不支持';
    var vn=$('kyc-virtual-notice');if(vn)vn.style.display='block';
  }
}
function kycSelBin(el,bin){
  document.querySelectorAll('#modalKYC .bin-option').forEach(function(x){x.classList.remove('selected');});
  el.classList.add('selected');kycBin=bin;
}
function kycNext(){if(kycStep<3){kycStep++;kycShowStep();}}
function kycBack(){if(kycStep>1){kycStep--;kycShowStep();}}
function kycGo(){cm('modalKYC');showToast('正在提交审核...','success');setTimeout(function(){showKycResult('passed');},1500);}
function showKycResult(type){
  ['Passed','Request','Canceled','Timeout'].forEach(function(t){
    var el=document.getElementById('kycResult'+t);if(el)el.style.display='none';
  });
  var map={passed:'Passed',request:'Request',canceled:'Canceled',timeout:'Timeout'};
  var key=map[type]||'Passed';
  var el=document.getElementById('kycResult'+key);
  if(el)el.style.display='block';
  om('modalKycResult');
}

// ===== New Card KYB =====
function kybShowStep(){
  for(var i=1;i<=3;i++){
    var stepEl=$('kyb-step-'+i);if(stepEl)stepEl.style.display=i===kybStep?'block':'none';
    var d=$('kyb-dot-'+i);if(d)d.className='step-dot '+(i<kybStep?'done':i===kybStep?'current':'pending');
  }
  var backBtn=$('kyb-back');if(backBtn)backBtn.style.display=kybStep>1?'inline-flex':'none';
  var nextBtn=$('kyb-next');if(nextBtn)nextBtn.style.display=kybStep<3?'inline-flex':'none';
  var goBtn=$('kyb-go');if(goBtn)goBtn.style.display=kybStep===3?'inline-flex':'none';
  if(kybStep===3){
    var confBin=$('kyb-conf-bin');if(confBin)confBin.textContent=kybBin==='bb'?'BB-BIN 🇨🇦 加拿大':'BZ-BIN 🇺🇸 美国';
    var confFx=$('kyb-conf-fx');if(confFx)confFx.textContent=kybBin==='bb'?'1.5%':'Pass through + 5bps';
    var confWallet=$('kyb-conf-wallet');if(confWallet)confWallet.textContent=kybBin==='bb'?'✅ GPW + Apple Pay':'❌ 不支持';
    var vn=$('kyb-virtual-notice');if(vn)vn.style.display='block';
  }
}
function kybSelBin(el,bin){
  document.querySelectorAll('#modalKYB .bin-option').forEach(function(x){x.classList.remove('selected');});
  el.classList.add('selected');kybBin=bin;
}
function kybNext(){if(kybStep<3){kybStep++;kybShowStep();}}
function kybBack(){if(kybStep>1){kybStep--;kybShowStep();}}
function kybGo(){cm('modalKYB');showToast('跳转至 KYB 认证页面...','success');}
"""
    
    html = before + new_script + '// (script fixed)\n' + after
    
    with open('12-卡片管理-v3.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('DONE: script replaced successfully')
"""
