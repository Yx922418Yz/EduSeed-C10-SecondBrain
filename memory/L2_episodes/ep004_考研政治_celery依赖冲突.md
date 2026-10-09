---
episode_id: ep004
challenge: C9
date: 2026-07-25
source_skill: debug-workflow
---

# EP004 — django-celery-beat 依赖冲突 + UnicodeDecodeError

## K（已检索到的相关知识）
- L1_raw/考研政治项目_celery冲突笔记.md

## S（Situation）
在考研政治项目里 `pip install django-celery-beat` 报依赖冲突；跑起来读自己写的中文 md 又报 UnicodeDecodeError。

## T（Task）
装好 celery-beat 并让 Python 能正确读 UTF-8 中文文件。

## Â（Action Plan）
1. `pip show django` 看真实版本。
2. 锁版本 `pip install "django==4.2.*"`，重装 celery-beat。
3. 所有 `open()` 加 `encoding="utf-8"`。

## R̂（预期结果）
20 分钟搞定。置信度 0.7。

## A（Action）
照做，中间还踩了一下"pip 缓存旧 wheel"的坑，加了 `--no-cache-dir` 才彻底干净。

## R（实际结果）
约 35 分钟搞定，比预期慢 15 分钟。

## ΔR
R̂ 0.7，实际 0.55 → ΔR ≈ -0.15（低估了 pip 缓存这种边角问题）。

## 写回 L3 的教训
- dependency conflict 排查 SOP：`pip show <被点名的包>` → 锁版本 → `--no-cache-dir` 重装。
- Windows 下读写中文文本，`encoding="utf-8"` 是强制项，不是可选项。
