# -*- coding: utf-8 -*-
"""
kstar_loop.py — 李亚轩的第二大脑 KSTAR 认知循环（Layer 3）。

闭环：K(nowledge 检索) -> S(ituation) -> T(ask) -> Â(action plan) -> R̂(预期)
     -> A(ction 执行) -> R(result 实际) -> ΔR = R̂ - R -> 写回记忆(L2 + 更新 L3)。

用法：
  python kstar_loop.py run --situation "我遇到了 xxx 报错" [--expected 0.6] [--actual 0.8] [--note "事后补一句"]
  python kstar_loop.py status        # 看记忆库统计与各技能使用情况
  python kstar_loop.py search "关键词" # K 阶段手动检索

纯标准库，Windows 原生 Python 3.13 实测可跑。
"""
import argparse
import datetime as dt
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
L2_DIR = os.path.join(ROOT, "memory", "L2_episodes")
L3_DIR = os.path.join(ROOT, "memory", "L3_skills")
LOG_DIR = os.path.join(ROOT, "logs")
os.makedirs(L2_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


# ---------- 极简 frontmatter 读写（只处理本仓库用到的子集） ----------
def split_frontmatter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return "", text
    return m.group(1), m.group(2)


def get_field(fm, key):
    m = re.search(rf"^{re.escape(key)}:\s*(.*)$", fm, re.M)
    return m.group(1).strip() if m else None


def set_field(fm, key, value):
    pat = re.compile(rf"^{re.escape(key)}:.*$", re.M)
    new_line = f"{key}: {value}"
    if pat.search(fm):
        return pat.sub(new_line, fm, count=1)
    return fm.rstrip() + "\n" + new_line + "\n"


def list_skills():
    out = []
    if not os.path.isdir(L3_DIR):
        return out
    for n in sorted(os.listdir(L3_DIR)):
        if not n.endswith(".md"):
            continue
        p = os.path.join(L3_DIR, n)
        fm, body = split_frontmatter(p)
        triggers_raw = get_field(fm, "triggers") or ""
        triggers = [t.strip().strip("[]'\" ") for t in triggers_raw.strip("[]").split(",") if t.strip()]
        out.append({
            "file": p,
            "name": get_field(fm, "name") or n[:-3],
            "desc": get_field(fm, "description") or "",
            "triggers": triggers,
            "usage_count": int(get_field(fm, "usage_count") or 0),
            "avg_delta_r": float(get_field(fm, "avg_delta_r") or 0.0),
            "status": get_field(fm, "status") or "active",
            "fm": fm, "body": body,
        })
    return out


# ---------- K：按情境打分选技能 ----------
def pick_skill(situation):
    skills = list_skills()
    scored = []
    low = situation.lower()
    for s in skills:
        if s["status"] != "active":
            continue
        score = 0.0
        for t in s["triggers"]:
            if t and t.lower() in low:
                score += 2.0
        if s["name"].lower() in low:
            score += 1.0
        # 使用越多、avg_delta_r 越接近 0（预测越准），加权略高
        score += min(s["usage_count"], 5) * 0.1
        scored.append((score, s))
    scored.sort(key=lambda x: -x[0])
    return scored


# ---------- 写回：更新技能 frontmatter ----------
def update_skill(skill, delta_r, note):
    fm = skill["fm"]
    new_count = skill["usage_count"] + 1
    # EMA 平滑 avg_delta_r
    prev = skill["avg_delta_r"]
    ema = round(prev * 0.7 + delta_r * 0.3, 3)
    today = dt.date.today().isoformat()
    fm = set_field(fm, "usage_count", str(new_count))
    fm = set_field(fm, "avg_delta_r", str(ema))
    fm = set_field(fm, "last_effect", f'"{today} run #{new_count}: {note[:60]}"')
    # 追加一条 iteration_log
    fm = fm.rstrip() + f"\n  - date: {today}\n    note: \"{note}\"\n"
    body = skill["body"]
    with open(skill["file"], "w", encoding="utf-8", newline="\n") as f:
        f.write("---\n" + fm + "---\n" + body)


# ---------- 写回：新增 L2 episode ----------
def write_episode(situation, skill, expected, actual, note, steps_run):
    existing = [n for n in os.listdir(L2_DIR) if re.match(r"ep\d+_", n)]
    nxt = len(existing) + 1
    today = dt.date.today().isoformat()
    slug = re.sub(r"[^\w一-鿿]+", "_", situation)[:24].strip("_") or "loop"
    fname = f"ep{nxt:03d}_{slug}.md"
    path = os.path.join(L2_DIR, fname)
    delta = round(expected - actual, 3)
    content = f"""---
episode_id: ep{nxt:03d}
date: {today}
source_skill: {skill['name']}
---

# EP{nxt:03d} — {situation[:40]}

## K（已检索到的相关知识）
- 命中技能：{skill['name']}（{skill['desc']}）
- 该技能历史 usage_count={skill['usage_count']}，avg_delta_r={skill['avg_delta_r']}

## S（Situation 情境）
{situation}

## T（Task 任务）
用最合适的技能处理上面这个情境。

## Â（Action Plan 行动计划）
""" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps_run)) + f"""

## R̂（预期结果）
置信度 / 预期评分 = {expected}

## A（Action 实际执行）
本次由 kstar_loop.py 驱动，按上述步骤打印执行清单并写回记忆。

## R（实际结果）
实际评分 = {actual}

## ΔR = R̂ − R
ΔR = {delta}
{'（预测偏保守，实际好于预期）' if delta < 0 else '（预测偏乐观，实际不如预期）' if delta > 0 else '（预测准确）'}

## 备注
{note}
"""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return path


# ---------- 写回：追加运行日志 ----------
def append_runlog(line):
    p = os.path.join(LOG_DIR, "run_log.md")
    head = ""
    if not os.path.exists(p):
        head = "# KSTAR Run Log\n\n| 时间 | 情境 | 选中技能 | R̂ | R | ΔR |\n|---|---|---|---|---|---|\n"
    with open(p, "a", encoding="utf-8", newline="\n") as f:
        if head:
            f.write(head)
        f.write(line + "\n")


# ---------- 主循环 ----------
def cmd_run(args):
    print("=" * 64)
    print("KSTAR LOOP 启动 @", dt.datetime.now().isoformat(timespec="seconds"))
    print("=" * 64)

    # K
    print("\n[K] 检索记忆库中可用技能 ...")
    scored = pick_skill(args.situation)
    for score, s in scored[:3]:
        print(f"    score={score:5.2f}  {s['name']:18s} usage={s['usage_count']:>2}  {s['desc'][:40]}")
    if not scored or scored[0][0] <= 0:
        print("    没有命中任何技能，退回通用 aar-generator。")
        skill = next((s for s in list_skills() if s["name"] == "aar-generator"), None)
        if skill is None:
            print("!! 连 aar-generator 都没有，中止。"); sys.exit(2)
    else:
        skill = scored[0][1]
    print(f"    >> 选中技能: {skill['name']}\n")

    # S / T
    print(f"[S] 情境: {args.situation}")
    print(f"[T] 任务: 调用 {skill['name']} 处理该情境\n")

    # Â + R̂：从技能正文里抽步骤
    steps = [ln.strip() for ln in skill["body"].splitlines()
             if re.match(r"^\d+\.\s", ln.strip())]
    print(f"[Â] 行动计划（来自 skills/{skill['name']}.md 的 Steps）:")
    for i, st in enumerate(steps, 1):
        print(f"    {st}")
    expected = args.expected
    print(f"\n[R̂] 预期评分（用户给定）= {expected}")

    # A：真实动作 = 打印执行清单（这一步本身就是"调用技能"）
    print("\n[A] 执行中 ...")
    for st in steps:
        print(f"    ✔ {st}")

    # R
    actual = args.actual
    print(f"\n[R] 实际评分（用户事后填）= {actual}")
    delta = round(expected - actual, 3)
    judge = "预测准确，技能继续用" if abs(delta) < 0.15 else \
            "预测偏保守，技能可以更激进" if delta > 0 else \
            "预测偏乐观，技能步骤要收紧"
    print(f"[ΔR] R̂−R = {delta}  ->  {judge}")

    # 写回
    note = args.note or f"{judge}；本次情境：{args.situation[:40]}"
    ep_path = write_episode(args.situation, skill, expected, actual, note, steps)
    update_skill(skill, delta, note)
    append_runlog(f"| {dt.datetime.now().isoformat(timespec='seconds')} | "
                  f"{args.situation[:30]} | {skill['name']} | {expected} | {actual} | {delta} |")
    print(f"\n[写回] 新 episode -> {os.path.relpath(ep_path, ROOT)}")
    print(f"[写回] 技能 {skill['name']} usage_count 已 +1，avg_delta_r 已更新，iteration_log 已追加")
    print("=" * 64)
    print("KSTAR 闭环完成。")


def cmd_status(_):
    skills = list_skills()
    print(f"技能库共 {len(skills)} 个技能：")
    for s in skills:
        print(f"  - {s['name']:18s} status={s['status']:10s} "
              f"usage={s['usage_count']:>2}  avgΔR={s['avg_delta_r']:+.2f}")
    eps = [n for n in os.listdir(L2_DIR) if n.endswith(".md")]
    print(f"\nL2_episodes 共 {len(eps)} 条经历。")
    l1 = os.listdir(os.path.join(ROOT, "memory", "L1_raw"))
    print(f"L1_raw 共 {len(l1)} 条原始笔记。")


def cmd_search(args):
    print(f"在记忆库检索: {args.keyword}")
    for s in pick_skill(args.keyword):
        pass
    for s in list_skills():
        blob = s["name"] + s["desc"] + " ".join(s["triggers"])
        if args.keyword.lower() in blob.lower():
            print(f"  [skill] {s['name']}: {s['desc']}")
    for n in os.listdir(L2_DIR):
        with open(os.path.join(L2_DIR, n), encoding="utf-8") as f:
            if args.keyword.lower() in f.read().lower():
                print(f"  [ep]    {n}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--situation", required=True)
    r.add_argument("--expected", type=float, default=0.6)
    r.add_argument("--actual", type=float, default=0.7)
    r.add_argument("--note", default="")
    sub.add_parser("status")
    s = sub.add_parser("search")
    s.add_argument("keyword")
    args = ap.parse_args()
    {"run": cmd_run, "status": cmd_status, "search": cmd_search}[args.cmd](args)


if __name__ == "__main__":
    main()
