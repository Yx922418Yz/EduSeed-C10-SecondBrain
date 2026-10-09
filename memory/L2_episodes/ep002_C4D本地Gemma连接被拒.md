---
episode_id: ep002
challenge: C4D
date: 2026-04-08
source_skill: debug-workflow
---

# EP002 — C4D 本地 Gemma Agent 连接被拒

## K（已检索到的相关知识）
- L1_raw/C4D_本地Gemma_踩坑记录.md
- 当时脑子里只有"报错→改代码"的本能反应。

## S（Situation）
写了个 agent.py 调 Ollama 的本地 Gemma 2B，第一次跑就 `ConnectionRefusedError 10061`。

## T（Task）
让 agent.py 能成功连上本地 Ollama 并返回一句话。

## Â（Action Plan，当时实际采用的错误版本）
1. 重写 agent.py 的连接逻辑。
2. 再跑。
3. 再重写。

## R̂（预期结果）
预期重写 1-2 次后能通。置信度 0.5。

## A（Action 实际行动）
- 重写了 3 遍 agent.py，全部同样报错。
- 第 4 次才想到：托盘里看看 Ollama 活着没——结果根本没启动。
- 打开 Ollama 桌面端，等图标出来，再跑 → 一行通了。

## R（实际结果）
真正花时间的不是代码，是"没检查依赖服务"。总共折腾约 2 小时，其中 1.5 小时在做无用功。

## ΔR
R̂ 0.5，实际"在错误方向上浪费了 1.5 小时" → ΔR ≈ -0.6（我对自己排错路径的预测严重失准）。

## 写回 L3 的教训
- debug-workflow 必须加"第 0 步：先确认所有依赖服务/进程/端口在跑"。
- 看到 `127.0.0.1 ConnectionRefused`，先 `netstat -ano | findstr :11434`，再谈代码。
