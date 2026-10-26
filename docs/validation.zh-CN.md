# v0.2.0 验证记录

验证日期：2026-10-26。[English](validation.md)。

## 发布前核对的依据

冻结的中文 0.2.0 规则已通过本地 62 项回归测试及三次虚构演练。GrokBot 另行复核并运行了同样的 62 项测试和六阶段模拟。我们核对了它回传的源码清单和 15 份演练文件，并独立重算账目，没有发现需要修改数值规则的阻断问题。

这里记录的是已检查的复核材料，不代表认证了 GrokBot 的执行环境。公开分发包不含私人交接日志、真实机器人身份和本机工作区路径。

## 本次双语公开版检查

- 中英文包分别通过同一套 62 项规则测试。它们是 **62 个独立用例在两包中各跑一次**，不是 124 个不同规则用例。
- 两包均按默认语言完成六阶段虚构演练：主笔 4.80 分、构建员 9.20 分、统筹与军务官正式分均为零。
- 四个事件形成五笔个人记功。协同成果只分一个 3 分池，分为 1.80／1.20；超帽项目实记零，已批未登记的 1 分不进入正式累计。
- 主笔在取得独立的模拟晋衔决定后才获上等兵。英文目标显示名使用英文军衔，机器记录保留兼容的中文军衔键。
- 特授元帅增加零分，普通军衔的在阶起算不变；重复记功与重复授衔均被阻止。
- 两包的 Python 文件和操作性政策一致，仅展示文案、默认语言和英文军衔名称不同。
- 离线分发校验检查许可、本地文档链接、模板数量、SVG 语法及常见私人数据模式。扫描配合人工复核使用，不能保证发现所有可能的秘密信息。
- 独立下载包包含完整 Skill、MIT 许可和文件校验清单，另提供两包下载校验值。

GitHub Actions 将在 Linux、Windows 和 Python 3.11、3.13 的组合下重复规则测试、分发检查和双语模拟。实际结果以 [Actions](https://github.com/situker/situk-mars/actions) 为准；本文不预先宣称远端运行成功。

## 本地复现

从仓库根目录运行：

```bash
python -B tools/validate_release.py
python -B -m unittest discover -s skills/zh-CN/situk-mars/tests -p test_merit_engine.py
python -B -m unittest discover -s skills/en/situk-mars/tests -p test_merit_engine.py
python -B skills/zh-CN/situk-mars/scripts/simulate.py --output .local/check-zh
python -B skills/en/situk-mars/scripts/simulate.py --output .local/check-en
python -B tools/build_packages.py
```

部分系统需改用 `python3`。模拟输出目录必须是 Skill 源码以外的新目录，最后一级目录不要提前创建。

## 这些检查的范围

演练采用虚构机器人、合成证据和程序生成的人类决定。它不能证明真实采用、认证真人、验证平台权限隔离或部署生产账本服务。没有创建、安装、改名或修改真实机器人，没有变更 routine。复杂冲正、处分和破格晋衔仍按人工模板处理。
