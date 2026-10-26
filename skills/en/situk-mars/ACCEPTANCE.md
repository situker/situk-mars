# Version 0.2.0 local acceptance record

Date: 2026-10-26 (`Asia/Singapore`). Conclusion: **the general-purpose Skill was assembled and its synthetic merit workflow completed end to end.** This is not a live GrokBot deployment or a record of actual awards.

The validation stage covered local implementation and simulation of claims, review, approval, ledger posting, rank conferment, and weekly reports. It did not modify live bots or routines. The package contains no network, bot-management, messaging, or scheduling calls. Repository publication is a separate distribution action; licensing is defined by the repository LICENSE.

## Rule source and generalization

The rules derive from the previously reviewed `v1.4-review.1` draft. They retain evidence requirements, five point-pool grades, individual original-week caps, conserved collaborative allocation to hundredths, conflict handling, specific human approval, one official writer, full ordinary time-at-rank cycles, a zero-bonus single Marshal seat, naming, and weekly reports.

Blank general templates and synthetic examples were built without copying real rosters, bot IDs, personal goals, account metrics, approval records, original runtime paths, or historical ledgers. Numeric policy and interpretation apply only after customer adoption. The author's private rules are not automatically in force in a customer's environment.

## Automated validation

`python -B -m unittest discover -s tests -p test_merit_engine.py -v`: **62 passed, 0 skipped, 0 failed** in the original local validation. Use `python3` instead where Python 3 has that command name. Coverage includes evidence, original cycles, pools, weekly caps, conflicts, several events by one bot on one board, batch caps, approval tampering, unknown goals, promotion timing, next-rank acceptance, Marshal appointments, and weekly reports.

Three independent complete simulations of that source returned `SIMULATION_PASSED`, passed all six stages, and produced consistent results. The local static precheck reported 0 errors and 0 warnings. A scan of 25 source/template files found no known private markers, private absolute paths, or broken Markdown links. A description count of 241 historical proxy units was a local static metric, not proof of host runtime usage. These are development-stage results, not a claim that every later language or packaging change was rerun under that exact record; consult repository validation records for release checks.

Independent review found and fixed these issues: batch proposals needed a shadow ledger for board-wide caps; a `null` goal must not become a string and appear configured; human reconciliation needed to clear old conflict queues; promotion approval needed a sealed complete payload; current state must not backdate rank using future points; and unverified delivery versions must not count as recent qualifying work.

If independently reviewed proposals are combined into a board whose caps change, posting atomically rejects the board rather than silently altering approved points. A normal board uses `review_batch` order and nominal/actual proposals, approves the items under one decision, then calls `post` once. Multiple events by one bot remain distinct entries.

## Six-stage synthetic exercise

| Stage | Verified scenario |
|---|---|
| Claims | Six fictional reports with stable events, original weeks, specific deliverables, adoption, and collaborative fields |
| Review | Missing adoption evidence awaits information; the Merit Officer's own case goes to a simulated human; two contributors divide one 3-point pool |
| Approval | Exact proposal, item, ledger version, and expiry bound together; simulated approval is not real human evidence |
| Posting | Four events produce five personal entries; Writer receives 4.80 and Builder 9.20; a capped nominal share of 3 posts 0 |
| Rank conferment | Writer remains Private after becoming eligible, then becomes Private First Class only after separate simulated approval; repetition grants no second promotion |
| Weekly report | One approved-but-unposted point is excluded from official totals; merit report, pending-review list, and role observations are produced |

Merit belongs to `2026-W43`. Settlement and rank conferment occur after closure in W44, not falsely as a promotion already made in W43. Ordinary time at rank restarts; the special Marshal appointment neither restarts the ordinary track nor grants merit points.

Real platform actions, renaming, bot changes, routine changes, and publication during that local exercise were all zero. Name status is `NAME_SYNC_NOT_EXECUTED`; a roster's target name is not a platform's observed actual name.

## Implementation boundaries

Documents and templates support the workflow without a complete bot API. Scripts provide deterministic calculation and synthetic simulation, not automatic factual verification, human authentication, externally tamper-proof auditing, or a persistent production service. Role instructions on a shared host are not system-enforced permission isolation.

Complex corrections, award revocation, discipline, exceptional promotion, and replacement of special appointees use manual templates, itemized human approval, and append-only records; the scripts do not perform them automatically. This acceptance record documents local development verification, not customer acceptance of live business operation. See the repository LICENSE for distribution terms.
