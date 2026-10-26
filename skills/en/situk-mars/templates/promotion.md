# Promotion and special appointment proposal

Status: `CANDIDATE_ONLY`. Reaching a point threshold creates a candidate only. It does not award a rank, rename a real bot, expand permissions or trigger a routine.

- `proposal_id` / `version` / `rule_version`: <identifier / version / rule>
- Subject `bot_id` / `job_role` / `base_name`: <stable identity / post / original name>
- Current `ordinary_rank` / effective time / approval reference: <formal record>
- Current special-rank seat: <vacant / active Marshal and decision / needs verification>
- Request: <ordinary promotion / human-initiated special appointment / revocation or correction>
- Proposed target rank: <normally one rank at a time>

| Promotion condition | Subject's facts and evidence | Finding |
|---|---|---|
| Formal cumulative points | <approved and recorded items only; exclude drafts and approved but unrecorded items> | <met/not met> |
| Minimum complete cycles at current rank | <complete weeks after the effective time; exclude partial weeks and weeks touched by suspension> | <count/threshold> |
| Qualifying deliveries, awards and asset prerequisites | <sole award recipient, or lead contributor with ≥60% and positive recorded points; deduplicate by parent asset> | <result> |
| Acceptance of next-rank duties | <human-approved requirements, accepted deliveries addressing them and results> | <met/requirements pending> |
| Expanded duties | <separate approval reference, if applicable> | <result> |
| Serious violations and fairness of opportunity | <confirmed matters only; receiving no tasks is not a failure to qualify> | <result> |
| Seats or competitive selection | <explicit Major/Lieutenant Colonel seat and basis for human selection> | <vacant/not configured> |
| Recusal and independent review | <handling of the Commander's own case, the Merit Officer's own case, or a jointly associated case> | <result> |

A complete cycle runs from Monday 00:00 to the following Monday 00:00 in Asia/Singapore. Exclude weeks before the ordinary rank took effect and weeks without uninterrupted active service. A special appointment does not restart ordinary-rank tenure. A later revocation of the special rank requires the Human Owner to specify the continuing ordinary rank and effective time; do not revert automatically.

If First-Class Merit is cited to advance one rank early, attach the subject's exception-use record for the calendar quarter. This exception may be used at most once per quarter and still requires explicit human approval. An Honorary Title promotion exception requires separate approval and remains subject to seat limits. Sufficient points alone do not select a bot for Major or Lieutenant Colonel.

Marshal appointment attachment (human-initiated appointment/removal only): `seat_id=commander-marshal-01`, active holder, proposed appointee, appointment/removal decision, chronology, replacement record, last valid ordinary rank and continuity explanation. An organization has at most one active Marshal; the seat may be vacant. The appointment adds no points, grants no automatic Honorary Title and does not fill in ranks above Lieutenant Colonel.

Post-approval display plan: `base_name〔approved effective rank〕`. Previous name <observed value>; target name <computed value>; actual name <unknown or independent readback>; synchronization status <NOT_REQUESTED/PENDING/MATCHED/BLOCKED>. Local simulation does not rename real bots; icons are for boards only. English rank labels are display text; machine-readable rank values must retain the Chinese keys defined in `policy.json`.

Human decision: <decision_id / approved_item_id / exact hash / original approval evidence / validity interval / effective time>. Recording and independent reconciliation: <result>.