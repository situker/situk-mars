<h1 align="center">situk-MARS</h1>

<p align="center">
  <strong>给机器人团队立军衔，按贡献论功行赏。</strong><br />
  军衔制机器人组织系统 · GrokBot Skill
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-126650" alt="MIT 许可证" /></a>
  <a href="https://github.com/situker/situk-mars/releases/tag/v0.2.0"><img src="https://img.shields.io/badge/release-v0.2.0-126650" alt="发行版 v0.2.0" /></a>
  <a href="https://github.com/situker/situk-mars/actions/workflows/ci.yml"><img src="https://github.com/situker/situk-mars/actions/workflows/ci.yml/badge.svg?branch=main" alt="双语规则验证" /></a>
</p>

<p align="center">
  <a href="https://github.com/situker/situk-mars/releases/download/v0.2.0/situk-mars-v0.2.0-zh-CN.zip"><strong>下载中文 ZIP</strong></a> ·
  <a href="docs/examples/README.zh-CN.md">看演练样张</a> ·
  <a href="docs/quickstart.zh-CN.md">试跑指南</a> ·
  <a href="README.md">English</a>
</p>

机器人越来越多，交付和采用记录却散在聊天里。MARS 给已有多个机器人的 GrokBot 团队，一套**报功、核功、奖赏与授衔机制**，每轮汇成三份文档：看清已记贡献、待决定事项和可复用成果。

## 先看一轮成果

![一轮虚构演练的三份文档概览：军功记录、待复核和岗位观察](docs/assets/overview.zh-CN.svg)

主笔记 **4.80 分**，经另行模拟批准升上等兵；构建员记 **9.20 分**，仍为列兵。晋衔同时看积分、任职时间与额外条件，并须另行批准。图中全部为虚构演练，内容取自三份样张及同轮输入。

打开完整样张：**[军功周报](docs/examples/zh-CN/weekly-report.md)** · **[待复核清单](docs/examples/zh-CN/pending-review.md)** · **[团队岗位观察](docs/examples/zh-CN/team-observations.md)**

## 三步跑出第一份周报

需要 **Python 3.11+**，只用标准库。固定虚构演练无需账号、密钥或真实机器人资料，下载后可离线运行。

1. [下载中文 ZIP](https://github.com/situker/situk-mars/releases/download/v0.2.0/situk-mars-v0.2.0-zh-CN.zip)，解压，进入其中的 **`situk-mars` 文件夹**。
2. 在这个文件夹打开终端，运行：

   ```bash
   python -B scripts/simulate.py --output ../mars-demo-new
   ```

3. 看到 **`SIMULATION_PASSED`** 后，打开相邻的新文件夹 `mars-demo-new`。先读 `06-军功周报.md`，再看 `06-待复核清单.md` 和 `06-团队岗位观察.md`。

输出目录不要提前创建；重跑时换一个新名字。部分系统需用 `python3`。[查看操作图与完整说明](docs/quickstart.zh-CN.md)。

也可[让 GrokBot 按文档演练](docs/quickstart.zh-CN.md#路线-b让-grokbot-在对话中演练)，前提是当前宿主能读取完整 Skill 文件夹。ZIP 内含 `SKILL.md`、制度细则、九份模板、虚构输入和可选 Python 核算器。

## 怎样论功行赏

**报功 → 核功 → 人类批准 → 记功 → 授衔 → 周报**

| 你关心的事 | MARS 的做法 |
|---|---|
| 谁做成了什么 | 业务机器人提交交付、验收与采用依据；同一成果只有一个分池，协作按贡献分摊 |
| 谁核、谁批、谁记 | 军务官独立核功，人类负责人最终批准，统筹者按有效批准登记正式账目 |
| 何时可以晋衔 | 积分、任职时间与额外条件共同产生候选，晋衔另行批准；已批未登记不计入正式累计 |

**元帅另行特授，全队最多一席。** 人类可任命统筹者为元帅：不赠分、不重置普通军衔的任职时间，不增加自批权。岗位、普通军衔和特授分别记录。

五档军功、每周上限、回避、迟报与更正等规则，见[制度细则](skills/zh-CN/situk-mars/references/rules.md)。

## 接入自己的团队

先看完演练，再确定人类负责人、业务目标、授权资料范围、军功起算日和现有角色绑定，手动跑通一轮。岗位观察优先考虑复用现有人员与资产，是否补岗由人类决定。

当前版本支持 **GrokBot 文档工作流与本地核算**。真实平台的建机器人、改名、权限隔离和 routine 配置需要另行接入。脚本不核验真实证据、不认证真人批准，也不提供持久化生产账本服务。[接入说明与使用边界](skills/zh-CN/situk-mars/references/grokbot-usage.md)。

## 文档与验证

| 继续了解 | 入口 |
|---|---|
| 角色分工和流程 | [架构图](docs/architecture.zh-CN.md) · [项目介绍](docs/introduction.zh-CN.md) |
| 完整工作指令 | [SKILL.md](skills/zh-CN/situk-mars/SKILL.md) · [九份模板](skills/zh-CN/situk-mars/templates) |
| 测试与下载校验 | [验证记录](docs/validation.zh-CN.md) · [发行页与校验文件](https://github.com/situker/situk-mars/releases/tag/v0.2.0) |
| 问题与建议 | [提交 Issue](https://github.com/situker/situk-mars/issues) |

中英两包分别通过同一套 **62 项规则测试**，CI 覆盖 Linux／Windows、Python 3.11／3.13。验证针对规则和虚构流程。两包共用 Skill ID `situk-mars`，同一环境只选一种语言。

## 作者与交流

**司徒K｜企业服务创业者** · 用 AI 做生意，用创造富养好奇心。

目前重点做 GEO 和企业 AI 落地，把方法做成工具，把想法做成作品，也分享实践中的判断与踩过的坑。[更多介绍与合作方向](docs/about-author.zh-CN.md)。

公众号／全网 ID：**司徒K** · [X：@situking](https://x.com/situking) · [个人网站](https://www.situking.com) · [GitHub](https://github.com/situker)

<table>
  <tr>
    <td align="center" width="50%">
      <img src="docs/assets/situk-wechat.png" alt="司徒K的微信好友二维码" width="160" /><br />
      <strong>微信交流</strong><br />带上业务背景和具体问题
    </td>
    <td align="center" width="50%">
      <img src="docs/assets/situk-gongzhonghao.png" alt="公众号司徒K的二维码" width="160" /><br />
      <strong>公众号：司徒K</strong><br />AI 实践、工具与作品
    </td>
  </tr>
</table>

**MARS** = Situk Merit-based Agent Rank System。Copyright © 2026 司徒K（Situk），采用 [MIT 许可证](LICENSE)。
