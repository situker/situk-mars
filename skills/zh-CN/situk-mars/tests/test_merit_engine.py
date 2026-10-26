"""Business-rule regression tests. All people, evidence and bots are synthetic."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from merit_engine import MeritSystem, MeritError, digest


NOW = "2026-10-26T09:00:00+08:00"
EXPIRY = "2026-10-27T09:00:00+08:00"
JOINED = "2026-10-12T00:00:00+08:00"
CYCLE = "2026-W43"
REQUIREMENTS = {
    "next_duty_ref": "synthetic://next-duty",
    "next_acceptance_ref": "synthetic://next-duty-acceptance",
}


def make_policy():
    thresholds = {
        "上等兵": {"weeks": 1, "points": 2},
        "下士": {"weeks": 2, "points": 5},
        "中士": {"weeks": 3, "points": 10},
        "上士": {"weeks": 4, "points": 16},
        "少尉": {"weeks": 6, "points": 28},
        "中尉": {"weeks": 8, "points": 45},
        "上尉": {"weeks": 10, "points": 70},
        "少校": {"weeks": 12, "points": 100},
        "中校": {"weeks": None, "points": None},
    }
    return {
        "rule_version": "0.2.0", "timezone": "Asia/Singapore",
        "grade_points": {"commendation": 1, "third": 3, "second": 8,
                         "first": 20, "honor": 50},
        "weekly_caps": {"commendation": 2, "third": 2, "second": 1, "first": 1},
        "rank_order": ["列兵", "上等兵", "下士", "中士", "上士", "少尉", "中尉",
                       "上尉", "少校", "中校"],
        "rank_thresholds": thresholds, "promotion_notes": {}, "seat_limit": 1,
    }


def make_roster():
    return [
        {"bot_id": bot_id, "base_name": name, "job_role": role,
         "ordinary_rank": "列兵", "rank_since": JOINED, "joined_at": JOINED,
         "inactive_cycles": [], "special_rank": None}
        for bot_id, name, role in (
            ("cmd", "统筹助手", "commander"),
            ("officer", "军务官", "military_officer"),
            ("alpha", "甲助手", "business"),
            ("beta", "乙助手", "business"),
        )
    ]


class MeritCase(unittest.TestCase):
    def setUp(self):
        self.system = MeritSystem(make_policy(), make_roster(), "owner", "合成业务目标", JOINED)
        self.counter = 0

    def report(self, *, grade="third", bot="alpha", participants=None, **overrides):
        self.counter += 1
        suffix = str(self.counter)
        report = {
            "report_id": "report-" + suffix, "event_id": "event-" + suffix,
            "task_id": "task-" + suffix, "author_bot_id": bot,
            "qualified_at": "2026-10-20T10:00:00+08:00",
            "delivery_ref": "synthetic://delivery/" + suffix,
            "delivery_version": "v1", "acceptance_criteria": "可核对的合成验收要求",
            "acceptance_ref": "synthetic://acceptance/" + suffix,
            "qualified": True, "adopted": True,
            "adoption_ref": "synthetic://adoption/" + suffix,
            "goal_link": "direct", "goal_evidence_ref": "synthetic://goal-chain/" + suffix,
            "requested_grade": grade,
            "participants": participants or [{"bot_id": bot, "share_pct": 100}],
        }
        if grade == "second":
            report.update(asset_id="asset-" + suffix, reuse_task_id="other-task-" + suffix,
                          reuse_ref="synthetic://reuse/" + suffix,
                          reuse_acceptance_ref="synthetic://reuse-acceptance/" + suffix)
        elif grade == "first":
            report.update(major_threshold_ref="synthetic://owner-defined-threshold",
                          before_ref="synthetic://before", after_ref="synthetic://after",
                          independent_ref="synthetic://independent-check")
        elif grade == "honor":
            report.update(owner_initiated=True, independent_new_result=True,
                          cross_quarter_refs=[{"quarter": "2026-Q2", "ref": "synthetic://q2"},
                                              {"quarter": "2026-Q3", "ref": "synthetic://q3"}])
        report.update(overrides)
        return report

    def review(self, report=None, reviewer="officer", now=NOW):
        report = report or self.report()
        self.system.submit(report)
        return self.system.review(report["event_id"], reviewer, now)

    def approve(self, review, *, decision=None, item=None, actor="owner", now=NOW,
                expires_at=EXPIRY, source_ref="synthetic://human-decision"):
        decision = decision or "decision-" + review["event_id"]
        item = item or "item-" + review["event_id"]
        return self.system.approve(review["review_id"], actor, decision, item,
                                   now, expires_at, source_ref)

    def award(self, report=None, *, reviewer="officer", decision=None, item=None):
        review = self.review(report, reviewer=reviewer)
        self.assertEqual("READY", review["status"], review)
        decision = decision or "decision-" + review["event_id"]
        self.approve(review, decision=decision, item=item)
        posted = self.system.post(decision, "cmd", NOW)
        return review, posted

    def assertMeritError(self, code, call):
        with self.assertRaises(MeritError) as caught:
            call()
        if code is not None:
            self.assertEqual(code, caught.exception.code)
        return caught.exception

    def totals(self):
        return self.system.weekly(CYCLE, NOW)["totals"]

    def bot_snapshot(self, bot_id):
        roster = self.system.snapshot()["roster"]
        if isinstance(roster, dict):
            return roster[bot_id]
        return next(bot for bot in roster if bot["bot_id"] == bot_id)


class EvidenceAndCycleTests(MeritCase):
    def test_missing_adoption_blocks_third_without_downgrading(self):
        review = self.review(self.report(adopted=False, adoption_ref=""))
        self.assertEqual("NEEDS_EVIDENCE", review["status"])
        self.assertTrue(review["issues"])
        self.assertFalse(self.system.snapshot()["ledger"])

    def test_commendation_can_reward_a_qualified_unadopted_delivery(self):
        review, posted = self.award(self.report(grade="commendation", adopted=False,
                                                adoption_ref=""))
        self.assertEqual("commendation", review["proposal"]["grade"])
        self.assertEqual("1.00", self.totals()["alpha"])

    def test_receipt_alone_cannot_replace_qualified_acceptance(self):
        review = self.review(self.report(qualified=False, acceptance_ref=""))
        self.assertEqual("NEEDS_EVIDENCE", review["status"])

    def test_third_requires_configured_goal_and_verified_goal_chain(self):
        for goal, link, evidence in (("", "direct", "synthetic://x"),
                                     ("业务目标", "no", "synthetic://x"),
                                     ("业务目标", "indirect", "")):
            with self.subTest(goal=goal, link=link, evidence=evidence):
                self.system = MeritSystem(make_policy(), make_roster(), "owner", goal, JOINED)
                review = self.review(self.report(goal_link=link, goal_evidence_ref=evidence))
                self.assertEqual("NEEDS_EVIDENCE", review["status"])

    def test_null_goal_is_missing_goal_not_the_string_none(self):
        self.system = MeritSystem(make_policy(), make_roster(), "owner", None, JOINED)
        self.assertEqual("NEEDS_EVIDENCE", self.review(self.report())["status"])

    def test_second_needs_stable_asset_and_independent_reuse_task(self):
        for changes in ({"asset_id": ""}, {"reuse_ref": ""}, {"reuse_task_id": ""},
                        {"reuse_acceptance_ref": ""}):
            with self.subTest(changes=changes):
                self.system = MeritSystem(make_policy(), make_roster(), "owner", "业务目标", JOINED)
                review = self.review(self.report(grade="second", **changes))
                self.assertEqual("NEEDS_EVIDENCE", review["status"])

    def test_second_reuse_in_original_task_is_not_an_independent_use(self):
        report = self.report(grade="second")
        report["reuse_task_id"] = report["task_id"]
        self.assertEqual("NEEDS_EVIDENCE", self.review(report)["status"])

    def test_first_requires_prior_major_threshold_and_independent_verification(self):
        for field in ("major_threshold_ref", "before_ref", "after_ref", "independent_ref"):
            with self.subTest(field=field):
                self.system = MeritSystem(make_policy(), make_roster(), "owner", "业务目标", JOINED)
                self.assertEqual("NEEDS_EVIDENCE", self.review(self.report(grade="first", **{field: ""}))["status"])

    def test_honor_requires_owner_initiation_and_distinct_quarters(self):
        report = self.report(grade="honor", owner_initiated=False)
        self.assertEqual("NEEDS_EVIDENCE", self.review(report)["status"])
        report = self.report(grade="honor", cross_quarter_refs=[
            {"quarter": "2026-Q3", "ref": "synthetic://q3-a"},
            {"quarter": "2026-Q3", "ref": "synthetic://q3-b"}])
        self.assertEqual("NEEDS_EVIDENCE", self.review(report)["status"])

    def test_honor_based_only_on_existing_results_awards_title_without_fifty_points(self):
        review, _ = self.award(self.report(grade="honor", independent_new_result=False))
        self.assertEqual("honor", review["proposal"]["grade"])
        self.assertEqual("0.00", review["proposal"]["pool"])
        self.assertEqual("0.00", self.totals().get("alpha", "0.00"))

    def test_late_review_keeps_original_closed_cycle(self):
        review = self.review(self.report())
        self.assertEqual(CYCLE, review["proposal"]["cycle_id"])

    def test_sunday_night_is_preview_and_cannot_be_approved_or_posted(self):
        review = self.review(self.report(qualified_at="2026-10-25T21:00:00+08:00"),
                             now="2026-10-25T22:00:00+08:00")
        self.assertEqual("PREVIEW", review["status"])
        self.assertMeritError(None, lambda: self.approve(review,
                             now="2026-10-25T22:00:00+08:00"))
        self.assertFalse(self.system.snapshot()["ledger"])

    def test_monday_boundary_opens_new_cycle_and_remains_preview(self):
        review = self.review(self.report(qualified_at="2026-10-26T00:00:00+08:00"))
        self.assertEqual("PREVIEW", review["status"])

    def test_prior_to_new_merit_epoch_is_rejected(self):
        report = self.report(qualified_at="2026-10-11T23:59:59+08:00")
        self.assertMeritError("BEFORE_EPOCH", lambda: self.system.submit(report))

    def test_same_event_cannot_be_rebuilt_under_new_report_id(self):
        report = self.report()
        self.system.submit(report)
        clone = dict(report, report_id="different-report", delivery_ref="synthetic://renamed")
        self.assertMeritError("DUPLICATE_EVENT", lambda: self.system.submit(clone))

    def test_same_delivery_version_is_same_event_even_with_new_identifiers(self):
        report = self.report()
        self.system.submit(report)
        clone = dict(report, report_id="different-report", event_id="new-event", task_id="new-task")
        self.assertMeritError("DUPLICATE_EVENT", lambda: self.system.submit(clone))


class AllocationAndCapsTests(MeritCase):
    def test_batch_review_previews_cap_before_human_approval_and_posts_atomically(self):
        reports = [
            self.report(grade="commendation", qualified_at="2026-10-21T10:00:00+08:00"),
            self.report(grade="commendation", qualified_at="2026-10-20T10:00:00+08:00"),
            self.report(grade="commendation", qualified_at="2026-10-22T10:00:00+08:00"),
        ]
        for report in reports:
            self.system.submit(report)
        batch = self.system.review_batch([r["event_id"] for r in reports], "officer", NOW)
        self.assertEqual("BATCH_REVIEWED", batch["status"], batch)
        self.assertTrue(all(review["status"] == "READY" for review in batch["reviews"]))
        self.assertEqual([reports[1]["event_id"], reports[0]["event_id"], reports[2]["event_id"]],
                         batch["order"])
        self.assertEqual(["1.00", "1.00", "0.00"],
                         [r["proposal"]["allocations"][0]["actual"] for r in batch["reviews"]])
        self.assertFalse(self.system.snapshot()["ledger"])
        for index, review in enumerate(batch["reviews"]):
            self.approve(review, decision="batch-board", item="batch-item-" + str(index))
        posted = self.system.post("batch-board", "cmd", NOW)
        self.assertEqual(3, len(posted["entries"]))
        self.assertEqual(["1.00", "1.00", "0.00"], [entry["points"] for entry in posted["entries"]])
        self.assertEqual("2.00", self.totals()["alpha"])

    def test_batch_order_uses_grade_then_evidence_time_and_event_id(self):
        reports = [self.report(grade="commendation"), self.report(grade="third"),
                   self.report(grade="second")]
        for report in reports:
            self.system.submit(report)
        batch = self.system.review_batch([r["event_id"] for r in reports], "officer", NOW)
        self.assertEqual("BATCH_REVIEWED", batch["status"])
        self.assertTrue(all(review["status"] == "READY" for review in batch["reviews"]))
        self.assertEqual([reports[2]["event_id"], reports[1]["event_id"], reports[0]["event_id"]],
                         batch["order"])

    def test_rounding_conserves_pool_and_equal_remainders_follow_stable_id(self):
        report = self.report(grade="commendation", participants=[
            {"bot_id": "beta", "share_pct": "30.335"},
            {"bot_id": "alpha", "share_pct": "60.335"},
            {"bot_id": "cmd", "share_pct": "9.33"}])
        review = self.review(report)
        self.assertEqual("READY", review["status"])
        amounts = {a["bot_id"]: a["nominal"] for a in review["proposal"]["allocations"]}
        self.assertEqual({"alpha": "0.61", "beta": "0.30", "cmd": "0.09"}, amounts)

    def test_equal_fractional_remainders_tie_break_by_id_not_input_order(self):
        report = self.report(grade="commendation", participants=[
            {"bot_id": "cmd", "share_pct": "9.33"},
            {"bot_id": "beta", "share_pct": "30.335"},
            {"bot_id": "alpha", "share_pct": "60.335"}])
        review = self.review(report)
        amounts = {a["bot_id"]: a["nominal"] for a in review["proposal"]["allocations"]}
        self.assertEqual({"alpha": "0.61", "beta": "0.30", "cmd": "0.09"}, amounts)

    def test_non_hundred_percent_shares_cannot_be_approved(self):
        report = self.report(participants=[{"bot_id": "alpha", "share_pct": 60},
                                           {"bot_id": "beta", "share_pct": 60}])
        try:
            review = self.review(report)
        except MeritError:
            return
        self.assertNotEqual("READY", review["status"])

    def test_cap_zeros_only_capped_person_and_never_transfers_or_downgrades(self):
        self.award(self.report())
        self.award(self.report())
        report = self.report(participants=[{"bot_id": "alpha", "share_pct": 60},
                                           {"bot_id": "beta", "share_pct": 40}])
        review, _ = self.award(report)
        allocation = {a["bot_id"]: a for a in review["proposal"]["allocations"]}
        self.assertEqual("third", review["proposal"]["grade"])
        self.assertEqual("1.80", allocation["alpha"]["nominal"])
        self.assertEqual("0.00", allocation["alpha"]["actual"])
        self.assertTrue(allocation["alpha"]["capped"])
        self.assertEqual("1.20", allocation["beta"]["actual"])
        self.assertFalse(allocation["beta"]["capped"])
        self.assertEqual("6.00", self.totals()["alpha"])
        self.assertEqual("1.20", self.totals()["beta"])

    def test_weekly_cap_is_per_grade_and_capped_share_is_not_carried_forward(self):
        self.award(self.report(grade="commendation"))
        self.award(self.report(grade="commendation"))
        review, _ = self.award(self.report(grade="commendation"))
        self.assertEqual("0.00", review["proposal"]["allocations"][0]["actual"])
        self.award(self.report(grade="third"))
        self.assertEqual("5.00", self.totals()["alpha"])
        other_week = self.system.weekly("2026-W44", "2026-11-02T09:00:00+08:00")
        self.assertEqual("0.00", other_week["cycle_totals"].get("alpha", "0.00"))
        self.assertEqual("5.00", other_week["totals"]["alpha"])


class ApprovalAndIndependenceTests(MeritCase):
    def test_officer_cannot_approve_or_write_formal_ledger(self):
        review = self.review()
        self.assertMeritError(None, lambda: self.approve(review, actor="officer"))
        self.approve(review, decision="approved")
        self.assertMeritError(None, lambda: self.system.post("approved", "officer", NOW))
        self.assertFalse(self.system.snapshot()["ledger"])

    def test_commander_cannot_approve_own_or_any_other_award(self):
        review = self.review()
        self.assertMeritError(None, lambda: self.approve(review, actor="cmd"))

    def test_officer_own_contribution_routes_whole_event_to_owner(self):
        report = self.report(bot="officer", participants=[
            {"bot_id": "officer", "share_pct": 60}, {"bot_id": "alpha", "share_pct": 40}])
        review = self.review(report)
        self.assertEqual("CONFLICT_TO_OWNER", review["status"])
        owner_review = self.system.review(report["event_id"], "owner", NOW)
        self.assertEqual("READY", owner_review["status"])

    def test_commander_event_is_reviewed_by_unrelated_officer(self):
        report = self.report(bot="cmd")
        self.system.submit(report)
        self.assertMeritError(None, lambda: self.system.review(report["event_id"], "cmd", NOW))
        review = self.system.review(report["event_id"], "officer", NOW)
        self.assertEqual("READY", review["status"])

    def test_commander_officer_shared_event_cannot_be_mutually_reviewed(self):
        report = self.report(bot="cmd", participants=[
            {"bot_id": "cmd", "share_pct": 60}, {"bot_id": "officer", "share_pct": 40}])
        self.assertEqual("CONFLICT_TO_OWNER", self.review(report)["status"])

    def test_approval_requires_original_human_source_and_unexpired_window(self):
        review = self.review()
        self.assertMeritError(None, lambda: self.approve(review, source_ref=""))
        self.assertMeritError(None, lambda: self.approve(review, expires_at="2026-10-25T09:00:00+08:00"))

    def test_expired_approval_does_not_post(self):
        review = self.review()
        self.approve(review, decision="expired-later", expires_at="2026-10-26T10:00:00+08:00")
        self.assertMeritError(None, lambda: self.system.post("expired-later", "cmd", "2026-10-26T11:00:00+08:00"))
        self.assertFalse(self.system.snapshot()["ledger"])

    def test_review_and_approval_bind_original_content_not_mutable_caller_report(self):
        report = self.report()
        review = self.review(report)
        report["participants"][0]["share_pct"] = 1
        review["proposal"]["pool"] = "999.00"
        self.approve(review, decision="bound-original")
        self.system.post("bound-original", "cmd", NOW)
        self.assertEqual("3.00", self.totals()["alpha"])

    def test_changed_ledger_invalidates_earlier_approved_review(self):
        earlier = self.review(self.report())
        self.approve(earlier, decision="stale")
        self.award(self.report())
        self.assertMeritError("STALE_REVIEW", lambda: self.system.post("stale", "cmd", NOW))

    def test_duplicate_post_is_idempotent_and_never_reawards(self):
        review = self.review()
        self.approve(review, decision="once")
        first = self.system.post("once", "cmd", NOW)
        entries_before = copy.deepcopy(self.system.snapshot()["ledger"])
        second = self.system.post("once", "cmd", NOW)
        self.assertEqual("ALREADY_RECORDED", second["status"])
        self.assertEqual(entries_before, self.system.snapshot()["ledger"])
        self.assertEqual("3.00", self.totals()["alpha"])

    def test_different_events_for_same_bot_have_distinct_approved_item_entries(self):
        first = self.review(self.report())
        second = self.review(self.report())
        self.approve(first, decision="same-board", item="item-a")
        self.approve(second, decision="same-board", item="item-b")
        posted = self.system.post("same-board", "cmd", NOW)
        self.assertEqual(2, len(posted["entries"]))
        self.assertEqual(2, len({entry["entry_id"] for entry in posted["entries"]}))
        self.assertEqual({"item-a", "item-b"},
                         {entry["approved_item_id"] for entry in posted["entries"]})
        self.assertEqual("6.00", self.totals()["alpha"])

    def test_same_board_that_changes_later_item_cap_is_rejected_atomically(self):
        reviews = [self.review(self.report()) for _ in range(3)]
        for index, review in enumerate(reviews):
            self.approve(review, decision="over-cap-board", item="item-" + str(index))
        self.assertMeritError("ALLOCATION_CHANGED", lambda: self.system.post(
            "over-cap-board", "cmd", NOW))
        self.assertFalse(self.system.snapshot()["ledger"])
        self.assertEqual("0.00", self.totals().get("alpha", "0.00"))


class PromotionAndMarshalTests(MeritCase):
    def set_rank(self, rank):
        roster = make_roster()
        alpha = next(bot for bot in roster if bot["bot_id"] == "alpha")
        alpha.update(ordinary_rank=rank, rank_since="2026-06-01T00:00:00+08:00",
                     joined_at="2026-06-01T00:00:00+08:00")
        self.system = MeritSystem(make_policy(), roster, "owner", "合成业务目标", JOINED)

    def test_points_and_full_weeks_create_candidate_only(self):
        self.award(self.report())
        candidate = self.system.promotion_candidate("alpha", NOW, REQUIREMENTS)
        self.assertEqual("ELIGIBLE", candidate["status"], candidate)
        self.assertEqual("上等兵", candidate["to_rank"])
        self.assertEqual("列兵", self.bot_snapshot("alpha")["ordinary_rank"])

    def test_next_rank_duty_and_acceptance_are_mandatory(self):
        self.award(self.report())
        for requirements in ({}, {"next_duty_ref": "synthetic://duty"},
                             {"next_acceptance_ref": "synthetic://acceptance"}):
            with self.subTest(requirements=requirements):
                candidate = self.system.promotion_candidate("alpha", NOW, requirements)
                self.assertEqual("NOT_ELIGIBLE", candidate["status"])
                self.assertTrue(candidate["issues"])

    def test_human_approved_promotion_is_single_step_and_idempotent(self):
        self.award(self.report())
        self.system.approve_promotion("alpha", "owner", "promotion-one", NOW, EXPIRY,
                                      "synthetic://human-promotion", REQUIREMENTS)
        self.assertMeritError(None, lambda: self.system.promote("promotion-one", "officer", NOW))
        result = self.system.promote("promotion-one", "cmd", NOW)
        self.assertEqual("上等兵", self.bot_snapshot("alpha")["ordinary_rank"])
        self.assertEqual("NAME_SYNC_NOT_EXECUTED", result["name_sync_status"])
        repeated = self.system.promote("promotion-one", "cmd", NOW)
        self.assertEqual("ALREADY_RECORDED", repeated["status"])
        self.assertEqual("上等兵", self.bot_snapshot("alpha")["ordinary_rank"])

    def test_promotion_decision_binds_requirements_and_original_approval_source(self):
        for field in ("requirements", "source_ref"):
            with self.subTest(field=field):
                self.setUp()
                self.award(self.report())
                self.system.approve_promotion("alpha", "owner", "bound-promotion", NOW,
                                              EXPIRY, "synthetic://human-promotion", REQUIREMENTS)
                decision = self.system.state["decisions"]["bound-promotion"]
                if field == "requirements":
                    decision["requirements"]["next_duty_ref"] = "synthetic://replacement-duty"
                else:
                    decision["source_ref"] = "synthetic://different-approval"
                self.assertMeritError("APPROVAL_CHANGED", lambda: self.system.promote(
                    "bound-promotion", "cmd", NOW))
                self.assertEqual("列兵", self.bot_snapshot("alpha")["ordinary_rank"])

    def test_future_recorded_points_cannot_create_a_backdated_promotion_candidate(self):
        self.award(self.report())
        self.assertMeritError("TIME_CONFLICT", lambda: self.system.promotion_candidate(
            "alpha", "2026-10-25T09:00:00+08:00", REQUIREMENTS))

    def test_new_rank_clock_resets_ordinary_track_without_leapfrogging(self):
        self.award(self.report())
        self.award(self.report())
        self.system.approve_promotion("alpha", "owner", "promote-alpha", NOW, EXPIRY,
                                      "synthetic://human-promotion", REQUIREMENTS)
        self.system.promote("promote-alpha", "cmd", NOW)
        candidate = self.system.promotion_candidate("alpha", NOW, REQUIREMENTS)
        self.assertEqual("下士", candidate["to_rank"])
        self.assertEqual(0, candidate["full_weeks"])
        self.assertEqual("NOT_ELIGIBLE", candidate["status"])
        # Promotion Monday at 09:00 still leaves that week partial. Only the two
        # full weeks beginning November 2 and November 9 count by November 16.
        later = self.system.promotion_candidate("alpha", "2026-11-16T09:00:00+08:00", REQUIREMENTS)
        self.assertEqual(2, later["full_weeks"])
        self.assertEqual("ELIGIBLE", later["status"])

    def test_partial_and_inactive_weeks_do_not_count(self):
        roster = make_roster()
        alpha = next(bot for bot in roster if bot["bot_id"] == "alpha")
        alpha["rank_since"] = "2026-10-13T09:00:00+08:00"
        alpha["inactive_cycles"] = [CYCLE]
        self.system = MeritSystem(make_policy(), roster, "owner", "业务目标", JOINED)
        candidate = self.system.promotion_candidate("alpha", NOW, REQUIREMENTS)
        self.assertEqual(0, candidate["full_weeks"])

    def test_recent_deliveries_need_version_but_do_not_require_adoption(self):
        self.set_rank("下士")
        roster = list(self.system.snapshot()["roster"].values())
        self.system = MeritSystem(make_policy(), roster, "owner", "合成业务目标",
                                  "2026-06-01T00:00:00+08:00")
        self.award(self.report(grade="first", qualified_at="2026-10-06T10:00:00+08:00"))
        for when in ("2026-10-13T10:00:00+08:00", "2026-10-20T10:00:00+08:00"):
            review = self.review(self.report(grade="commendation", qualified_at=when,
                                             delivery_version="", adopted=False, adoption_ref=""))
            self.assertEqual("NEEDS_EVIDENCE", review["status"])
        candidate = self.system.promotion_candidate("alpha", NOW, REQUIREMENTS)
        self.assertEqual("中士", candidate["to_rank"])
        self.assertGreaterEqual(candidate["full_weeks"], 3)
        self.assertEqual("20.00", candidate["total_points"])
        self.assertEqual("NOT_ELIGIBLE", candidate["status"])
        # Two accepted, versioned deliveries qualify as recent work even if the
        # owner did not adopt them; adopting work is not a weekly activity gate.
        for when in ("2026-10-13T11:00:00+08:00", "2026-10-20T11:00:00+08:00"):
            review = self.review(self.report(grade="commendation", qualified_at=when,
                                             adopted=False, adoption_ref=""))
            self.assertEqual("READY", review["status"])
        self.assertEqual("ELIGIBLE", self.system.promotion_candidate(
            "alpha", NOW, REQUIREMENTS)["status"])

    def test_second_lieutenant_requires_explicit_expanded_scope_acceptance(self):
        self.set_rank("少尉")
        self.award(self.report(grade="honor"))
        candidate = self.system.promotion_candidate("alpha", NOW, REQUIREMENTS)
        self.assertEqual("中尉", candidate["to_rank"])
        self.assertEqual("NOT_ELIGIBLE", candidate["status"])
        ready = self.system.promotion_candidate("alpha", NOW,
                    dict(REQUIREMENTS, expanded_scope_ref="synthetic://owner-expanded-scope"))
        self.assertEqual("ELIGIBLE", ready["status"], ready)

    def test_staff_sergeant_specific_award_condition_is_not_replaced_by_raw_points(self):
        self.set_rank("中士")
        self.award(self.report(grade="first"))
        candidate = self.system.promotion_candidate("alpha", NOW, REQUIREMENTS)
        self.assertEqual("上士", candidate["to_rank"])
        self.assertEqual("NOT_ELIGIBLE", candidate["status"])
        self.award(self.report(grade="third"))
        self.assertEqual("ELIGIBLE", self.system.promotion_candidate("alpha", NOW,
                                                                   REQUIREMENTS)["status"])

    def test_same_parent_asset_reused_twice_is_still_one_promotion_asset(self):
        self.set_rank("中尉")
        self.award(self.report(grade="honor"))
        self.award(self.report(grade="second", asset_id="asset-original", asset_root_id="same-parent-asset",
                               qualified_at="2026-10-13T10:00:00+08:00"))
        self.assertMeritError("DUPLICATE_EVENT", lambda: self.system.submit(
            self.report(grade="second", asset_id="asset-renamed", asset_root_id="same-parent-asset")))
        self.award(self.report(grade="third", qualified_at="2026-10-13T10:00:00+08:00"))
        self.award(self.report(grade="third", qualified_at="2026-10-14T10:00:00+08:00"))
        self.award(self.report(grade="third"))
        self.award(self.report(grade="third"))
        candidate = self.system.promotion_candidate("alpha", NOW, REQUIREMENTS)
        self.assertEqual("上尉", candidate["to_rank"])
        self.assertEqual("70.00", candidate["total_points"])
        self.assertEqual("NOT_ELIGIBLE", candidate["status"])

    def test_special_marshal_does_not_add_points_or_reset_ordinary_rank_clock(self):
        before = self.bot_snapshot("cmd")
        self.system.appoint_marshal("cmd", "owner", "marshal-one", NOW,
                                   "synthetic://owner-special-appointment")
        after = self.bot_snapshot("cmd")
        self.assertEqual("元帅", after["special_rank"])
        self.assertEqual(before["ordinary_rank"], after["ordinary_rank"])
        self.assertEqual(before["rank_since"], after["rank_since"])
        self.assertFalse(self.system.snapshot()["ledger"])
        repeated = self.system.appoint_marshal("cmd", "owner", "marshal-one", NOW,
                                              "synthetic://owner-special-appointment")
        self.assertEqual("ALREADY_RECORDED", repeated["status"])

    def test_marshal_is_not_automatic_and_only_human_can_appoint_commander(self):
        self.assertIsNone(self.bot_snapshot("cmd").get("special_rank"))
        self.assertMeritError(None, lambda: self.system.appoint_marshal(
            "cmd", "cmd", "self-appointed", NOW, "synthetic://self"))
        self.assertMeritError(None, lambda: self.system.appoint_marshal(
            "alpha", "owner", "wrong-role", NOW, "synthetic://human"))

    def test_marshal_has_at_most_one_active_holder(self):
        roster = make_roster()
        roster.append(dict(roster[0], bot_id="cmd-two", base_name="第二统筹助手"))
        try:
            system = MeritSystem(make_policy(), roster, "owner", "业务目标", JOINED)
        except MeritError:
            # Rejecting two commander writers is also a valid stricter boundary.
            return
        system.appoint_marshal("cmd", "owner", "first-seat", NOW, "synthetic://first")
        self.assertMeritError(None, lambda: system.appoint_marshal(
            "cmd-two", "owner", "second-seat", NOW, "synthetic://second"))


class WeeklyAndSnapshotTests(MeritCase):
    def test_resolved_owner_conflict_leaves_active_queue_after_formal_post_and_reconcile(self):
        report = self.report(bot="officer", grade="commendation")
        first = self.review(report)
        self.assertEqual("CONFLICT_TO_OWNER", first["status"])
        review = self.system.review(report["event_id"], "owner", NOW)
        self.assertEqual("READY", review["status"])
        self.approve(review, decision="owner-resolved")
        self.system.post("owner-resolved", "cmd", NOW)
        self.assertEqual("RECONCILED", self.system.reconcile("owner")["status"])
        self.assertFalse(self.system.weekly(CYCLE, NOW)["conflict_queue"])

    def test_fixed_policy_thresholds_and_single_seat_cannot_silently_change(self):
        for alteration in ("rank_thresholds", "seat_limit"):
            with self.subTest(alteration=alteration):
                policy = make_policy()
                if alteration == "seat_limit":
                    policy["seat_limit"] = 9
                else:
                    policy["rank_thresholds"]["上等兵"]["points"] = 0
                self.assertMeritError("RULE_VERSION", lambda: MeritSystem(
                    policy, make_roster(), "owner", "业务目标", JOINED))

    def test_marshal_appointment_decision_id_cannot_be_reused_for_award(self):
        self.system.appoint_marshal("cmd", "owner", "marshal-decision", NOW,
                                   "synthetic://appointment")
        review = self.review()
        self.assertMeritError("DECISION_CONFLICT", lambda: self.approve(
            review, decision="marshal-decision"))

    def test_marshal_appointment_decision_id_cannot_be_reused_for_promotion(self):
        self.award(self.report())
        self.system.appoint_marshal("cmd", "owner", "marshal-decision", NOW,
                                   "synthetic://appointment")
        self.assertMeritError("DECISION_CONFLICT", lambda: self.system.approve_promotion(
            "alpha", "owner", "marshal-decision", NOW, EXPIRY,
            "synthetic://human-promotion", REQUIREMENTS))

    def test_tampered_internal_report_is_detected_before_post(self):
        review = self.review()
        self.approve(review, decision="bound-report")
        self.system.state["reports"][review["event_id"]]["adopted"] = False
        self.assertMeritError("APPROVAL_CHANGED", lambda: self.system.post(
            "bound-report", "cmd", NOW))
        self.assertFalse(self.system.snapshot()["ledger"])

    def test_tampered_internal_decision_proposal_is_detected_before_post(self):
        review = self.review()
        self.approve(review, decision="bound-proposal")
        item = self.system.state["decisions"]["bound-proposal"]["items"][0]
        item["proposal"]["pool"] = "999.00"
        self.assertMeritError("APPROVAL_CHANGED", lambda: self.system.post(
            "bound-proposal", "cmd", NOW))
        self.assertFalse(self.system.snapshot()["ledger"])

    def test_reconciliation_detects_entry_amount_changed_even_with_same_entry_id(self):
        self.award(self.report())
        self.system.state["ledger"][0]["points"] = "99.00"
        result = self.system.reconcile("officer")
        self.assertEqual("MISMATCH", result["status"])
        self.assertIn("APPROVED_VALUE_MISMATCH", result["issues"])
        self.assertEqual(0, result["formal_writes"])

    def test_officer_reconciliation_of_own_award_remains_for_human_review(self):
        self.award(self.report(bot="officer"), reviewer="owner")
        result = self.system.reconcile("officer")
        self.assertEqual("PARTIAL_OWNER_REVIEW", result["status"])
        self.assertTrue(result["owner_review_pending"])
        self.assertEqual(0, result["formal_writes"])

    def test_approved_but_unposted_is_visible_and_excluded_from_official_totals(self):
        review = self.review()
        self.approve(review, decision="not-yet-posted")
        weekly = self.system.weekly(CYCLE, NOW)
        self.assertEqual("CLOSED", weekly["status"])
        self.assertTrue(weekly["approved_unposted"])
        self.assertEqual("0.00", weekly["totals"].get("alpha", "0.00"))
        self.system.post("not-yet-posted", "cmd", NOW)
        self.assertEqual("3.00", self.totals()["alpha"])

    def test_weekly_preview_never_claims_final_closed_board(self):
        weekly = self.system.weekly(CYCLE, "2026-10-25T20:00:00+08:00")
        self.assertEqual("PREVIEW", weekly["status"])

    def test_snapshot_is_deep_copy_of_roster_reports_policy_and_approvals(self):
        report = self.report()
        review = self.review(report)
        self.approve(review, decision="stable")
        original = self.system.snapshot()
        changed = self.system.snapshot()
        changed["policy"]["grade_points"]["third"] = 999
        if isinstance(changed["roster"], dict):
            changed["roster"]["alpha"]["ordinary_rank"] = "中校"
        else:
            next(b for b in changed["roster"] if b["bot_id"] == "alpha")["ordinary_rank"] = "中校"
        changed["reports"].clear()
        changed["reviews"].clear()
        changed["decisions"].clear()
        self.assertEqual(original, self.system.snapshot())

    def test_mutating_constructor_inputs_does_not_rewrite_internal_rule_or_roster(self):
        policy, roster = make_policy(), make_roster()
        system = MeritSystem(policy, roster, "owner", "业务目标", JOINED)
        policy["grade_points"]["third"] = 999
        roster[0]["ordinary_rank"] = "中校"
        snapshot = system.snapshot()
        self.assertEqual(3, snapshot["policy"]["grade_points"]["third"])

    def test_digest_is_key_order_independent_and_sensitive_to_values(self):
        self.assertEqual(digest({"a": 1, "b": 2}), digest({"b": 2, "a": 1}))
        self.assertNotEqual(digest({"a": 1}), digest({"a": 2}))


if __name__ == "__main__":
    unittest.main()
