---
episode_id: ep007
date: 2026-10-09
source_skill: debug-workflow
---

# EP007 — pip install django-celery-beat 报 depende

## K（已检索到的相关知识）
- 命中技能：debug-workflow（当代码/脚本报错时，按 SOP 定位根因而不是瞎改）
- 该技能历史 usage_count=5，avg_delta_r=-0.18

## S（Situation 情境）
pip install django-celery-beat 报 dependency conflict

## T（Task 任务）
用最合适的技能处理上面这个情境。

## Â（Action Plan 行动计划）
1. 0. **先确认外部依赖活着**：`netstat -ano | findstr :<端口>`；服务类（Ollama/MySQL/Redis）先看托盘/任务管理器。
2. 1. **读报错最后一行**：那是真正的异常类型。往上翻第一个属于"我自己写的文件"的栈帧，那才是出事地点。
3. 2. **搜错误码/异常类名**：`pip show <被点名的包>`；Windows 中文文件检查 `encoding="utf-8"`；网络问题先换条路（ep005 的教训）。
4. 3. **只改一个变量**：每次只动一处，改完立刻复跑。不要同时改三处然后问"哪处生效了"。
5. 4. **修好之后写一条 L2 episode**：记 S→T→Â→R̂→A→R→ΔR，别让同样的坑踩第二次。

## R̂（预期结果）
置信度 / 预期评分 = 0.7

## A（Action 实际执行）
本次由 kstar_loop.py 驱动，按上述步骤打印执行清单并写回记忆。

## R（实际结果）
实际评分 = 0.55

## ΔR = R̂ − R
ΔR = 0.15
（预测偏乐观，实际不如预期）

## 备注
实际比预期慢，pip 缓存旧 wheel 又踩了一次
