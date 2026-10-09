# LiYaxuan_C10_architecture.md — 第二大脑架构与数据流

> 李亚轩（Yx922418Yz）的个人 Agent 系统。纯 Markdown + Python CLI，零外部依赖，Windows 原生可跑。

## 一、五层总览

```
┌─────────────────────────────────────────────────────────┐
│ Layer 5  Interface  CLI (kstar_loop.py) + Markdown 文件树 │
├─────────────────────────────────────────────────────────┤
│ Layer 4  Tool/Access  config/L4/tools.md 列出可用工具      │
├─────────────────────────────────────────────────────────┤
│ Layer 3  Agent Loop  kstar_loop.py: K→S→T→Â→R̂→A→R→ΔR→写回│
├─────────────────────────────────────────────────────────┤
│ Layer 2  Skill System  memory/L3_skills/*.md (5 个真实技能)│
├─────────────────────────────────────────────────────────┤
│ Layer 1  Memory  memory/L1_raw → L2_episodes → L3_skills │
│                   config/L4/identity.md + tools.md      │
└─────────────────────────────────────────────────────────┘
```

## 二、目录结构

```
c10-secondbrain/
├── kstar_loop.py            # Layer 3 主循环（CLI 入口）
├── skill_manager.py         # 技能生命周期：create/score/iterate/deprecate
├── AGENT.md                 # 主配置：循环逻辑、调用规则（给人看的 README）
├── architecture.md          # 本文件
├── usage_log.md             # ≥6 个真实使用场景
├── AAR.md                   # 系统级反思
├── AI日志.md
├── 拿来说明.md
├── memory/
│   ├── L1_raw/              # 5 条原始笔记（C1/C4D/书法MaaS/考研政治/身体状况）
│   ├── L2_episodes/         # 11 条 KSTAR 经历（ep001–ep011）
│   └── L3_skills/           # 5 个技能（canonical，loop 直接读写这里）
├── config/
│   └── L4/
│       ├── identity.md     # 我是谁、五条原则、能力边界、项目资产
│       └── tools.md         # 工具清单（含"我没有的工具"诚实记录）
├── skills/                  # L3_skills 的交付镜像（给评审看）
├── logs/run_log.md          # 每次闭环一行：时间/情境/技能/R̂/R/ΔR
└── demo/
    ├── full_run.log         # 5 次闭环完整终端输出
    ├── terminal_screenshot.png
    └── run1_debug.txt ...   # 每次运行的单独留痕
```

## 三、数据流（一次完整 KSTAR 循环发生了什么）

以 `python kstar_loop.py run --situation "pip install django-celery-beat 报 dependency conflict"` 为例：

1. **K（Knowledge 检索）**：脚本 `list_skills()` 扫 `memory/L3_skills/*.md`，解析 frontmatter（name/triggers/usage_count/avg_delta_r）。对当前 situation 做关键词打分——triggers 命中 +2，name 命中 +1，使用次数加成。本场景命中 `dependency conflict` → debug-workflow 得分 2.50，排第一。
2. **S（Situation）**：把 situation 原文打印出来。
3. **T（Task）**：任务 = "调用 debug-workflow 处理该情境"。
4. **Â（Action Plan）**：从选中技能正文里正则抽出 `N. xxx` 步骤，作为行动计划打印。
5. **R̂（预期）**：用户用 `--expected 0.7` 给定。
6. **A（Action 执行）**：逐条打印 ✔ 执行清单（这一步本身就是"调用技能"的真实动作——技能的 Steps 被逐条展开并勾选）。
7. **R（实际）**：用户用 `--actual 0.55` 事后填入。
8. **ΔR = R̂ − R = 0.15**：脚本判定"预测偏保守，技能可以更激进"。
9. **写回记忆（关键）**：
   - 在 `memory/L2_episodes/` 新建 `ep007_*.md`，把 K/S/T/Â/R̂/A/R/ΔR 完整落盘。
   - 用正则把选中技能 frontmatter 的 `usage_count += 1`、`avg_delta_r` 做 EMA 平滑、`last_effect` 更新、`iteration_log` 追加一行。
   - 在 `logs/run_log.md` 追加一行表格记录。

**这就是闭环：下一次同样的 situation 再来，K 阶段读到的 debug-workflow 已经是"用过 6 次、avgΔR=-0.081、踩过 pip 缓存坑"的版本，而不是昨天那个空壳。**

## 四、设计决策（为什么这么做）

| 决策 | 为什么 |
|------|--------|
| 记忆用 Markdown 文件而不是 SQLite | 我是零基础，Markdown 我能用 VS Code 直接翻；SQLite 虽然更"高级"但我现在维护不动。先跑起来，以后真需要检索再加 SQLite。 |
| 技能 frontmatter 用极简正则解析 | 不引 PyYAML 依赖，避免 Windows 上又装环境出问题。只解析我自己用到的那几个字段。 |
| ΔR 用 0-1 的"评分"而不是钱/时间 | 我做的大部分任务（写文案、排计划、调 bug）没有客观货币度量。用 0-1 主观评分 + EMA 平滑，足够驱动"哪个技能该改"。 |
| L3_skills 是 canonical，skills/ 是镜像 | 挑战要求记忆层四层齐全，同时交付物要有 skills/ 目录。同一份文件两处出现，避免双写不一致。 |
| 技能漏召时靠人工 `skill_manager.py iterate` 补 triggers | 没接 embedding 向量检索（我没 OpenAI key），先用关键词打分 + 人工补词。这是诚实的降级方案，不是假装做了语义检索。 |

## 五、自进化机制怎么落地

不是口号，是脚本里真实存在的路径：

- **从经验生成技能**：`python skill_manager.py create <name> --desc ... --triggers ...` 从模板起一个新技能骨架。
- **优化已有技能**：每次 loop 跑完会写 iteration_log；发现 ΔR 持续大时，人工改 Steps，用 `skill_manager.py iterate --note` 记录这次改了什么。
- **淘汰**：`skill_manager.py deprecate <name>` 把 status 改成 deprecated，K 阶段打分时自动跳过。
- **健康分**：`skill_manager.py score` 给每个技能算 0-40 分（用过的次数 + |ΔR| 小 + active），一眼看出哪个技能该重构。

## 六、长期可使用性

- 所有数据是纯文本 markdown，不依赖任何平台。Elite20 结束后这个文件夹还能直接用。
- 加新技能 = 往 `memory/L3_skills/` 丢一个 .md 文件，不用改 kstar_loop.py。
- 加新工具 = 改 `config/L4/tools.md`，不影响其他层。
- 已经真实跑了 5 次闭环，留下 11 条 episode、5 个技能的 usage_count 都不是 0。
