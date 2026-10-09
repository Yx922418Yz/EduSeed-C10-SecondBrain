# L1 原始笔记 — C4D 本地大模型 Agent 技能

> C4D 挑战期间的随手记录，全是报错原文和当时的崩溃心情。

## 环境

- Windows 11，Python 3.11 当时装的，Ollama 跑 Gemma 2B。
- 目标：写一个本地 agent，让 Gemma 能调用我自己写的几个小工具。

## 报错现场（原样记的）

```
ollama pull gemma:2b  ← 这步通了
python -m venv .venv
.venv\Scripts\activate
pip install ollama
python agent.py
→ ConnectionRefusedError: [WinError 10061] 由于目标计算机积极拒绝，无法连接。
```

## 当时怎么想到的

- 一开始以为是代码错了，把 agent.py 重写了三遍。
- 后来才反应过来：Ollama 桌面端根本没启动！它只是装好了，服务没起来。
- 打开 Ollama 客户端，等托盘图标出来，再跑 agent.py → 通了。

## 教训（当时写在便签上）

> "ConnectionRefused 在 127.0.0.1 上，第一件事不是改代码，是检查那个服务进程活着没有。"

这条后来变成 debug-workflow 技能里的"第 0 步：先确认依赖服务在跑"。

## 另一个坑

- Windows 上 Ollama 默认绑 127.0.0.1，我后来想让手机访问，设置 OLLAMA_HOST=0.0.0.0，结果防火墙又拦了。最后没折腾完，只在本机用。
