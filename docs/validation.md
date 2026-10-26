# Validation of v0.2.0

Validated on 2026-10-26. [中文](validation.zh-CN.md).

## Evidence reviewed before release

The frozen Chinese 0.2.0 rules passed 62 local regression tests and three fictional local runs. A separate GrokBot review ran the same 62 cases and the six-stage exercise. Its source manifest and 15 exercise files were checked against the frozen input; the ledger was independently recalculated. No blocking numeric-policy change was found.

This describes inspected review evidence, not authentication of GrokBot's execution environment. Private handoff logs, real bot identities and local workspace paths are excluded from the public distribution.

## Public bilingual release checks

- Both language packs pass the same 62 rule regression cases. These are **62 unique cases run in two packs**, not 124 different rule cases.
- Each pack completes a local six-stage synthetic exercise in its default language. Both produce 4.80 points for the writer, 9.20 for the builder, and zero formal points for the Commander and Merit Officer.
- Four events produce five personal ledger entries. A shared 3-point pool splits 1.80/1.20. An over-cap item posts zero; an approved but unrecorded 1-point item remains outside totals.
- The writer receives Private First Class only after a separate simulated rank decision. The English display target uses an English label; stored rank keys retain the canonical Chinese schema.
- The Marshal appointment adds zero points and preserves the ordinary-rank clock. Duplicate awards and promotions are prevented.
- Both packs have identical Python files and operational policy. Only presentation text, default language and English rank labels differ.
- Offline distribution validation checks licenses, local documentation links, template inventories, SVG syntax and common private-data patterns. This scan complements human review; it cannot guarantee that every possible secret is detected.
- Standalone release archives include the complete Skill, MIT license and a file manifest. Download checksums cover both archives.

The repository's GitHub Actions workflow repeats the rule tests, distribution checks and both exercises on Linux and Windows with Python 3.11 and 3.13. The actual result of each run is visible in [Actions](https://github.com/situker/situk-mars/actions); this document does not predeclare a remote run successful.

## Reproduce locally

From the repository root:

```bash
python -B tools/validate_release.py
python -B -m unittest discover -s skills/zh-CN/situk-mars/tests -p test_merit_engine.py
python -B -m unittest discover -s skills/en/situk-mars/tests -p test_merit_engine.py
python -B skills/zh-CN/situk-mars/scripts/simulate.py --output .local/check-zh
python -B skills/en/situk-mars/scripts/simulate.py --output .local/check-en
python -B tools/build_packages.py
```

Use `python3` where appropriate. Exercise output folders must be new and outside Skill source. Do not pre-create them.

## What remains outside these checks

The exercise uses fictional bots, synthetic evidence and code-generated owner decisions. It does not establish real adoption, authenticate a human, test platform access control, or deploy a production ledger service. No live bot is created, installed, renamed or modified; no routine is changed. Complex corrections, disciplinary actions and exceptional promotions remain manual workflows.
