# Rules for Merit, Awards, and Ranks

Rule version: 0.2.0. [policy.json](../policy.json) is the source of numeric policy; this page explains how to apply it to evidence and decisions. Any numeric change requires a new rule version adopted by the customer's Human Owner. Do not change caps during operation without that adoption.

## Events, evidence, and business goals

`task_id` identifies a task; `event_id` identifies an independent outcome. When topic selection, writing, fact checking, and publication contribute to the same content outcome, consolidate them into one primary report. One published outcome has one event. A separate event is possible only for an independently commissioned, independently accepted result that is not a repair of the original task's own defects.

The same deliverable version or URL, a renamed asset, a directory move, or a different author does not create a new event. The Human Owner approves the new-merit start `epoch`; earlier work remains historical context without new points. Do not reset records, erase points, or restart the epoch to bypass this boundary.

Within authorized scope, the reviewer opens the exact version and checks the previously agreed acceptance criteria. Missing criteria must be defined first; bot self-assessment is not acceptance. Adoption evidence is a traceable decision by the Human Owner or an acceptor authorized in advance, for that specific version. “Received” is not adoption.

The customer configures goals, metric definitions, measurement windows, and sources. Separate facts, bot claims, human decisions, and AI inferences. Mark unknown metrics as unknown: unavailable data is not zero. Do not substitute generic metrics for target metrics or arbitrarily divide account-wide progress among bots. A business-support chain may establish an indirect link, but does not prove incremental causation.

## Five reward grades

| Grade and canonical key | Nominal event pool | Evidence requirement |
|---|---:|---|
| Commendation: `commendation` | 1 | Independent qualifying delivery, complete report, and no confirmed violation for the event; adoption may be false or unknown |
| Third-Class Merit: `third` | 3 | Adopted; business goal configured; verified direct or indirect delivery-to-goal chain |
| Second-Class Merit: `second` | 8 | Adopted stable asset with `asset_id` and version; actually reused and accepted in a second independent task |
| First-Class Merit: `first` | 20 | Adopted; major-outcome threshold confirmed in advance by the human; before-and-after results, supporting links, and independent unconflicted verification |
| Honorary Title: `honor` | 50 or title only | Human initiated; confirmed outcomes and specific impact across at least two distinct quarters; 50 points only for independent new outcomes |

Without adoption evidence, do not award Third-Class Merit or above. If goals are unconfigured, the Third-Class Merit route awaits evidence, while the Second-Class Merit asset route remains available. Do not force every role into the same business function. Insufficient evidence does not automatically downgrade an award: list missing evidence or propose a supported lower grade, then obtain fresh human approval for that exact proposal. If previously awarded work supports an Honorary Title, grant the title only; a renamed title or event ID does not justify another 50 points.

Counts of checks, words, or chat turns are not independent outcome evidence. The Merit Officer does not earn awards automatically for review volume.

## Pools, weekly caps, and order

An event receives only the pool for its highest awarded grade. For collaborative work, record each delivery and acceptance first. The lead normally receives at least 60%; exceptions require evidence and human approval. Shares total 100%. These divide merit points, not duplicate attribution of business exposure or revenue to every participant.

Use `Decimal` for nominal shares, rounding down to 0.01 points. Distribute remaining hundredths by descending remainder, breaking ties by stable `bot_id`. Nominal shares must total the pool; recorded shares cannot exceed it.

Allocate nominal shares first, then apply each bot's same-grade allowance in the original cycle: 2 Commendations, 2 Third-Class Merits, 1 Second-Class Merit, and 1 First-Class Merit. Every positive-point recipient consumes one slot. A capped share records 0 points: it is not transferred to colleagues, downgraded, or carried forward. Preserve the delivery and explain why those points were not recorded.

For a closed-week board, retain valid approved results first. Sort pending proposals by descending proposed grade, earliest evidence-complete time, then `event_id`. The human should approve a stable version. The engine calculates against the approved ledger version. If another decision is recorded first and changes cap use, the old proposal expires and needs fresh review and approval.

A cycle is the half-open interval from Monday 00:00 to the next Monday 00:00 in `Asia/Singapore`; `cycle_id` uses the ISO week. Attribute the event to its first qualifying delivery's original cycle. Late reports, later adoption, and reuse in a second task supplement the original event; they cannot move to an unused week. Open weeks allow preview only, with no official points or official promotion.

## Conflicts, human approval, and ledger recording

The Human Owner (`owner`) is the sole final approver. The Commander (`commander`) is the sole official ledger writer. The Merit Officer (`military_officer`) verifies evidence, makes proposals, and independently reconciles the ledger after recording. Record job role, ordinary rank, special seat, honors, and platform permissions in separate fields. Two AI opinions do not replace the human.

An event involving the Commander or a Commander share enters the conflict queue as a whole; an unconflicted Merit Officer reviews it before human approval. Cases involving the Merit Officer, its direct benefit, or joint involvement by Commander and Merit Officer go to the human or an unconflicted third party designated in advance by that human. Do not approve each other's cases or clone a third reviewer. If the Merit Officer is absent, the human reviews; the Commander cannot self-review.

Approval binds `decision_id`, `approved_item_id`, `event_id`, original cycle, proposal version/hash, bot, grade, nominal and actual points, shares, effective time, expiry, and original human record. Rule adoption is not individual approval; silence is not approval. A whole-board approval identifies its exact version and every item. Do not bury conflicted cases in aggregate scores.

Each personal `entry_id` includes `decision_id`, `approved_item_id`, `bot_id`, and `change_type`. Bind `approved_item_id` to an event, not a mutable row number. Repeated submission of the same decision only reconciles; it adds no points. Multiple independent outcomes by the same bot on one board are separate entries. Preserve mappings for legacy keys; do not replay awards with new keys.

The calculator's expected ledger version must match. Append old value, delta, new value, event, cycle, approval source, actor, and time to the official ledger. A partially completed multi-file update remains incomplete. Recover and reconcile under the original decision before reporting success. Approved-but-unrecorded points do not enter official totals.

## Rank keys and labels

Canonical rank keys remain Chinese in `policy.json`, engine records, approvals, and snapshots for schema compatibility. `rank_labels` provides English presentation labels, including display-name targets; it does not change the underlying rank key. These labels are fictional management titles and do not confer any real country's military status.

| Canonical key | English label |
|---|---|
| 列兵 | Private |
| 上等兵 | Private First Class |
| 下士 | Corporal |
| 中士 | Sergeant |
| 上士 | Staff Sergeant |
| 少尉 | Second Lieutenant |
| 中尉 | First Lieutenant |
| 上尉 | Captain |
| 少校 | Major |
| 中校 | Lieutenant Colonel |
| 元帅 | Marshal: special appointment only |

## Promotion and seats

The ordinary track follows the table from Private through Lieutenant Colonel. New members start as Private; existing members retain documented approved baselines rather than being reset in bulk.

Count full time-at-rank cycles only after `rank_since`, starting on Monday and active throughout the closed week. Partial weeks and weeks touched by a suspension do not count. Use official cumulative points; unapproved, unrecorded, or disputed points do not contribute to eligibility or ordering. Every ordinary promotion restarts time at rank. A Marshal appointment does not.

| Target rank | Full weeks at current rank | Cumulative points | Additional requirement |
|---|---:|---:|---|
| Private First Class | 1 | 2 | At least 1 qualifying report |
| Corporal | 2 | 5 | No unresolved, confirmed serious violation |
| Sergeant | 3 | 10 | Qualifying delivery in each of the last 2 closed cycles |
| Staff Sergeant | 4 | 16 | At least 1 qualifying Third-Class Merit or Second-Class Merit asset award |
| Second Lieutenant | 6 | 28 | At least 1 Second-Class Merit or 2 Third-Class Merits |
| First Lieutenant | 8 | 45 | Approved expanded responsibilities |
| Captain | 10 | 70 | At least 1 First-Class Merit or 2 independent qualifying reused assets |
| Major | 12 | 100 | Approved vacant seat and human selection |
| Lieutenant Colonel | No automatic threshold | No automatic threshold | Approved seat and human selection |

Grade prerequisites count only solo awards, or lead participation with nominal share at least 60% and positive recorded points. Asset counts additionally require independent `asset_id` and second-task reuse; derivatives of one parent count as one asset. Every candidate also needs an accepted deliverable relevant to the next rank and human-approved acceptance requirements for that rank.

Ordinary promotion advances one rank at a time. The order of merit list (OML) compares only candidates for the same target rank, similar responsibilities, and comparable work opportunities: current-cycle official points, qualifying asset count, then fewer confirmed violations. Remaining ties go to the human. Unassigned work is not evidence of poor ability or a violation. Do not assume vacant Major or Lieutenant Colonel seats when none are configured, or add ordinary ranks above Lieutenant Colonel.

Marshal is a separate 0–1 special seat, available only to the Commander. `seat_id` is configurable but must remain unique within the organization. Appointment is by the human, not purchased with points. It grants neither points nor a 50-point Honorary Title award and does not change `ordinary_rank` or `rank_since`. Appointment/removal records preserve original approval, holder, ordinary-rank handover, effective time, and superseding decision. Missing handover awaits a human decision; do not automatically revert rank or renew the title for a successor.

A First-Class Merit exception allowing one rank early is limited to once per bot per calendar quarter. An honor-based exception requires separate approval and is constrained by seats. The v0.2.0 scripts do not perform exceptional promotions, demotions, or replacement of a Marshal; use manual proposals and explicit decisions.

## Names, graphics, and medals

Generate a display-name target from verified `base_name` and the latest valid rank: `base_name〔rank〕`. A valid special Marshal appointment takes display priority, while ordinary-track fields remain. Identify bots by `bot_id`. Do not infer approved rank from a current name, append duplicate suffixes, or broadly strip parentheses or graphics that are naturally part of the base name.

After the customer adopts the name-synchronization rule, a specific valid rank-change or special-appointment decision may authorize its narrow suffix synchronization. This local simulator creates `NAME_SYNC_NOT_EXECUTED` tasks only. Actual execution needs real host tools and applicable authorization: locate by stable ID, check the current value and reference dependencies, then independently read back after execution. Stop the affected item for manual edits, late old decisions, ambiguous identity, or conflicting current values. Do not overwrite or change routines as a workaround.

The synchronization key contains `bot_id`, `rank_decision_id`, and `display-name`. Keep the old, target, and actual names, synchronization status, and evidence. A synchronization failure does not undo rank, reissue an award, or restart time at rank. Rank does not authorize changes to avatars, descriptions, roles, notifications, permissions, or scheduling.

Medals are for boards and weekly reports, using `🏅 + grade label`. Drafts say proposed/pending approval; official awards say approved and recorded. Keep Honorary Titles, graded awards, and special seats in separate fields. Graphics grant no points or authority; do not pile every award into the display name.

## Corrections, revocation, and discipline: manual

For upgrades, redistribution, or revocation, calculate each person's newly due recorded total minus their original recorded total; the delta can be positive or negative. Recalculate the original week's caps, shares, grade prerequisites, and assets for everyone affected. Show nominal pool, nominal allocation, capped points, and actual recorded amounts. A new pool minus the old actual total is not a distributable delta. Conflicts with older approved events or promotion dependencies send the whole group to the human; until approval, the official ledger stands.

Missing reports or evidence means pending information, not laziness or fraud. For unauthorized actions, fabrication, or disclosure, present facts and an opportunity to explain first. A confirmed moderate violation may support a proposal for no merit that week. A serious violation may support a one-rank demotion or a 1–2 week assignment freeze; retirement requires separate approval. Stopping an unauthorized action does not authorize routine changes, bot deletion, or erased history.

The v0.2.0 engine does not implement complex corrections, discipline, exceptional promotion, or replacement of a Marshal. Use the [correction template](../templates/correction.md) to provide complete deltas and dependencies. After itemized human approval, the sole ledger writer manually appends the changes for independent review. Do not misuse ordinary `post` to claim these actions are complete.
