# Documentation images

## Exercise and first-run previews

- `overview.en.svg` and `overview.zh-CN.svg` are the compact, horizontal overview used on the project homepage: recorded merit, pending review and role observations. Rebuild both with `python -B docs/examples/build_overview.py` from the repository root. The renderer checks the six sample hashes and the same fictional exercise input before writing the figures.
- `exercise-preview.en.svg` and `exercise-preview.zh-CN.svg` show the fictional local exercise documents and selected input context. Sources, line-ending-normalized hashes and the standard-library renderer are in [examples](../examples/README.md).
- `first-run.en.svg` and `first-run.zh-CN.svg` show the verified ZIP-based local route: extract, run one command, open the three documents. See the [first-run guide](../quickstart.md).
- These figures describe local documentation and fictional data; they are not GrokBot interface screenshots.

横版概览和原有长版成果图，以公开样张和同轮虚构输入为依据重新组织内容，并非周报或岗位观察的逐字截图；检查清单细节来自同轮构建员战报。首次试跑图对应已验证的 ZIP 路线。六张图均为可编辑的文字矢量图，旧长图和首次操作图继续保留。

## Author contact images

The two QR images are reused byte for byte from Situk's existing public project:

| File | Purpose | Public source | SHA256 |
|---|---|---|---|
| situk-wechat.png | Add the author on WeChat | [Original](https://github.com/situker/situk-yangtao-perspective/blob/main/docs/situk-wechat.png) | c7d692e75db680e565f4d40e163f33c6b4709834292f269d8d42a4ad640afb86 |
| situk-gongzhonghao.png | WeChat Official Account: 司徒K | [Original](https://github.com/situker/situk-yangtao-perspective/blob/main/docs/situk-gongzhonghao.png) | a64d60b2d2438a787dff7de70931de7f271847f886d4d0a62105d451ebfae325 |

Source checked on 2026-10-26. The images were not regenerated or edited. Their published identity and image integrity were checked; scanning them in WeChat was not part of this check.

两张图分别用于微信好友和公众号，复用作者已有公开原图，未重绘或修改二维码。核对了公开来源与文件校验值，未实扫验证。
