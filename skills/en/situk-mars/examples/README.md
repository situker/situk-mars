# Synthetic exercise inputs

`synthetic-reports.json` is a fixed practice input, not an execution result. The four role IDs—`demo_writer`, `demo_builder`, `demo_commander`, and `demo_officer`—are fictional. Every `synthetic://` reference is an illustrative placeholder, not proof of real delivery, adoption, reuse, or human approval. Never copy these references into an actual merit ledger.

Suggested simulation configuration: new-merit start `2026-10-12T00:00:00+08:00`; all four roles join then with ordinary rank Private and the same time-at-rank start. The goal is “make the fictional service delivery process more complete and verifiable.” Use final observation time `2026-10-26T10:00:00+08:00`, when original cycle `2026-W43` has closed. The Commander's special Marshal rank still needs a separate simulated human decision. A role title does not establish a Marshal appointment.

Canonical rank keys in JSON and snapshots remain Chinese, while the English package uses translated display labels. Its local simulation documents default to English; `--lang` can override presentation.

| Order | Scenario | Expected result after itemized simulated human approval and Commander posting |
|---|---|---|
| 1 | Writer's adopted Third-Class Merit with complete goal link | Writer +3.00 |
| 2 | Builder's stable asset reused in a second independent task | Builder +8.00 |
| 3 | Shared Third-Class Merit outcome: Writer 60%, Builder 40% | Writer +1.80, Builder +1.20; total 3.00 |
| 4 | Writer's third Third-Class Merit claim in the same week | Contribution retained; nominal 3.00, capped posting 0.00 |
| 5 | Claimed adoption without adoption evidence | `NEEDS_EVIDENCE`; no approval or posting, no automatic lower grade |
| 6 | Merit Officer's own Commendation claim | No self-review; refer to human; no points until approved and posted |

After the first four items are processed in order, expected official totals are Writer 4.80, Builder 9.20, Commander 0.00, and Merit Officer 0.00. If a simulated human then reviews, approves, and posts item six, the Merit Officer gains 1.00. Independent reconciliation still goes to the simulated human rather than the Merit Officer checking its own award.

The Second-Class Merit example separately provides `reuse_task_id`, `reuse_ref`, and `reuse_acceptance_ref`. These identify the second independent task, actual reuse, and acceptance of the reuse result in that task. Acceptance of the original asset cannot substitute for second-task acceptance. All three evidence references here are synthetic.

The promotion exercise can initially produce only a candidate. Writer may be proposed from Private to Private First Class if it also satisfies at least one full time-at-rank cycle, qualifying delivery, and human-approved next-rank responsibilities and their acceptance. A candidate does not change rank. The Commander posts the separately simulated human approval; names become pending synchronization targets without a real platform call.

The runner writes actual simulation logs, synthetic approvals, ledger, roster, and weekly reports to a project `.local/` runtime location, never into this directory. Supply a new output directory outside Skill source and do not precreate it. A local operator's `owner` identity and `synthetic://` approval records are simulation assertions, not biometric, signature, or platform-message authentication.
