# situk-MARS · English Skill

**Situk Merit-based Agent Rank System (MARS) · v0.2.0**

Give your GrokBot team a consistent way to report contributions, review evidence, approve rewards, record merit, confer ranks and report the results each week. Start with [SKILL.md](SKILL.md); the numeric rules are in [policy.json](policy.json), and the forms are in [templates/](templates/).

## Roles and workflow

The **Commander** coordinates and is the sole official ledger writer. The **Merit Officer** reviews evidence and reconciles the records. The **Human Owner** gives final approval. **Marshal** is a separate special appointment for the Commander, with **zero or one seat**, no points and no change to the ordinary-rank clock.

**Report → Review → Human approval → Record → Confer rank → Weekly report**

Approval binds exact items. Approved but unrecorded points stay outside formal totals, and a promotion needs its own approval. One event has one award pool, shared among contributors. An Honorary Title awards **50 points** only for independent new outcomes; previously awarded work receives the title only, without another **50 points**.

## Set up a first run

Configure the Human Owner, business goal, authorized data directory, merit start date and existing role bindings before using the workflow. If a role is unfilled, the human can cover it while a separate setup proposal is considered.

The English and Chinese packs share the same Skill ID, `situk-mars`. Choose one language pack per environment. Both use the same rule engine and numeric policy; stored rank keys remain Chinese, with English display labels mapped separately.

From this Skill folder, run the fictional exercise and tests:

```bash
python3 -B scripts/simulate.py --output ../.local/mars-demo-en
python3 -B -m unittest discover -s tests -p test_merit_engine.py -v
```

Use `python` where it invokes Python **3.11+**. Leave the final output folder uncreated, even as an empty directory. Keep runtime files outside the Skill source folder. The default output is English; `--lang en` or `--lang zh-CN` selects another presentation language.

## What you will see

The exercise produces six-stage notes, a practice ledger, rank records, a weekly merit report, a pending-review list and team-role observations. Its fictional writer records **4.80** points and receives a separately approved promotion; the builder records **9.20**. The Commander and Merit Officer each have **0.00** formal points.

Both language packs pass the same **62 rule tests**. These check rule behavior; all example bots, evidence and approvals are synthetic. See [ACCEPTANCE.md](ACCEPTANCE.md) for validation history.

## Current scope

This pack provides a document workflow and local helpers. It does not connect to GrokBot, send messages, create bots, rename profiles or configure routines. The helpers do not verify real-world facts, authenticate humans or supply a persistent production ledger service. Complex corrections, discipline and exceptional actions use manual proposals and decisions.

Project, architecture and both languages: [situker/situk-mars](https://github.com/situker/situk-mars). Download the existing [v0.2.0 release](https://github.com/situker/situk-mars/releases/tag/v0.2.0). Licensed under [MIT](LICENSE).

Created by **司徒K (Situk)**, a business services entrepreneur focused on GEO and practical AI adoption. [About the author](https://github.com/situker/situk-mars/blob/main/docs/about-author.md) · [www.situking.com](https://www.situking.com) · [X: @situking](https://x.com/situking)
