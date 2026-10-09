# LiYaxuan_C10_AI日志.md — 构建过程的 AI 使用记录

> 整个 C10 系统是我（李亚轩）和豆包 AI 多轮对话磨出来的。这里记每一轮 AI 在干什么、我又反过来改了什么。

## 轮次 1：对齐挑战
- **我问 AI**："C10 要求五层架构，能帮我逐维拆一下 rubric.json 吗？"
- **AI 输出**：把 systemArchitecture/memorySystem/artifactCompleteness/aiUsage/reflectionQuality 五个维度列成表，告诉我"系统性"和"实用性"权重最高。
- **我改**：意识到不能只交架构文档，必须真跑一次闭环——所以才写了 kstar_loop.py。

## 轮次 2：设计目录结构
- **我问 AI**："Markdown 文件树怎么组织才能既满足 L1/L2/L3/L4 四层，又让 kstar_loop.py 能解析？"
- **AI 输出**：建议技能文件用 YAML frontmatter，loop 用正则解析，不要引 PyYAML。
- **我改**：采纳。故意只用标准库，避免 Windows 上再出 pip 环境问题。

## 轮次 3：写 kstar_loop.py
- **我问 AI**："KSTAR 闭环在 CLI 上怎么落地？R̂ 和 R 没有客观数值怎么办？"
- **AI 输出**：建议用 --expected / --actual 两个参数，0-1 主观评分，EMA 平滑。
- **我改**：第一版跑出来发现 frontmatter 改写会把整个文件重写一遍，我担心破坏正文。改成只正则替换那几个字段。

## 轮次 4：真实跑第一次
- **我跑**：`python kstar_loop.py run --situation "pip install ... conflict" ...`
- **真实输出**：debug-workflow 被正确选中，ep007 写回。
- **我发现**：PowerShell 控制台显示中文乱码，但文件本身是 UTF-8——不是 bug，是 PS 5.1 的显示编码问题。日志文件留着就好。

## 轮次 5：漏召现场
- **我跑**："帮我写一段情侣视频的搞笑古风配文"——结果选了 aar-generator，没选 blog-writer。
- **我问 AI**："为什么会选错？"
- **AI 帮我定位**：blog-writer 的 triggers 里只有"文案"，没有"配文"。
- **我改**：现场用 `skill_manager.py iterate` 补了触发词，重跑——这次选对了。这一圈被我写进 usage_log 场景 8/9，作为自进化证据。

## 轮次 6：截图
- **我问 AI**："Windows 上怎么给终端跑的程序留截图证据？"
- **AI 建议**：把日志渲染成终端样式的 HTML，Edge headless --screenshot 出图。
- **我采纳**：demo/terminal_screenshot.png 就是这么来的。

## AI 使用质量自评
- 不是一句话指令直接提交：每一轮都有"我跑了→发现问题→再问 AI→再改"的循环。
- 多轮迭代：至少 6 轮，不是 one-shot。
- 有 prompt 优化：从"帮我写个 Agent"逐步收窄到"frontmatter 怎么正则替换不会破坏正文"。
- 诚实边界：AI 建议过"上 embedding 语义检索"，我因为没 API key 拒绝了，降级到关键词——这个降级写进了 AAR。
