# Itemized human approval

Status: `DRAFT_FOR_HUMAN`. Change to `HUMAN_APPROVED` only after an explicit, verifiable human approval. An AI-generated form, a human name entered in it, or a summary of a decision is not actual approval.

- `decision_id`: <stable unique ID>
- `board_version` / `rule_version`: <exact versions>
- `content_hash`: <hash of the canonicalized items being approved>
- `approval_ref`: <original human approval message/signature record; separately mark simulations as synthetic>
- `approved_by` / `approved_at`: <human identity / timestamp with timezone>
- `valid_from` / `valid_until`: <interval in which recording is authorized; do not reuse old approval indefinitely>
- `effective_at`: <effective time of the decision, with timezone>
- Human approval scope: <item IDs / all explicitly listed items in this exact version>
- Conflicts presented to the Human Owner: <Commander, Merit Officer, shared beneficiaries, etc.>
- Mode: <LOCAL_SIMULATION / separately authorized live execution>

| `approved_item_id` | Action | `event_id` / original cycle | Stable subject ID | Tier/nominal proportions/exact recorded amounts or rank seat | Basis and review ID | Explicit decision |
|---|---|---|---|---|---|---|
| <stable item ID, never a row number> | <award/correction/promotion/special appointment> | <event/cycle> | <ID> | <complete approved values> | <references> | <approve/reject/needs evidence> |

For merit awards, attach every participant, percentage, nominal share, weekly cap and actual amount to record. Approval of a complete board must explicitly cover these details. For promotion, attach the current rank, target rank, next-rank duty acceptance and seat conditions. For a Marshal appointment, attach the unique seat, retained ordinary rank and appointment/removal chronology.

Before recording, verify that the original approval is genuinely human, its hash matches the pending content, it has not expired, the rule and scope match, stable IDs are unique, and the formal ledger's pre-write version is unchanged. Stop the affected item if its content changes, a field is missing, evidence changes or approval cannot be located. The Commander cannot interpret missing approval into existence. Silence, “received” or “looks good” does not approve a specific award.

Approving merit does not approve renaming, additional permissions, messages, publication, new posts or routines. A local simulation updates synthetic records only. This version does not rename real bots. Even if suffix synchronization is added later, it may act only on an approved rank, an authorized subject and the exact authorized suffix; it must not extend to other profile fields.

Recording result: <not executed / PARTIAL / recorded, awaiting independent reconciliation / reconciled>. Itemized entry_id values and reasons for incomplete items: <list>.