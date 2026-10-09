# L1 原始笔记 — 考研政治项目（Python / Django）

> 我自己发起的 C9 风格项目：用 Python 做一个考研政治知识点抽背 + 艾宾浩斯复习提醒的小工具。

## 技术栈

- Django + django-celery-beat（定时推送复习提醒）+ SQLite 起步。
- 目标：把马原 / 毛中特的知识点切成卡片，按遗忘曲线提醒我复习。

## 经典报错现场

```
pip install django-celery-beat
→ ERROR: Cannot install django-celery-beat because these package versions have conflicting dependencies.
→ The conflict is caused by:
    The user requested django==4.2
    django-celery-beat 2.5.0 depends on django>=3.2
```

看起来冲突信息很绕，实际上是我本地已经装了某个包把 Django 顶到了更高的版本，而 celery-beat 只认 3.2-4.2。

## 解决过程

- 先 `pip show django` 看当前版本 → 发现被某个依赖顶到了 5.0。
- 再 `pip install "django==4.2.*"` 锁版本，重装 celery-beat → 通了。
- 事后才学会：以后凡是这种 dependency conflict，第一步永远是 `pip show <那个被点名的包>`，不要瞎猜。

## 另一个大坑：UnicodeDecodeError

- 读自己写的中文 markdown 知识点文件时，Python 报 `UnicodeDecodeError: 'gbk' codec can't decode byte 0x94`。
- 原因：Windows 上 open() 默认用 gbk，我的 md 文件是 UTF-8。
- 修复：所有 open() 一律加 `encoding="utf-8"`。这条后来写进了 debug-workflow。
