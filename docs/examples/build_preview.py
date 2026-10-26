"""Render bilingual previews from the samples and their fictional exercise input.

This is a documentation renderer. It never connects to GrokBot or runs the engine.
"""

from html import escape
import json
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"

COPY = {
    "en": {
        "title": "See what one exercise produces",
        "subtitle": "Three documents to see results and next actions.",
        "weekly": "Weekly merit report",
        "weekly_file": "06-weekly-report.md · formal points",
        "writer": "Example Writer",
        "writer_rank": "Private → Private First Class · separately approved",
        "builder": "Example Builder",
        "builder_rank": "Remains Private · promotion needs its own approval",
        "cycle": "Merit: W43 · rank change effective: W44",
        "pending": "Pending-review list",
        "pending_file": "06-pending-review.md",
        "missing": "Adoption evidence missing",
        "missing_detail": "Builder summary → 0 formal points",
        "unposted": "Approved, still unrecorded",
        "unposted_detail": "Officer's 1 point stays outside formal totals",
        "observations": "Team-role observations",
        "observations_file": "06-team-observations.md + exercise input",
        "reuse": "Reuse the accepted checklist first.",
        "reuse_detail": "Accepted in a second independent task.",
        "draft": "Observations stay as proposals.",
        "no_creation": "No automatic role or bot creation.",
        "footer1": "Fictional exercise · Local document preview",
        "footer2": "Not a GrokBot interface · No live bot or routine changes",
        "description": "A reformatted preview of three local exercise documents and their fictional input: writer 4.80 points, builder 9.20, missing adoption evidence, an approved but unrecorded 1-point item, and reuse of an accepted checklist without automatic bot creation.",
    },
    "zh-CN": {
        "title": "一轮演练，你会拿到什么",
        "subtitle": "三份文档，看清成果和接下来要处理的事。",
        "weekly": "军功周报",
        "weekly_file": "06-军功周报.md · 正式累计",
        "writer": "示例主笔",
        "writer_rank": "列兵 → 上等兵 · 另行模拟批准后授衔",
        "builder": "示例构建员",
        "builder_rank": "保持列兵 · 候选资格不等于已经晋衔",
        "cycle": "军功归属 W43 · 晋衔生效 W44",
        "pending": "待复核清单",
        "pending_file": "06-待复核清单.md",
        "missing": "缺采用凭据",
        "missing_detail": "构建员摘要：补采用确认后再核功，正式分 0",
        "unposted": "已批未登记",
        "unposted_detail": "军务官嘉奖 1 分，尚未进入正式累计",
        "observations": "团队岗位观察",
        "observations_file": "06-团队岗位观察.md + 同轮虚构输入",
        "reuse": "先复用已验收的检查清单。",
        "reuse_detail": "清单已在第二个独立任务中验收。",
        "draft": "观察先作为建议草案。",
        "no_creation": "不自动补岗或创建机器人。",
        "footer1": "虚构演练 · 本地文档内容预览",
        "footer2": "不是 GrokBot 界面 · 没有改动真实机器人或 routine",
        "description": "三份本地演练文档及同轮虚构输入的整理预览：主笔4.80分、构建员9.20分、缺采用凭据、已批未登记1分，以及优先复用已验收检查清单、不自动补岗的团队观察。",
    },
}


def check_samples(language):
    """Fail rather than publish a preview that disagrees with its source."""
    base = HERE / language
    weekly = (base / "weekly-report.md").read_text(encoding="utf-8")
    pending = (base / "pending-review.md").read_text(encoding="utf-8")
    observations = (base / "team-observations.md").read_text(encoding="utf-8")
    input_path = HERE.parent.parent / "skills" / language / "situk-mars" / "examples" / "synthetic-reports.json"
    reports = json.loads(input_path.read_text(encoding="utf-8"))
    checklist = next(item for item in reports if item["event_id"] == "synthetic-event-builder-01")
    assert checklist["delivery_ref"] == "synthetic://deliveries/reusable-checklist-01"
    assert checklist["asset_id"] == "synthetic-asset-checklist-01"
    assert checklist["reuse_task_id"] == "synthetic-task-builder-reuse-02"
    assert checklist["reuse_task_id"] != checklist["task_id"]
    assert checklist["reuse_acceptance_ref"] == "synthetic://reuse-acceptance/independent-task-02"
    assert checklist["qualified"] is True and checklist["adopted"] is True
    for fragment in ("4.80", "9.20", "2026-W43", "2026-W44"):
        assert fragment in weekly, (language, fragment)
    if language == "en":
        assert "Private First Class" in weekly
        assert "1-point" in weekly and "unrecorded" in weekly
        assert "evidence missing" in pending and "not recorded" in pending
        assert "Reuse" in observations and "does not justify new positions" in observations
        assert "fictional" in weekly
        assert "reusable checklist" in checklist["acceptance_criteria"]
        assert "accepted in a second independent task" in checklist["acceptance_criteria"]
        assert "fictional" in checklist["source_note"]
    else:
        assert "上等兵" in weekly
        assert "嘉奖1分" in weekly and "未计入正式累计" in weekly
        assert "缺采用凭据" in pending and "尚未正式登记" in pending
        assert "优先复用资产" in observations and "不足以认定缺岗" in observations
        assert "虚构" in weekly
        assert "检查清单" in checklist["acceptance_criteria"]
        assert "第二独立任务中完成验收" in checklist["acceptance_criteria"]
        assert "虚构" in checklist["source_note"]


def render(language):
    check_samples(language)
    t = COPY[language]
    bits = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="1210" viewBox="0 0 760 1210" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(t["title"])}</title>',
        f'<desc id="desc">{escape(t["description"])}</desc>',
        '<style>text{font-family:Inter,"Segoe UI","Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#152b32} .muted{fill:#536a72} .heading{font-weight:700} .mono{font-family:"Cascadia Code",Consolas,"Microsoft YaHei",monospace} .green{fill:#0d715d} .amber{fill:#92620a}</style>',
        '<rect width="760" height="1210" rx="24" fill="#f2f6f6"/>',
        '<rect x="40" y="34" width="5" height="112" rx="2" fill="#167f6a"/>',
    ]

    def text(x, y, value, size=24, cls="", anchor=None):
        extra = f' text-anchor="{anchor}"' if anchor else ""
        bits.append(f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}"{extra}>{escape(value)}</text>')

    text(61, 54, "SITUK-MARS / EXERCISE PREVIEW", 18, "heading green")
    text(61, 104, t["title"], 36, "heading")
    text(61, 144, t["subtitle"], 24, "muted")

    def card(y, height, number, title, filename, badge_color):
        bits.append(f'<rect x="40" y="{y}" width="680" height="{height}" rx="18" fill="#ffffff" stroke="#d8e3e4"/>')
        bits.append(f'<rect x="60" y="{y+21}" width="45" height="38" rx="10" fill="{badge_color}"/>')
        text(82, y+48, number, 23, "heading green", "middle")
        text(120, y+48, title, 30, "heading")
        text(64, y+80, filename, 20, "muted mono")
        bits.append(f'<line x1="64" y1="{y+96}" x2="696" y2="{y+96}" stroke="#e5ebec"/>')

    card(177, 300, "01", t["weekly"], t["weekly_file"], "#e0f3ee")
    text(64, 314, t["writer"], 26, "heading")
    text(690, 317, "4.80", 42, "heading green", "end")
    text(64, 350, t["writer_rank"], 22, "muted")
    text(64, 400, t["builder"], 26, "heading")
    text(690, 403, "9.20", 42, "heading green", "end")
    text(64, 436, t["builder_rank"], 22, "muted")
    text(64, 463, t["cycle"], 19, "muted")

    card(497, 285, "02", t["pending"], t["pending_file"], "#fff1d7")
    text(64, 628, t["missing"], 26, "heading amber")
    text(64, 664, t["missing_detail"], 24, "muted")
    text(64, 716, t["unposted"], 26, "heading amber")
    text(64, 752, t["unposted_detail"], 24, "muted")

    card(802, 285, "03", t["observations"], t["observations_file"], "#e0f3ee")
    text(64, 934, t["reuse"], 26, "heading green")
    text(64, 970, t["reuse_detail"], 24, "muted")
    text(64, 1022, t["draft"], 25, "heading")
    text(64, 1058, t["no_creation"], 24, "muted")

    text(380, 1137, t["footer1"], 24, "heading", "middle")
    text(380, 1174, t["footer2"], 21, "muted", "middle")
    bits.append("</svg>")
    svg = "\n".join(bits) + "\n"
    ET.fromstring(svg)
    target = ASSETS / f"exercise-preview.{language}.svg"
    target.write_text(svg, encoding="utf-8")
    print(target.relative_to(HERE.parent.parent))


if __name__ == "__main__":
    for language in COPY:
        render(language)
