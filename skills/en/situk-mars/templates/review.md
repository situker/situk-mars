# Merit verification draft

Status: `EVIDENCE_REVIEWED` / `NEEDS_EVIDENCE` / `CONFLICT_TO_HUMAN`. Write this document only in the Merit Officer's own draft location. It does not change formal reports, approval forms, the roster or cumulative totals.

- `review_id` / `version` / `rule_version`: <identifier / version / rule>
- Linked `report_id`, version and content hash: <exact report>
- `event_id` / `cycle_id`: <stable event / original cycle>
- Reviewer `bot_id` / observation time: <ID / timestamp with timezone>
- Read scope: <materials actually read and time window>
- Unread scope/read failures: <none if there are none>
- Conflict of interest: <no relationship and supporting basis / personal benefit / jointly associated with the Commander / unknown>
- Recusal route: <unconflicted Merit Officer / Human Owner / unconflicted third party designated in advance by the Human Owner>

| Check | Finding | Evidence or gap |
|---|---|---|
| One event_id for the same achievement; no renamed resubmission | <pass/needs verification/fail> | <index> |
| Delivery exists and meets prior acceptance criteria | <result> | <version and acceptance> |
| Adoption is real and tied to a version | <yes/no/unknown> | <record from the Human Owner or authorized accepting person> |
| Goal chain/second-task reuse/major threshold required for the tier | <result> | <evidence> |
| Merit epoch and original cycle are correct | <result> | <qualifying time and epoch> |
| Same-cycle, same-tier quota | <already used / this item / limit> | <approved original ledger and proposed award order> |
| Percentages total 100%; lead has ≥60% or an approved exception | <result> | <each participant's actual contribution> |
| Prior awards, upgrades, corrections and promotion dependencies | <present/none/unknown> | <prior entry and approval> |

Recommended tier and nominal pool: <tier / 1, 3, 8, 20, or a separate human-initiated Honorary Title worth 50>. If prerequisites are not met, recommend a lower tier supported by evidence or request more evidence; a subjective claim of “major” is insufficient. Use the unchanged `policy.json` tier keys `commendation`, `third`, `second`, `first` and `honor` in structured data.

| `bot_id` | Percentage % | Nominal share | Same-tier awards already used in original week | Expected recorded amount | Reason for excluded points | Qualifies for promotion prerequisites? |
|---|---:|---:|---:|---:|---|---|
| <ID> | <60> | <1.80> | <1> | <1.80> | <none/over cap> | <lead ≥60% and positive points/no> |

Allocate shares first, then apply each participant's weekly cap. An over-cap participant's share becomes 0; it does not transfer, move to a lower tier or carry forward. Round to 0.01: first round each allocation down to two decimals, then distribute the remainder in descending fractional-remainder order, breaking ties by stable ID. Total recorded points cannot exceed the event pool.

Conclusion and items for human decision: <itemized list, especially cases benefiting the Commander, the Merit Officer's own cases and cases involving both>.

Readback reconciliation (append a separate draft after recording): <approved values / entries / totals / target names and independent actual-name readback / consistent, PARTIAL or BLOCKED>. Refer the Merit Officer's own cases to the Human Owner; do not alternate approvals with the Commander. The Commander cannot accept their own recording result.
