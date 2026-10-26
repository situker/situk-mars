"""Run the SIX merit stages with fictional bots only. Never connects to GrokBot."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import stat
import sys

from merit_engine import MeritError, MeritSystem

LABELS = {"commendation": "嘉奖", "third": "三等功", "second": "二等功", "first": "一等功", "honor": "荣誉称号"}
NOW = "2026-10-26T09:00:00+08:00"
EXPIRES = "2026-10-27T09:00:00+08:00"
EPOCH = "2026-10-12T00:00:00+08:00"
OWNER = "demo_owner"
COMMANDER = "demo_commander"
OFFICER = "demo_officer"


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def roster(language="zh-CN"):
    names = {COMMANDER: "Example Commander", OFFICER: "Example Merit Officer", "demo_writer": "Example Writer", "demo_builder": "Example Builder"}
    return [{"bot_id": bot, "base_name": name, "job_role": role, "ordinary_rank": "列兵",
             "rank_since": EPOCH, "joined_at": EPOCH, "inactive_cycles": []}
            for bot, name, role in [(COMMANDER, "示例统筹", "commander"), (OFFICER, "示例军务官", "military_officer"),
                                    ("demo_writer", "示例主笔", "business"), ("demo_builder", "示例构建员", "business")]] if language != "en" else [
        {"bot_id": bot, "base_name": name, "job_role": "commander" if bot == COMMANDER else ("military_officer" if bot == OFFICER else "business"),
         "ordinary_rank": "列兵", "rank_since": EPOCH, "joined_at": EPOCH, "inactive_cycles": []} for bot, name in names.items()]


def references(value):
    if isinstance(value, str) and value.startswith("synthetic://"):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from references(child)
    elif isinstance(value, list):
        for child in value:
            yield from references(child)


def run(output, language=None):
    source = Path(__file__).resolve().parents[1]
    locale_file = source / "locale.json"
    default = json.loads(locale_file.read_text(encoding="utf-8")).get("language", "zh-CN") if locale_file.exists() else "zh-CN"
    language = language or default
    if language not in {"en", "zh-CN"}:
        raise MeritError("INVALID_INPUT", "Supported languages: en, zh-CN")
    destination = Path(output).absolute()
    for part in [destination, *destination.parents]:
        if part.exists():
            info = part.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise MeritError("UNSAFE_PATH", "Simulation output cannot cross symlinks or reparse points")
    if destination.resolve().is_relative_to(source):
        raise MeritError("UNSAFE_PATH", "Runtime artifacts must be outside the Skill source folder")
    if destination.exists():
        raise MeritError("CONFLICT", "Use a new output directory; existing data is never reset")
    policy = json.loads((source / "policy.json").read_text(encoding="utf-8"))
    reports = json.loads((source / "examples" / "synthetic-reports.json").read_text(encoding="utf-8"))
    assert len(reports) == 6
    goal = "Fictional training business: reduce delivery rework with evidence-based acceptance." if language == "en" else "虚构培训业务：减少交付返工，建立有证据的资料验收。"
    system = MeritSystem(policy, roster(language), OWNER, goal, EPOCH)
    destination.mkdir(parents=True, exist_ok=False)
    evidence = {ref: {"kind": "synthetic_fixture", "ref": ref,
                      "notice": "Fictional evidence; not real customer adoption, platform receipts or human approval." if language == "en" else "虚构练习凭据，不是真实客户采用、平台回执或人类批准。"} for ref in sorted(set(references(reports)))}
    write_json(destination / "evidence-index.json", evidence)
    appointment = system.appoint_marshal(COMMANDER, OWNER, "synthetic-appointment-01", NOW, "synthetic://owner/marshal-appointment")
    initial_roster = deepcopy(system.state["roster"])
    reviews, decisions, posted = [], [], []
    for index, report in enumerate(reports, 1):
        system.submit(report)
        assert all(ref in evidence for ref in references(report))
        review = system.review(report["event_id"], OFFICER, NOW)
        reviews.append(review)
        if index <= 4:
            assert review["status"] == "READY", review
            decision = system.approve(review["review_id"], OWNER, f"synthetic-decision-{index:02d}",
                                      f"synthetic-item-{index:02d}", NOW, EXPIRES, f"synthetic://owner/approval-{index:02d}")
            decisions.append(decision)
            posted.append(system.post(decision["decision_id"], COMMANDER, NOW))
        elif index == 5:
            assert review["status"] == "NEEDS_EVIDENCE"
        else:
            assert review["status"] == "CONFLICT_TO_OWNER"
            owner_review = system.review(report["event_id"], OWNER, NOW)
            assert owner_review["status"] == "READY"
            reviews.append(owner_review)
            # Leave this owner-approved item unposted to show approval != formal points.
            decisions.append(system.approve(owner_review["review_id"], OWNER, "synthetic-officer-pending",
                                            "synthetic-officer-item", NOW, EXPIRES, "synthetic://owner/officer-approved-not-recorded"))
    duplicate_post = system.post("synthetic-decision-01", COMMANDER, NOW)
    assert duplicate_post["status"] == "ALREADY_RECORDED"
    try:
        system.submit(reports[0])
    except MeritError as error:
        assert error.code == "DUPLICATE_EVENT"
    else:
        raise AssertionError("Duplicate event was accepted")
    try:
        system.post("synthetic-officer-pending", OFFICER, NOW)
    except MeritError as error:
        assert error.code == "DENIED"
    else:
        raise AssertionError("Officer wrote the formal ledger")
    requirements = {"next_duty_ref": "synthetic://next-rank/accepted-source-checking-delivery",
                    "next_acceptance_ref": "synthetic://owner/next-rank-acceptance-standard"}
    candidate = system.promotion_candidate("demo_writer", NOW, requirements)
    assert candidate["status"] == "ELIGIBLE"
    assert system.state["roster"]["demo_writer"]["ordinary_rank"] == "列兵"
    promotion_approval = system.approve_promotion("demo_writer", OWNER, "synthetic-promotion-01", NOW, EXPIRES,
                                                "synthetic://owner/specific-promotion-approval", requirements)
    promotion = system.promote(promotion_approval["decision_id"], COMMANDER, NOW)
    repeated_promotion = system.promote(promotion_approval["decision_id"], COMMANDER, NOW)
    assert repeated_promotion["status"] == "ALREADY_RECORDED"
    check = system.reconcile(OFFICER)
    assert check["status"] == "RECONCILED", check
    weekly = system.weekly("2026-W43", NOW)
    assert weekly["totals"]["demo_writer"] == "4.80"
    assert weekly["totals"]["demo_builder"] == "9.20"
    assert weekly["totals"][OFFICER] == "0.00"
    assert weekly["totals"][COMMANDER] == "0.00"
    assert len(weekly["approved_unposted"]) == 1
    assert posted[3]["entries"][0]["nominal"] == "3.00" and posted[3]["entries"][0]["points"] == "0.00"
    assert system.state["roster"][COMMANDER]["ordinary_rank"] == initial_roster[COMMANDER]["ordinary_rank"]
    assert system.state["roster"][COMMANDER]["rank_since"] == initial_roster[COMMANDER]["rank_since"]
    result = {"status": "SIMULATION_PASSED", "rule_version": "0.2.0", "synthetic": True,
              "business_cycle": "2026-W43", "recording_and_promotion_cycle": "2026-W44", "now": NOW,
              "stages": {"报功": "PASSED", "核功": "PASSED", "批准": "PASSED", "记功": "PASSED", "授衔": "PASSED", "周报": "PASSED"},
              "totals": weekly["totals"], "recorded_events": 4, "ledger_entries": len(system.state["ledger"]),
              "missing_evidence_events": 1, "owner_conflict_events": 1, "approved_unposted_events": 1,
              "promotion": promotion, "marshal": appointment, "reconciliation": check,
              "duplicate_award_prevented": True, "duplicate_promotion_prevented": True,
              "real_platform_actions": 0, "real_human_decisions": 0, "existing_agents_modified": 0,
              "routines_changed": 0, "published": False,
              "limitation": "Synthetic data, local role assertions and simulated owner decisions only; not GrokBot deployment or factual verification."}
    result["language"] = language
    if language == "en":
        result["stages"] = {name: "PASSED" for name in ["report", "review", "approval", "recording", "rank_conferral", "weekly_report"]}
    write_json(destination / "simulation.json", result)
    write_json(destination / "snapshot.json", system.snapshot())
    write_json(destination / "reviews.json", reviews)
    write_json(destination / "decisions.json", decisions + [promotion_approval])
    write_json(destination / "weekly.json", weekly)
    if language == "en":
        from render_english import render
        render(destination, result, system.snapshot(), reviews, reports, candidate)
        files = sorted(p for p in destination.iterdir() if p.is_file())
        (destination / "MANIFEST.sha256").write_text("\n".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name for p in files) + "\n", encoding="utf-8")
        return result
    header = "模拟演练 · 全部机器人、交付、采用与批准均为虚构。没有连接 GrokBot，没有真实改名或 routine。\n\n"
    (destination / "00-模拟说明.md").write_text("# 军衔制奖赏系统完整演练\n\n" + header +
        "四个虚构机器人；军功归属 2026-W43，闭合后于 W44 结算及授衔。证据索引使用 synthetic://，仅验证制度和核算流程。\n\n"
        "按顺序阅读 01 至 06。snapshot.json 保存演练最终账；未使用私人花名册、战报或实际人类决定。\n", encoding="utf-8")
    (destination / "01-报功.md").write_text("# 01 报功\n\n" + header +
        "| event_id | 申请人 | 申请等级 | 周期 |\n|---|---|---|---|\n" +
        "\n".join(f"| {r['event_id']} | {r['author_bot_id']} | {LABELS[r['requested_grade']]} | 2026-W43 |" for r in reports) +
        "\n\n原始练习输入见 Skill examples/synthetic-reports.json；本次证据引用索引见 evidence-index.json。\n", encoding="utf-8")
    (destination / "02-核功.md").write_text("# 02 核功\n\n" + header +
        "| 事件 | 复核者 | 结果 | 缺项或回避 |\n|---|---|---|---|\n" +
        "\n".join(f"| {r['event_id']} | {r['reviewer_id']} | {r['status']} | {'; '.join(r['issues']) or '合成证据字段齐全'} |" for r in reviews) +
        "\n\n军务官本人事件转模拟人类复核；两次 AI 意见不能替代真实人类批准。脚本不验证现实事实真伪。\n", encoding="utf-8")
    (destination / "03-批准.md").write_text("# 03 逐项批准\n\n" + header +
        "每项绑定决定号、批准条目、review_hash、原周期分摊、账本版本、批准来源及失效时间，详见 decisions.json。\n\n"
        "前四项模拟批准并登记。军务官嘉奖另由模拟人类核批，刻意保留未登记，其正式分仍为0。缺采用凭证的一项不批准。\n\n"
        "这些批准由演练代码生成，绝非真实人类授权凭据。\n", encoding="utf-8")
    (destination / "04-记功与奖章.md").write_text("# 04 记功与奖章\n\n" + header +
        "| 事件 | 机器人 | 军功章 | 名义份额 | 实记分 | 超帽 |\n|---|---|---|---|---|---|\n" +
        "\n".join(f"| {r['event_id']} | {r['bot_id']} | {('超帽未记功：' if r['capped'] else '🏅 ') + LABELS[r['grade']]} | {r['nominal']} | {r['points']} | {'是' if r['capped'] else '否'} |" for r in system.state["ledger"]) +
        "\n\n协同只分一个3分池：主笔1.80、构建员1.20。主笔第三份三等功超个人周帽，名义3.00、实记0.00，不降档、不转分、不顺延。\n\n"
        "重放同一决定返回ALREADY_RECORDED；独立本地账目核对为RECONCILED，实际事实仍须真实复核。\n", encoding="utf-8")
    (destination / "05-授衔与展示.md").write_text("# 05 授衔与展示\n\n" + header +
        f"主笔正式累计{candidate['total_points']}分、在阶完整周期{candidate['full_weeks']}周，形成上等兵候选。此时仍为列兵；取得特定晋衔模拟批准后才登记上等兵。\n\n"
        f"目标显示名：{promotion['display_name_target']}。真实同步状态：NAME_SYNC_NOT_EXECUTED。重复登记不会再次晋升，也不重起周期。\n\n"
        "统筹的元帅为单席特授：普通轨仍是列兵、在阶起算不变、赠送分数0。构建员达到候选条件也不会自动授衔。图标只用于榜单展示，不改变权限。\n", encoding="utf-8")
    lines = ["# 06 军功周报", "", header, "军功归属：2026-W43（已闭合）；本次结算与晋衔时间：2026-W44。", "",
             "| 机器人 | 正式累计 | W43实记 | 普通军衔 | 特授 |", "|---|---|---|---|---|"]
    for bot, person in system.state["roster"].items():
        lines.append(f"| {person['base_name']} | {weekly['totals'][bot]} | {weekly['cycle_totals'][bot]} | {person['ordinary_rank']} | {person['special_rank'] or '无'} |")
    lines.extend(["", "本轮晋衔：示例主笔列兵→上等兵（生效归W44，不伪记成W43已发生）。", "",
                  "待补证：构建员一项自报采用但没有采用凭据，未计分。", "",
                  "已批未登记：军务官嘉奖1分，仅为模拟人类批准，未计入正式累计。", "",
                  "覆盖：仅本次6条虚构战报，不是全平台盘点。没有新报不等于没有工作，也不作处分。", "",
                  "本周三份文档为手动生成样例；没有建立周更调度、通知或任何routine。", ""])
    (destination / "06-军功周报.md").write_text("\n".join(lines), encoding="utf-8")
    (destination / "06-待复核清单.md").write_text("# 待复核清单 · 2026-W43\n\n" + header +
        "| 事件 | 当前状态 | 未完成事项 | 正式分影响 |\n|---|---|---|---|\n"
        "| 构建员摘要 | 自报采用、缺采用凭据 | 补具体版本的采用确认，再独立核功 | 0，尚未批准 |\n"
        "| 军务官独立说明 | 本人回避后由模拟人类核批 | 尚未正式登记；真实流程还须保留实际人类批准来源 | 0，批准未登记不计分 |\n"
        "| 主笔第三份三等功 | 已核实的虚构合格成果、个人周帽已满 | 保留贡献记录，不转分、不顺延 | 实记0.00 |\n\n"
        "来源限本轮6条虚构战报及reviews.json/decisions.json；无真实团队判定。\n", encoding="utf-8")
    (destination / "06-团队岗位观察.md").write_text("# 团队岗位观察 · 2026-W43\n\n" + header +
        "- 本练习中主笔与构建员分工形成同一协同成果，只分一个分池，不能按人数各领全额。\n"
        "- 复用资产通过第二独立任务及验收说明价值，优先复用资产，不因多一个流程步骤就建议增岗。\n"
        "- 统筹与军务官没有本次正式获分事项；这不等于没有工作，也不据此处分。\n"
        "- 当前材料不足以认定缺岗、重复岗位或需要新增机器人，不提出实际编制变更。\n"
        "- 所有建议留作草案；不创建岗位，不改职责、显示名、权限或routine。\n", encoding="utf-8")
    files = sorted(p for p in destination.iterdir() if p.is_file())
    (destination / "MANIFEST.sha256").write_text("\n".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name for p in files) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description="Six-stage synthetic military merit exercise; no real bot actions")
    parser.add_argument("--output", required=True, help="NEW output directory outside the Skill source")
    parser.add_argument("--lang", choices=["en", "zh-CN"], help="Output language; default comes from this language pack")
    args = parser.parse_args()
    try:
        result = run(args.output, args.lang)
        # Keep machine-readable CLI output safe on legacy Windows console encodings.
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0
    except (MeritError, OSError, ValueError, AssertionError) as error:
        print(json.dumps({"status": "SIMULATION_FAILED", "code": getattr(error, "code", "CHECK_FAILED"), "message": str(error)}, ensure_ascii=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
