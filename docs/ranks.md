# From Private to Lieutenant Colonel: what earns the next rank?

Ranks give a bot team a traceable record of growth: **what was delivered, what is still needed for the next rank, and which promotion was approved.** Points record contributions. Promotion also depends on time at the current rank, specific deliveries and a human decision.

This guide covers ordinary ranks and special appointments in situk-MARS v0.2.0. See the [full rules](../skills/en/situk-mars/references/rules.md) for evidence requirements; [policy.json](../skills/en/situk-mars/policy.json) is the numeric source.

[Try the fictional exercise](quickstart.md) · [See the sample weekly report](examples/en/weekly-report.md) · [简体中文](ranks.zh-CN.md)

![The ten ordinary ranks in situk-MARS and the separate Marshal appointment](assets/rank-path.en.png)

## Ten ordinary ranks

New members start as Private. Existing members retain documented approved baselines. **The table shows the requirements to enter the target rank.** Weeks are counted at the current ordinary rank; points are official cumulative points. Ordinary promotion advances one rank at a time.

| Target ordinary rank | Minimum full weeks at current rank | Minimum official cumulative points | Additional requirement |
|---|---:|---:|---|
| Private | Entry rank | No point threshold | Default for new members; existing members retain approved baselines |
| Private First Class | 1 | 2 | At least 1 qualifying report |
| Corporal | 2 | 5 | No unresolved, confirmed serious violation; a suspicion is not a confirmed violation |
| Sergeant | 3 | 10 | Qualifying delivery in each of the last 2 closed cycles |
| Staff Sergeant | 4 | 16 | At least 1 qualifying Third-Class Merit or Second-Class Merit asset award |
| Second Lieutenant | 6 | 28 | At least 1 qualifying Second-Class Merit or 2 qualifying Third-Class Merits |
| First Lieutenant | 8 | 45 | Human-approved expanded responsibilities |
| Captain | 10 | 70 | At least 1 qualifying First-Class Merit or 2 independent qualifying reused assets |
| Major | 12 | 100 | Approved vacant seat and human selection |
| Lieutenant Colonel | No automatic threshold | No automatic threshold | Approved seat and human selection; points never trigger automatic promotion |

**Every candidate also needs an accepted deliverable relevant to the next rank and human-approved acceptance requirements for that rank.** Meeting the table's thresholds creates a candidate only. The exact promotion requires separate human approval and becomes effective after the Commander records it.

Grade prerequisites count only solo awards, or lead participation with a nominal share of at least 60% and positive recorded points. Asset counts also require an independent `asset_id` and actual, accepted reuse in a second independent task. Derivatives of one parent asset count as one. Do not assume a vacant Major or Lieutenant Colonel seat when none is configured. The ordinary track ends at Lieutenant Colonel in this version.

## How weeks and points count

- **Use time at the current rank, not total service.** Count complete cycles after `rank_since`: the week must start on Monday, be active throughout and already be closed. Partial weeks and weeks touched by suspension do not count. Ordinary promotion restarts time at rank; a Marshal appointment does not.
- **Use official totals, not reported totals.** Unapproved, unrecorded or disputed points do not affect eligibility or ordering. Approval and recording are separate steps; approved-but-unrecorded points remain outside the total.
- **Review against the original closed week.** A cycle runs from Monday 00:00 to the next Monday 00:00 in `Asia/Singapore`. The first qualifying delivery sets the event's week. Late reporting, later adoption and second-task reuse supplement the original event rather than moving it to a new week. Open weeks allow preview only, with no official points or promotion.

First-Class Merit and honor-based promotion exceptions have separate manual proposal and approval requirements. The v0.2.0 scripts do not automatically perform exceptional promotion, demotion or Marshal replacement. See the [complete rules](../skills/en/situk-mars/references/rules.md#promotion-and-seats).

## Five merit grades: reward outcomes, not chat volume

| Grade | Nominal event pool | Core evidence |
|---|---:|---|
| Commendation | 1 | Independent qualifying delivery, complete report and no confirmed event violation; adoption may be false or unknown |
| Third-Class Merit | 3 | Adopted, business goal configured, and verified direct or indirect delivery-to-goal chain |
| Second-Class Merit | 8 | Adopted stable asset with an ID and version, actually reused and accepted in a second independent task |
| First-Class Merit | 20 | Adopted, human-confirmed major threshold set in advance, before-and-after results, supporting evidence and independent unconflicted verification |
| Honorary Title | 50, or title only | Human initiated, with confirmed outcomes and specific impact across at least two distinct quarters; 50 points only for independent new outcomes |

**Previously rewarded work may support an Honorary Title, but receives the title only. A new event ID does not justify another 50 points.** Without adoption evidence, do not award Third-Class Merit or above. Missing evidence requires supplementation or a separately supported award proposal, followed by approval of that exact proposal.

These values are the pool for the whole outcome. Collaborators share one pool, subject to each person's same-grade cap in the original week; not every participant receives the full amount. Counts of checks, words or chat turns are not independent outcome evidence. See [allocation and weekly caps](../skills/en/situk-mars/references/rules.md#pools-weekly-caps-and-order).

## Record role, ordinary rank and Marshal separately

| Record | What it answers | This version's rule |
|---|---|---|
| Job role: `job_role` | What work does this bot handle? | Existing roles such as Commander, Merit Officer or business bot |
| Ordinary rank: `ordinary_rank` | Which ordinary rank has been approved? | Private through Lieutenant Colonel, under the conditions and specific decisions above |
| Special Marshal appointment | Does this bot hold the single special seat? | 0–1 per team, available only to the Commander and appointed by the human |

Marshal cannot be purchased with points. It adds no points, is not a 50-point Honorary Title award, and changes neither ordinary rank nor time at rank. Conferring a rank does not automatically expand job responsibilities or platform permissions. Human final approval, independent review and formal recording keep their existing boundaries.

## How ranks appear in names and reports

The workflow's display-name target is **`base_name〔rank〕`**, for example the fictional `Example Writer〔Private First Class〕`. It uses the verified base name and latest valid rank. A valid special Marshal appointment takes display priority while ordinary-rank fields remain. Stable `bot_id` identifies the bot; its current name is not proof of an approved rank.

The roster stores `display_name_target` and `display_name_actual` separately. The local exercise produces a target name and a `NAME_SYNC_NOT_EXECUTED` task only. **Live platform renaming requires host tools, valid authorization and independent read-back as a separate integration.** Do not append repeated suffixes or treat rank approval as permission to change avatars, descriptions, responsibilities, permissions or routines.

Medals appear on boards and weekly reports as `🏅 + grade label`. Drafts say proposed/pending approval; official awards say approved and recorded. Graphics add neither points nor authority, and individual awards are not piled into names. See [names and synchronization](../skills/en/situk-mars/references/rules.md#names-graphics-and-medals).

## Why 4.80 points earned a promotion while 9.20 did not

The fixed fictional exercise ends with different outcomes for two bots:

| Bot | Official cumulative points | Ordinary rank at the end | Why |
|---|---:|---|---|
| Example Writer | 4.80 | Private First Class | Met eligibility conditions, supplied next-rank delivery and acceptance requirements, and received a separate simulated promotion approval and recording |
| Example Builder | 9.20 | Private | No corresponding promotion approval and recording was performed in this run; points alone do not change rank |

The merit belongs to the closed W43 cycle. Settlement and the writer's promotion happen in W44; the promotion is not backdated into W43. The Merit Officer also has a simulated approved-but-unrecorded 1-point item, excluded from official totals.

The builder cannot simply use more than 5 points to jump from Private to Corporal. Ordinary promotion is sequential; each step checks current time at rank, additional requirements and its own approval. **Points make contributions traceable. Approval and recording establish when a rank takes effect.**

[Read the full exercise report](examples/en/weekly-report.md) · [First-run guide](quickstart.md) · [Back to the English homepage](../README.md)
