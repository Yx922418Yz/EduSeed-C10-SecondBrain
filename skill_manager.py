# -*- coding: utf-8 -*-
"""
skill_manager.py — 技能生命周期管理（创建 / 评分 / 迭代 / 淘汰）。

用法：
  python skill_manager.py create <skill-name> --desc "一句话" --triggers "词1,词2"
  python skill_manager.py score                       # 全部技能健康分
  python skill_manager.py iterate <skill-name> --note "改了什么"
  python skill_manager.py deprecate <skill-name>      # 标记 deprecated
"""
import datetime as dt
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
L3_DIR = os.path.join(ROOT, "memory", "L3_skills")
os.makedirs(L3_DIR, exist_ok=True)


def read_skill(name):
    p = os.path.join(L3_DIR, name + ".md")
    if not os.path.exists(p):
        # 模糊匹配
        for n in os.listdir(L3_DIR):
            if n.startswith(name) and n.endswith(".md"):
                p = os.path.join(L3_DIR, n); break
        else:
            sys.exit(f"找不到技能: {name}")
    with open(p, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    return p, m.group(1), m.group(2)


def cmd_create(args):
    p = os.path.join(L3_DIR, args.name + ".md")
    if os.path.exists(p):
        sys.exit(f"技能已存在: {p}")
    today = dt.date.today().isoformat()
    triggers = args.triggers or args.name
    body = f"""---
name: {args.name}
description: {args.desc or "待补"}
triggers: [{triggers}]
usage_count: 0
last_effect: "尚未使用"
avg_delta_r: 0.0
status: active
iteration_log:
  - date: {today}
    note: "技能创建，待验证。"
---

# Skill: {args.name}

## What
（一句话说清做什么）

## When to Use
（触发条件）

## Input
（需要什么输入）

## Steps
1. TODO
2. TODO

## Tools
- TODO

## Output
（产出什么）
"""
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print(f"CREATED {p}")


def _field(fm, key):
    m = re.search(rf"^{re.escape(key)}:\s*(.*)$", fm, re.M)
    return m.group(1).strip() if m else ""


def cmd_score(_):
    print(f"{'技能':22s} {'状态':10s} {'次数':>4s} {'avgΔR':>8s}  健康分")
    for n in sorted(os.listdir(L3_DIR)):
        if not n.endswith(".md"):
            continue
        with open(os.path.join(L3_DIR, n), encoding="utf-8") as f:
            fm = re.match(r"^---\n(.*?)\n---", f.read(), re.S).group(1)
        name = _field(fm, "name") or n[:-3]
        status = _field(fm, "status") or "active"
        usage = int(_field(fm, "usage_count") or 0)
        avg = float(_field(fm, "avg_delta_r") or 0)
        # 健康分：用过 + 预测准（|ΔR|小）+ 状态 active
        health = min(usage, 10) * 2 + max(0, 20 - abs(avg) * 100)
        if status != "active":
            health = 0
        print(f"{name:22s} {status:10s} {usage:>4d} {avg:>+8.2f}  {health:5.1f}/40")


def cmd_iterate(args):
    p, fm, body = read_skill(args.name)
    today = dt.date.today().isoformat()
    fm = fm.rstrip() + f"\n  - date: {today}\n    note: \"{args.note}\"\n"
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("---\n" + fm + "---\n" + body)
    print(f"ITERATED {os.path.basename(p)}: {args.note}")


def cmd_deprecate(args):
    p, fm, body = read_skill(args.name)
    fm = re.sub(r"^status:.*$", "status: deprecated", fm, count=1, flags=re.M)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write("---\n" + fm + "---\n" + body)
    print(f"DEPRECATED {os.path.basename(p)}")


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    cmd = sys.argv[1]
    rest = sys.argv[2:]
    if cmd == "create":
        ns = argparse_ns(rest)
        cmd_create(ns)
    elif cmd == "score":
        cmd_score(None)
    elif cmd == "iterate":
        ns = argparse_ns(rest)
        if not hasattr(ns, "note"):
            sys.exit("需要 --note")
        cmd_iterate(ns)
    elif cmd == "deprecate":
        ns = argparse_ns(rest)
        cmd_deprecate(ns)
    else:
        print(__doc__); sys.exit(1)


def argparse_ns(argv):
    class Ns: pass
    ns = Ns()
    ns.name = argv[0] if argv else ""
    i = 1
    while i < len(argv):
        if argv[i] == "--desc":
            ns.desc = argv[i + 1]; i += 2
        elif argv[i] == "--triggers":
            ns.triggers = argv[i + 1]; i += 2
        elif argv[i] == "--note":
            ns.note = argv[i + 1]; i += 2
        else:
            i += 1
    if not hasattr(ns, "desc"): ns.desc = ""
    if not hasattr(ns, "triggers"): ns.triggers = ""
    return ns


if __name__ == "__main__":
    main()
