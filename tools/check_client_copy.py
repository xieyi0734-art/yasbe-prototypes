# -*- coding: utf-8 -*-
"""客户端原型文案闸门 —— 检查「面向客户」合规性 + PM 备注规范化。

用法:
  python tools/check_client_copy.py <路径...> [--only GLOB] [--json 报告路径]

规则:
  · 只扫「页面可见文案」: <script>/<style>/<!--注释--> 不计入禁词扫描
    （替换为等量换行以保持行号）
  · 文件名含「客户端」→ 客户端规则(硬禁内部词/业务描述腔/原型痕迹/品牌形态)
                含「管理端」→ 管理端规则(原型痕迹 + 品牌形态)
                其它        → 通用规则
  · PM 备注规范: 期望单行块 <!-- PM-NOTE: … --><div class="pmnote"><b>PM 备注</b>…</div>
    已标注的 pmnote 内容视为「备注」, 不计入客户文案禁词扫描;
    其它形态(注释中文/正文「备注：」/ alert 无前缀)记为 WARN;
    每页无规范 PM 备注块也记 WARN
退出码: ERROR > 0 → 1，否则 0
"""
import io, os, re, sys, json, glob

# ---------------------------------------------------------------- 词表
ERROR_CLIENT = {
    '兜底': '内部口径词', '商务': '内部口径词(商务经理/商务调整)', '人工审核': '内部流程词',
    '转人工': '内部流程词', '风控': '内部职能词', '后台': '内部系统词', '上游': '内部链路词',
    '我司': '内部称谓', '内部': '内部口径词', '灰度': '内部发布词', '埋点': '内部技术词',
    '白名单': '内部技术词', '黑名单': '内部技术词', '状态机': '内部技术词', '幂等': '内部技术词',
    '商户': '内部业务词(客户侧用"用户/账户")', '对账': '内部业务词', '打款': '内部业务词(用"结算/到账")',
    '放款': '内部业务词', '网关': '内部技术词', '审批流': '内部流程词', '跑批': '内部技术词',
    '规则引擎': '内部技术词', '配置项': '内部技术词',
}
WARN_CLIENT = {
    '配置': '确认是否面向客户(如"安全配置"可留)', '字段': '技术词，建议改"信息项"',
    '接口': '技术词', '参数': '技术词', '校验': '技术词("核验/验证"更面向客户)',
    '平台默认': '内部默认值口径(改"标准")', '平台侧': '内部视角', '默认值': '内部默认值口径',
    '本条': '条款引用，确认客户是否需要', '本规则': '规则说明腔调', '该页面': '设计视角',
    '本页面': '设计视角', '此页面': '设计视角', '用于说明': '设计说明腔调', '实现方式': '实现细节',
}
PROTO_TRACE = {
    '原型': '原型痕迹', 'demo': '原型痕迹', 'mock': '原型痕迹', 'TODO': '原型痕迹', 'FIXME': '原型痕迹',
    '占位': '原型痕迹', '待定': '原型痕迹', '测试数据': '原型痕迹', '假数据': '原型痕迹',
    '示例数据': '原型痕迹', '演示数据': '原型痕迹',
}
BRAND_ERROR = {'积分': '品牌口径禁用(应为 Points / yasbee+)'}
BRAND_WARN = {'YASBee': '确认语境：奖励名称可用，平台名称须 YASBe'}

PMNOTE_CLASS = 'pmnote'
# 非规范备注的疑似形态
NOTE_VISIBLE = re.compile(r'^\s*(?:[【\[]\s*(备注|说明|注|提示|注意|PM|产品经理|设计说明)\s*[】\]])|'
                          r'^\s*(备注|说明|提示|注意|PM 备注|产品经理(?:原型)?备注)\s*[:：]')
NOTE_COMMENT = re.compile(r'<!--(?!\s*(?:PM-NOTE|pmnote))[^>]*[\u4e00-\u9fff]')
BLOCK = re.compile(r'<(script|style)\b[^>]*>(.*?)</\1>', re.S | re.I)
PMNOTE_DIV = re.compile(r'<div class="pmnote')


def mask_blocks(src):
    """把 script/style/注释内容换成等量换行，保持行号不变。"""
    src = BLOCK.sub(lambda m: m.group(0)[:m.group(0).index('>') + 1]
                    + '\n' * m.group(2).count('\n') + '</%s>' % m.group(1), src)
    return re.sub(r'<!--.*?-->', lambda m: '\n' * m.group(0).count('\n'), src, flags=re.S)


def iter_files(paths, only=None):
    out = []
    for p in paths:
        if os.path.isdir(p):
            out += glob.glob(os.path.join(p, '*.html'))
        else:
            out += glob.glob(p)
    if only:
        out = [f for f in out if glob.fnmatch.fnmatch(os.path.basename(f), only)]
    return sorted(set(out))


def kind_of(name):
    if '客户端' in name:
        return '客户端'
    if '管理端' in name:
        return '管理端'
    return '通用'


def scan(path):
    src = io.open(path, encoding='utf-8', errors='replace').read()
    masked = mask_blocks(src)
    kinds = kind_of(os.path.basename(path))
    errs, warns, notes = [], [], 0
    for i, line in enumerate(masked.split('\n'), 1):
        is_note = bool(PMNOTE_DIV.search(line))
        if is_note:
            notes += len(PMNOTE_DIV.findall(line))
        # pmnote 是「已标注为备注」的块, 内容允许含内部口径, 不按客户文案扫
        scanline = re.sub(r'<div class="pmnote[^"]*">.*?</div>', ' ', line) if is_note else line
        visible = re.sub(r'<[^>]+>', ' ', scanline)
        vis_attrs = ' '.join(re.findall(r'(?:title|placeholder|aria-label)="([^"]*)"', line))
        hay = visible + ' ' + vis_attrs
        for m in re.finditer(r"alert\('([^']*)'\)", line):
            at = m.group(1)
            if (re.search(r'[\u4e00-\u9fff]', at)
                    and not at.startswith('[原型演示]') and not at.startswith('[PM 备注]')
                    and re.search(r'演示|占位|补录', at)):
                warns.append((i, 'alert 备注未规范化',
                              '占位类加前缀 [原型演示]，口径类加 [PM 备注]', at[:60]))
        tables = [(BRAND_ERROR, 'ERROR'), (BRAND_WARN, 'WARN'), (PROTO_TRACE, 'WARN')]
        if kinds == '客户端':
            tables = [(ERROR_CLIENT, 'ERROR'), (WARN_CLIENT, 'WARN')] + tables
        elif kinds == '通用':
            tables = [(ERROR_CLIENT, 'ERROR')] + tables
        for table, sev in tables:
            for w, why in sorted(table.items(), key=lambda kv: -len(kv[0])):
                if w in hay:
                    rec = (i, w, why, visible.strip()[:70])
                    (errs if sev == 'ERROR' else warns).append(rec)
                    break
        m = NOTE_VISIBLE.match(visible.strip())
        if m and PMNOTE_CLASS not in line:
            warns.append((i, '备注未规范化', '改用 <div class="pmnote">…</div>', visible.strip()[:70]))
        if NOTE_COMMENT.search(line):
            warns.append((i, 'HTML 注释含中文说明', '建议改为 pmnote 块(可见)或 <!-- PM-NOTE: … -->', line.strip()[:70]))
    if notes == 0 and kinds in ('客户端', '管理端'):
        warns.append((0, '本页无规范 PM 备注块', '每页至少 1 条: <!-- PM-NOTE: … --><div class="pmnote">…</div>', ''))
    return {'file': path, 'kind': kinds, 'errors': errs, 'warns': warns, 'pmnotes': notes}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
    jout = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None
    files = iter_files(args or ['.'], only)
    if not files:
        print('没有匹配到 HTML 文件'); return 2
    res = [scan(f) for f in files]
    ne = sum(len(r['errors']) for r in res)
    nw = sum(len(r['warns']) for r in res)
    nn = sum(r['pmnotes'] for r in res)
    for r in res:
        if not r['errors'] and not r['warns']:
            print('[OK]   %s  (%s, PM备注 %d)' % (r['file'], r['kind'], r['pmnotes']))
            continue
        print('[%s] %s  (%s)' % ('FAIL' if r['errors'] else 'WARN', r['file'], r['kind']))
        for i, w, why, snip in r['errors']:
            print('   ERROR L%-5d %-10s %s\n         > %s' % (i, w, why, snip))
        for i, w, why, snip in r['warns']:
            print('   warn  L%-5d %-10s %s\n         > %s' % (i, w, why, snip))
    print('\n== 汇总: %d 文件 · ERROR %d · WARN %d · 规范 PM 备注块 %d ==' % (len(res), ne, nw, nn))
    if jout:
        io.open(jout, 'w', encoding='utf-8').write(json.dumps(res, ensure_ascii=False, indent=1))
        print('报告: %s' % jout)
    return 1 if ne else 0


if __name__ == '__main__':
    sys.exit(main())
