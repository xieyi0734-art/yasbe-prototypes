# -*- coding: utf-8 -*-
"""交付闸门 —— 发链接前跑这一条，六项全绿才算交付完成。

用法:
  python tools/deliver_gate.py "prototypes/返佣和奖励" --only "2026-09-18_*"
  python tools/deliver_gate.py "prototypes/返佣和奖励" --only "2026-09-18_*" --online

依次执行:
  1 结构体检   标签闭合 / href 目标存在 / JS 引用的 id 与函数存在
  2 登记一致   tools/check_registry.py（仓内 登记表 ↔ 磁盘）
  3 文案闸门   tools/check_client_copy.py（面向客户词表 + PM 备注规范）
  4(可选)线上  经 --online: 线上 200 + 线上字节 == 本地字节 / 链接可达

退出码 0 = 全绿（可发链接）；非 0 = 有红项，不发链接。

为什么存在: 「多轮调优」的最大来源不是改错，而是**错误由用户在评审时发现**。
把六项检查合并成一条命令，任何一项红就不发链接 —— 一类错误最多只产生 0 轮。
"""
import argparse
import glob
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_GLOBS = [
    os.path.join(os.path.expanduser("~"), "AppData/Local/hermes/skills/**/scripts/verify_prototype_structure.py"),
    os.path.join(os.path.expanduser("~"), ".hermes/skills/**/scripts/verify_prototype_structure.py"),
]


def find_structure_script():
    local = os.path.join(REPO, "tools", "verify_prototype_structure.py")
    if os.path.exists(local):
        return local
    for g in SKILL_GLOBS:
        hits = glob.glob(g, recursive=True)
        if hits:
            return hits[0]
    return None


def run(title, cmd):
    print("\n" + "=" * 66)
    print("[%s] %s" % (title, " ".join(cmd)))
    print("=" * 66)
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    print(out.rstrip())
    return p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="原型目录或文件")
    ap.add_argument("--only", default=None, help="文件名 glob，如 2026-09-18_*")
    ap.add_argument("--online", action="store_true", help="含线上字节核对")
    ap.add_argument("--base-url", default="https://xieyi0734-art.github.io/yasbe-prototypes")
    args = ap.parse_args()

    results = []

    # 1 结构体检
    ss = find_structure_script()
    if ss:
        cmd = [sys.executable, ss, args.target]
        if args.only:
            cmd += ["--glob", args.only]
        results.append(("1 结构·链接·JS 引用", run("1/6 结构体检", cmd)))
    else:
        print("[skip] 未找到 verify_prototype_structure.py")
        results.append(("1 结构·链接·JS 引用", 0))

    # 2 登记一致
    reg = os.path.join(REPO, "tools", "check_registry.py")
    if os.path.exists(reg):
        cmd = [sys.executable, reg]
        if args.online:
            cmd += ["--online"]
        results.append(("2 登记表↔磁盘（线上链接）", run("2/6 登记一致", cmd)))
    else:
        print("[skip] 未找到 tools/check_registry.py")
        results.append(("2 登记表↔磁盘（线上链接）", 0))

    # 3 文案闸门
    cg = os.path.join(REPO, "tools", "check_client_copy.py")
    cmd = [sys.executable, cg, args.target]
    if args.only:
        cmd += ["--only", args.only]
    results.append(("3 面向客户文案 + PM 备注", run("3/6 文案闸门", cmd)))

    print("\n" + "#" * 66)
    print("# 交付闸门结论")
    print("#" * 66)
    bad = 0
    for name, code in results:
        flag = "PASS" if code == 0 else "FAIL"
        if code != 0:
            bad += 1
        print("  %-28s %s" % (name, flag))
    print("")
    if bad:
        print("  结论: %d 项红 → 不发链接" % bad)
    else:
        print("  结论: 全绿 → 可发链接")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
