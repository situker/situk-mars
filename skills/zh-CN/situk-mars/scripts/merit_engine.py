"""Deterministic merit bookkeeping. No network, bot tools, scheduler or fact authentication.

Evidence references are supplied by a reviewer; this module checks rule consistency,
not whether a document is true or an actor is an authenticated human.
"""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_DOWN
import hashlib
import json
import re

SG = timezone(timedelta(hours=8))
CENT = Decimal("0.01")


class MeritError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code, self.message = code, message


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def timestamp(value):
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("timezone required")
        return parsed.astimezone(SG)
    except (AttributeError, ValueError, TypeError) as exc:
        raise MeritError("INVALID_INPUT", "A timezone-aware ISO timestamp is required") from exc


def key(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,100}", value):
        raise MeritError("INVALID_INPUT", "IDs must be safe ASCII, 1..100 characters")
    return value


def money(value):
    return format(Decimal(str(value)).quantize(CENT), ".2f")


def cycle_of(value):
    year, week, _ = timestamp(value).isocalendar()
    return f"{year}-W{week:02d}"


def cycle_start(cycle):
    try:
        match = re.fullmatch(r"(\d{4})-W(\d{2})", cycle)
        return datetime.fromisocalendar(int(match[1]), int(match[2]), 1).replace(tzinfo=SG)
    except (TypeError, ValueError, AttributeError) as exc:
        raise MeritError("INVALID_INPUT", "Invalid ISO week") from exc


class MeritSystem:
    def __init__(self, policy, roster, owner_id, goal, epoch):
        self.policy = deepcopy(policy)
        if goal is not None and not isinstance(goal, str):
            raise MeritError("INVALID_INPUT", "Goal must be text or unknown (null)")
        self.owner_id, self.goal, self.epoch = key(owner_id), goal or "", timestamp(epoch)
        if policy.get("timezone") != "Asia/Singapore" or policy.get("rule_version") != "0.2.0":
            raise MeritError("RULE_VERSION", "This engine implements the 0.2.0 weekly merit rules")
        if policy.get("grade_points") != {"commendation": 1, "third": 3, "second": 8, "first": 20, "honor": 50}:
            raise MeritError("RULE_VERSION", "Changed grade points need explicit policy implementation and validation")
        if policy.get("weekly_caps") != {"commendation": 2, "third": 2, "second": 1, "first": 1}:
            raise MeritError("RULE_VERSION", "Changed caps need explicit policy implementation and validation")
        if policy.get("rank_order") != ["列兵", "上等兵", "下士", "中士", "上士", "少尉", "中尉", "上尉", "少校", "中校"]:
            raise MeritError("RULE_VERSION", "Unexpected rank ladder")
        thresholds = {name: {"weeks": weeks, "points": points} for name, weeks, points in [
            ("上等兵", 1, 2), ("下士", 2, 5), ("中士", 3, 10), ("上士", 4, 16),
            ("少尉", 6, 28), ("中尉", 8, 45), ("上尉", 10, 70), ("少校", 12, 100), ("中校", None, None)]}
        if policy.get("rank_thresholds") != thresholds or policy.get("seat_limit") != 1:
            raise MeritError("RULE_VERSION", "Changed rank thresholds/seat limit require a new validated policy version")
        people = {}
        for record in roster:
            record = deepcopy(record)
            bot = key(record["bot_id"])
            if bot in people or bot == owner_id or record["ordinary_rank"] not in policy["rank_order"]:
                raise MeritError("AMBIGUOUS", "Duplicate identity or unknown rank")
            if record.get("job_role") not in {"commander", "military_officer", "business"}:
                raise MeritError("INVALID_INPUT", "Unknown job role")
            if not isinstance(record.get("base_name"), str) or not record["base_name"].strip():
                raise MeritError("INVALID_INPUT", "Explicit base_name required")
            timestamp(record["rank_since"])
            timestamp(record["joined_at"])
            if record.get("special_rank"):
                raise MeritError("NEEDS_APPROVAL", "Special rank requires an explicit appointment decision")
            record["special_rank"] = None
            record.setdefault("inactive_cycles", [])
            people[bot] = record
        for role in ["commander", "military_officer"]:
            if sum(p["job_role"] == role for p in people.values()) > 1:
                raise MeritError("AMBIGUOUS", "Choose one primary holder for each governance role")
        self.state = {"roster": people, "reports": {}, "reviews": {}, "decisions": {}, "ledger": [],
                      "ledger_version": 0, "balances": {bot: "0.00" for bot in people},
                      "promotions": [], "appointments": [], "checks": []}

    def _owner(self, actor):
        if actor != self.owner_id:
            raise MeritError("DENIED", "Only the configured human owner can approve")

    def _commander(self, actor):
        if self.state["roster"].get(actor, {}).get("job_role") != "commander":
            raise MeritError("DENIED", "Only the commander mechanically records approved changes")

    def _valid_decision(self, decision, now):
        if decision["approved_by"] != self.owner_id or decision["rule_version"] != self.policy["rule_version"]:
            raise MeritError("NEEDS_APPROVAL", "Decision owner/rule binding differs")
        if timestamp(now) < timestamp(decision["approved_at"]) or timestamp(now) >= timestamp(decision["expires_at"]):
            raise MeritError("APPROVAL_EXPIRED", "Decision is not currently effective")

    def _not_past(self, now):
        when = timestamp(now)
        recorded = [timestamp(r["recorded_at"]) for r in self.state["ledger"]]
        recorded += [timestamp(r["effective_at"]) for r in self.state["promotions"] + self.state["appointments"]]
        if recorded and when < max(recorded):
            raise MeritError("TIME_CONFLICT", "Current-state operations cannot predate existing formal records; use an explicit historical snapshot")
        return when

    def submit(self, report):
        value = deepcopy(report)
        for field in ["report_id", "event_id", "task_id", "author_bot_id"]:
            key(value.get(field))
        event = value["event_id"]
        if value["author_bot_id"] not in self.state["roster"]:
            raise MeritError("UNKNOWN_BOT", "Report author must be in the enrolled roster")
        when = timestamp(value["qualified_at"])
        if when < self.epoch:
            raise MeritError("BEFORE_EPOCH", "No retroactive merit before the configured start")
        if type(value.get("qualified")) is not bool or value.get("adopted") not in [True, False, None] or type(value.get("adopted")) not in [bool, type(None)]:
            raise MeritError("INVALID_INPUT", "qualified/adopted must be explicit booleans or adopted=null")
        if value.get("requested_grade") not in self.policy["grade_points"]:
            raise MeritError("INVALID_INPUT", "Unknown merit grade")
        participants = value.get("participants")
        if not isinstance(participants, list) or not participants:
            raise MeritError("INVALID_INPUT", "Explicit contribution shares required")
        seen, total = set(), Decimal(0)
        for part in participants:
            bot = key(part.get("bot_id"))
            if bot not in self.state["roster"] or bot in seen:
                raise MeritError("AMBIGUOUS", "Unknown or duplicate contributor")
            if when < timestamp(self.state["roster"][bot]["joined_at"]) or cycle_of(value["qualified_at"]) in self.state["roster"][bot]["inactive_cycles"]:
                raise MeritError("NOT_ACTIVE", "Contributions cannot predate enrollment or belong to inactive weeks")
            try:
                if isinstance(part.get("share_pct"), bool):
                    raise ValueError()
                share = Decimal(str(part["share_pct"]))
                if not share.is_finite() or not 0 < share <= 100:
                    raise ValueError()
            except (InvalidOperation, KeyError, ValueError) as exc:
                raise MeritError("INVALID_INPUT", "Share percentages must be finite and positive") from exc
            total += share
            part["share_pct"] = str(share)
            seen.add(bot)
        if total != 100 or value["author_bot_id"] not in seen:
            raise MeritError("INVALID_SHARES", "Shares must sum to 100 and include the report author")
        if event in self.state["reports"] or any(r["report_id"] == value["report_id"] for r in self.state["reports"].values()):
            raise MeritError("DUPLICATE_EVENT", "An event/report may not be resubmitted to earn merit twice")
        if value.get("delivery_ref") and any(r.get("delivery_ref") == value["delivery_ref"] and r.get("delivery_version") == value.get("delivery_version") for r in self.state["reports"].values()):
            raise MeritError("DUPLICATE_EVENT", "Same delivery/version cannot become another event")
        if value.get("requested_grade") == "second" and value.get("asset_id"):
            asset = value.get("asset_root_id", value["asset_id"])
            if any(r.get("requested_grade") == "second" and r.get("asset_root_id", r.get("asset_id")) == asset for r in self.state["reports"].values()):
                raise MeritError("DUPLICATE_EVENT", "A reused asset needs linked evidence/correction, not another independent asset award")
        value["cycle_id"] = cycle_of(value["qualified_at"])
        value["report_hash"] = digest({k: v for k, v in value.items() if k != "report_hash"})
        self.state["reports"][event] = value
        return deepcopy(value)

    def _evidence_issues(self, report):
        issues = []
        for field in ["delivery_ref", "delivery_version", "acceptance_criteria", "acceptance_ref"]:
            if not isinstance(report.get(field), str) or not report[field].strip():
                issues.append("Missing " + field)
        if report.get("qualified") is not True:
            issues.append("Independent qualified delivery not confirmed")
        if len(report["participants"]) > 1 and max(Decimal(p["share_pct"]) for p in report["participants"]) < 60 and not report.get("share_exception_ref"):
            issues.append("Lead share below 60% needs explicit owner exception evidence")
        grade = report["requested_grade"]
        if grade != "commendation" and (report.get("adopted") is not True or not report.get("adoption_ref")):
            issues.append("Adoption and its reference are required")
        if grade == "third" and (not self.goal.strip() or report.get("goal_link") not in {"direct", "indirect"} or not report.get("goal_evidence_ref")):
            issues.append("Third class needs a configured business goal and verified delivery chain")
        if grade == "second":
            if not all(report.get(k) for k in ["asset_id", "reuse_task_id", "reuse_ref"]) or report.get("reuse_task_id") == report["task_id"]:
                issues.append("Second class needs a stable asset and a second independent accepted task")
            if not report.get("reuse_acceptance_ref"):
                issues.append("Missing reuse_acceptance_ref")
        if grade == "first" and not all(report.get(k) for k in ["major_threshold_ref", "before_ref", "after_ref", "independent_ref"]):
            issues.append("First class needs owner-defined importance, before/after facts and independent verification")
        if grade == "honor":
            refs = report.get("cross_quarter_refs", [])
            quarters = {x.get("quarter") for x in refs if isinstance(x, dict) and x.get("quarter") and x.get("ref")}
            if report.get("owner_initiated") is not True or len(quarters) < 2:
                issues.append("Honor is owner-initiated and requires evidenced results across quarters")
            if type(report.get("independent_new_result")) is not bool:
                issues.append("Honor must distinguish a new result from already awarded results")
        return issues

    def _allocation(self, report, ledger=None):
        ledger = self.state["ledger"] if ledger is None else ledger
        grade = report["requested_grade"]
        pool = Decimal(self.policy["grade_points"][grade])
        if grade == "honor" and report.get("independent_new_result") is False:
            pool = Decimal(0)
        raw = [(p["bot_id"], pool * Decimal(p["share_pct"]) / 100) for p in report["participants"]]
        shares = {bot: value.quantize(CENT, rounding=ROUND_DOWN) for bot, value in raw}
        remaining = int((pool - sum(shares.values())) / CENT)
        order = sorted(raw, key=lambda pair: (-(pair[1] - shares[pair[0]]), pair[0]))
        for bot, _ in order[:remaining]:
            shares[bot] += CENT
        allocations = []
        for bot in sorted(shares):
            used = sum(row["bot_id"] == bot and row["grade"] == grade and row["cycle_id"] == report["cycle_id"] and Decimal(row["points"]) > 0 for row in ledger)
            cap = self.policy["weekly_caps"].get(grade)
            capped = cap is not None and used >= cap
            allocations.append({"bot_id": bot, "nominal": money(shares[bot]),
                                "actual": "0.00" if capped else money(shares[bot]), "capped": capped})
        return {"grade": grade, "cycle_id": report["cycle_id"], "pool": money(pool),
                "allocations": allocations, "report_hash": report["report_hash"],
                "expected_ledger_version": self.state["ledger_version"]}

    def review(self, event_id, reviewer_id, now):
        return self._review(event_id, reviewer_id, now)

    def _review(self, event_id, reviewer_id, now, ledger=None):
        self._not_past(now)
        if reviewer_id != self.owner_id and self.state["roster"].get(reviewer_id, {}).get("job_role") != "military_officer":
            raise MeritError("DENIED", "Independent officer or owner must review")
        report = self.state["reports"].get(event_id)
        if not report:
            raise MeritError("NOT_FOUND", "Unknown report")
        participants = {p["bot_id"] for p in report["participants"]}
        conflict = reviewer_id != self.owner_id and (reviewer_id in participants or any(self.state["roster"][p]["job_role"] == "military_officer" for p in participants))
        issues = self._evidence_issues(report)
        closed = timestamp(now) >= cycle_start(report["cycle_id"]) + timedelta(days=7)
        if conflict:
            status, issues = "CONFLICT_TO_OWNER", ["Officer has a personal/beneficial interest; human review required"] + issues
        elif issues:
            status = "NEEDS_EVIDENCE"
        elif not closed:
            status = "PREVIEW"
        else:
            status = "READY"
        proposal = self._allocation(report, ledger) if not issues else None
        value = {"event_id": event_id, "reviewer_id": reviewer_id, "reviewed_at": now,
                 "status": status, "issues": issues, "proposal": proposal, "rule_version": self.policy["rule_version"]}
        value["review_hash"] = digest(value)
        value["review_id"] = "review-" + value["review_hash"][:24]
        self.state["reviews"][value["review_id"]] = deepcopy(value)
        return deepcopy(value)

    def review_batch(self, event_ids, reviewer_id, now):
        """Review a whole board with provisional caps; approve/post in returned order."""
        if not isinstance(event_ids, list) or len(event_ids) > 200 or len(set(event_ids)) != len(event_ids):
            raise MeritError("INVALID_INPUT", "A bounded list of distinct event IDs is required")
        if any(event not in self.state["reports"] for event in event_ids):
            raise MeritError("NOT_FOUND", "Unknown batch event")
        order = sorted(event_ids, key=lambda event: (
            -self.policy["grade_points"][self.state["reports"][event]["requested_grade"]],
            timestamp(self.state["reports"][event].get("evidence_ready_at", self.state["reports"][event]["qualified_at"])), event))
        shadow, reviews = deepcopy(self.state["ledger"]), []
        for event in order:
            value = self._review(event, reviewer_id, now, shadow)
            reviews.append(value)
            if value["status"] == "READY":
                for allocation in value["proposal"]["allocations"]:
                    shadow.append({"bot_id": allocation["bot_id"], "grade": value["proposal"]["grade"],
                                   "cycle_id": value["proposal"]["cycle_id"], "event_id": event, "points": allocation["actual"]})
        return {"status": "BATCH_REVIEWED", "reviews": reviews, "order": order,
                "expected_ledger_version": self.state["ledger_version"]}

    def approve(self, review_id, actor_id, decision_id, approved_item_id, now, expires_at, source_ref):
        self._owner(actor_id)
        self._not_past(now)
        key(decision_id); key(approved_item_id)
        if any(r["decision_id"] == decision_id for r in self.state["appointments"]):
            raise MeritError("DECISION_CONFLICT", "Decision ID already belongs to an appointment")
        if not source_ref or timestamp(expires_at) <= timestamp(now):
            raise MeritError("NEEDS_APPROVAL", "A source reference and future expiry are required")
        review = self.state["reviews"].get(review_id)
        if not review or review["status"] != "READY":
            raise MeritError("REVIEW_NOT_READY", "Only a complete closed-cycle review can be approved")
        if timestamp(now) < timestamp(review["reviewed_at"]):
            raise MeritError("INVALID_INPUT", "Approval cannot predate its review")
        if review["proposal"]["expected_ledger_version"] != self.state["ledger_version"]:
            raise MeritError("STALE_REVIEW", "Re-review and approve after ledger changes")
        group = self.state["decisions"].get(decision_id)
        if group and (group["kind"] != "AWARD" or group["source_ref"] != source_ref or group["expires_at"] != expires_at):
            raise MeritError("DECISION_CONFLICT", "Decision ID is bound to a different approval")
        item = {"approved_item_id": approved_item_id, "review_id": review_id, "review_hash": review["review_hash"],
                "event_id": review["event_id"], "proposal": deepcopy(review["proposal"])}
        if group:
            old = next((x for x in group["items"] if x["approved_item_id"] == approved_item_id), None)
            if old:
                if old != item:
                    raise MeritError("DECISION_CONFLICT", "Approved item ID reused with different contents")
                return deepcopy(group)
            if group.get("posted"):
                raise MeritError("DECISION_CONFLICT", "A posted decision is immutable")
            if any(x["event_id"] == item["event_id"] for x in group["items"]):
                raise MeritError("DUPLICATE_EVENT", "Same event appears twice in one decision")
        else:
            group = {"kind": "AWARD", "decision_id": decision_id, "approved_by": actor_id, "approved_at": now,
                     "expires_at": expires_at, "source_ref": source_ref, "rule_version": self.policy["rule_version"],
                     "origin": "operator_assertion_not_human_authentication", "items": [], "posted": False}
            self.state["decisions"][decision_id] = group
        group["items"].append(item)
        group["decision_hash"] = digest({k: v for k, v in group.items() if k not in {"decision_hash", "posted"}})
        return deepcopy(group)

    def post(self, decision_id, actor_id, now):
        self._commander(actor_id)
        self._not_past(now)
        decision = self.state["decisions"].get(decision_id)
        if not decision or decision["kind"] != "AWARD":
            raise MeritError("NEEDS_APPROVAL", "Exact award decision required")
        if decision.get("posted"):
            return {"status": "ALREADY_RECORDED", "entries": deepcopy([r for r in self.state["ledger"] if r["decision_id"] == decision_id]), "ledger_version": self.state["ledger_version"]}
        self._valid_decision(decision, now)
        if digest({k: v for k, v in decision.items() if k not in {"decision_hash", "posted"}}) != decision.get("decision_hash"):
            raise MeritError("APPROVAL_CHANGED", "Approved decision contents were changed")
        shadow, entries = deepcopy(self.state["ledger"]), []
        for item in decision["items"]:
            proposal = item["proposal"]
            report = self.state["reports"][item["event_id"]]
            review = self.state["reviews"][item["review_id"]]
            report_hash = digest({k: v for k, v in report.items() if k != "report_hash"})
            review_hash = digest({k: v for k, v in review.items() if k not in {"review_hash", "review_id"}})
            if review_hash != item["review_hash"] or report_hash != proposal["report_hash"]:
                raise MeritError("APPROVAL_CHANGED", "Report/review differs from the approved item")
            if proposal["expected_ledger_version"] != self.state["ledger_version"]:
                raise MeritError("STALE_REVIEW", "Ledger changed after approval; re-review required")
            if any(row["event_id"] == item["event_id"] for row in shadow):
                raise MeritError("DUPLICATE_EVENT", "Event already has a formal award; use an explicit correction")
            current = self._allocation(report, shadow)
            if current != proposal:
                raise MeritError("ALLOCATION_CHANGED", "Batch caps differ from approved shares; re-review the entire affected group")
            for allocation in proposal["allocations"]:
                entry = {"entry_id": digest([decision_id, item["approved_item_id"], allocation["bot_id"], "merit"]),
                         "decision_id": decision_id, "approved_item_id": item["approved_item_id"], "event_id": item["event_id"],
                         "bot_id": allocation["bot_id"], "grade": proposal["grade"], "cycle_id": proposal["cycle_id"],
                         "nominal": allocation["nominal"], "points": allocation["actual"], "capped": allocation["capped"],
                         "pool": proposal["pool"], "recorded_by": actor_id, "recorded_at": now,
                         "approval_ref": decision["source_ref"], "change_type": "merit"}
                shadow.append(entry)
                entries.append(entry)
        self.state["ledger"] = shadow
        self.state["ledger_version"] += 1
        decision["posted"] = True
        self.state["balances"] = self._totals()
        return {"status": "RECORDED", "entries": deepcopy(entries), "ledger_version": self.state["ledger_version"]}

    def _totals(self):
        return {bot: money(sum((Decimal(r["points"]) for r in self.state["ledger"] if r["bot_id"] == bot), Decimal(0))) for bot in self.state["roster"]}

    def _full_weeks(self, person, now):
        since = max(timestamp(person["rank_since"]), timestamp(person["joined_at"]))
        start = cycle_start(cycle_of(since.isoformat()))
        if start < since:
            start += timedelta(days=7)
        count = 0
        while start + timedelta(days=7) <= timestamp(now):
            if cycle_of(start.isoformat()) not in person["inactive_cycles"]:
                count += 1
            start += timedelta(days=7)
        return count

    def _qualifying_awards(self, bot):
        result = []
        for row in self.state["ledger"]:
            if row["bot_id"] != bot or Decimal(row["points"]) <= 0:
                continue
            report = self.state["reports"][row["event_id"]]
            share = next(p for p in report["participants"] if p["bot_id"] == bot)
            if Decimal(share["share_pct"]) >= 60:
                result.append((row, report))
        return result

    def promotion_candidate(self, bot_id, now, requirements):
        person = self.state["roster"].get(bot_id)
        if not person:
            raise MeritError("UNKNOWN_BOT", "Unknown rank candidate")
        self._not_past(now)
        ladder = self.policy["rank_order"]
        current = person["ordinary_rank"]
        index = ladder.index(current)
        target = ladder[index + 1] if index + 1 < len(ladder) else None
        total, weeks = self._totals()[bot_id], self._full_weeks(person, now)
        issues = []
        if target is None:
            issues.append("No further ordinary rank in this policy")
        for field in ["next_duty_ref", "next_acceptance_ref"]:
            if not requirements.get(field):
                issues.append("Missing " + field)
        if target:
            threshold = self.policy["rank_thresholds"][target]
            if threshold["weeks"] is not None and weeks < threshold["weeks"]:
                issues.append("Insufficient complete active weeks at current rank")
            if threshold["points"] is not None and Decimal(total) < Decimal(str(threshold["points"])):
                issues.append("Insufficient formal merit points")
        reports = [r for r in self.state["reports"].values() if any(p["bot_id"] == bot_id for p in r["participants"])
                   and timestamp(r["qualified_at"]) <= timestamp(now) and r.get("qualified") is True
                   and all(isinstance(r.get(k), str) and r[k].strip() for k in ["delivery_ref", "delivery_version", "acceptance_ref", "acceptance_criteria"])]
        awards = self._qualifying_awards(bot_id)
        count = lambda grade: sum(row["grade"] == grade for row, _ in awards)
        assets = {report.get("asset_root_id", report.get("asset_id")) for row, report in awards if row["grade"] == "second" and report.get("asset_id")}
        if target == "上等兵" and not reports:
            issues.append("At least one qualified report required")
        if target == "下士" and person.get("unresolved_severe_violation"):
            issues.append("Unresolved confirmed severe violation")
        if target == "中士":
            last = cycle_start(cycle_of(now))
            needed = {cycle_of((last - timedelta(days=7 * i)).isoformat()) for i in [1, 2]}
            if not needed.issubset({r["cycle_id"] for r in reports}):
                issues.append("Qualified deliveries required in each of the last two closed weeks")
        if target == "上士" and not (count("third") or count("second")):
            issues.append("A qualifying third-class award or reusable asset required")
        if target == "少尉" and not (count("second") or count("third") >= 2):
            issues.append("One qualifying second-class or two third-class awards required")
        if target == "中尉" and not requirements.get("expanded_scope_ref"):
            issues.append("Expanded duties need explicit owner confirmation")
        if target == "上尉" and not (count("first") or len(assets) >= 2):
            issues.append("One first-class award or two independently reused assets required")
        if target in {"少校", "中校"} and not requirements.get("seat_ref"):
            issues.append("Approved vacant seat required")
        if target == "中校" and not requirements.get("selection_ref"):
            issues.append("Owner selection required; no automatic points promotion")
        return {"status": "NOT_ELIGIBLE" if issues else "ELIGIBLE", "bot_id": bot_id,
                "from_rank": current, "to_rank": target, "total_points": total, "full_weeks": weeks,
                "issues": issues, "requirements": deepcopy(requirements), "expected_ledger_version": self.state["ledger_version"]}

    def approve_promotion(self, bot_id, actor_id, decision_id, now, expires_at, source_ref, requirements):
        self._owner(actor_id)
        key(decision_id)
        if any(r["decision_id"] == decision_id for r in self.state["appointments"]):
            raise MeritError("DECISION_CONFLICT", "Decision ID already belongs to an appointment")
        if not source_ref or timestamp(expires_at) <= timestamp(now):
            raise MeritError("NEEDS_APPROVAL", "Exact promotion needs a source and future expiry")
        existing = self.state["decisions"].get(decision_id)
        if existing:
            if existing["kind"] == "PROMOTION" and existing["bot_id"] == bot_id and existing["requirements"] == requirements and existing["source_ref"] == source_ref:
                return deepcopy(existing)
            raise MeritError("DECISION_CONFLICT", "Decision ID already used")
        candidate = self.promotion_candidate(bot_id, now, requirements)
        if candidate["status"] != "ELIGIBLE":
            raise MeritError("NOT_ELIGIBLE", "; ".join(candidate["issues"]))
        decision = {"kind": "PROMOTION", "decision_id": decision_id, "bot_id": bot_id, "candidate": candidate,
                    "requirements": deepcopy(requirements), "person_hash": digest(self.state["roster"][bot_id]),
                    "approved_by": actor_id, "approved_at": now, "expires_at": expires_at, "source_ref": source_ref,
                    "rule_version": self.policy["rule_version"], "posted": False,
                    "origin": "operator_assertion_not_human_authentication"}
        decision["decision_hash"] = digest({k: v for k, v in decision.items() if k not in {"decision_hash", "posted"}})
        self.state["decisions"][decision_id] = decision
        return deepcopy(decision)

    def promote(self, decision_id, actor_id, now):
        self._commander(actor_id)
        self._not_past(now)
        decision = self.state["decisions"].get(decision_id)
        if not decision or decision["kind"] != "PROMOTION":
            raise MeritError("NEEDS_APPROVAL", "Explicit promotion approval required")
        if decision["posted"]:
            return {"status": "ALREADY_RECORDED", "decision_id": decision_id, "name_sync_status": "NAME_SYNC_NOT_EXECUTED"}
        self._valid_decision(decision, now)
        if digest({k: v for k, v in decision.items() if k not in {"decision_hash", "posted"}}) != decision.get("decision_hash"):
            raise MeritError("APPROVAL_CHANGED", "Promotion approval contents changed")
        person = self.state["roster"][decision["bot_id"]]
        if digest(person) != decision["person_hash"] or self.state["ledger_version"] != decision["candidate"]["expected_ledger_version"]:
            raise MeritError("STALE_REVIEW", "Roster or ledger changed since promotion approval")
        current = self.promotion_candidate(decision["bot_id"], now, decision["requirements"])
        if current["status"] != "ELIGIBLE" or current["to_rank"] != decision["candidate"]["to_rank"]:
            raise MeritError("NOT_ELIGIBLE", "Promotion conditions changed")
        change = {"decision_id": decision_id, "bot_id": decision["bot_id"], "from_rank": person["ordinary_rank"],
                  "to_rank": current["to_rank"], "effective_at": now, "recorded_by": actor_id, "approval_ref": decision["source_ref"]}
        person["ordinary_rank"], person["rank_since"] = current["to_rank"], now
        decision["posted"] = True
        self.state["promotions"].append(change)
        rank = person["special_rank"] or person["ordinary_rank"]
        label = self.policy.get("rank_labels", {}).get(rank, rank)
        return {"status": "PROMOTED", **deepcopy(change), "display_name_target": person["base_name"] + "〔" + label + "〕",
                "name_sync_status": "NAME_SYNC_NOT_EXECUTED"}

    def appoint_marshal(self, bot_id, actor_id, decision_id, now, source_ref):
        self._owner(actor_id)
        self._not_past(now)
        key(decision_id); timestamp(now)
        if not source_ref or self.state["roster"].get(bot_id, {}).get("job_role") != "commander":
            raise MeritError("NEEDS_APPROVAL", "Marshal needs an explicit owner appointment of the commander")
        previous = next((r for r in self.state["appointments"] if r["decision_id"] == decision_id), None)
        if previous:
            if previous["bot_id"] != bot_id or previous["approval_ref"] != source_ref:
                raise MeritError("DECISION_CONFLICT", "Appointment decision already used")
            return {"status": "ALREADY_RECORDED", **deepcopy(previous)}
        if decision_id in self.state["decisions"]:
            raise MeritError("DECISION_CONFLICT", "Decision ID already used")
        if any(p["special_rank"] == "元帅" for p in self.state["roster"].values()):
            raise MeritError("SEAT_OCCUPIED", "The 0-1 marshal seat is already occupied")
        person = self.state["roster"][bot_id]
        record = {"bot_id": bot_id, "decision_id": decision_id, "seat_id": "commander-marshal-01",
                  "special_rank": "元帅", "effective_at": now, "approved_by": actor_id, "approval_ref": source_ref}
        person["special_rank"] = "元帅"
        self.state["appointments"].append(record)
        return {"status": "APPOINTED", **deepcopy(record), "points_added": "0.00", "name_sync_status": "NAME_SYNC_NOT_EXECUTED"}

    def reconcile(self, actor_id):
        if actor_id != self.owner_id and self.state["roster"].get(actor_id, {}).get("job_role") != "military_officer":
            raise MeritError("DENIED", "Commander cannot self-certify the formal ledger")
        issues, owner_pending = [], []
        if self._totals() != self.state["balances"]:
            issues.append("BALANCE_MISMATCH")
        seen = set()
        for row in self.state["ledger"]:
            expected = digest([row["decision_id"], row["approved_item_id"], row["bot_id"], "merit"])
            if row["entry_id"] != expected or row["entry_id"] in seen:
                issues.append("ENTRY_ID_MISMATCH")
            seen.add(row["entry_id"])
            decision = self.state["decisions"].get(row["decision_id"], {})
            item = next((x for x in decision.get("items", []) if x["approved_item_id"] == row["approved_item_id"]), None)
            allocation = next((x for x in item["proposal"]["allocations"] if x["bot_id"] == row["bot_id"]), None) if item else None
            if not allocation or any(row.get(field) != expected_value for field, expected_value in {
                "points": allocation["actual"] if allocation else None,
                "nominal": allocation["nominal"] if allocation else None,
                "event_id": item["event_id"] if item else None,
                "grade": item["proposal"]["grade"] if item else None,
                "cycle_id": item["proposal"]["cycle_id"] if item else None,
            }.items()):
                issues.append("APPROVED_VALUE_MISMATCH")
            report = self.state["reports"][row["event_id"]]
            if actor_id != self.owner_id and any(p["bot_id"] == actor_id for p in report["participants"]):
                owner_pending.append(row["decision_id"])
        result = {"status": "MISMATCH" if issues else ("PARTIAL_OWNER_REVIEW" if owner_pending else "RECONCILED"),
                "issues": sorted(set(issues)), "owner_review_pending": sorted(set(owner_pending)),
                "formal_writes": 0, "checked_by": actor_id, "ledger_version": self.state["ledger_version"],
                "checked_entry_ids": [r["entry_id"] for r in self.state["ledger"]],
                "evidence_limitation": "Local consistency check; facts and actor identity require independent verification"}
        self.state["checks"].append(deepcopy(result))
        return result

    def weekly(self, cycle_id, now):
        self._not_past(now)
        start = cycle_start(cycle_id)
        closed = timestamp(now) >= start + timedelta(days=7)
        events = {r["event_id"] for r in self.state["ledger"] if r["cycle_id"] == cycle_id}
        reports = [r for r in self.state["reports"].values() if r["cycle_id"] == cycle_id]
        approved_unposted = [deepcopy(d) for d in self.state["decisions"].values() if d["kind"] == "AWARD" and not d["posted"]
                             and any(i["proposal"]["cycle_id"] == cycle_id for i in d["items"])]
        conflicts = []
        seen_conflicts = set()
        owner_checked = {entry for check in self.state["checks"] if check["checked_by"] == self.owner_id and check["status"] == "RECONCILED" for entry in check["checked_entry_ids"]}
        for review in self.state["reviews"].values():
            if review["status"] != "CONFLICT_TO_OWNER" or review["event_id"] in seen_conflicts:
                continue
            event = review["event_id"]
            if self.state["reports"][event]["cycle_id"] != cycle_id:
                continue
            seen_conflicts.add(event)
            owner_reviewed = any(r["event_id"] == event and r["reviewer_id"] == self.owner_id and r["status"] == "READY" for r in self.state["reviews"].values())
            entries = [r["entry_id"] for r in self.state["ledger"] if r["event_id"] == event]
            if owner_reviewed and (not entries or all(entry in owner_checked for entry in entries)):
                continue
            conflicts.append({**deepcopy(review), "pending_action": "owner independent reconciliation" if owner_reviewed else "owner evidence review"})
        active = {p["bot_id"] for r in reports for p in r["participants"]}
        return {"status": "CLOSED" if closed else "PREVIEW", "cycle_id": cycle_id,
                "awards": deepcopy([r for r in self.state["ledger"] if r["cycle_id"] == cycle_id]),
                "totals": self._totals(), "cycle_totals": {bot: money(sum((Decimal(r["points"]) for r in self.state["ledger"] if r["cycle_id"] == cycle_id and r["bot_id"] == bot), Decimal(0))) for bot in self.state["roster"]},
                "approved_unposted": approved_unposted, "pending": [r["event_id"] for r in reports if r["event_id"] not in events],
                "rank_changes": deepcopy([r for r in self.state["promotions"] if cycle_of(r["effective_at"]) == cycle_id]),
                "no_new_count": len(self.state["roster"]) - len(active), "coverage": {"source": "explicitly supplied local report set", "platform_inventory_complete": False, "report_count": len(reports)},
                "conflict_queue": conflicts, "no_new_meaning": "No new reports in supplied set; not proof of no work or complete platform coverage"}

    def snapshot(self):
        return {"policy": deepcopy(self.policy), "owner_id": self.owner_id, "goal": self.goal,
                "epoch": self.epoch.isoformat(), **deepcopy(self.state)}
