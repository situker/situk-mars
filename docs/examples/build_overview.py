"""Build the compact README overview from checked, fictional exercise samples.

This renderer reads local documentation only. It does not run the merit engine,
connect to GrokBot, or change bots or routines. Run with ``python -B
docs/examples/build_overview.py`` from the repository root.
"""

from hashlib import sha256
from html import escape
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from build_preview import check_samples


HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"

COPY = {
    "en": {
        "title": "One exercise, three useful documents",
        "scope": "6 fictional reports",
        "records": "Merit records",
        "writer": "Writer",
        "builder": "Builder",
        "promotion": "Writer: separate rank approval",
        "pending": "Pending review",
        "evidence": "Adoption evidence missing",
        "unrecorded": "1 point approved, unposted",
        "outside": "Outside recorded totals",
        "observations": "Role observations",
        "checklist": "Accepted checklist",
        "reuse": "Reuse first",
        "no_creation": "No automatic role creation",
        "footer": "Fictional exercise · Document preview",
        "description": (
            "A compact preview of three fictional exercise documents. "
            "Recorded totals: Example Writer 4.80 and Example Builder 9.20. "
            "The writer receives Private First Class only after a separate "
            "simulated approval. Pending items include missing adoption "
            "evidence and the Merit Officer's approved but unrecorded 1 point; "
            "neither adds to recorded totals. Reuse the accepted checklist "
            "before proposing new roles. This is a document preview, not an "
            "application interface. No live bots or routines are changed."
        ),
    },
    "zh-CN": {
        "title": "一轮演练，三份结果",
        "scope": "6 条虚构战报",
        "records": "军功记录",
        "writer": "主笔",
        "builder": "构建员",
        "promotion": "主笔另批：列兵 → 上等兵",
        "pending": "待复核",
        "evidence": "缺采用凭据",
        "unrecorded": "已批未登记 · 1 分",
        "outside": "未计入正式累计",
        "observations": "岗位观察",
        "checklist": "已验收的检查清单",
        "reuse": "先复用",
        "no_creation": "不自动建岗",
        "footer": "虚构演练 · 文档预览",
        "description": (
            "三份虚构演练文档的横版概览。正式累计：示例主笔 4.80 分、"
            "示例构建员 9.20 分。主笔列兵晋上等兵经过另行模拟批准。"
            "待复核事项包括缺采用凭据，以及军务官已批未登记的 1 分，"
            "均未加入正式累计。优先复用已验收的检查清单，不自动建岗。"
            "这是文档内容预览，不是应用界面；未改动真实机器人或 routine。"
        ),
    },
}


def verify_sources():
    """Check the published samples' provenance and the fields shown here."""
    mapping = json.loads((HERE / "source-map.json").read_text(encoding="utf-8"))
    assert mapping["rule_version"] == "0.2.0"
    for entry in mapping["files"]:
        contents = (HERE / entry["sample"]).read_text(encoding="utf-8")
        normalized = contents.replace("\r\n", "\n").replace("\r", "\n")
        actual = sha256(normalized.encode("utf-8")).hexdigest()
        assert actual == entry["sha256_utf8_lf"], entry["sample"]

    for language in COPY:
        check_samples(language)
        weekly = (HERE / language / "weekly-report.md").read_text(encoding="utf-8")
        input_path = HERE.parent.parent / "skills" / language / "situk-mars" / "examples" / "synthetic-reports.json"
        reports = json.loads(input_path.read_text(encoding="utf-8"))
        assert len(reports) == 6
        missing = next(item for item in reports if item["event_id"] == "synthetic-event-missing-adoption-01")
        officer = next(item for item in reports if item["event_id"] == "synthetic-event-officer-self-01")
        assert missing["adopted"] is True and missing["adoption_ref"] == ""
        assert officer["requested_grade"] == "commendation"
        if language == "en":
            assert "| Example Writer | 4.80 | Private First Class |" in weekly
            assert "| Example Builder | 9.20 | Private |" in weekly
        else:
            assert "| 示例主笔 | 4.80 | 4.80 | 上等兵 |" in weekly
            assert "| 示例构建员 | 9.20 | 9.20 | 列兵 |" in weekly


def render(language):
    t = COPY[language]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="440" viewBox="0 0 1200 440" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(t["title"])}</title>',
        f'<desc id="desc">{escape(t["description"])}</desc>',
        '<style>text{font-family:"Segoe UI","Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#18332e}.heading{font-weight:700}.muted{fill:#536760}.green{fill:#126650}.amber{fill:#80551a}</style>',
        '<rect width="1200" height="440" rx="20" fill="#f2f6f4"/>',
    ]

    def text(x, y, value, size=22, cls="", anchor=None):
        position = f' text-anchor="{anchor}"' if anchor else ""
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}"{position}>{escape(value)}</text>')

    text(32, 52, t["title"], 32, "heading")
    text(1168, 52, t["scope"], 20, "muted", "end")

    def card(x, title, accent):
        parts.append(f'<rect x="{x}" y="90" width="368" height="276" rx="16" fill="#ffffff" stroke="#cad8d1"/>')
        parts.append(f'<rect x="{x + 24}" y="112" width="36" height="4" rx="2" fill="{accent}"/>')
        text(x + 24, 150, title, 26, "heading")

    card(32, t["records"], "#126650")
    text(56, 212, t["writer"], 24)
    text(376, 216, "4.80", 44, "heading green", "end")
    text(56, 270, t["builder"], 24)
    text(376, 274, "9.20", 44, "heading green", "end")
    text(56, 335, t["promotion"], 22, "muted")

    card(416, t["pending"], "#a07031")
    text(440, 211, t["evidence"], 24, "amber")
    text(440, 270, t["unrecorded"], 23, "amber")
    text(440, 335, t["outside"], 22, "muted")

    card(800, t["observations"], "#126650")
    text(824, 211, t["checklist"], 24)
    text(824, 272, t["reuse"], 34, "heading green")
    text(824, 335, t["no_creation"], 22, "muted")

    text(600, 414, t["footer"], 22, "muted", "middle")
    parts.append("</svg>")
    content = "\n".join(parts) + "\n"
    ET.fromstring(content)
    target = ASSETS / f"overview.{language}.svg"
    target.write_text(content, encoding="utf-8")
    print(target.relative_to(HERE.parent.parent))


if __name__ == "__main__":
    verify_sources()
    for language in COPY:
        render(language)
