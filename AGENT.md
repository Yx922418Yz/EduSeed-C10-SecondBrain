# AGENT.md — 李亚轩的第二大脑主配置

> 这是 Agent 的入口。每次启动 kstar_loop.py 时，等价于把这份文件 + config/L4/identity.md + 选中的 skill 喂给它。

## 一句话定义

我是李亚轩的第二大脑：一个跑在本地 Markdown 文件上、靠 KSTAR 闭环持续自进化的个人 Agent。

## 启动方式

```powershell
# 跑一次闭环
python kstar_loop.py run --situation "你现在遇到的事" --expected 0.6 --actual 0.7 --note "事后补一句"

# 看记忆库状态
python kstar_loop.py status

# 手动检索
python kstar_loop.py search "报错"

# 技能生命周期
python skill_manager.py create new-skill --desc "..." --triggers "词1,词2"
python skill_manager.py score
python skill_manager.py iterate <skill> --note "改了什么"
python skill_manager.py deprecate <skill>
```

## 循环规则（kstar_loop.py 严格按这个跑）

1. **K**：扫 memory/L3_skills/，按 triggers 关键词给当前 situation 打分。
2. **S/T**：打印情境，明确任务 = "调用 top-1 技能处理它"。
3. **Â/R̂**：把技能 Steps 抽出来当行动计划，R̂ 由 --expected 给。
4. **A**：逐条勾选执行。
5. **R/ΔR**：--actual 是事后填的，ΔR = R̂ − R。
6. **写回**：新建 epNNN.md + 更新技能 frontmatter + 追加 run_log.md。

## 三条铁律（每次跑之前默念）

1. 诚实填 R̂ 和 R，不要为了好看填 0.9/0.9。
2. 漏召了就改 triggers，不要绕过它——那是系统在教你东西。
3. 写回是强制的，跑完不写回 = 这次白跑。
