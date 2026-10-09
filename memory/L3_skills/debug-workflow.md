---
name: debug-workflow
description: 当代码/脚本报错时，按 SOP 定位根因而不是瞎改
triggers: [报错, error, exception, traceback, debug, 失败, 连不上, timeout, conflict, UnicodeDecodeError, ConnectionRefused]
usage_count: 6
last_effect: "2026-10-09 run #6: 实际比预期慢，pip 缓存旧 wheel 又踩了一次"
avg_delta_r: -0.081
status: active
iteration_log:
  - date: 2026-04-09
    note: "从 ep002（Ollama 没启动白改 3 遍）提炼：加'第 0 步：先确认依赖服务/端口活着'。"
  - date: 2026-07-25
    note: "从 ep004 提炼：dependency conflict 排查加 pip show + 锁版本 + --no-cache-dir 三步。"
  - date: 2026-10-09
    note: "实际比预期慢，pip 缓存旧 wheel 又踩了一次"
---

# Skill: debug-workflow

## What（做什么）
把"看到报错就瞎改"的本能，替换成一条确定性的排查流水线，最少走弯路。

## When to Use（触发条件）
- 任何命令/脚本报错，且你第一反应是"要不重写一遍"——这时候必须停下走 SOP。
- 报错信息里包含：Traceback / Error / refused / timeout / conflict / UnicodeDecode。

## Input（输入）
- 完整报错原文（不要只截最后一行）。
- 我刚才执行的完整命令。
- 我已经试过什么（避免重复试）。

## Steps（步骤）
0. **先确认外部依赖活着**：`netstat -ano | findstr :<端口>`；服务类（Ollama/MySQL/Redis）先看托盘/任务管理器。
1. **读报错最后一行**：那是真正的异常类型。往上翻第一个属于"我自己写的文件"的栈帧，那才是出事地点。
2. **搜错误码/异常类名**：`pip show <被点名的包>`；Windows 中文文件检查 `encoding="utf-8"`；网络问题先换条路（ep005 的教训）。
3. **只改一个变量**：每次只动一处，改完立刻复跑。不要同时改三处然后问"哪处生效了"。
4. **修好之后写一条 L2 episode**：记 S→T→Â→R̂→A→R→ΔR，别让同样的坑踩第二次。

## Tools（需要什么工具）
- PowerShell（netstat / pip show / python -c）
- 浏览器搜异常信息
- 本仓库 L2_episodes/（查以前踩过的坑）

## Output（输出）
- 一句"根因是 XXX"
- 一行修复命令
- 一条新的 L2 episode 文件（写回记忆）
