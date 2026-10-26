# Using situk-MARS in GrokBot

Run the reward workflow in six stages: **Report → Review → Human approval → Record → Confer rank → Weekly report**. Start with the documents and templates; bot-management APIs are unnecessary for preparing drafts. Recording means entering approved decisions in the formal ledger. Local synthetic validation did not create, modify, or rename real bots or operate routines. A published Skill is not evidence of a live deployment.

## Customer onboarding

1. The customer specifies organization, stable Human Owner ID, runtime directory, readable material boundaries, business goals, new-merit start time, active roster, and rule version. Unknown goals stay unknown; defer Third-Class Merit through the goal route.
2. Prefer binding the existing coordinating bot as `commander` and an unconflicted reviewer as `military_officer`. Binding is a roster record, not an automatic change to platform responsibilities or permissions. The customer can cover missing roles. Prepare [role charters](../templates/role-charters.md) and bot-creation recommendations for later approval; do not create bots.
3. The human adopts `rule_version` and separately approves the runtime directory, existing baseline, and exact action scope. Missing approval evidence for historical rosters, scores, or ranks means pending reconciliation, not resets or automatic retroactive awards.
4. Run a closed cycle manually first. Check event deduplication, conflicts, weekly caps, original approvals, official entries, and the weekly report before considering automation.

Business analysis clarifies goal links and existing roles. Reuse people, bots, or deterministic tools before recommending roles for genuine independent delivery gaps. Create additional roles only under separate, later approval. An award review alone is no reason to expand the team.

## When tools are available

In an existing Commander or user conversation, use only native tools whose actual definitions are visible, whose parameters have been verified, and whose use is authorized. Do not assume a tool is named `CreateAgent` or invent API endpoints, request schemas, or default behavior. Record definition source, observation time, stable object ID, and raw receipt reference. Without independent readback, do not claim a platform change took effect.

Mark capabilities separately for each action: `DOCS_ONLY` for drafting/manual work, `OBSERVED_TOOL` for a visible definition, `EXECUTED` for an actual receipt, and `READBACK_VERIFIED` for independent readback. Missing tools block their platform actions, not evidence drafts or the document-based system.

Role instructions and file-directory conventions in a shared account are not platform access controls. If the Merit Officer cannot technically be prevented from writing the official ledger, label the boundary `POLICY_ONLY` and retain human supervision. Do not claim verified isolation or expand tool access because of a Commander title.

Creating a bot does not install a Skill or prove access to runtime materials. Consider creating a bot for a vacant role only after explicit customer authorization. Separately verify responsibilities, data visibility, attached routines or initial messages, and independent readback. If the result is unknown, reconcile first instead of blindly creating again. This Skill does not provide a bot-creation executor.

## Local calculation and simulation

`scripts/merit_engine.py` is a deterministic, network-free calculator. `scripts/simulate.py` uses a fictional customer and synthetic evidence markers. The caller explicitly supplies an output directory within authorized runtime scope, outside Skill source.

Local `actor_id` is an operator assertion, not human authentication. Inputs such as `qualified`, `adopted`, and evidence references do not establish the facts as true. In real use, the human or Merit Officer opens evidence and verifies its source before submitting verified facts to the calculator. Simulated human decisions cannot approve real awards.

From the Skill root, run `python -B scripts/simulate.py --output ../.local/merit-demo-new`. Use `python3` instead if that is the local Python 3 command. The target must be a new directory outside source: do not precreate it, because existing directories are rejected rather than reset. The English package defaults to English documents; `--lang` overrides presentation language. Canonical rank keys remain Chinese for schema compatibility.

Outputs include `simulation.json`, six-stage documents, roster and official ledger, weekly documents, and acceptance results. They contain no actual host execution receipts.

The scripts calculate ordinary awards, record approved points, assess ordinary one-rank promotion eligibility, record approved promotions, manage the single special Marshal seat, and produce weekly reports. Complex corrections, award revocation, discipline, exceptional promotions, and appointment replacement use manual templates. There are no platform calls for renaming, messaging, creating roles, routines, or external delivery.

## Weekly documents

The Merit Officer manually produces a merit report, pending-review list, and team-role observations. Separate approved-and-recorded points, approved-but-unrecorded items, pending review/approval, rank changes, special appointments, pending name synchronization, coverage, and gaps. The customer separately decides recipients, timing, and scheduling. A weekly-report responsibility does not authorize creating or starting a routine.

Deliver the first report for human acceptance manually. If later authorization permits an existing scheduler, retain a single execution endpoint to avoid duplicate ledger recording or notifications. This Skill does not proactively read, modify, start, stop, or trigger routines for reporting.
