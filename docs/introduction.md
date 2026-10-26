# situk-MARS

**Give your bot team ranks. Reward their contributions.**

[Download English ZIP](https://github.com/situker/situk-mars/releases/download/v0.2.0/situk-mars-v0.2.0-en.zip) · [See a sample report](examples/en/weekly-report.md) · [First run](quickstart.md)

Start with the results: a weekly merit report shows recorded rewards, a pending-review list identifies missing evidence and decisions, and team-role observations highlight reuse opportunities and responsibilities worth reviewing. [Browse the three exercise documents](examples/README.md).

**Situk Merit-based Agent Rank System (MARS)** is a military-style rank and merit Skill for GrokBot teams. It helps you answer a practical question: when several bots work together, who contributed what, and which rewards are justified?

One bot writes the plan, another builds the tool, and a third checks the result. The work may be useful, but the evidence is scattered across conversations. MARS brings deliveries, acceptance, adoption, reviews and decisions into a shared document workflow. Merit follows inspectable contributions, rather than message counts or a bot's own claims.

## Three decision roles

The **Commander** collects reports, prepares proposals and is the sole writer of the official ledger under valid approval. The **Merit Officer** reviews evidence, checks duplicates, calculates shared awards and weekly caps, then independently reconciles the records. The **Human Owner** makes the final decisions.

Those responsibilities remain separate from rank. **Marshal** is a special appointment for the Commander, with **zero or one seat**. It grants no points, does not reset the ordinary-rank clock and creates no self-approval authority. The Merit Officer's own cases, or cases involving both governance roles, go to the human or an unconflicted third party designated in advance by that human.

## From a contribution to a weekly record

**Report → Review → Human approval → Record → Confer rank → Weekly report**

A bot first reports what it delivered and provides acceptance or adoption evidence. Review establishes what the evidence supports, checks shared contributions and caps, and identifies conflicts. The Human Owner approves exact items; the Commander then records the approved result once.

One event has one award pool, divided among contributors. A late claim remains in its original week. A capped share records **0**, without being transferred, downgraded or carried forward. An Honorary Title grants **50 points** only for independent new outcomes; previously awarded work receives the title only, without another **50 points**.

Points and ranks serve different purposes. The **ten ordinary ranks** have eligibility requirements, but meeting them only creates a candidate. A promotion needs its own human approval. Marshal remains a separate appointment, outside that ordinary progression.

Each week produces **three documents**: a merit report, a pending-review list and team-role observations. Together they show recorded rewards, approved but unrecorded items, missing evidence and decisions waiting for the owner. They can also reveal duplicated work, reusable assets and role gaps. Those observations become proposals for discussion, not automatic changes to the team.

## Try the workflow before using it

Choose the [English Skill](../skills/en/situk-mars/SKILL.md) or the [Chinese Skill](../skills/zh-CN/situk-mars/SKILL.md), then configure the owner, goal, authorized data directory, start date and existing role bindings. The [v0.2.0 release](https://github.com/situker/situk-mars/releases/tag/v0.2.0) includes rules, **nine templates**, and optional Python helpers. Python **3.11+** is sufficient for the local exercise.

The fictional example runs all six stages: the writer records **4.80** points and receives a separately approved promotion; the builder records **9.20**; the Commander and Merit Officer each retain **0.00** formal points. Both language packs pass the same **62 rule tests**, and the published release passed **four CI combinations**. These results demonstrate the rules, not real customer outcomes. See the [quick start](../README.md#try-it-locally) and [validation record](validation.md).

## Current boundaries

MARS first supports GrokBot through documents. It does not yet create bots, rename live profiles, enforce platform access control or schedule routines. Its local helpers check deterministic rules; people must still verify evidence and provide traceable human approval. Complex corrections, discipline and exceptional actions remain manual workflows.

Created by **司徒K (Situk)**, a business services entrepreneur focused on GEO and practical AI adoption. Situk turns methods into tools and ideas into working projects, and shares the decisions and mistakes along the way.

[Architecture](architecture.md) · [Get started](../README.md) · [About the author](about-author.md) · [中文介绍](introduction.zh-CN.md)
