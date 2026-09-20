#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YASBe 原型登记「三闸」校验器 —— 每轮 push 前跑一次。

  闸 1 · 命名规范    prototypes/ 下的【新增】原型/PRD 文件名是否合规
  闸 2 · 登记覆盖    全仓可发布 .html/.md 与 PROTOTYPE-LINKS.md 登记条目的差集
                    （扣除 tools/registry_baseline.txt 里的已知欠账）
  闸 3 · 一致性      登记表行尾 / 死链 / 未部署登记 / 工作区误删
                    / 线上字节数 == 本地字节数（--online）

用法
  python tools/check_registry.py                   本地三闸（不联网）
  python tools/check_registry.py --online          追加线上比对（约 20 秒）
  python tools/check_registry.py --write-baseline  把当前差集写成已知欠账基线
  python tools/check_registry.py --quiet           只打印结论行

退出码
  0 = 全通过（可 push）   1 = 有阻塞项（不可 push）

规范原文见 prototypes/README.md。
"""

import argparse
import contextlib
import io
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote, quote

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SITE = "https://xieyi0734-art.github.io/yasbe-prototypes/"
REPO = Path(__file__).resolve().parent.parent
REGISTRY = REPO / "PROTOTYPE-LINKS.md"
BASELINE = REPO / "tools" / "registry_baseline.txt"
NAV_PAGES = ["index.html", "admin/prototypes/index.html"]

EXCLUDE_DIRS = {
    ".git", "node_modules", "scripts", "tools", "diagrams", "docs", "mesh_docs",
    "_bridge_research", "_op_research", "_archive", "archive", "_smoke", "_build",
    "cyro-website", "card-prototypes",          # .gitignore 内，从未部署
}
EXCLUDE_FILES = {
    "PROTOTYPE-LINKS.md", "prototypes/README.md", "原型链接.txt",
    ".gitignore", "README.md",
}
SKIP_NAME_MARKERS = (".bak", ".zip", "_text.txt", "存档", "旧版", ".txt", ".xlsx", ".json")
RETIRED_HINTS = ("失效", "未部署", "废弃")

END_SIDES = ("管理端", "客户端", "B端", "代币官网", "白标门户")
NAME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}_.+_(?:" + "|".join(END_SIDES) + r")(?:_v[\d.]+)?\.(?:html|md)$"
)

problems, warns = [], []


def rel(p: Path) -> str:
    return p.relative_to(REPO).as_posix()


def git(*args):
    p = subprocess.run(["git", "-c", "core.quotepath=false", *args],
                       cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8", "replace").strip())
    out = p.stdout.decode("utf-8", "replace")
    return [x for x in out.split("\0") if x]


def scan_files():
    pages, docs = set(), set()
    for p in REPO.rglob("*"):
        if not p.is_file():
            continue
        r = rel(p)
        if any(d in EXCLUDE_DIRS for d in r.split("/")[:-1]):
            continue
        if r in EXCLUDE_FILES or any(m in p.name for m in SKIP_NAME_MARKERS):
            continue
        if p.suffix == ".html":
            pages.add(r)
        elif p.suffix == ".md":
            docs.add(r)
    return pages, docs


def parse_registry():
    """逐行解析，记录每条登记所属的小节标题（用于识别 §14 失效/未部署清单）。"""
    text = REGISTRY.read_text(encoding="utf-8")
    entries, heading = [], ""
    for lineno, line in enumerate(text.splitlines(), 1):
        ls = line.strip()
        if ls.startswith("#"):
            heading = ls.lstrip("#").strip()
            continue
        m = re.search(r"\[([^\]]+)\]\(" + re.escape(SITE) + r"([^)\s]+)\)", line)
        if not m:
            continue
        tail = m.group(2)
        rp = unquote(tail).rstrip("/")
        entries.append({
            "label": m.group(1), "url": SITE + tail, "rp": rp, "line": lineno,
            "heading": heading,
            "template": ("相对路径" in rp or rp.endswith("文件名.html") or "<" in rp),
            "retired": any(k in heading for k in RETIRED_HINTS),
        })
    return entries, text


def load_baseline():
    if not BASELINE.exists():
        return None
    return {l.strip() for l in BASELINE.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")}


def gate1_naming():
    print("\n【闸 1 · 命名规范】")
    try:
        # 必须 -z：否则多行输出会被当成单条记录，闸1 静默失效
        untracked = {x.replace("\\", "/") for x in git("ls-files", "--others", "--exclude-standard", "-z")}
    except Exception as e:
        warns.append(f"闸1 跳过：git 不可用（{e}）")
        print(f"  ! git 不可用：{e}")
        return
    base = load_baseline() or set()
    cand = sorted(f for f in untracked
                  if f.startswith("prototypes/") and Path(f).suffix in (".html", ".md")
                  and f not in EXCLUDE_FILES and not any(m in f for m in SKIP_NAME_MARKERS))
    bad = [f for f in cand if not NAME_RE.match(Path(f).name) and f not in base]
    if not cand:
        print("  无新增文件，跳过。")
    elif not bad:
        print(f"  PASS — 新增 {len(cand)} 个文件全部合规。")
    else:
        print(f"  FAIL — {len(bad)}/{len(cand)} 个新增文件命名不合规：")
        for f in bad:
            print(f"    ✗ {f}")
        problems.append(f"闸1：{len(bad)} 个新增文件命名不合规")

    legacy = []
    for p in (REPO / "prototypes").rglob("*"):
        if not p.is_file() or p.suffix not in (".html", ".md"):
            continue
        r = rel(p)
        if r in EXCLUDE_FILES or any(m in p.name for m in SKIP_NAME_MARKERS) or r in base:
            continue
        if not NAME_RE.match(p.name):
            legacy.append(r)
    print(f"  （存量不合规 {len(legacy)} 个 —— 按「存量不迁移」不阻塞）")


def gate2_coverage(pages, docs, registered, write_baseline=False):
    print("\n【闸 2 · 登记覆盖】")
    unreg_pages = sorted(pages - registered)
    unreg_docs = sorted(docs - registered)
    if write_baseline:
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        lines = ["# 已知漏登欠账基线（tools/check_registry.py --write-baseline 生成）",
                 "# 每补登记一个就删一行；本文件内条目不阻塞 push。"]
        lines += unreg_pages + unreg_docs
        # 显式 newline="\n"：Windows 上 write_text 默认会把 \n 翻成 \r\n
        BASELINE.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        shown = BASELINE.relative_to(REPO).as_posix() if REPO in BASELINE.parents else str(BASELINE)
        print(f"  已写入 {shown}：页面 {len(unreg_pages)} + 文档 {len(unreg_docs)}")
        return
    base = load_baseline()
    allunreg = set(unreg_pages) | set(unreg_docs)
    print(f"  可发布页面 {len(pages)} / 文档 {len(docs)}；登记条目 {len(registered)}")
    if base is None:
        print(f"  未登记：页面 {len(unreg_pages)} / 文档 {len(unreg_docs)}（尚无基线，跑 --write-baseline 固化）")
        for r in unreg_pages + unreg_docs:
            print(f"    · {r}")
        warns.append(f"闸2：尚无基线，当前未登记 {len(allunreg)} 个")
        return
    known, new = allunreg & base, sorted(allunreg - base)
    print(f"  已知欠账（基线内，不阻塞）：{len(known)}")
    if new:
        print(f"  FAIL — 新增漏登 {len(new)} 个：")
        for r in new:
            print(f"    ✗ {r}")
        problems.append(f"闸2：新增漏登 {len(new)} 个")
    else:
        print("  PASS — 无新增漏登。")


def check_online(entries):
    def one(e):
        import urllib.request
        # 登记表里的中文路径可能是裸中文，必须重新逐段百分号编码再请求
        req = urllib.request.Request(SITE + quote(e["rp"]),
                                     headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                return e, resp.status, len(resp.read())
        except Exception as ex:
            code = getattr(ex, "code", None)
            return e, code or 0, 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        return list(ex.map(one, entries))


def gate3_consistency(entries, registered, online=False):
    print("\n【闸 3 · 一致性】")
    raw = REGISTRY.read_bytes()
    crlf, lf = raw.count(b"\r\n"), raw.count(b"\n")
    eol = "CRLF" if crlf and crlf == lf else ("LF" if not crlf else "MIXED")
    print(f"  登记表 {len(raw)} B / {lf} 行 / 行尾 {eol}")
    if eol == "MIXED":
        problems.append("闸3：登记表行尾混用（CRLF+LF）")
        print("    ✗ 行尾混用")

    try:
        head = set(git("ls-tree", "-r", "--name-only", "-z", "HEAD"))
        deleted = [x[3:] for x in git("status", "--porcelain", "-z")
                   if len(x) > 3 and x[:2] in (" D", "D ")]
    except Exception as e:
        head, deleted = set(), []
        warns.append(f"闸3 跳过 git 核对：{e}")

    real = [e for e in entries if not e["template"]]
    dead = [e for e in real if not (REPO / e["rp"]).exists() and not e["retired"]]
    deployed_missing = [e for e in real if not e["retired"] and e["rp"] not in head]
    if dead:
        print(f"  FAIL — 登记条目指向本地不存在的文件 {len(dead)} 条：")
        for e in dead:
            print(f"    ✗ L{e['line']} {e['rp']}")
        problems.append(f"闸3：{len(dead)} 条登记为死链")
    else:
        print("  死链 0 条（§14 失效清单内的失效条目不计数）")
    if deployed_missing:
        print(f"  FAIL — 已登记但 git 未部署（线上必 404）{len(deployed_missing)} 条：")
        for e in deployed_missing[:20]:
            print(f"    ✗ L{e['line']} {e['rp']}")
        problems.append(f"闸3：{len(deployed_missing)} 条已登记但未部署")
    if deleted:
        print(f"  FAIL — 工作区已删、HEAD 仍在（下次误提交会让线上链接失效）{len(deleted)} 条：")
        for d in deleted:
            print(f"    ✗ {d}")
        problems.append(f"闸3：{len(deleted)} 个文件工作区已删但 HEAD 仍在")

    mods = {}
    for r in registered:
        d = str(Path(r).parent).replace("\\", "/")
        if d in (".", "prototypes") or any(x in EXCLUDE_DIRS for x in d.split("/")):
            continue          # 根级文件 / 研究资料，导航页本就不该挂
        mods.setdefault(d, set()).add(r)
    if mods:
        dated = {}
        for m, fs in mods.items():
            ds = sorted(f for f in fs if re.match(r"\d{4}-\d{2}-\d{2}", Path(f).name))
            dated[m] = Path(ds[-1]).name[:10] if ds else "—"
    for nav in NAV_PAGES:
        np = REPO / nav
        if not np.exists():
            print(f"  ! 导航页缺失：{nav}")
            problems.append(f"闸3：导航页缺失 {nav}")
            continue
        base, hrefs = np.parent, set()
        for h in re.findall(r'href="([^"]+)"', np.read_text(encoding="utf-8", errors="replace")):
            if h.startswith(("http", "#", "mailto:", "javascript:")):
                continue
            try:
                hrefs.add(rel((base / unquote(h.split("#")[0].split("?")[0])).resolve()))
            except Exception:
                pass
        miss = sorted((m for m, fs in mods.items() if not (fs & hrefs)),
                      key=lambda m: dated.get(m, ""), reverse=True)
        print(f"  {nav}：href {len(hrefs)} 个，未覆盖目录 {len(miss)}/{len(mods)}")
        for m in miss[:12]:
            print(f"    · ({dated.get(m,'—')}) {m}/")
        if len(miss) > 12:
            print(f"    … 另有 {len(miss) - 12} 个")
        if miss:
            warns.append(f"闸3：{nav} 未覆盖 {len(miss)} 个目录")

    if not online:
        print("  （线上比对跳过，加 --online 启用）")
        return
    print(f"  线上比对 {len(real)} 条 …")
    res = check_online(real)
    ok = mism = err = 0
    live_not_local = []
    for e, code, size in res:
        if code != 200:
            err += 1
            if not e["retired"]:
                print(f"    ✗ HTTP {code}  {e['rp']}")
        else:
            local = REPO / e["rp"]
            if not local.exists():
                live_not_local.append(e["rp"])
                ok += 1
            else:
                lb = len(local.read_bytes().replace(b"\r\n", b"\n"))   # 线上为 LF 版
                if size == lb:
                    ok += 1
                else:
                    mism += 1
                    print(f"    ✗ 字节不符 {e['rp']}  线上 {size} 本地(归一) {lb}")
    print(f"  线上：一致 {ok} / 字节不符 {mism} / 非 200 {err}"
          f" / 线上在·本地已删 {len(live_not_local)}")
    for r in live_not_local:
        print(f"    ! 线上仍在但本地已删：{r}")
    if mism:
        problems.append(f"闸3：{mism} 条线上字节数与本地不符")
    if err:
        warns.append(f"闸3：{err} 条线上非 200（若确为退役，请移入 §14 失效清单）")


def run(a):
    print("=" * 62)
    print("YASBe 原型登记三闸校验")
    print("=" * 62)
    entries, _ = parse_registry()
    pages, docs = scan_files()
    registered = {e["rp"] for e in entries if not e["template"]}
    print(f"登记条目 {len(entries)} 条（模板占位 {len(entries)-len(registered)} 已忽略）"
          f" / 扫描页面 {len(pages)} / 文档 {len(docs)}")
    gate1_naming()
    gate2_coverage(pages, docs, registered, a.write_baseline)
    if not a.write_baseline:
        gate3_consistency(entries, registered, a.online)
    print("\n" + "=" * 62)
    if problems:
        print(f"结论：FAIL — {len(problems)} 类阻塞项")
        for p in problems:
            print(f"  ✗ {p}")
    else:
        print("结论：PASS — 可 push")
    for w in warns:
        print(f"  ! {w}")
    print("=" * 62)
    sys.exit(0 if not problems else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--online", action="store_true", help="追加线上比对")
    ap.add_argument("--write-baseline", action="store_true", help="把当前差集写成已知欠账基线")
    ap.add_argument("--quiet", action="store_true", help="只打印结论行")
    a = ap.parse_args()
    if a.quiet:
        buf, code = io.StringIO(), 0
        try:
            with contextlib.redirect_stdout(buf):
                run(a)
        except SystemExit as e:                    # run() 用 sys.exit 表结论，必须透传
            code = e.code if isinstance(e.code, int) else 1
        lines = buf.getvalue().splitlines()
        concl = [l for l in lines if l.startswith("结论：")]
        print(concl[0] if concl else (lines[-1] if lines else "（无输出）"))
        sys.exit(code)
    else:
        run(a)


if __name__ == "__main__":
    main()
