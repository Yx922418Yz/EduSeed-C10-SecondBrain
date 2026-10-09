# LiYaxuan_C10_usage_log.md — 真实使用记录

> 每条都有日期、输入、输出、ΔR、后续改进。前 6 条来自 C1–C9 的真实经历（事后结构化进 L2），后 5 条是 2026-10-09 当天 kstar_loop.py 真实跑出来的（见 demo/full_run.log）。

---

## 场景 1：用 research-scanner 处理 C1 课程资料
- **日期**：2026-03-12
- **输入**：CS146S_offline.zip，里面几十份英文 PDF / 字幕
- **调用的 Skill**：research-scanner（当时还没正式命名，靠手感）
- **输出**：一份按"高/中/低"打标签、只精读高标签的中文学习笔记
- **ΔR**：R̂=0.6（预期 3 天一次过审），R=0.9（实际一次过审 + 同学正面反馈），ΔR=-0.3
- **后续改进**：把"先取舍再精读"写成 research-scanner 的第 2 步。

## 场景 2：用 debug-workflow 解决 C4D Ollama 连接被拒
- **日期**：2026-04-08
- **输入**：`ConnectionRefusedError 10061`
- **调用的 Skill**：debug-workflow（当时是本能反应，没走 SOP）
- **输出**：发现 Ollama 桌面端根本没启动，打开后一行通了
- **ΔR**：R̂=0.5（预期重写 1-2 次代码解决），R=-0.1（在错误方向上浪费 1.5 小时），ΔR=+0.6
- **后续改进**：给 debug-workflow 加"第 0 步：先确认依赖服务活着"。

## 场景 3：用 debug-workflow 修书法 MaaS 的 start.bat
- **日期**：2026-05-20
- **输入**：队友双击 start.bat 报"系统找不到指定路径"
- **调用的 Skill**：debug-workflow
- **输出**：脚本第一行加 `cd /d %~dp0`，队友一次跑通
- **ΔR**：R̂=0.8，R=0.9，ΔR=-0.1
- **后续改进**：把"给别人用的脚本第一行必须自报家门"写进 debug-workflow。

## 场景 4：用 debug-workflow 解 django-celery-beat 依赖冲突
- **日期**：2026-07-25
- **输入**：`Cannot install django-celery-beat because these package versions have conflicting dependencies`
- **调用的 Skill**：debug-workflow
- **输出**：`pip show django` 发现被顶到 5.0，锁 `django==4.2.*` + `--no-cache-dir` 重装
- **ΔR**：R̂=0.7（预期 20 分钟），R=0.55（实际 35 分钟），ΔR=+0.15
- **后续改进**：dependency conflict SOP 加"pip 缓存旧 wheel"这一条。

## 场景 5：用 research-scanner 思路解决 git push 超时
- **日期**：2026-06-10
- **输入**：`git push` github.com 卡 5 分钟超时
- **调用的 Skill**：debug-workflow 的"网络问题先换条路"分支
- **输出**：测通 api.github.com 可达，写了 gh_helper.py 走 REST API 上传
- **ΔR**：R̂=0.6（预期 1 小时写完脚本），R=0.4（实际 2 小时），ΔR=+0.2；但长期收益极高
- **后续改进**：这条本身变成了 L4 tools.md 里的"GitHub REST API"工具。

## 场景 6：用 weekly-planning 处理人际边界
- **日期**：2026-06-29
- **输入**：发小深夜找我聊游戏 vs 男友不开心
- **调用的 Skill**：weekly-planning（借了"排约束"的思路）
- **输出**：分别私下聊 + 立"深夜只说正事"的规矩
- **ΔR**：R̂=0.5，R=0.7，ΔR=-0.2
- **后续改进**：暂时沉淀在 L2，没抽象成新技能（只发生过一次，样本不够）。

---

## 场景 7（kstar_loop 真实运行）：pip dependency conflict
- **日期**：2026-10-09 18:03
- **输入**：`python kstar_loop.py run --situation "pip install django-celery-beat 报 dependency conflict" --expected 0.7 --actual 0.55`
- **选中技能**：debug-workflow（score=2.50，第一）
- **输出**：展开 5 步 SOP，写回 ep007，debug-workflow usage 5→6
- **ΔR**：0.15
- **后续改进**：见 demo/run1_debug.txt 完整日志。

## 场景 8（kstar_loop 真实运行，漏召）：情侣视频配文
- **日期**：2026-10-09 18:03
- **输入**：`"帮我写一段情侣视频的搞笑古风配文，要去AI味"`
- **选中技能**：aar-generator（**错了**——因为 blog-writer 的 triggers 里没有"配文"）
- **输出**：展开了 AAR 步骤，写回 ep008
- **ΔR**：-0.15
- **后续改进**：这就是自进化的真实触发——见场景 9。

## 场景 9（kstar_loop 真实运行，自进化后重跑）：同场景 8
- **日期**：2026-10-09 18:04
- **动作**：`python skill_manager.py iterate blog-writer --note "...补 triggers 加 配文/视频文案"`，并直接编辑 blog-writer.md 的 triggers 行
- **重跑**：同样的情境，这次正确命中 blog-writer（score=2.40）
- **输出**：写回 ep011，blog-writer usage 4→5
- **ΔR**：-0.18
- **后续改进**：这就是"漏召→补触发词→重跑命中"的完整自进化闭环，截图见 demo/。

## 场景 10（kstar_loop 真实运行）：周日晚排下周计划
- **日期**：2026-10-09 18:03
- **输入**：`"周日晚排下周计划：高数弱项、四级听力、膝盖怕冷"`
- **选中技能**：weekly-planning（score=4.50，命中"周计划/周日/排期/膝盖怕冷"多个词）
- **输出**：展开 6 步计划 SOP，写回 ep009
- **ΔR**：-0.15
- **后续改进**：身体约束这一步真实生效（雨天提醒护膝）。

## 场景 11（kstar_loop 真实运行）：英文 PDF 资料包
- **日期**：2026-10-09 18:03
- **输入**：`"收到一个 zip 里面几十份英文 PDF 要提炼重点"`
- **选中技能**：research-scanner（score=2.30）
- **输出**：展开 5 步"取舍→精读→摘要"SOP，写回 ep010
- **ΔR**：-0.25
- **后续改进**：说明 research-scanner 预测偏保守，下次可以把预期评分调高。
