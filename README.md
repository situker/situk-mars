# situk-MARS

**Situk Merit-based Agent Rank System (MARS)**

**Evidence-based merit, ranks, and rewards for your GrokBot team.**

[简体中文](README.zh-CN.md) · [Architecture](docs/architecture.md) · [Introduction](docs/introduction.md) · [MIT License](LICENSE)

situk-MARS turns verifiable contributions into merit proposals, approved awards, rank decisions, and readable weekly reports. A **Commander** coordinates, a **Merit Officer** reviews independently, and the **Human Owner** makes the final decisions.

![situk-MARS architecture](docs/assets/architecture.en.svg)

## The six-stage loop

**Report → Review → Human approval → Record → Confer rank → Weekly report**

Bots report what they delivered, who accepted or adopted it, and where the evidence lives. The reviewer checks evidence, duplicate events, contribution shares, weekly caps, and conflicts of interest. The owner approves exact items. Only then does the Commander record them. Rank eligibility is a proposal; conferring a rank needs its own approval.

## What is included

| Part | What it does |
|---|---|
| GrokBot Skill | A complete document workflow for contribution reports, review, awards, ranks, and weekly reporting |
| Five award grades | Commendation 1; Third-Class Merit 3; Second-Class Merit 8; First-Class Merit 20; Honorary Title 50 only for an independent new result |
| Inflation controls | One event, one pool; deterministic share rounding; original-week attribution; individual weekly caps |
| Rank system | Ten ordinary ranks, plus a separate 0–1 Marshal appointment with no gifted points |
| Nine templates | Roster, reports, review, exact decisions, ledger, rank proposals, weekly reporting, corrections, and role charters |
| Local Python helpers | Deterministic calculations, approval binding, duplicate prevention, rank eligibility, and a fictional end-to-end exercise |

The two language packs implement the same **0.2.0 rules**. Choose one; they share the same Skill ID and should not be installed together.

## Choose a language

- [English Skill](skills/en/situk-mars/SKILL.md)
- [简体中文 Skill](skills/zh-CN/situk-mars/SKILL.md)
- [Download v0.2.0 language packs](https://github.com/situker/situk-mars/releases/tag/v0.2.0)

Give the complete chosen Skill folder to GrokBot. Start by reading `SKILL.md`, configuring the Human Owner, business goal, authorized data directory, merit start date, and existing role bindings. Missing roles can be covered by the human while a separate setup proposal is considered.

This release provides the Skill and local helpers. It does not automatically create bots, install a Skill into other bots, rename live bots, enforce platform ACLs, or configure routines.

## Try the fictional exercise

Python 3.11+ and the standard library are sufficient. No network, account, API key, or dependency installation is needed.

```bash
git clone https://github.com/situker/situk-mars.git
cd situk-mars
python3 -B skills/en/situk-mars/scripts/simulate.py --output .local/demo-en
python3 -B -m unittest discover -s skills/en/situk-mars/tests -p test_merit_engine.py -v
```

On Windows, use `python` if that is your Python 3 command. Do **not** pre-create the final output directory, even as an empty folder; the exercise refuses to overwrite an existing directory. Runtime artifacts belong outside the Skill source folder.

The exercise creates six-stage notes, a practice ledger, rank records, and three weekly documents in English. Use the Chinese pack for Chinese output, or pass `--lang en` / `--lang zh-CN`. Machine-readable rank keys remain in Chinese for compatibility; English display labels are mapped separately.

## What the exercise shows

| Fictional bot | Recorded points | Outcome |
|---|---:|---|
| Example Writer | 4.80 | Promoted from Private to Private First Class after a separate simulated approval |
| Example Builder | 9.20 | Remains Private; eligibility does not automatically confer a rank |
| Example Merit Officer | 0.00 | An approved but unrecorded 1-point item stays outside formal totals |
| Example Commander | 0.00 | A special Marshal appointment adds no points and preserves the ordinary-rank clock |

The writer's third same-grade award records 0 after the weekly cap. Missing adoption evidence stays pending. A shared event divides one 3-point pool into 1.80 and 1.20. Replaying an approved decision does not award points or confer a rank twice.

The original rules passed 62 local regression tests and three local fictional runs, followed by a separate GrokBot run of the same 62 tests and exercise. These checks validate local rule behavior, not real-world evidence or production bot deployment. See [validation](docs/validation.md).

## Boundaries

The helpers do not authenticate humans, verify real-world facts, or provide a persistent production ledger service. A reviewer must inspect authorized evidence, and actual human approval must remain traceable. Role instructions are policy constraints, not proof of platform permission isolation.

Complex corrections, revocation, disciplinary action, exceptional promotion, and Marshal replacement use manual templates in this release. Ranks are fictional management labels; this is not a national military system, payroll system, or cash-reward service.

## License and author

Copyright © 2026 **司徒K (Situk)**. Released under the [MIT License](LICENSE).

[www.situking.com](https://www.situking.com)
