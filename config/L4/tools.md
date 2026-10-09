# L4 Tools — 李亚轩的工具清单（Action = Plan × Access Token × Energy）

> 本表是 Agent 的"行动半径"。任何 Skill 在执行前必须先查这里：这个 Skill 需要的工具我到底有没有。

## 核心工具（3-5 个，真正天天用的）

| 类别 | 工具 | 用途 | 接入方式 | 状态 |
|------|------|------|----------|------|
| LLM | 豆包 / Doubao（本助手） | 推理、写文案、改代码、翻译 | 桌面客户端 | ✅ 日常主力 |
| LLM（本地探索） | Ollama + Gemma（C4D 时搭过） | 离线推理实验 | 本地 localhost:11434 | 🟡 偶尔启动 |
| 代码 | VS Code / Cursor | 写 Python、改 start.bat | 桌面 | ✅ |
| 版本控制 | GitHub REST API（gh_helper.py） | 传仓库、查文件 | Python urllib | ✅ git push 被墙后的替代方案 |
| 知识管理 | 本仓库的 Markdown 文件树 | L1/L2/L3 记忆 | 文件系统 | ✅ |

## 辅助工具

| 类别 | 工具 | 用途 | 备注 |
|------|------|------|------|
| 浏览器 | Edge（headless 可截图） | 抓网页、留证据截图 | 截图用 --headless --screenshot |
| 终端 | PowerShell 5.1 | 跑脚本、重定向日志 | 注意：不能用 && / \|\|，用 ; 和 if($?) |
| 数据库 | MySQL 8.0 | 书法 MaaS / 考研政治项目 | 本机服务 |
| 后端 | Spring Boot（Java）/ Django（Python） | 两个项目分别用 | 跟队友分工 |
| 协作 | Gitee（团队代码） / 微信群 | 竞赛队长带队 | 个人 GitHub 是 Yx922418Yz |
| 文档 | WPS / Markdown | 交作业、写 AAR | 中文 UTF-8 无 BOM |

## 我没有的工具（诚实记录，防止 Skill 瞎调用）

- ❌ 没有 OpenAI / Anthropic API key（C10H 阶段 OpenRouter key 留占位）
- ❌ 没有 Vercel / Railway / 云服务器
- ❌ 没有 Telegram Bot token（C10H Level 2 卡在这一步）
- ❌ Docker 未安装

## 工具调用纪律

1. 任何 Skill 执行前，先在本表确认工具可用——缺工具就降级方案，不要硬上。
2. 需要外部 API key 的工具，key 一律留占位符 `<PUT_KEY_HERE>`，绝不把真 key 写进仓库。
3. 每个 Skill 的 Output 必须能落地到上面某一个工具，否则这个 Skill 是空壳。
