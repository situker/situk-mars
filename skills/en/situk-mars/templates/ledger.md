# Formal merit ledger

Only the Commander appends entries under valid human approval. Preserve the original ledger; totals are a recomputable view. The Merit Officer has read-only access and must not enter awards on someone else's behalf or change cumulative totals.

- `ledger_version` / `previous_hash`: <pre-write version / link to the previous record>
- Scope `organization_id` / `rule_version`: <organization / rule>
- Mode: <LOCAL_SIMULATION / live ledger; never mix the two>

| `entry_id` | `decision_id` | `approved_item_id` | `event_id` | Original `cycle_id` | `bot_id` | Change type | Tier | Nominal share | Excluded by cap | Previous value | Delta | New value | Approval reference and hash | Recorder/time | Independent reconciliation |
|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| <combination key> | <ID> | <ID> | <ID> | <ISO week> | <stable ID> | <award/correction> | <tier> | <1.80> | <0.00> | <2.00> | <+1.80> | <3.80> | <evidence> | <Commander/time> | <pending/verified/blocked> |

The personal deduplication key consists of `decision_id + approved_item_id + bot_id + change_type`; it may be canonicalized and hashed. If one approval includes several independent achievements by the same bot, each has a different item ID and must not be incorrectly deduplicated. Retrying the same item records it at most once. Preserve legacy key mappings; do not replay history under new keys. Stable identity, event and item IDs must not be derived from names, row numbers or paths.

For each event, display its nominal pool, all participants' nominal allocations, each participant's over-cap exclusion, and all actual recorded amounts. The actual total may be smaller than the nominal pool; do not distribute the gap to other participants.

Incomplete recording: <completed entries / incomplete entries / reasons / reconciliation retry plan using the same decision_id>. A failed multi-file write is not “all complete.” Before retrying, check existing entries and the exact approved values; never add the points twice.

Corrections use a new approval and appended entries for each person's “revised cumulative amount due − cumulative amount already recorded.” The delta may be negative. Do not overwrite history or reissue the whole pool. If a correction affects promotions, seats or other quotas in the original cycle, submit the affected group for a decision. Keep the original formal ledger until approval.

Append reconciliation records only: <unconflicted reviewer / time / approved values versus entries and totals / differences / resolution status>. A local hash chain helps detect changes; it is not external notarization or host-enforced permission isolation.
