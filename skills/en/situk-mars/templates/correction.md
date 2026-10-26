# Append-Only Correction Proposal

**Prepared by:** Merit Officer as a draft; conflicted cases require an independent reviewer or the Human Owner.

**When:** New evidence or an error may change a previously recorded award or its dependencies.

**Hand-off:** Submit the complete affected group for human approval; the Commander appends approved corrections for independent reconciliation.

Status: `CORRECTION_PENDING_HUMAN`. Preserve the original report, approval, award board and ledger entries. Do not overwrite, delete or replay them under new keys. The Merit Officer prepares the proposal only. After human approval, the Commander appends the correction to the formal ledger.

- `correction_id` / version / `rule_version`: <identifier / version / rule>
- Original `event_id` / `cycle_id`: <stable event / original cycle of the first qualifying delivery>
- Original `decision_id` / `approved_item_id` / `entry_id`: <linked records>
- Original approval and recorded facts: <version, hash, original values and evidence>
- Reason: <additional evidence supporting an upgrade / share adjustment / adoption withdrawn / award revoked / timing or data-entry error>
- New facts and time when their evidence became complete: <a correction cannot substitute a new event or cycle>
- Conflict declaration and independent reviewer: <refer to the Human Owner if no unconflicted reviewer is available>

| `bot_id` | Original nominal share | Cumulative amount already recorded | Revised nominal share | Recalculated original-week quotas/caps | Revised cumulative amount due | Delta to append now | Changes to award/asset prerequisites |
|---|---:|---:|---:|---|---:|---:|---|
| <ID> | <1.80> | <1.80> | <4.80> | <details> | <4.80> | <+3.00> | <changes> |

Each participant's delta = revised cumulative amount due − cumulative amount already recorded. Deltas may be positive or negative; the event delta equals their sum. Do not treat “new-tier total pool − old total recorded” as a lump sum to distribute. An over-cap share does not transfer to another participant, justify a lower award tier to evade a cap, or carry into a new week.

Dependencies: <other approved events in the same original cycle, tier quotas, dependencies of prior promotions, asset ownership, seats and display names>. If the correction could displace a previously approved event or affect an awarded rank, submit the whole affected group to the Human Owner. Keep the formal ledger unchanged until approval. Do not automatically demote a bot, revoke an award or roll back a name.

Proposed new approval: <new decision_id, new approved_item_id, exact content hash, original human decision record, validity interval and effective time>. Each new personal entry uses the new approval combination key and links to the original entry. Retrying the same correction must not record it twice.

Recording/reconciliation result: <completed and incomplete entries, confirmation that original records remain, recomputed cumulative amounts, independent readback reconciliation>. A rank correction must preserve the original ordinary-rank tenure basis and chronology. Correcting a typo cannot restart tenure or manufacture a missing historical approval.
