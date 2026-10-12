# -*- coding: utf-8 -*-
"""生成《白标系统 · 一期业务全景流程图》(单文件 HTML, 纯内嵌 SVG)

依据: prd/白标系统/白标系统-一期PRD-业务流程稿.md (v1.0 业务流程定稿)
输出: diagrams/whitelabel-phase1-full-business-flow.html
跑法: python tools/gen_whitelabel_flow.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "diagrams", "whitelabel-phase1-full-business-flow.html")

BG = "#0B0E14"; CARD = "#131820"; TXT = "#E8ECF0"; SUB = "#7B8CA8"
GOLD = "#E59303"; BLUE = "#3B82F6"; GREEN = "#22C55E"; RED = "#EF4444"
GREY = "#4B5563"; PURPLE = "#A855F7"; TEAL = "#14B8A6"; CYAN = "#22D3EE"; LGREY = "#9CA3AF"

TONE = {
    "default": ("#131820", "rgba(255,255,255,.18)"),
    "gold": ("rgba(229,147,3,.10)", GOLD),
    "green": ("rgba(34,197,94,.10)", GREEN),
    "red": ("rgba(239,68,68,.10)", RED),
    "blue": ("rgba(59,130,246,.10)", BLUE),
    "grey": ("rgba(75,85,99,.20)", LGREY),
    "purple": ("rgba(168,85,247,.10)", PURPLE),
    "teal": ("rgba(20,184,166,.10)", TEAL),
}
ROLE = {
    "ops": ("🏢 平台运营", GOLD),
    "sys": ("⚙️ 平台系统", BLUE),
    "dev": ("🧑‍💻 租户·开发", GREEN),
    "biz": ("🧑‍💼 租户·业务", CYAN),
    "up": ("🌐 上游渠道", PURPLE),
    "end": ("👤 终端客户", LGREY),
}
EDGE_COLOR = {
    "grey": "rgba(255,255,255,.24)", "green": GREEN, "red": RED,
    "gold": GOLD, "blue": BLUE, "purple": PURPLE, "teal": TEAL,
}


def cw(ch, fs):
    return (6.8 if ord(ch) < 0x2E80 else 13.3) * fs / 13.0


def tw(s, fs=13):
    return sum(cw(c, fs) for c in s)


def wrap(s, maxw, fs=13):
    out, cur = [], ""
    for ch in s:
        if cur and tw(cur + ch, fs) > maxw:
            out.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out or [""]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def markers_svg():
    parts = []
    for name, col in EDGE_COLOR.items():
        parts.append(
            f'<marker id="ar-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
            f'markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{col}"/></marker>')
    return "\n".join(parts)


class Fig(object):
    def __init__(self, w, h):
        self.W = w; self.H = h
        self.regions = []; self.edges = []; self.node_svg = []; self.labels = []
        self.nodes = {}; self.maxY = 0; self.maxX = 0

    def _txt(self, x, y, s, fs=13, fill=TXT, weight="500", anchor="middle"):
        return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{fs}" '
                f'font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>')

    def region(self, x, y, w, h, label="", sub=""):
        self.regions.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" '
            f'fill="rgba(255,255,255,.025)" stroke="rgba(255,255,255,.07)" stroke-width="1"/>')
        if label:
            self.regions.append(self._txt(x + 18, y + 27, label, 12.5, SUB, "700", "start"))
        if sub:
            self.regions.append(self._txt(x + 18, y + 48, sub, 11, "rgba(123,140,168,.85)", "400", "start"))
        self.maxX = max(self.maxX, x + w); self.maxY = max(self.maxY, y + h)

    def box(self, x, y, w, title, subs=(), tone="default", chip=None, badge=None,
            dashed=False, rx=9, fs=13, min_h=None, sub_fs=11):
        tone_fill, stroke = TONE[tone]
        tl = wrap(title, w - 26, fs)
        sl = []
        for s in subs:
            sl += wrap(s, w - 26, sub_fs)
        h = 15 + len(tl) * (fs + 6) + (9 + len(sl) * (sub_fs + 4) if sl else 0) + 15
        if min_h:
            h = max(h, min_h)
        if dashed:
            da = ' stroke-dasharray="7 5"'; tone_fill = "#131820"
        else:
            da = ""
        out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
               f'fill="{tone_fill}" stroke="{stroke}" stroke-width="1.5"{da}/>']
        cy = y + 15 + fs
        for ln in tl:
            out.append(self._txt(x + w / 2, cy, ln, fs, TXT, "600"))
            cy += fs + 6
        if sl:
            cy += 3
            for ln in sl:
                out.append(self._txt(x + w / 2, cy, ln, sub_fs, SUB, "400"))
                cy += sub_fs + 4
        if chip:
            label, col = ROLE[chip]
            cwid = tw(label, 10) + 18
            out.append(f'<rect x="{x:.1f}" y="{y-22:.1f}" width="{cwid:.1f}" height="18" rx="9" '
                       f'fill="{CARD}" stroke="{col}" stroke-width="1"/>')
            out.append(self._txt(x + cwid / 2, y - 9.5, label, 10, col, "700"))
        if badge:
            bw = tw(badge, 10) + 18
            out.append(f'<rect x="{x + w - bw:.1f}" y="{y-22:.1f}" width="{bw:.1f}" height="18" rx="9" '
                       f'fill="{tone_fill}" stroke="{stroke}" stroke-width="1"/>')
            out.append(self._txt(x + w - bw / 2, y - 9.5, badge, 10, stroke, "700"))
        self.node_svg.append("".join(out))
        nid = "n%d" % len(self.nodes)
        self.nodes[nid] = dict(x=x, y=y, w=w, h=h, cx=x + w / 2, cy=y + h / 2, kind="box")
        self.maxX = max(self.maxX, x + w); self.maxY = max(self.maxY, y + h)
        return nid

    def diamond(self, cx, cy, hw, hh, title, subs=(), tone="gold", chip=None, fs=12.5):
        tone_fill, stroke = TONE[tone]
        pts = f"{cx:.1f},{cy-hh:.1f} {cx+hw:.1f},{cy:.1f} {cx:.1f},{cy+hh:.1f} {cx-hw:.1f},{cy:.1f}"
        out = [f'<polygon points="{pts}" fill="{tone_fill}" stroke="{stroke}" stroke-width="1.6"/>']
        tl = wrap(title, hw * 1.32, fs)
        sl = []
        for s in subs:
            sl += wrap(s, hw * 1.45, 10)
        total = len(tl) * (fs + 4) + (len(sl) * 13 + 4 if sl else 0)
        cy0 = cy - total / 2 + fs
        for ln in tl:
            out.append(self._txt(cx, cy0, ln, fs, TXT, "600")); cy0 += fs + 4
        for ln in sl:
            out.append(self._txt(cx, cy0, ln, 10, SUB, "400")); cy0 += 13
        yx, yy = cx + hw + 20, cy
        nx, ny = cx, cy + hh + 20
        out.append(f'<path d="M {cx+hw:.1f},{cy:.1f} L {yx-11:.1f},{yy:.1f}" stroke="{GREEN}" stroke-width="1.6" fill="none"/>')
        out.append(f'<circle cx="{yx:.1f}" cy="{yy:.1f}" r="11" fill="{GREEN}"/>')
        out.append(self._txt(yx, yy + 4, "Y", 11, "#0F172A", "700"))
        out.append(f'<path d="M {cx:.1f},{cy+hh:.1f} L {nx:.1f},{ny-11:.1f}" stroke="{RED}" stroke-width="1.6" fill="none"/>')
        out.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="11" fill="{RED}"/>')
        out.append(self._txt(nx, ny + 4, "N", 11, "#FFFFFF", "700"))
        if chip:
            label, col = ROLE[chip]
            cwid = tw(label, 10) + 18
            out.append(f'<rect x="{cx-hw+6:.1f}" y="{cy-hh-26:.1f}" width="{cwid:.1f}" height="18" rx="9" '
                       f'fill="{CARD}" stroke="{col}" stroke-width="1"/>')
            out.append(self._txt(cx - hw + 6 + cwid / 2, cy - hh - 13.5, label, 10, col, "700"))
        self.node_svg.append("".join(out))
        nid = "n%d" % len(self.nodes)
        self.nodes[nid] = dict(cx=cx, cy=cy, hw=hw, hh=hh, kind="diamond")
        self.maxX = max(self.maxX, cx + hw + 45); self.maxY = max(self.maxY, cy + hh + 45)
        return nid

    def anchor(self, nid, side):
        r = self.nodes[nid]
        if r["kind"] == "box":
            if side == "t": return (r["cx"], r["y"])
            if side == "b": return (r["cx"], r["y"] + r["h"])
            if side == "l": return (r["x"], r["cy"])
            return (r["x"] + r["w"], r["cy"])
        cx, cy, hw, hh = r["cx"], r["cy"], r["hw"], r["hh"]
        if side == "t": return (cx, cy - hh)
        if side == "b": return (cx, cy + hh)
        if side == "l": return (cx - hw, cy)
        if side == "r": return (cx + hw, cy)
        if side == "y": return (cx + hw + 32, cy)
        if side == "n": return (cx, cy + hh + 32)
        return (cx, cy)

    def route(self, sx, sy, ex, ey, fs_, ts_):
        vfrom = fs_ in ("t", "b", "n")
        vto = ts_ in ("t", "b")
        if abs(sx - ex) < 3 and abs(sy - ey) < 3:
            return None
        if not vfrom and not vto:
            if abs(sy - ey) < 3:
                return f"M {sx:.1f},{sy:.1f} L {ex:.1f},{ey:.1f}"
            mx = (sx + ex) / 2
            return f"M {sx:.1f},{sy:.1f} L {mx:.1f},{sy:.1f} L {mx:.1f},{ey:.1f} L {ex:.1f},{ey:.1f}"
        if vfrom and vto:
            if abs(sx - ex) < 3:
                return f"M {sx:.1f},{sy:.1f} L {ex:.1f},{ey:.1f}"
            my = (sy + ey) / 2
            return f"M {sx:.1f},{sy:.1f} L {sx:.1f},{my:.1f} L {ex:.1f},{my:.1f} L {ex:.1f},{ey:.1f}"
        if vfrom and not vto:
            return f"M {sx:.1f},{sy:.1f} L {sx:.1f},{ey:.1f} L {ex:.1f},{ey:.1f}"
        return f"M {sx:.1f},{sy:.1f} L {ex:.1f},{sy:.1f} L {ex:.1f},{ey:.1f}"

    def edge(self, a, b=None, fs_="auto", ts_="auto", color="grey", label=None,
             dashed=False, marker=True, pts=None, lx=None, ly=None, lw=240):
        col = EDGE_COLOR[color]
        da = ' stroke-dasharray="6 5"' if dashed else ""
        mk = f' marker-end="url(#ar-{color})"' if marker else ""
        if pts is None:
            ra, rb = self.nodes[a], self.nodes[b]
            if fs_ == "auto":
                if ra["kind"] == "box" and rb["kind"] == "box":
                    if rb["x"] >= ra["x"] + ra["w"] - 4:
                        fs_, ts_ = "r", "l"
                    elif rb["y"] >= ra["y"] + ra["h"] - 4:
                        fs_, ts_ = "b", "t"
                    else:
                        fs_, ts_ = "t", "b"
                elif ra["kind"] == "diamond":
                    rtop = rb["y"] if rb["kind"] == "box" else rb["cy"] - rb["hh"]
                    if rtop >= ra["cy"]:
                        fs_, ts_ = "n", "t"
                    else:
                        fs_, ts_ = "y", "l"
                else:
                    fs_, ts_ = "b", "t"
            sx, sy = self.anchor(a, fs_)
            ex, ey = self.anchor(b, ts_)
            p = self.route(sx, sy, ex, ey, fs_, ts_)
            horiz = (fs_ in ("r", "y", "l")) and (ts_ in ("l", "r"))
            if lx is None:
                lx = (sx + ex) / 2
            if ly is None:
                ly = (min(sy, ey) - 46) if horiz else (sy + ey) / 2
        else:
            p = "M " + " L ".join("%.1f,%.1f" % (x, y) for x, y in pts)
            if lx is None:
                lx = (pts[0][0] + pts[-1][0]) / 2
            if ly is None:
                ly = (pts[0][1] + pts[-1][1]) / 2
        if p:
            self.edges.append(f'<path d="{p}" fill="none" stroke="{col}" stroke-width="1.8"{da}{mk}/>')
        if label:
            self.edge_label(lx, ly, label, col, lw)

    def edge_label(self, x, y, text, col, maxw=240):
        lines = wrap(text, maxw, 11)
        bw = max(tw(l, 11) for l in lines) + 16
        bh = len(lines) * 15 + 8
        self.labels.append(
            f'<rect x="{x-bw/2:.1f}" y="{y-bh/2:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="6" '
            f'fill="rgba(11,14,20,.96)" stroke="{col}" stroke-width="1" stroke-opacity=".6"/>')
        cy = y - bh / 2 + 15
        for ln in lines:
            self.labels.append(self._txt(x, cy, ln, 11, col, "600"))
            cy += 15

    def note(self, x, y, text, color=SUB, fs=11.5, maxw=600):
        cy = y
        for ln in wrap(text, maxw, fs):
            self.node_svg.append(self._txt(x, cy, ln, fs, color, "400", "start"))
            cy += fs + 6
        return cy

    def svg(self):
        self.W = int(max(self.maxX + 60, self.W))
        self.H = int(max(self.maxY + 60, self.H))
        return ('<svg viewBox="0 0 %d %d" width="%d" height="%d" xmlns="http://www.w3.org/2000/svg" '
                "font-family=\"Inter, -apple-system, 'Segoe UI', sans-serif\">" % (self.W, self.H, self.W, self.H)
                + "<defs>" + markers_svg() + "</defs>"
                + f'<rect x="0" y="0" width="{self.W}" height="{self.H}" fill="{CARD}"/>'
                + "".join(self.regions) + "".join(self.edges) + "".join(self.node_svg)
                + "".join(self.labels) + "</svg>")


# ============================== 1. 关系与角色 ==============================
def sec_boundary():
    f = Fig(3200, 1000)
    f.region(60, 90, 3080, 500, "关系基准（三层）",
             "我方是能力的上游 · 租户是集成我方的下游 · 终端客户是租户自己的客户")

    a = f.box(110, 200, 620, "上游渠道（能力兑现方）",
              ["Bridge（USD）· OpenPayd（EUR / GBP）", "SafeHeron（加密）· Interlace（卡片）", "未来：BitGo 币兑（预留）"],
              tone="purple", chip="up", dashed=True)
    b = f.box(920, 180, 1180, "我方（平台 / 上游能力的开放方）",
              ["对租户只暴露三类界面：开发者门户 · 租户自助后台 · 运营台",
               "不提供终端客户界面 —— 品牌化在我方几乎没有功能量",
               "合规两段式：终端客户合规归租户；我方对上游负责 + KYB 租户 + 合同约束"],
              tone="gold", min_h=210)
    c = f.box(2300, 180, 620, "白标租户（下游集成方）",
              ["自带产品、自带终端客户", "一份合同 + 一个 API key + 已授权模块"],
              tone="green", min_h=210)
    d = f.box(2300, 440, 620, "终端客户", ["与我方无直接关系", "只体现为「资金」与「消费行为」"],
              tone="grey", dashed=True, chip="end")
    f.edge(a, b, color="purple", label="申请 KYB / 开通", ly=246)
    f.edge(b, c, color="gold", label="建户 / 发 key / 文档 / 回调", ly=246)
    f.edge(c, d, fs_="b", ts_="t", color="grey", dashed=True, label="租户自己的客户")
    f.note(120, 560, "推论：我方给下游的体验下限 = 我方自己在 Bridge 侧的体验。通道选择与路由是平台内部事务，租户不可见，且可换渠道、加渠道。", SUB, 12, 2200)

    f.region(60, 640, 3080, 290, "六类角色", "本图中每个节点左上角的小标签 = 该动作的执行角色")
    roles = [
        ("up", "能力兑现方：开户 / 收付 / 发卡 / 广播", "通道对租户不可见 · 可换可加"),
        ("ops", "建档 · 分模块审核 · 签约 · 切生产 · 异常处置", "一期大量环节靠人工，是「人工接客」的承担者"),
        ("sys", "通道路由 · 账本 · 风控筛查 · 计费结算 · Webhook", "闸门与限额由系统强制，不靠人记"),
        ("dev", "调 API：建主体 / 收付 / 提现 / 开卡 / 收回调", "真正的对接方，一期由运营陪跑第一单"),
        ("biz", "用自助后台：看载体 / 交易 / 对账 / 结算单", "只读为主，一期不能发起争议"),
        ("end", "不在我方系统内", "只体现为资金与消费行为，不是我方用户"),
    ]
    x = 110
    for key, t, s in roles:
        f.box(x, 730, 460, t, [s], tone="default", chip=key)
        x += 500
    return f


# ============================== 2. 接入闭环主图 ==============================
def sec_master():
    f = Fig(4200, 1500)
    f.region(60, 90, 4080, 1330, "公共主轴 F1 · 租户接入与模块授权（一期唯一的主线）",
             "一期目标：把已合作的那个平台「租户化」；第二个租户接入时，团队不用写代码、不用工程介入")

    y = 330
    g = 56
    cur = 110
    n1 = f.box(cur, y, 300, "① 建档", ["录入租户档案：拟开通模块 + 定价口径", "人工"],
               chip="ops", badge="阶段① 已建立"); cur += 300 + g
    n2 = f.box(cur, y, 320, "② 分模块审核", ["法币 / 加密 / 卡片 各自出结论", "通过 · 驳回 · 补件"],
               chip="ops", badge="阶段②"); cur += 320 + g
    d1cx = cur + 190
    d1 = f.diamond(d1cx, y + 46, 190, 108, "至少一个模块通过？", ["独立结论，互不影响"], chip="ops")
    cur = d1cx + 190 + g
    n3 = f.box(cur, y, 320, "③ 签署合同并生效", ["生产闸门的硬条件 · 人工线下"], tone="gold",
               chip="ops", badge="阶段③ 已签约"); cur += 320 + g
    n4 = f.box(cur, y, 320, "④ 开通联调", ["生成受限 key + 限额度 + 白名单", "半自动（人工交付）"],
               chip="ops", badge="阶段④ 可联调"); n4x = cur; cur += 320 + g
    n4b = f.box(n4x, y + 250, 320, "按档案开通模块权限", ["推送文档入口与错误码字典"], tone="blue", chip="sys")
    n5 = f.box(cur, y, 330, "⑤ 按模块联调", ["健康检查 → 建主体 → 价值进入", "→ 价值出去 → Webhook 回调"],
               chip="dev"); cur += 330 + g
    d2cx = cur + 195
    d2 = f.diamond(d2cx, y + 46, 195, 110, "该模块联调通过？", ["逐模块判定"], chip="ops")
    cur = d2cx + 195 + g
    d3cx = cur + 210
    d3 = f.diamond(d3cx, y + 46, 210, 114, "闸门：资质 ∧ 合同 ∧ 联调", ["三者齐备才放行"], chip="sys")
    cur = d3cx + 210 + g
    n7 = f.box(cur, y, 330, "⑦ 生产运行（解除限额）", ["租户真实调用 → 产生用量"],
               tone="green", chip="dev", badge="阶段⑤/⑥ 生产中"); cur += 330 + g
    n8 = f.box(cur, y, 320, "账务闭环", ["计量 → 计费（价格快照）", "→ 结算单 → 收款 → 对账"],
               tone="blue", chip="sys"); n8x = cur

    f.edge(n1, n2, color="grey")
    f.edge(n2, d1, color="grey")
    f.edge(d1, n3, color="green", label="可开放")
    f.edge(n3, n4, color="gold")
    f.edge(n4, n5, color="grey")
    f.edge(n4, n4b, fs_="b", ts_="t", color="blue")
    f.edge(n5, d2, color="grey")
    f.edge(d2, d3, color="green", label="该模块可切生产")
    f.edge(d3, n7, color="green", label="放行")
    f.edge(n7, n8, color="blue", label="产生用量即计费")

    upn = f.box(1900, 140, 1500, "🌐 上游渠道：能力兑现方（Bridge · OpenPayd · SafeHeron · Interlace）",
                ["通道选择与路由由平台内部决定，租户不可见；可随时换渠道、加渠道而不影响租户"],
                tone="purple", dashed=True, chip="up")
    f.edge(upn, n7, fs_="b", ts_="t", color="purple", dashed=True, label="能力在此兑现")

    b1 = f.box(d1cx - 210, y + 330, 420, "驳回 / 需补件 → 该模块停止", ["不影响其他模块的单独推进"],
               tone="red", chip="ops")
    f.edge(d1, b1, color="red", label="不通过")
    f.edge(b1, n1, fs_="l", ts_="l", color="red", dashed=True, label="补件后重审", lx=300, ly=790)

    b2 = f.box(d2cx - 210, y + 330, 420, "停在联调态 → 禁止切生产",
               ["自助排错：文档 / 错误码 / 调试台", "人工陪跑第一单"], tone="red", chip="dev")
    f.edge(d2, b2, color="red", label="不通过")
    f.edge(b2, n5, fs_="t", ts_="b", color="red", dashed=True, label="改对接后重试", lx=d2cx - 280, ly=y + 250)

    b3 = f.box(d3cx - 210, y + 330, 420, "拦截 → 不得进入生产", ["差额项（资质 / 合同 / 联调）补齐后重走"],
               tone="red", chip="sys")
    f.edge(d3, b3, color="red", label="任一不满足")

    n9 = f.box(n8x, y + 330, 320, "租户·业务侧可见", ["载体 / 交易记录 / 对账单 / 结算单"], chip="biz")
    f.edge(n8, n9, fs_="b", ts_="t", color="teal")
    n10 = f.box(n8x, y + 500, 320, "三处可见（贯穿）", ["Webhook · 租户自助后台 · 运营台"], tone="gold", chip="sys")
    f.edge(n9, n10, color="gold")

    f.region(110, 900, 1800, 200, "本流程中不出现的角色", "避免误画界面")
    f.note(140, 970, "👤 终端客户：接入闭环与我方能力开放都不产生终端客户界面。终端客户只在下游三条业务流里作为「资金来源 / 消费主体」出现，不与我方系统发生任何直接关系。",
           LGREY, 12, 1740)
    f.region(1980, 900, 2160, 200, "「人工接客，自动跑数」的落点", "一期手段")
    f.note(2010, 970, "人工：建档 · 分模块审核 · 签约 · 切生产确认 · 异常处置。自动：发 key · 闸门校验 · 计量计费 · 结算单 · Webhook。半自动：受限 key 生成 · 限额解除。",
           SUB, 12, 2100)

    f.region(110, 1140, 4080, 270, "图例", "菱形 = 判定点（只有菱形产生分支）；其余节点都是顺序推进")
    items = [("grey", "主流程 / 顺序推进"), ("green", "通过 · 放行 · 终态"), ("red", "驳回 · 拦截 · 失败"),
             ("gold", "闸门 · 硬条件 · 关键节点"), ("purple", "上游渠道（外部，租户不可见）"),
             ("blue", "平台系统自动动作"), ("teal", "租户业务侧可见内容")]
    cx = 150
    for col, t in items:
        f.edges.append(f'<path d="M {cx},{1200} L {cx+70},{1200}" stroke="{EDGE_COLOR[col]}" '
                       f'stroke-width="2.4" marker-end="url(#ar-{col})"/>')
        f.node_svg.append(f._txt(cx + 84, 1204, t, 12, TXT, "500", "start"))
        cx += 96 + tw(t, 12) + 40
    f.note(150, 1280, "绿色 Y 圆 = 通过出口；红色 N 圆 = 不通过出口；红色虚线回环 = 补件后重审 / 改对接后重试。所有 N 分支都在本图中给出了后果。",
           SUB, 12, 2400)
    return f


# ============================== 3. 三模块业务流 ==============================
def band(f, gx, gy, label, sub, rows):
    f.region(gx, gy, 3960, 700, label, sub)
    y = gy + 150
    cur = gx + 50
    ids = []
    g = 52
    for r in rows:
        kind, w, title, subs, tone, chip = r
        if kind == "box":
            nid = f.box(cur, y, w, title, subs, tone=tone, chip=chip)
            cur += w + g
        else:
            cx = cur + w
            nid = f.diamond(cx, y + 46, w, 108, title, subs, chip=chip)
            cur = cx + w + g
        ids.append(nid)
    for i in range(len(ids) - 1):
        f.edge(ids[i], ids[i + 1], color="grey")
    return ids


def sec_modules():
    f = Fig(4060, 2320)
    # ---- 法币 ----
    ids = band(f, 60, 90, "法币模块 · 业务流（上游：USD → Bridge；EUR / GBP → OpenPayd）",
               "每个终端客户一个 VA · 靠 VA 号自动归因 · 到账时延按通道 T+0 ~ T+2 · 可退回",
               [("box", 300, "② 建主体：VA 账户", ["每终端客户一个 · 租户代其申请"], "default", "dev"),
                ("diamond", 190, "同一组合已存在？", ["租户+终端客户+币种 → 返回原 VA"], "gold", "sys"),
                ("box", 320, "通道路由 + 上游开户", ["按币种选通道，租户无感 · 异步返回"], "blue", "sys"),
                ("diamond", 180, "上游返回成功？", [], "gold", "sys"),
                ("box", 330, "账户 = 已创建 → 已激活", ["Webhook 通知 + 后台可查"], "green", "sys"),
                ("box", 350, "③ 入金：终端客户汇款入其专属 VA", ["凭 VA 号自动归因，无需附言"], "default", "end"),
                ("diamond", 180, "归因成功？", [], "gold", "sys"),
                ("box", 340, "记账 + 快照 + 通知 + 计费", ["挂到「租户 + 终端客户账户」"], "green", "sys"),
                ("box", 320, "④ 存量与变更", ["余额 / 明细 · 冻结 / 解冻 / 关闭"], "default", "biz"),
                ("box", 330, "⑤ 出金：租户发起指令", ["校验链 → 扣账 → 上游"], "default", "dev")])
    d1, d2, d3 = ids[1], ids[3], ids[6]
    a7, a10 = ids[7], ids[9]
    f.edge(d1, f.box(f.nodes[d1]["cx"] - 200, 90 + 395, 400, "直接返回原 VA（幂等）", ["重复请求不重复开户"], tone="green"), color="green", label="命中")
    f.edge(d2, f.box(f.nodes[d2]["cx"] - 200, 90 + 395, 400, "终态失败 + 告警", ["不产生可用账户"], tone="red"), color="red", label="失败")
    f.edge(d3, f.box(f.nodes[d3]["cx"] - 210, 90 + 395, 420, "挂账待处理（T+3）", ["超时原路退回并通知"], tone="red"), color="red", label="归因失败")
    f.edge(a10, f.box(f.nodes[a10]["cx"] - 230, 90 + 395, 460, "出金校验链", ["租户状态 / 模块生产 / 账户状态 / 余额 / 限额 / 风控", "任一不过 → 拒绝 + 原因码（不扣账）"], tone="grey"), color="grey")
    f.note(120, 730, "后果：上游超时 → 主动查询上游终态（禁止重复扣账）；上游失败 → 资金回冲 + 通知；冻结后不可出金，变更须通知租户。", SUB, 12, 3000)

    # ---- 加密 ----
    ids = band(f, 60, 820, "加密模块 · 业务流（上游：SafeHeron）",
               "每个终端客户一个地址 · 按区块确认数入账 · 链上不可逆 · 地址风险筛查是第二道闸门",
               [("box", 320, "② 建主体：充值地址", ["每终端客户一个 · 幂等键含链 / 币种"], "default", "dev"),
                ("diamond", 190, "同一组合已存在？", ["返回原地址"], "gold", "sys"),
                ("box", 320, "上游分配地址并绑定", ["租户 + 终端客户维度"], "purple", "up"),
                ("box", 340, "③ 链上充值：监听入账", ["记录「待确认」"], "default", "sys"),
                ("diamond", 175, "确认数达标？", [], "gold", "sys"),
                ("box", 330, "来源地址风险筛查", ["0–2 自动通过 · 3–5 转人工"], "gold", "sys"),
                ("diamond", 175, "人工判定拒收？", [], "gold", "ops"),
                ("box", 340, "记账 + 快照 + 通知 + 计费", ["链上不可逆：记账后不回冲"], "green", "sys"),
                ("box", 320, "④ 存量与变更", ["余额 / 地址 / 明细 · 归集对租户隐形"], "default", "biz"),
                ("box", 320, "⑤ 提现：租户发起", ["校验链 → 扣账 → 广播"], "default", "dev")])
    e2, e3, e5 = ids[4], ids[6], ids[9]
    f.edge(e2, f.box(f.nodes[e2]["cx"] - 200, 820 + 395, 400, "保持「待确认」", ["不入账、不通知成功"], tone="grey"), color="red", label="未达标")
    f.edge(e3, f.box(f.nodes[e3]["cx"] - 220, 820 + 395, 440, "入金拒结 → 原路退回", ["后台自动退款 + 通知租户"], tone="red"), color="red", label="拒收")
    xj = f.box(f.nodes[e5]["cx"] - 240, 820 + 395, 480, "提现校验链", ["余额 / 限额 / 目标地址风险筛查", "高风险 → 拦截 + 原因码"], tone="grey")
    yb = f.box(f.nodes[e5]["cx"] - 240, 820 + 530, 480, "通过后广播 → 已广播不可回冲", ["等链上确认；异常转人工兜底", "广播前失败可返还原额"], tone="red")
    f.edge(e5, xj, color="grey")
    f.edge(xj, yb, color="red")
    f.note(120, 1460, "后果：确认数不足期间不入账、不通知成功；3–5 转人工（暂定 24h），超时未处置视为拒收；记账后不可回冲。", SUB, 12, 3000)

    # ---- 卡片 ----
    ids = band(f, 60, 1550, "卡片模块 · 业务流（上游：Interlace）",
               "卡产品是项目级（平台与上游开通）· 每个终端客户一个持卡人 · 实时授权 + T+1 清算两段式",
               [("box", 340, "② 卡产品 / 项目", ["BIN · 卡种 · 币种（项目级）", "对租户 = 可用卡种"], "gold", "ops"),
                ("box", 320, "持卡人：每终端客户一个", ["提交持卡人资料"], "default", "dev"),
                ("diamond", 185, "卡片模块审核通过？", [], "gold", "ops"),
                ("box", 330, "开卡（虚拟 / 实体）", ["卡 = 未激活 → 激活后活跃"], "blue", "sys"),
                ("box", 350, "③ 卡账户充值", ["从法币账户余额内部划转", "（暂定：不引入独立充值通道）"], "default", "dev"),
                ("box", 300, "记账 + 快照 + 通知", [], "green", "sys"),
                ("box", 330, "④ 卡状态管理", ["激活 / 冻结 / 注销 · 冻结后不可消费"], "default", "biz"),
                ("box", 340, "⑤ 刷卡消费（两段式）", ["商户发起授权请求"], "default", "up"),
                ("diamond", 185, "余额/额度/商户类别通过？", [], "gold", "sys"),
                ("box", 330, "授权通过 + 占用额度", ["T+1 清算：扣实际金额、释放多余占用"], "green", "sys")])
    c1, c9, c10 = ids[2], ids[8], ids[9]
    f.edge(c1, f.box(f.nodes[c1]["cx"] - 190, 1550 + 395, 380, "不能开卡", ["先补齐卡片模块资质"], tone="red"), color="red", label="不通过")
    f.edge(c9, f.box(f.nodes[c9]["cx"] - 210, 1550 + 395, 420, "拒绝授权", ["宁可拒绝，不超卖 · 重试由商户侧发起"], tone="red"), color="red", label="不通过")
    f.edge(c10, f.box(f.nodes[c10]["cx"] - 230, 1550 + 530, 460, "退款 / 撤销 → 反向入账", ["释放或回补额度；授权超时 → 释放占用"], tone="teal"), color="teal")
    f.note(120, 2190, "后果：授权必须走独立链路、不得阻塞主流程；授权超时或上游不可用 → 拒绝（宁可拒绝不超卖）；退款 / 撤销 → 反向入账。", SUB, 12, 3000)
    return f


# ============================== 4. 状态与后果 ==============================
def sec_states():
    f = Fig(4060, 2700)
    f.region(60, 90, 3900, 470, "4.1 租户生命周期八阶段 —— 每个阶段「能做什么 / 不能做什么」",
             "阶段是租户级；「能否生产某个模块」是模块级 —— 所以「部分生产」是常态，不是过渡态")
    stages = [("① 已建立", "档案已录，未审核", "无 key，不能调用", "grey"),
              ("② 审核通过", "逐模块出结论", "无 key，不能调用", "grey"),
              ("③ 已签约", "合同生效", "可发受限 key", "gold"),
              ("④ 可联调", "受限 key + 限额 + 白名单", "可建载体、跑小额", "blue"),
              ("⑤ 部分生产", "某模块已解除限额", "该模块正常；其余仍受限", "green"),
              ("⑥ 全部生产", "所有已授权模块生产中", "全部生产", "green"),
              ("⑦ 暂停", "停止新交易", "存量可查可退回，不可新建", "red"),
              ("⑧ 终止", "关系结束", "只读 + 存量处置（30 天）", "red")]
    x = 110; sid = []
    for t, s1, s2, tone in stages:
        sid.append(f.box(x, 210, 440, t, [s1, s2], tone=tone, min_h=110)); x += 490
    for i in range(len(sid) - 1):
        f.edge(sid[i], sid[i + 1], color="grey")
    f.note(120, 390, "关键约束：③ 合同未生效 → 永远拿不到生产权限（闸门硬条件）；⑤ 是常态，一个模块没过不影响其他模块；⑦⑧ 的存量处置口径见 D3。", SUB, 12, 3700)

    f.region(60, 590, 1900, 440, "4.2 载体状态机（每个终端客户一套）", "状态变化的后果：能不能收、能不能付")
    v1 = f.box(110, 700, 340, "已创建", ["可查看，尚不能收付"], tone="grey")
    v2 = f.box(490, 700, 340, "已激活", ["可收可付（正常态）"], tone="green")
    v3 = f.box(870, 700, 340, "已冻结", ["不可出金 / 不可消费", "存量仍可见、可退回"], tone="red")
    v4 = f.box(1250, 700, 340, "已关闭", ["只读；不再产生新交易"], tone="grey")
    f.edge(v1, v2, color="green", label="上游开户成功")
    f.edge(v2, v3, color="red", label="平台冻结")
    f.edge(v3, v2, fs_="t", ts_="t", color="green", label="解冻", lx=1040, ly=660)
    f.edge(v3, v4, color="grey", label="关闭")
    f.note(120, 900, "加密侧地址同构（每终端客户一个）。卡片侧主体是持卡人，其下可挂多张卡：未激活 → 活跃 → 冻结 → 注销。", SUB, 12, 1780)

    f.region(1990, 590, 1970, 440, "4.3 交易状态（按模块）—— 每种状态的后果", "资金去向 · 能否重试 · 是否通知 · 是否计费")
    f.box(2030, 700, 450, "法币 · 入金",
          ["成功 → 入账并计费", "挂账待处理 → 不进余额，T+3 超时退回", "已退回 → 原路退回并通知"], min_h=160)
    f.box(2500, 700, 450, "法币 · 出金",
          ["处理中 → 已扣账，不可重复发起", "成功 → 扣账完成", "失败 → 资金回冲 + 通知"], min_h=160)
    f.box(2970, 700, 450, "加密 · 充值 / 提现",
          ["待确认 → 不入账、不通知成功", "已记账 → 不可逆，不回冲", "拒收退回 → 原路退回", "提现失败 → 广播前可返还原额"], min_h=160)
    f.box(3440, 700, 480, "卡片 · 消费",
          ["授权通过 → 占用额度，T+1 清算", "授权拒绝 → 不占额度，商户可重试", "已清算 → 扣实际金额、释放占用", "已退款 → 反向入账"], min_h=160)

    f.region(60, 1060, 3900, 420, "4.4 风控判定：分值决定后果（加密模块，入金查来源、出金查目标）", "同一个判定点，不同分值的后果完全不同")
    f.box(110, 1190, 900, "风险等级 0–2 → 自动通过",
          ["入账：记账 + 快照 + 通知 + 计费", "资金去向：进入该终端客户账户余额", "通知：Webhook 推送租户"], tone="green", min_h=160)
    f.box(1050, 1190, 900, "风险等级 3–5 → 转人工（24h 时限）",
          ["人工放行 → 与 0–2 同路径入账", "超时未处置 → 视为拒收，原路退回", "通知：先推「待确认」，判定后推终态"], tone="gold", min_h=160)
    f.box(1990, 1190, 900, "判定拒收 → 入金拒结 + 原路退回",
          ["资金去向：不进余额，后台自动退款", "租户后果：该笔不计费、不产生余额", "通知：Webhook 推送「拒收退回」"], tone="red", min_h=160)
    f.box(2930, 1190, 990, "提现目标地址高风险",
          ["拦截：拒绝并返回原因码", "资金去向：不扣账、不广播", "后果：租户可换地址重新发起"], tone="red", min_h=160)

    f.region(60, 1510, 3900, 420, "4.5 三个「不可逆点」—— 最容易出事的后果", "一旦越过，平台无法自动回退，只能人工介入")
    f.box(110, 1640, 1240, "① 加密充值已记账",
          ["链上不可逆：记账后不回冲", "若判错，只能人工处理，不能靠系统冲正"], tone="red", min_h=160)
    f.box(1390, 1640, 1240, "② 加密提现已广播",
          ["链上广播后无法撤回", "只能等确认结果，异常转人工兜底"], tone="red", min_h=160)
    f.box(2670, 1640, 1290, "③ 卡片授权已通过",
          ["已占用额度，商户随后清算", "撤销只能走退款反向入账"], tone="gold", min_h=160)
    f.note(120, 1840, "结论：出金类动作必须「先校验、后扣账」，把不可逆动作放在最后一步；加密模块的不可逆性决定它必须比法币更重的风控前置。", SUB, 12, 3700)

    f.region(60, 1960, 3900, 1010, "4.6 通知矩阵 —— 哪些事件必须通知租户，以及在哪三处可见", "Webhook / 租户自助后台 / 平台运营台")
    y = 2060
    for cat, ev, w, b, o in NOTIFY_ROWS:
        f.box(110, y, 1050, cat, [ev], tone="default", min_h=56, fs=12, sub_fs=10.5)
        f.box(1200, y, 620, "推送 ✓" if w == "✓" else "—", [], tone="green" if w == "✓" else "grey", min_h=56, fs=12)
        f.box(1860, y, 620, "可见 ✓" if b == "✓" else "—", [], tone="green" if b == "✓" else "grey", min_h=56, fs=12)
        f.box(2520, y, 620, "可见 ✓" if o == "✓" else "—", [], tone="green" if o == "✓" else "grey", min_h=56, fs=12)
        y += 86
    return f


# ============================== 5. 异常分流 ==============================
def sec_exceptions():
    f = Fig(3000, 1800)
    f.note(90, 130, "5. 异常与兜底分流 —— 共 19 条：触因 → 处置 → 后果（谁做 / 资金去哪 / 有没有时限）。一期「半自动」代表需要人工点一下，不是纯自动。", TXT, 13, 2800)

    groups = [
        (110, 200, "A 组 · 准入与联调类", [
            ("资质驳回 / 需补件", "回到建档或补材料，不进联调", "该模块停止，不影响其他模块", "ops", "red"),
            ("联调不通过", "停在联调态，系统硬拦，禁止切生产", "不消耗生产权限与额度", "sys", "red"),
            ("合同未生效", "不得发放生产权限", "闸门自动拦截，补齐后重试", "sys", "gold"),
            ("受限环境额度耗尽", "拦截并提示租户走「切生产」流程", "避免受限环境被当生产用", "sys", "grey"),
        ]),
        (1540, 200, "B 组 · 入金类", [
            ("入金金额不符 / 来源不明", "挂账待处理（T+3）", "不进余额；超时原路退回", "ops", "gold"),
            ("入金被上游退回", "原路退回 + 通知租户", "该笔不计费", "sys", "red"),
            ("加密入金确认数不足", "保持「待确认」", "不入账、不通知成功", "sys", "grey"),
            ("加密来源地址 3–5", "转人工（24h）；判拒收则入金拒结", "原路退回，后台自动退款", "ops", "gold"),
            ("加密提现目标地址高风险", "拦截，拒绝并给原因码", "不扣账、不广播", "sys", "red"),
        ]),
        (110, 1010, "C 组 · 出金与卡片类", [
            ("出金校验不过（余额/限额/风控）", "拒绝并返回原因码", "不扣账，租户可调整后重试", "sys", "red"),
            ("出金上游超时", "主动查询上游终态后再定终态", "避免双重扣账", "sys", "gold"),
            ("出金上游失败", "资金回冲 + 通知租户", "余额恢复原状", "sys", "red"),
            ("加密提现已广播", "不可回冲，等链上结果", "异常转人工兜底", "ops", "red"),
            ("卡片授权超时 / 上游不可用", "拒绝授权（宁可拒绝不超卖）", "重试由商户侧发起", "sys", "red"),
        ]),
        (1540, 1010, "D 组 · 系统与运营类", [
            ("卡片退款 / 撤销", "反向入账，释放或回补额度", "额度恢复，通知租户", "sys", "green"),
            ("账户 / 卡冻结、解冻", "平台侧操作", "冻结后不可出金 / 不可消费", "ops", "gold"),
            ("Webhook 投递失败", "重试 → 最终失败告警", "租户可主动补偿查询", "sys", "grey"),
            ("租户暂停 / 终止", "暂停停新交易；终止按 D3 处置存量", "存量 30 天内清零", "ops", "red"),
            ("上游通道异常", "重试 / 降级 / 告警", "租户侧状态可见，不暴露通道", "sys", "purple"),
        ]),
    ]
    for gx, gy, gtitle, rows in groups:
        gh = 90 + len(rows) * 108
        f.region(gx, gy, 1350, gh, gtitle, "")
        yy = gy + 70
        for trig, act, cons, chip, tone in rows:
            t = f.box(gx + 24, yy, 560, trig, [], tone="default", min_h=64, chip=chip, fs=12)
            a = f.box(gx + 640, yy, 690, act, [cons], tone=tone, min_h=64, fs=12, sub_fs=10.5)
            f.edge(t, a, color=tone)
            yy += 108
    return f


NOTIFY_ROWS = [
    ("租户自身", "审核结果（按模块）/ 联调环境开通 / 生产启用（按模块）/ 暂停 / 终止", "✓", "✓", "✓"),
    ("密钥", "轮换 · 吊销", "✓", "✓", "✓"),
    ("法币 · 账户", "已创建 / 已激活 / 已冻结 / 已关闭", "✓", "✓", "—"),
    ("法币 · 入金", "成功 / 失败 / 已退回 / 挂账", "✓", "✓", "✓"),
    ("法币 · 出金", "处理中 / 成功 / 失败", "✓", "✓", "—"),
    ("加密 · 充值", "待确认 / 已到账 / 拒收退回", "✓", "✓", "✓"),
    ("加密 · 提现", "处理中 / 成功 / 失败", "✓", "✓", "—"),
    ("卡片 · 卡", "已开卡 / 已激活 / 已冻结 / 已注销", "✓", "✓", "—"),
    ("卡片 · 充值", "成功", "✓", "✓", "—"),
    ("卡片 · 消费", "授权结果 / 已清算 / 已退款", "✓", "✓", "—"),
    ("结算", "结算单生成 / 扣款结果", "✓", "✓", "✓"),
]


def notify_table():
    rows = []
    for cat, ev, w, b, o in NOTIFY_ROWS:
        rows.append("<tr><td class='cat'>%s</td><td>%s</td><td class='c'>%s</td>"
                    "<td class='c'>%s</td><td class='c'>%s</td></tr>"
                    % (esc(cat), esc(ev), w, b, o))
    return ("<table class='grid'><thead><tr><th>类别</th><th>事件</th>"
            "<th>Webhook（推给租户系统）</th><th>租户自助后台（给人看）</th><th>平台运营台（给我方看）</th>"
            "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>")


def frame(svg, w, h, fid):
    return ("<div class='frame' id='%s' style='height:%dpx'><div class='inner' style='width:%dpx'>%s</div></div>"
            % (fid, h, w, svg))


def main():
    figs = [sec_boundary(), sec_master(), sec_modules(), sec_states(), sec_exceptions()]
    svgs = [x.svg() for x in figs]
    frames = [frame(svgs[i], figs[i].W, figs[i].H, "f%d" % (i + 1)) for i in range(len(figs))]

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>白标系统 · 一期业务全景流程图</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#0B0E14; color:#E8ECF0; font-family:Inter,-apple-system,'Segoe UI',sans-serif; padding-bottom:90px; }
  header { padding:22px 26px 14px; border-bottom:1px solid rgba(255,255,255,.08); }
  h1 { font-size:20px; font-weight:700; }
  h1 span { color:#E59303; }
  .meta { color:#7B8CA8; font-size:12px; margin-top:6px; line-height:1.75; }
  .meta b { color:#B0C0D8; }
  .toc { margin-top:12px; display:flex; flex-wrap:wrap; gap:8px; }
  .toc a { color:#B0C0D8; font-size:12px; text-decoration:none; padding:5px 11px; border-radius:14px;
           border:1px solid rgba(255,255,255,.12); background:rgba(255,255,255,.03); }
  .toc a:hover { border-color:#E59303; color:#E59303; }
  main { padding:0 20px; }
  section { margin-top:26px; }
  h2 { font-size:15px; font-weight:700; margin:0 0 10px 6px; }
  h2 em { font-style:normal; color:#7B8CA8; font-weight:400; font-size:12px; margin-left:8px; }
  .frame { overflow:auto; border:1px solid rgba(255,255,255,.08); border-radius:12px; background:#131820; }
  .inner { transform-origin:0 0; }
  .grid { width:100%; border-collapse:collapse; font-size:12.5px; }
  .grid th, .grid td { border:1px solid rgba(255,255,255,.08); padding:9px 12px; text-align:left; }
  .grid th { background:rgba(229,147,3,.08); color:#E59303; font-size:12px; font-weight:600; }
  .grid tr:nth-child(even) td { background:rgba(255,255,255,.02); }
  .grid td.cat { color:#B0C0D8; font-weight:600; white-space:nowrap; }
  .grid td.c { text-align:center; color:#22C55E; font-weight:700; }
  .pmnote { background:rgba(229,147,3,.07); border-left:3px solid #E59303; border-radius:8px;
            padding:12px 16px; margin:10px 0; font-size:12.5px; line-height:1.85; }
  .pmnote b { color:#E59303; }
  body.hidden .pmnote { display:none; }
  .bar { position:fixed; right:18px; bottom:18px; z-index:99; display:flex; gap:6px;
         background:rgba(19,24,32,.94); border:1px solid rgba(255,255,255,.12); border-radius:10px;
         padding:7px 9px; }
  .bar button { background:transparent; border:none; color:#B0C0D8; font-size:13px; padding:5px 10px;
                border-radius:6px; cursor:pointer; font-family:inherit; }
  .bar button:hover { background:rgba(255,255,255,.08); color:#E59303; }
</style>
</head>
<body>
<header>
  <h1>白标系统 · <span>一期业务全景流程图</span></h1>
  <div class="meta">
    依据 <b>《白标系统 · 一期业务流程》v1.0（业务流程定稿）</b> · 2026-10-12 · 客户类型：同行平台（要底层能力，自己再叠一层产品）<br>
    主轴：<b>接入闭环</b>（租户接入才是系统主线）· 业务范围：<b>法币 / 加密 / 卡片</b> 三模块 · 手段：<b>人工接客，自动跑数</b>
  </div>
  <div class="toc">
    <a href="#s1">1 关系与角色</a>
    <a href="#s2">2 接入闭环主图</a>
    <a href="#s3">3 三模块业务流</a>
    <a href="#s4">4 状态与后果</a>
    <a href="#s5">5 异常与兜底分流</a>
    <a href="#s6">6 通知矩阵</a>
  </div>
</header>
<main>
  <section id="s1">
    <h2>1 · 关系与角色 <em>三层关系 · 六类角色 · 明确不出现的角色</em></h2>
    __F1__
  </section>
  <section id="s2">
    <h2>2 · 接入闭环主图 <em>建档 → 分模块审核 → 签约 → 开通联调 → 联调 → 切生产 → 运行，含全部分支后果</em></h2>
    __F2__
  </section>
  <section id="s3">
    <h2>3 · 三模块业务流 <em>法币 / 加密 / 卡片：建主体 → 价值进入 → 存量变更 → 价值出去</em></h2>
    __F3__
  </section>
  <section id="s4">
    <h2>4 · 状态与后果 <em>租户八阶段 · 载体状态机 · 交易状态 · 风控分级后果 · 三个不可逆点 · 通知矩阵</em></h2>
    __F4__
  </section>
  <section id="s5">
    <h2>5 · 异常与兜底分流 <em>19 条：触因 → 处置 → 后果（谁做 / 资金去哪 / 有无时限）</em></h2>
    __F5__
  </section>
  <section id="s6">
    <h2>6 · 通知矩阵（明细表） <em>哪些事件必须通知租户，以及在哪三处可见</em></h2>
    __TABLE__
  </section>

  <div class="pmnote"><b>PM 备注</b> 本图对应业务流程稿 v1.0；流程中 12 个待确认项已给出暂定口径。以下几条直接影响画法，等你确认：</div>
  <div class="pmnote"><b>PM 备注</b> D6 卡账户资金来源 —— 暂按「从法币账户余额内部划转」画；若走独立充值通道，第 3 节卡片模块的「③ 卡账户充值」整段要重画。</div>
  <div class="pmnote"><b>PM 备注</b> D8 币兑（BitGo）位次 —— 暂按「未来第四个独立模块」处理，所以本图只画三个模块；若它是法币模块下的一个动作，法币模块要加一条支线。</div>
  <div class="pmnote"><b>PM 备注</b> D11 加密侧主体粒度 —— 暂按「与法币同构，每个终端客户一个地址」画；若改用租户级地址池 + 子地址，加密模块的建主体与入金归因都要改。</div>
  <div class="pmnote"><b>PM 备注</b> D12 沙盒替代 —— 本图按「受限环境（限额 + 白名单）」画，没有沙盒环境切换这一段。</div>
</main>

<div class="bar">
  <button id="zo">−</button><button id="zr">100%</button><button id="zi">+</button>
  <button id="zf">适应宽度</button><button id="hp">隐藏备注</button>
</div>
<script>
(function(){
  var frames = [].slice.call(document.querySelectorAll('.frame'));
  frames.forEach(function(fr){
    var inner = fr.querySelector('.inner');
    fr.dataset.w = inner.style.width.replace('px','');
    fr.dataset.h = fr.style.height.replace('px','');
  });
  function apply(fr, z){
    var inner = fr.querySelector('.inner');
    var h = parseFloat(fr.dataset.h);
    inner.style.transform = 'scale(' + z + ')';
    fr.style.height = (h * z) + 'px';
    fr.dataset.zoom = z;
  }
  document.getElementById('zi').onclick = function(){
    frames.forEach(function(fr){ apply(fr, Math.min(2, parseFloat(fr.dataset.zoom || 1) * 1.25)); });
  };
  document.getElementById('zo').onclick = function(){
    frames.forEach(function(fr){ apply(fr, Math.max(0.1, parseFloat(fr.dataset.zoom || 1) / 1.25)); });
  };
  document.getElementById('zr').onclick = function(){ frames.forEach(function(fr){ apply(fr, 1); }); };
  document.getElementById('zf').onclick = function(){
    frames.forEach(function(fr){
      var w = parseFloat(fr.dataset.w);
      apply(fr, Math.min(1, fr.clientWidth / w));
    });
  };
  document.getElementById('hp').onclick = function(){
    document.body.classList.toggle('hidden');
    this.textContent = document.body.classList.contains('hidden') ? '显示备注' : '隐藏备注';
  };
  frames.forEach(function(fr){ apply(fr, 1); });
})();
</script>
</body>
</html>
"""
    html = (html.replace("__F1__", frames[0]).replace("__F2__", frames[1])
            .replace("__F3__", frames[2]).replace("__F4__", frames[3])
            .replace("__F5__", frames[4]).replace("__TABLE__", notify_table()))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print("OK ->", OUT)
    print("bytes:", os.path.getsize(OUT))
    for i, s in enumerate(figs, 1):
        print("  fig%d: %dx%d nodes=%d" % (i, s.W, s.H, len(s.nodes)))


if __name__ == "__main__":
    main()
