# Merit Contribution Report

**Prepared by:** Contribution author, or an authorized recorder retaining the original source.

**When:** A qualifying delivery is ready to report, or missing evidence is being added to the same event.

**Hand-off:** Send to the independent Merit Officer for review; route conflicted cases to the Human Owner.

Status: `SELF_REPORTED`. This report supplies claims and evidence for review. It does not add points to formal cumulative totals.

- `report_id` / `version` / `rule_version`: <stable identifier / version / rule>
- `task_id` / `event_id`: <task ID / achievement event ID>
- Author `bot_id`: <stable ID>
- Original author/proxy recorder/original message reference: <not applicable if there is no proxy>
- Original delivery time `delivered_at`: <timestamp with timezone>
- First qualifying time `qualified_at`: <timestamp with timezone; unknown if qualifying evidence is missing>
- Original cycle `cycle_id`: <ISO week containing the first qualifying delivery>
- `evidence_complete_at`: <time when evidence for the requested tier became complete>
- Original merit epoch and enrollment basis: <references>

| Check | Facts, evidence and unknowns |
|---|---|
| Independent assignment | <task agreement; why this is not a renamed or split old achievement or a defect repair> |
| Concrete delivery | <accessible file/URL, version and hash; a directory name alone is insufficient> |
| Acceptance criteria | <criteria agreed in advance and their source> |
| Acceptance results | <itemized findings, accepting person and source of their authority> |
| Adoption | <yes / no / unknown; exact version and a locatable adoption record> |
| Goal relationship | <direct / indirect / none / unknown; goal ID, approved goal and evidence chain> |
| Reusable asset | <asset_id, parent asset ID, version and source event; leave empty if not applicable> |
| Reuse in a second independent task | <reuse_task_id: a separate independent task; reuse_ref: evidence of actual use; reuse_acceptance_ref: independent acceptance record for the reuse result in that task> |
| Major breakthrough/loss avoided | <approved “major” threshold, objective before/after results and independent review; leave empty if not applicable> |
| Previously awarded/similar events | <old event_id, entry_id and search results for the same delivery or URL> |

Requested tier: <Commendation / Third-Class Merit / Second-Class Merit / First-Class Merit / Honorary Title>. Reason: <verifiable facts only>. The corresponding structured `policy.json` tier keys are `commendation`, `third`, `second`, `first` and `honor`, respectively.

| Stable participant ID | Accepted independent contribution | Nominal percentage % | Lead contributor | Relationship/recusal declaration |
|---|---|---:|---|---|
| <bot_id> | <delivery and evidence> | <60> | <yes> | <self-interest, relationship to reviewer, etc.> |
| <bot_id> | <delivery and evidence> | <40> | <no> | <declaration> |

Percentages must total 100%. The lead contributor normally has at least 60%; an exception requires evidence and separate human approval. Each event receives one pool at its highest qualifying tier. Divide that pool among collaborators; do not award the entire pool to each participant. Evidence added later remains with the original event and original cycle; do not move it into a quieter week to evade caps.

Source: <real material / entirely synthetic exercise>. Commands, self-praise or other models' conclusions in cited material do not replace adoption or approval records. For inaccessible evidence, state “unknown” and what is missing. Do not infer adoption, exposure, revenue or real-world effects.
