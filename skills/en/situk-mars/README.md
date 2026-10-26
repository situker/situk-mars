# situk-MARS · English Skill

**Situk Merit-based Agent Rank System**, version 0.2.0.

A GrokBot document workflow for contribution reports, independent evidence review, human approval, merit records, rank conferral, and weekly reporting. Begin with [SKILL.md](SKILL.md). Numeric rules are in [policy.json](policy.json); reusable forms are in [templates/](templates/).

The English and Chinese packs share the same Skill ID `situk-mars`. Choose one language pack per environment. Both have the same rule engine and numeric policy; canonical rank keys remain Chinese, with English display labels mapped separately.

From this Skill folder:

```bash
python3 -B scripts/simulate.py --output ../.local/mars-demo-en
python3 -B -m unittest discover -s tests -p test_merit_engine.py -v
```

Use `python` on systems where it invokes Python 3.11+. Do not pre-create the final output folder, even empty. The default exercise output is English; `--lang en` or `--lang zh-CN` overrides presentation language. All inputs, bots, evidence and approvals are fictional. Nothing connects to GrokBot, sends messages, creates bots, renames profiles or changes routines.

The exercise produces six-stage notes, a practice ledger, rank records, a weekly merit report, a pending-review list and team-role observations. The helpers check deterministic rules; they do not verify real-world facts, authenticate people or provide a persistent production ledger service. Complex corrections, discipline and exceptional actions use manual templates.

Project, architecture and both languages: [situker/situk-mars](https://github.com/situker/situk-mars). Validation history: [ACCEPTANCE.md](ACCEPTANCE.md). Licensed under [MIT](LICENSE).

Author: **司徒K (Situk)** · [www.situking.com](https://www.situking.com)
