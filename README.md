# EduSeed-C10-SecondBrain

李亚轩（Yx922418Yz）的个人 Agent 系统——"第二大脑"。纯 Markdown + Python CLI，Windows 原生可跑。

## 快速开始

```powershell
python kstar_loop.py status
python kstar_loop.py run --situation "我现在遇到了 xxx" --expected 0.6 --actual 0.7
python skill_manager.py score
```

## 目录

- `architecture.md` — 五层架构与数据流
- `kstar_loop.py` — Agent Loop 主脚本
- `skill_manager.py` — 技能生命周期管理
- `memory/L1_raw/` — 5 条原始笔记
- `memory/L2_episodes/` — 11 条 KSTAR 经历
- `memory/L3_skills/` — 5 个技能（canonical）
- `config/L4/` — identity.md + tools.md
- `skills/` — L3_skills 的交付镜像
- `demo/` — 终端截图 + 完整运行日志
- `usage_log.md` — 11 个真实使用场景
- `AAR.md` — 系统级反思
- `AI日志.md` — 构建过程的 AI 使用记录
- `拿来说明.md` — 借鉴 Obsidian / Claude Skill / PARA / LangChain

## 已真实跑通证据

- 2026-10-09 本机跑了 5 次闭环，留下 demo/full_run.log 和 demo/terminal_screenshot.png。
- 写回结果：memory/L2_episodes/ 从 6 条涨到 11 条，debug-workflow usage_count 5→6，blog-writer 在漏召后现场补 triggers 重跑命中（自进化证据）。
