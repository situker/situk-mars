# Documentation images

## Panda illustrations / 红鼻熊猫配图

The bilingual homepages and guides use three project illustrations, each with separate Chinese and English labels:

| Files | Content |
|---|---|
| `overview.en.png`, `overview.zh-CN.png` | The panda reads a bamboo ledger beside merit, pending-review and reuse previews |
| `team-architecture.en.png`, `team-architecture.zh-CN.png` | Human approval, independent merit review, formal recording and reconciliation |
| `rank-path.en.png`, `rank-path.zh-CN.png` | Ten ordinary ranks and the separate Marshal appointment |

The artwork combines Situk's red-nosed panda, ink and watercolor on ivory paper, and bamboo AI tools. Labels and connectors are laid out separately and checked against the published samples and rules. These are illustrated explanations, not platform screenshots. The original character sheets and production prompts are not included in this repository.

首页与说明页统一使用红鼻熊猫配图：米白纸纹、水墨功夫服、朱红腰带与青绿竹木 AI 机关。角色、图表和留白随内容安排；文字、数字与箭头单独排版，按公开样张和规则核对。下方保留的 SVG 为纯矢量参考版，制图脚本不会重建熊猫插画。

## Exercise and first-run previews

- `overview.en.svg` and `overview.zh-CN.svg` are the plain vector overview: recorded merit, pending review and role observations. Rebuild both with `python -B docs/examples/build_overview.py` from the repository root. The renderer checks the six sample hashes and the same fictional exercise input before writing the figures.
- `exercise-preview.en.svg` and `exercise-preview.zh-CN.svg` show the fictional local exercise documents and selected input context. Sources, line-ending-normalized hashes and the standard-library renderer are in [examples](../examples/README.md).
- `first-run.en.svg` and `first-run.zh-CN.svg` show the verified ZIP-based local route: extract, run one command, open the three documents. See the [first-run guide](../quickstart.md).
- These figures describe local documentation and fictional data; they are not GrokBot interface screenshots.

纯矢量横版概览和原有长版成果图，以公开样张和同轮虚构输入为依据重新组织内容，并非周报或岗位观察的逐字截图；检查清单细节来自同轮构建员战报。首次试跑图对应已验证的 ZIP 路线。这六份 SVG 保留可编辑文字，旧长图和首次操作图继续保留。

## Team architecture and rank progression

- `team-architecture.en.svg` and `team-architecture.zh-CN.svg` explain reporting, independent review, human approval, formal recording and reconciliation. They summarize the [architecture guide](../architecture.md).
- `rank-path.en.svg` and `rank-path.zh-CN.svg` show the ten ordinary ranks and the separate Marshal appointment. Exact points, full weeks at the current rank, acceptance requirements and seat rules are in the [rank guide](../ranks.md) and the language pack's `policy.json`.
- Rebuild all four with `python -B docs/examples/build_explainers.py` from the repository root. The renderer reads the published policies only; it does not connect to GrokBot or change any runtime data.

纯矢量架构图说明谁核、谁批、谁记；军衔图展示普通阶梯和独立特授。它们是可编辑的制度解释图，不是产品界面。首页展示同一规则下的熊猫 PNG 版，专页保留完整说明。

## Author contact images

The two QR images are reused byte for byte from Situk's existing public project:

| File | Purpose | Public source | SHA256 |
|---|---|---|---|
| situk-wechat.png | Add the author on WeChat | [Original](https://github.com/situker/situk-yangtao-perspective/blob/main/docs/situk-wechat.png) | c7d692e75db680e565f4d40e163f33c6b4709834292f269d8d42a4ad640afb86 |
| situk-gongzhonghao.png | WeChat Official Account: 司徒K | [Original](https://github.com/situker/situk-yangtao-perspective/blob/main/docs/situk-gongzhonghao.png) | a64d60b2d2438a787dff7de70931de7f271847f886d4d0a62105d451ebfae325 |

Source checked on 2026-10-26. The images were not regenerated or edited. Their published identity and image integrity were checked; scanning them in WeChat was not part of this check.

两张图分别用于微信好友和公众号，复用作者已有公开原图，未重绘或修改二维码。核对了公开来源与文件校验值，未实扫验证。
