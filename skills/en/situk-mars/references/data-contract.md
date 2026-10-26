# Input, state, and output contract

## Runtime boundaries

The customer sets `MERIT_ROOT` to an explicitly authorized runtime directory. Skill source contains only rules, templates, examples, and scripts. Instance data belongs in separate `roster`, `reports`, `reviews`, `decisions`, `ledger`, `promotions`, `weekly`, `corrections`, and `archive` locations. Simulation outputs go to an explicitly supplied output directory. Paths embedded in materials do not expand authorization.

Instance configuration includes at least `organization_id`, `owner_id`, `rule_version`, `rule_adoption_ref`, goal and evidence definitions, `epoch`, timezone, role bindings, baseline sources, allowed file scope, adoption of name synchronization, and seat configuration. Adopting 0.2.0 requires its complete numeric policy and interpretation. Customized rules need a new version, migration impacts, and human adoption before use.

The calculator constructor validates fixed 0.2.0 point values, weekly caps, ordinary rank order, promotion thresholds, and the single Marshal seat. Do not retain `rule_version=0.2.0` while secretly changing those values. A `null` or empty-string goal means unknown; other non-text types are rejected.

Canonical rank keys remain Chinese for cross-language schema compatibility. English `rank_labels` are presentation only. Do not replace Chinese keys in records or approvals with English labels. Both language packs use the same Skill ID; select one rather than loading both as separate Skills.

## Stable fields

| Object | Required retained information |
|---|---|
| Roster | `bot_id`, `base_name`, `job_role`, `ordinary_rank`, `rank_since`, `joined_at`, active status, cycles touched by suspension, current total, baseline evidence |
| Special seat | `special_rank`, `seat_id`, `holder_bot_id`, `appointment_decision_id`, `approval_ref`, `effective_at`, `status`, `supersedes_decision_id`, ordinary-track handover |
| Contribution report | `report_id`, `event_id`, `task_id`, `author_bot_id`, `qualified_at`, original `cycle_id`, `delivery_ref/version`, `acceptance_criteria/ref`, `qualified`, `adopted`, `adoption_ref`, `goal_link/evidence`, `requested_grade`, `participants` and each contribution |
| Asset | `asset_id`, parent-asset identifier, version, `reuse_task_id`, `reuse_ref`, `reuse_acceptance_ref` for second-task acceptance |
| First-Class Merit / Honorary Title | Original approval of major threshold, before-and-after results, independent verification; honors additionally require human initiation, cross-quarter evidence, and a new-outcome determination |
| Review | `review_id`, `reviewer_id`, conflict declaration, `report_hash`, `issues`, `proposal`, original-cycle cap use, `expected_ledger_version`, `review_hash` |
| Decision | `decision_id`, `approved_item_id`, owner, `source_ref`, rule/proposal versions, `review_hash`, original cycle, target bot, pool/shares/posted points or rank, expiry, effective time |
| Ledger entry | `entry_id`, `change_type`, `event_id`, original `cycle_id`, decision/item, bot, old value/delta/new value, actor, time, posting version, reconciliation status |
| Name-synchronization side record | `bot_id`, `base_name`, `rank_decision_id`, old name, `target`, `actual`, `sync_key`, `name_sync_status`, readback evidence and time |

“Qualified” and “adopted” fields are factual claims awaiting verification. Real approval requires checking actual authorized evidence. Missing values are not zero and unknown is not false. Use `null` or explicit pending-evidence text; an empty string cannot masquerade as verified evidence.

## State machine

Report submitted → evidence missing / conflict referred to human / proposal ready → specific human approval → sole-writer official posting → independent reconciliation. Retain each original object and version without overwriting the previous stage.

Calculator review states: `NEEDS_EVIDENCE` means missing evidence; `CONFLICT_TO_OWNER` means conflict referral; `PREVIEW` means the original week is still open; `READY` means the input claims and rule checks support a pending proposal. `READY` is neither fact authentication nor human approval.

For multiple bots or multiple outcomes by one bot on a board, use `review_batch(event_ids, reviewer_id, now)`. It returns `{status, reviews, order, expected_ledger_version}`. It orders by descending grade, evidence-complete time, then `event_id`, calculating original-week caps item by item in a shadow ledger. Thus capped items explicitly show 0 actual points. In the returned order, call `approve` on each exact `review_id` using the same `decision_id` and a distinct `approved_item_id` per item. After all specific approvals, call `post` once. Do not change the order, substitute content, or present old independently reviewed shares as a batch review. Single-item `review` remains supported. If the batch's internal cap results disagree with approval, `post` atomically rejects the whole batch without partially changing the official ledger.

Points become official only after posting. `ALREADY_RECORDED` reconciles a repeated decision and adds no points. `STALE_REVIEW` means the ledger version or cap use changed and requires fresh review and approval. `NAME_SYNC_NOT_EXECUTED` means a display-name task was generated, not that a platform rename succeeded.

User-facing outputs consistently identify `state`, `rule_version`, `cycle_id`, coverage, evidence status, approval source, completed items, pending items, and effects:

- `EMPTY`: the entire authorized scope was read and there are no new items.
- `BLOCKED`: required approval, identity, evidence, or permission is missing; list gaps and draft work that may continue.
- `AMBIGUOUS`: stable identity or outcome attribution is not unique; list candidates, without merging matching names.
- `RATE_LIMITED`: a real tool returned a rate limit; retain its retry time rather than guessing quotas.
- `PARTIAL`: reading, posting, or reconciliation is incomplete; list completed and incomplete items.
- `CLOSED`: an official report for a complete closed cycle; still state coverage and reconciliation status.
- `PREVIEW`: review of an open cycle or incomplete coverage, not a final conclusion.

## Concurrency and audit

There is one official ledger writer. Verify the expected version before writing. Stop the affected item for changed content, cap use, or expired approval. The writer cannot regrade or reinterpret approved content. For partial multi-file posting, retain the same decision for recovery and reconciliation; do not recreate decisions or events to bypass deduplication.

Local example state and summaries are not externally tamper-proof audit evidence. The calculator's in-memory versions provide consistency checks. Production use additionally requires customer-managed versions, backups, and original approval records appropriate to the environment. A model's verbal “done” is not proof of a saved file.

The current-state API cannot set `now` earlier than an existing official entry, promotion, or appointment; it returns `TIME_CONFLICT`. Do not backdate promotions using points posted later. A historical review requires a separately retained snapshot from that time, with its collection time stated. Current totals are not historical snapshots.
