"""Build bilingual role and rank diagrams from the local 0.2.0 policy.

Run ``python -B docs/examples/build_explainers.py`` from the repository root.
This standard-library documentation renderer never runs the merit engine,
connects to a service, or changes bots, permissions, or routines.
"""

from html import escape
import json
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "docs" / "assets"
POLICIES = {
    language: json.loads((ROOT / "skills" / language / "situk-mars" / "policy.json").read_text(encoding="utf-8"))
    for language in ("en", "zh-CN")
}

COPY = {
    "en": {
        "architecture_title": "Human approval, independent review, one formal recorder",
        "architecture_desc": (
            "Business bots deliver work and report evidence to the Commander. "
            "The Commander preserves versioned reports for the Merit Officer's "
            "independent review. The officer sends proposals and weekly reports "
            "to the Human Owner. Only the owner approves exact awards and separate "
            "rank changes. The Commander alone records approved changes in the "
            "formal ledger; the Merit Officer reads that ledger independently "
            "to reconcile it. Marshal is a separate human appointment for zero "
            "or one Commander, without points or self-approval authority."
        ),
        "owner": "Human Owner",
        "owner_detail": "Final award / rank approval",
        "commander": "Commander",
        "commander_detail": "Sole formal recorder",
        "commander_sub": "Keep original reports",
        "officer": "Merit Officer",
        "officer_detail": "Independent merit review",
        "officer_sub": "Reconcile; escalate conflicts",
        "bots": "Business bots",
        "bots_detail": "Deliver work and evidence",
        "ledger": "Ledger and rank records",
        "ledger_detail": "Approved changes only",
        "approval": "Approve exact items",
        "proposal": "Proposals and weekly report",
        "reports": "Original versioned reports",
        "deliver": "Deliver / report",
        "record": "Record approved items",
        "reconcile": "Independent ledger read-back",
        "marshal": "Marshal · 0–{seats} special seat",
        "marshal_who": "Human-appointed Commander",
        "marshal_effect": "No points or self-approval",
        "architecture_footer": "Document workflow · Local helpers calculate; evidence and human approval remain required.",
        "ranks_title": "Ten ordinary ranks, one separate special appointment",
        "ranks_condition": "Applicable points, full weeks, acceptance and other conditions → candidate; separate human approval → promotion.",
        "selection": "Major / Lieutenant Colonel: approved seats and human selection; no automatic point threshold for Lieutenant Colonel.",
        "marshal_label": "Special appointment",
        "marshal_scope": "0–{seats} seats · Commander only · Human appointment",
        "marshal_separate": "No points or self-approval; ordinary rank and its clock stay unchanged.",
        "ranks_desc": (
            "Ten ordinary ranks in policy order: Private, Private First Class, "
            "Corporal, Sergeant, Staff Sergeant, Second Lieutenant, First Lieutenant, "
            "Captain, Major and Lieutenant Colonel. Applicable points, completed "
            "full weeks in the current rank, acceptance requirements and other "
            "relevant rule conditions create candidates, not automatic "
            "promotions. Each promotion requires separate human approval. Major "
            "and Lieutenant Colonel also require approved seats and human "
            "selection; Lieutenant Colonel has no automatic point threshold. "
            "Marshal is a separate zero-to-one human appointment for the Commander. "
            "It adds no points, changes neither ordinary rank nor its time clock, "
            "and grants no self-approval. These are management titles, not real "
            "military status. Full requirements remain in the rules."
        ),
    },
    "zh-CN": {
        "architecture_title": "人类批准，独立核功，唯一正式登记",
        "architecture_desc": (
            "业务机器人将交付及证据报给统筹者，统筹者保留有版本的原始战报，"
            "交军务官独立核功。军务官将提案和周报交给人类负责人。奖赏与另行"
            "晋衔均由人类最终批准；统筹者是唯一正式登记者，只追加已批准变更。"
            "军务官从正式流水独立回读对账。元帅是仅授统筹者的零至一席人类"
            "特授头衔，不加分，不产生自批权。"
        ),
        "owner": "人类负责人",
        "owner_detail": "最终批准：奖赏与另行晋衔",
        "commander": "统筹者",
        "commander_detail": "唯一正式登记者",
        "commander_sub": "归集报功 · 保留来源",
        "officer": "军务官",
        "officer_detail": "独立核功 · 对账",
        "officer_sub": "本人关联事项回避",
        "bots": "业务机器人",
        "bots_detail": "交付与证据 · 提交报功",
        "ledger": "正式流水与军衔记录",
        "ledger_detail": "只保存已批准变更",
        "approval": "批准具体事项",
        "proposal": "提案与周报",
        "reports": "保留原始战报及版本",
        "deliver": "交付 / 报功",
        "record": "登记已批准项",
        "reconcile": "回读正式流水，独立对账",
        "marshal": "元帅特授 · 0–{seats} 席",
        "marshal_who": "仅统筹者 · 人类任命",
        "marshal_effect": "不加分 · 不产生自批权",
        "architecture_footer": "文档工作流 · 可选脚本只做核算，真实证据与人类批准仍须保留",
        "ranks_title": "普通十级逐阶，元帅单独特授",
        "ranks_condition": "适用的积分、完整在阶周、验收与其他条件 → 候选；晋衔另经人类批准。",
        "selection": "少校、中校另须批准席位与人类选升；中校不设自动分数门槛。",
        "marshal_label": "与普通阶梯分开",
        "marshal_scope": "0–{seats} 席 · 仅统筹者 · 人类任命",
        "marshal_separate": "不加分、不自批，不改变普通军衔与在阶起算。",
        "ranks_desc": (
            "普通军衔按顺序为列兵、上等兵、下士、中士、上士、少尉、中尉、上尉、"
            "少校、中校。适用的积分、当前军衔完整在阶周、验收要求及其他规则条件只产生候选，"
            "每次晋衔仍须另经人类批准。少校和中校另须已批准席位及人类选升；"
            "中校不设自动分数门槛。元帅独立设零至一席，仅由人类特授统筹者，"
            "不加分，不改变普通军衔与在阶起算，不产生自批权。图中称呼为管理"
            "头衔，不代表真实军事身份；完整条件仍以规则为准。"
        ),
    },
}


class Figure:
    def __init__(self, height, title, description):
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>',
            f'<desc id="desc">{escape(description)}</desc>',
            '<style>text{font-family:"Segoe UI","Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#18332e}.heading{font-weight:700}.muted{fill:#536760}.green{fill:#126650}.amber{fill:#80551a}</style>',
            '<defs><marker id="arrow-green" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#126650"/></marker><marker id="arrow-muted" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#6a7d74"/></marker><marker id="arrow-amber" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a07031"/></marker></defs>',
            f'<rect width="1200" height="{height}" rx="20" fill="#f2f6f4"/>',
        ]

    def text(self, x, y, value, size=22, cls="", anchor=None):
        assert 0 <= x <= 1200 and 0 < y < self.height, (x, y, value)
        alignment = f' text-anchor="{anchor}"' if anchor else ""
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}"{alignment}>{escape(value)}</text>')

    def box(self, x, y, width, height, special=False):
        fill, stroke = ("#fff4df", "#d6b77f") if special else ("#ffffff", "#cad8d1")
        self.parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="14" fill="{fill}" stroke="{stroke}"/>')

    def arrow(self, points, color="green", dashed=False):
        stroke = {"green": "#126650", "muted": "#6a7d74", "amber": "#a07031"}[color]
        dash = ' stroke-dasharray="7 5"' if dashed else ""
        self.parts.append(f'<polyline points="{points}" fill="none" stroke="{stroke}" stroke-width="2" stroke-linejoin="round" marker-end="url(#arrow-{color})"{dash}/>')

    def write(self, basename, language):
        contents = "\n".join([*self.parts, "</svg>"]) + "\n"
        ET.fromstring(contents)
        target = ASSETS / f"{basename}.{language}.svg"
        target.write_text(contents, encoding="utf-8", newline="\n")
        print(target.relative_to(ROOT))


def architecture(language):
    t = COPY[language]
    f = Figure(520, t["architecture_title"], t["architecture_desc"])
    f.arrow("490,128 490,168 204,168 204,202")
    f.arrow("996,202 996,168 710,168 710,128", "amber")
    f.arrow("376,260 824,260", "muted")
    f.arrow("204,386 204,318", "muted")
    f.arrow("332,318 332,356 600,356 600,386")
    f.arrow("764,433 792,433 792,346 996,346 996,318", "muted", dashed=True)

    f.box(438, 24, 324, 104)
    f.text(600, 64, t["owner"], 28, "heading", "middle")
    f.text(600, 100, t["owner_detail"], 20, "green", "middle")
    f.box(32, 202, 344, 116)
    f.text(56, 240, t["commander"], 28, "heading")
    f.text(56, 276, t["commander_detail"], 22, "green")
    f.text(56, 302, t["commander_sub"], 20, "muted")
    f.box(824, 202, 344, 116)
    f.text(848, 240, t["officer"], 28, "heading")
    f.text(848, 276, t["officer_detail"], 22, "green")
    f.text(848, 302, t["officer_sub"], 20, "muted")
    f.box(32, 386, 344, 94)
    f.text(56, 425, t["bots"], 26, "heading")
    f.text(56, 459, t["bots_detail"], 20, "muted")
    f.box(440, 386, 324, 94)
    f.text(602, 425, t["ledger"], 22, "heading", "middle")
    f.text(602, 459, t["ledger_detail"], 20, "muted", "middle")
    f.box(824, 386, 344, 94, special=True)
    f.text(848, 414, t["marshal"].format(seats=POLICIES[language]["seat_limit"]), 23, "heading amber")
    f.text(848, 443, t["marshal_who"], 19, "amber")
    f.text(848, 469, t["marshal_effect"], 20, "muted")

    f.text(340, 155, t["approval"], 20, "green", "middle")
    f.text(853, 155, t["proposal"], 20, "amber", "middle")
    f.text(600, 246, t["reports"], 20, "muted", "middle")
    f.text(192, 361, t["deliver"], 20, "muted", "end")
    f.text(466, 344, t["record"], 20, "green", "middle")
    f.text(996, 373, t["reconcile"], 19, "muted", "middle")
    f.text(600, 508, t["architecture_footer"], 18, "muted", "middle")
    f.write("team-architecture", language)


def rank_lines(label, language):
    if language == "en" and len(label) > 13:
        words = label.split()
        return [words[0], " ".join(words[1:])]
    return [label]


def rank_path(language):
    t, policy = COPY[language], POLICIES[language]
    f = Figure(400, t["ranks_title"], t["ranks_desc"])
    f.text(32, 40, t["ranks_title"], 30, "heading")
    f.text(32, 70, t["ranks_condition"], 20, "muted")
    xs = [32, 264, 496, 728, 960]
    for y in (126, 234):
        for x in xs[:-1]:
            f.arrow(f"{x + 208},{y} {x + 232},{y}", "muted")
    f.arrow("1168,126 1184,126 1184,180 16,180 16,234 32,234", "muted")
    labels = policy.get("rank_labels", {})
    for i, canonical in enumerate(policy["rank_order"]):
        x, y = xs[i % 5], 94 if i < 5 else 202
        f.box(x, y, 208, 64, special=canonical in ("少校", "中校"))
        label = labels.get(canonical, canonical)
        lines = rank_lines(label, language)
        size = 24 if language == "en" else 26
        baseline = y + 27 if len(lines) == 2 else y + 42
        for j, line in enumerate(lines):
            f.text(x + 104, baseline + j * 25, line, size, "heading", "middle")
    f.text(32, 300, t["selection"], 20, "amber")
    f.box(32, 322, 1136, 60, special=True)
    f.text(56, 350, labels.get("元帅", "元帅特授"), 26, "heading amber")
    f.text(56, 375, t["marshal_label"], 18, "amber")
    f.text(350, 348, t["marshal_scope"].format(seats=policy["seat_limit"]), 20, "amber")
    f.text(350, 374, t["marshal_separate"], 20, "muted")
    f.write("rank-path", language)


def validate_policies():
    en, zh = POLICIES["en"], POLICIES["zh-CN"]
    for key in ("rule_version", "rank_order", "rank_thresholds", "seat_limit"):
        assert en[key] == zh[key], key
    assert zh["rule_version"] == "0.2.0"
    assert len(zh["rank_order"]) == 10
    assert zh["rank_order"][-2:] == ["少校", "中校"]
    assert zh["rank_thresholds"]["中校"] == {"weeks": None, "points": None}
    assert zh["seat_limit"] == 1
    assert all(key in en["rank_labels"] for key in [*zh["rank_order"], "元帅"])


if __name__ == "__main__":
    validate_policies()
    for language in COPY:
        architecture(language)
        rank_path(language)
