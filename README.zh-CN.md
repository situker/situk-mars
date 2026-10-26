# situk-MARS｜军衔制机器人组织系统

**给机器人团队立军衔，按贡献论功行赏。**

给已有多个机器人的 GrokBot 团队，一套军功、授衔与周报 Skill。把散落在聊天里的交付和采用记录，整理成**军功周报、待复核清单、团队岗位观察**，让你看清谁做成了什么、还有哪些事情需要决定。

军务官独立核功，奖赏和晋衔由你拍板。先用虚构团队跑一轮，再决定怎样接入自己的机器人。

**[下载中文 ZIP](https://github.com/situker/situk-mars/releases/download/v0.2.0/situk-mars-v0.2.0-zh-CN.zip) · [先看周报样张](docs/examples/zh-CN/weekly-report.md) · [首次试跑指南](docs/quickstart.zh-CN.md) · [English](README.md)**

MIT 开源 · 中英双语 · 文档 Skill 与九份模板 · 可选本地 Python 核算器

英文全名：Situk Merit-based Agent Rank System，简称 **MARS**。

## 先看跑完会得到什么

一项虚构的协同指南中，主笔完成说明，构建员完成核对清单。两部分作为同一成果被模拟采用，共分 3 分：主笔 1.80、构建员 1.20。这两笔份额计入下面周报中的正式累计。

![虚构演练生成的军功周报、待复核清单和团队岗位观察预览](docs/assets/exercise-preview.zh-CN.svg)

*图中内容取自仓库固定虚构演练，是三份文档与同轮输入的整理预览。*

| 三份结果 | 打开后看什么 | 完整样张 |
|---|---|---|
| **军功周报** | 已记军功、普通军衔和特授 | [查看周报](docs/examples/zh-CN/weekly-report.md) |
| **待复核清单** | 缺什么证据，哪些待批准，哪些已批未登记 | [查看待办](docs/examples/zh-CN/pending-review.md) |
| **团队岗位观察** | 哪些资产可复用，哪里重复劳动，哪些职责需要再看 | [查看观察](docs/examples/zh-CN/team-observations.md) |

演练中，主笔记 4.80 分，经单独模拟批准升为上等兵；构建员记 9.20 分，仍为列兵。军务官一项已批未登记的 1 分未计入总分。**分数、候选、批准和正式登记分别记录。**

## 下载后先试一轮

下载得到一个 `situk-mars` 文件夹，里面有 `SKILL.md`、制度细则、九份模板、虚构输入，以及可选核算与演练脚本。下面两条路径**任选一条**；固定演练无需先配置真实团队。

### 路径 A：在本地跑出同样的文档

需要 Python 3.11+，使用标准库。演练无需账号、密钥或联网。

![下载语言包、解压后运行一条命令、打开三份结果的首次试跑操作图](docs/assets/first-run.zh-CN.svg)

1. [下载中文 ZIP](https://github.com/situker/situk-mars/releases/download/v0.2.0/situk-mars-v0.2.0-zh-CN.zip)，解压后进入其中的 `situk-mars` 文件夹。
2. 在这个文件夹打开终端，复制这一条命令：

```bash
python -B scripts/simulate.py --output ../mars-demo-new
```

3. 看到 `SIMULATION_PASSED` 后，打开旁边新生成的 `mars-demo-new` 文件夹，先读 `06-军功周报.md`，再看 `06-待复核清单.md` 和 `06-团队岗位观察.md`。

Linux/macOS 可把 `python` 改为 `python3`。**不要提前创建 `mars-demo-new`**；它须位于 Skill 文件夹之外，且最后一级目录尚不存在。重跑时换一个输出目录名，保留原结果。[完整试跑说明](docs/quickstart.zh-CN.md)。

### 路径 B：让 GrokBot 按文档演练

把完整解压文件夹放到你的 GrokBot 当前能读取的位置，提供 `SKILL.md` 的实际路径，再发送：

> 读取这份 situk-MARS Skill，先在当前对话中用虚构机器人和模拟批准完整演练报功、核功、人类批准、记功、授衔和周报。最后给出军功周报、待复核清单和团队岗位观察。所有材料明确标注演练；不读取真实花名册，不安装 Skill，不创建或修改机器人，不动 routine。若不能读取完整文件夹或执行某一步，说明缺口，不声称已完成。

这条路径取决于当前 GrokBot 宿主的文件读取与输出能力；无需假定它可以执行 Python。若不能提供完整文件读取，使用路径 A。[GrokBot 读取与交接说明](docs/quickstart.zh-CN.md)。

## 一笔军功怎样记下来

**报功 → 核功 → 人类批准 → 记功 → 授衔 → 周报**

业务机器人提交具体交付、验收和采用依据。军务官核查重复成果、协作份额、每周获奖上限和利益冲突。你批准具体事项后，统筹者登记正式账目；达到晋衔条件时先列候选，具体晋升另行批准。

| 角色 | 职责 |
|---|---|
| **人类负责人：你** | 定业务目标、采纳规则，最终批准军功、晋衔和特授 |
| **统筹者（Commander）** | 归集战报，保留原始版本，按有效批准登记正式账目 |
| **军务官（Merit Officer）** | 独立核功和对账，整理周报；本人或双方共同关联事项交人类处理 |
| **业务机器人** | 在原岗位交付、报功，并补齐证据 |

**元帅是另行特授的头衔。** 人类可任命统筹者为元帅，全队最多一席。它与岗位和普通军衔分别记录，不赠分、不重置普通军衔的任职时间，也不增加自批权。

<details>
<summary>展开角色、流程与文档架构图</summary>

![situk-MARS 角色、流程与文档架构](docs/assets/architecture.zh-CN.svg)

[阅读完整架构说明](docs/architecture.zh-CN.md)

</details>

## 规则怎样管住重复记功

| 规则 | 默认做法 |
|---|---|
| 五档军功 | 嘉奖 1、三等功 3、二等功 8、一等功 20；荣誉对独立新成果可记 50，已获奖旧成果只授称号 |
| 同一成果只有一个分池 | 协作者按证据分摊，按固定规则分配小数余分 |
| 每个机器人每周有获奖上限 | 嘉奖 2 次、三等功 2 次、二等功 1 次、一等功 1 次；超出部分实记 0，不转给他人、不降档、不顺延 |
| 迟报仍用原周 | 按首次合格交付所属周核算；周期为 Asia/Singapore 周一 00:00 至下周一 00:00 |
| 十级普通军衔 | 列兵至中校；积分、当前军衔的完整任职周数和额外条件只产生候选，授衔另批 |
| 批准与记功分开 | 只计已批准且已登记的分数；重复执行同一决定不会重复奖赏 |

完整门槛、回避和更正规则见[制度细则](skills/zh-CN/situk-mars/references/rules.md)。正式使用入口是 [SKILL.md](skills/zh-CN/situk-mars/SKILL.md)。中英两包的 Skill ID 都是 `situk-mars`，同一环境只选一种。

## 演练之后，再接入自己的团队

正式接入时，再确定人类负责人、业务目标、授权资料目录、新军功起算日和现有角色绑定。职责缺位由人类先承接，岗位观察优先考虑现有人员和资产，建岗另作决定。

当前版本支持 **GrokBot 文档工作流**和本地核算。真实平台改名、建机器人、向其他机器人安装 Skill、平台权限隔离和 routine 配置需要各自的接入与授权，本版没有自动实现。

事实要打开来源核查，真实批准要保留人类原始依据。脚本不认证真人，也不提供持久化生产账本服务；复杂更正、撤奖、处分、破格和元帅撤换按模板交人类处理。军衔为自拟管理称呼，不对应真实国家军衔、薪酬或现金奖励。

## 验证与文档

同一套 **62 项规则测试**已在中英文包中分别通过；Linux／Windows、Python 3.11／3.13 四组远端检查也已通过。这些验证覆盖规则和虚构流程，不能当作真实业务成效。

[验证记录](docs/validation.zh-CN.md) · [GitHub Actions](https://github.com/situker/situk-mars/actions) · [项目介绍](docs/introduction.zh-CN.md) · [全部演练样张](docs/examples/README.md) · [发行页与校验文件](https://github.com/situker/situk-mars/releases/tag/v0.2.0)

## 作者与交流

**司徒K｜企业服务创业者**

**用 AI 做生意，用创造富养好奇心。**

长期从事互联网创业，目前重点做 GEO 和企业 AI 落地。我喜欢把方法做成工具，把想法做成作品，也分享实践中的判断与踩过的坑。

欢迎聊机器人团队、Skill 和企业 AI 落地。有相关需求，可以带着业务背景和具体问题交流。[更多介绍与合作方向](docs/about-author.zh-CN.md)。

公众号／全网 ID：**司徒K** · X：[@situking](https://x.com/situking) · 个人网站：[www.situking.com](https://www.situking.com) · [GitHub](https://github.com/situker)

<table>
<tr>
<td align="center" width="50%">
  <img src="docs/assets/situk-wechat.png" alt="司徒K的微信好友二维码" width="200" />
  <br /><strong>微信交流</strong><br />带上你的业务背景和具体问题
</td>
<td align="center" width="50%">
  <img src="docs/assets/situk-gongzhonghao.png" alt="公众号司徒K的二维码" width="200" />
  <br /><strong>公众号：司徒K</strong><br />AI 实践、工具与作品
</td>
</tr>
</table>

## 开源许可

Copyright © 2026 **司徒K（Situk）**。项目采用 [MIT 许可证](LICENSE)。
