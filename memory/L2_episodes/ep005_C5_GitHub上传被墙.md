---
episode_id: ep005
challenge: C5
date: 2026-06-10
source_skill: debug-workflow
---

# EP005 — git push github.com 超时的绕行方案

## K（已检索到的相关知识）
- 学长提示过："api.github.com 比 github.com 好连。"

## S（Situation）
C5 要求把仓库推到 GitHub。我 `git push` 直接卡 5 分钟超时，换网络也没用。

## T（Task）
把本地文件传到 GitHub 仓库，且要可复现（以后 C6/C10/C10H 都还要用）。

## Â（Action Plan）
1. 先 ping / curl 对比 github.com vs api.github.com。
2. 写一个 Python 脚本，用 REST API `/repos/{owner}/{repo}/contents/{path}` PUT 上传 base64 内容。
3. 批量 walk 目录，逐文件上传。

## R̂（预期结果）
脚本 1 小时能写完并跑通第一个文件。置信度 0.6。

## A（Action）
- 实测：github.com 22 端口超时，api.github.com 443 经 urllib 秒回。
- 写了 gh_helper.py（就是本工作目录下那个），支持 whoami / create-repo / upload / upload-dir / zipball / list。
- 第一次 upload 一个 README 成功。

## R（实际结果）
脚本写完约 2 小时，比预期慢；但从此 C5/C6/C8/C10/C10H 全部走它，没再为 push 发过愁。

## ΔR
R̂ 0.6，实际"一次性投入 2 小时，长期省了无数次" → ΔR ≈ +0.4（低估了"写一次工具、终身受用"的复利）。

## 写回 L3 的教训
- 网络问题先测"哪条路通"，不要在死路上反复重试。
- 凡是"要做 N 次的手工操作"，第 2 次做的时候就应该停下来写脚本。
