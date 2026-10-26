# Bot Roster

**Prepared by:** Commander, using human-approved enrollment and baseline records.

**When:** The organization adopts the system, enrolls a bot, or records an approved roster change.

**Hand-off:** Give the roster and its source records to the Human Owner for confirmation and the Merit Officer for read-only checks.

Start this register from a blank template. Store stable identity, job role, ordinary rank, special-rank seat and actual platform permissions in separate fields. Do not infer an awarded rank from an existing display name or reset an uncertain historical record to Private.

- `organization_id`: <stable organization ID>
- `rule_version`: <rule version>
- `roster_version`: <this roster's version/content hash>
- `merit_epoch`: <approved starting time for new merit, with timezone>
- `timezone`: Asia/Singapore
- Epoch approval: <original human approval record>
- Read coverage/gaps: <inventory and observation times>

| Field | Record for one bot |
|---|---|
| `bot_id` | <stable ID that does not change with renaming> |
| `base_name` | <verified original functional name> |
| `job_role` | <business role / commander / military_officer> |
| `ordinary_rank` | <Private through Lieutenant Colonel; unknown requires verification; store the matching Chinese policy key> |
| `ordinary_rank_effective_at` | <effective time of the most recent valid ordinary rank> |
| `ordinary_rank_decision_id` | <enrollment or promotion/demotion decision> |
| `active_intervals` | <service start/end and suspension/resumption times; omit none> |
| `special_rank` | <empty / 元帅 (Marshal)> |
| `seat_id` | <empty / commander-marshal-01> |
| `appointment_decision_id` | <special appointment or removal decision> |
| `special_effective_at` / `special_status` | <effective time / vacant, active, revoked or needs verification> |
| `formal_points` | <recomputed from approved entries; exclude drafts and approved but unrecorded items> |
| `approved_duties` | <current duties and approval basis> |
| `permission_enforcement` | <POLICY_ONLY / verified technical controls and evidence> |
| `display_name_target` | <base_name〔verified effective rank〕> |
| `display_name_actual` | <independently observed name; unknown if unread> |
| `name_sync_status` | <NOT_REQUESTED / PENDING / MATCHED / BLOCKED / FAILED> |
| `name_sync_key` | <bot_id + rank_decision_id + display-name> |
| `name_readback_ref` / `observed_at` | <actual name readback evidence / time> |

At most one bot in an organization may hold the special Marshal seat, which may be vacant. It adds no points, does not restart ordinary-rank tenure and grants no permissions. A job role named “Marshal” does not establish a special appointment. The Merit Officer role does not determine its holder's ordinary rank either.

Generate the display name from `base_name` and the latest valid rank. Do not repeatedly append suffixes to the existing name. Use icons only on award boards, as “🏅 Tier text” and label proposed awards “proposed/pending approval.” Local simulation generates target names only and leaves actual names at their synthetic observed values. Do not rename a real bot without approval, capability and current authorization for that action.

Enrollment attachments: duty scope, deliveries and acceptance criteria, merit epoch, initial ordinary rank and approval references. Count complete weeks only after the ordinary rank becomes effective; exclude partial weeks and any week touched by suspension. Do not penalize a bot for having no task or report.

English ordinary-rank display labels, in order: Private, Private First Class, Corporal, Sergeant, Staff Sergeant, Second Lieutenant, First Lieutenant, Captain, Major, Lieutenant Colonel. These labels do not replace the Chinese rank keys in `policy.json` or structured records.
