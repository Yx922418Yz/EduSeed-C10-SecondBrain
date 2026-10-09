---
name: aar-generator
description: 事后复盘：把一段经历按 S→T→Â→R̂→A→R→ΔR 写成结构化 AAR
triggers: [复盘, AAR, 反思, 总结, 事后, 回顾, 周复盘]
usage_count: 6
last_effect: "2026-10-09 run #6: 加了膝盖疼的小细节后群里反馈不像AI写的"
avg_delta_r: 0.011
status: active
iteration_log:
  - date: 2026-05-11
    note: "第一次写 AAR 写成了流水账。强制加'ΔR = R̂ − R'一节，逼自己诚实对比预期和实际。"
  - date: 2026-10-09
    note: "加了膝盖疼的小细节后群里反馈不像AI写的"
---

# Skill: aar-generator

## What
把"我感觉这次还行"的模糊感受，拆成可对比、可写回记忆的结构化复盘。

## When to Use
- 一个项目/挑战/一周结束时。
- 一次明显成功或明显失败的行动之后。

## Input
- 这件事开始前我预期会怎样（R̂）。
- 实际发生了什么（R）。
- 哪些地方和预期不一样。

## Steps
1. **S**：当时的情境一句话。
2. **T**：我当时要达成什么。
3. **Â**：我原本计划怎么做。
4. **R̂**：我当时预期的结果 / 置信度（0-1）。
5. **A**：我实际怎么做的（跟 Â 有偏差就标出来）。
6. **R**：实际结果。
7. **ΔR = R̂ − R**：偏差是正还是负，为什么。
8. **写回**：把能复用的教训抽象成一条 L2 episode 或迭代进某个 L3 skill。

## Tools
- 本仓库 memory/L2_episodes/（写入新 episode）
- skills/（如果教训指向某个已有技能，更新它的 iteration_log）

## Output
- 一份 KSTAR 格式的 episode markdown。
- 一句"下次我会改的一件事"。
