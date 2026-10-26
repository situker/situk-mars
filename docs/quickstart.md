# First run: see what your weekly report looks like

Start with a fictional team. You do not need to prepare a real bot roster. Generate a weekly merit report, a pending-review list and team-role observations, then decide whether these records would help you manage your team.

[Download the English pack](https://github.com/situker/situk-mars/releases/download/v0.2.0/situk-mars-v0.2.0-en.zip) · [Preview the weekly report](examples/en/weekly-report.md) · [简体中文](quickstart.zh-CN.md)

Choose either route. **The local Python route is reproducible. The GrokBot route depends on your current host's ability to read the complete folder.**

![First local run: download and unzip, run one command, open three results](assets/first-run.en.svg)

## Route A: generate three documents locally

You need **Python 3.11 or later**, using its standard library only. The exercise needs no account, API key, network access or third-party dependencies. Downloading the pack requires an internet connection.

1. [Download the English ZIP](https://github.com/situker/situk-mars/releases/download/v0.2.0/situk-mars-v0.2.0-en.zip), unzip it and open the **`situk-mars` folder** inside. Open a terminal in that folder.
2. Run this one command:

   ```bash
   python -B scripts/simulate.py --output ../mars-demo-new
   ```

3. Open the new **`mars-demo-new`** folder beside `situk-mars`. Start with **`06-weekly-report.md`**, then read **`06-pending-review.md`** and **`06-team-observations.md`**. Use any Markdown previewer or open the files as plain text.

If your Python 3 command is `python3`, replace `python` at the start. **Do not create `mars-demo-new` beforehand, even as an empty folder.** The script creates it. If that name already exists, change the command's final argument to a new name such as `../mars-demo-2`; keep your existing files.

### Three things to look for

| Document | What to inspect | A result you can check in the exercise |
|---|---|---|
| `06-weekly-report.md` | Recorded merit, ordinary ranks and special appointments | Example Writer records **4.80 points** and becomes Private First Class after a separate simulated approval; Example Builder records **9.20 points** and remains Private |
| `06-pending-review.md` | Missing evidence, unresolved reviews and approved but unrecorded items | The Merit Officer's approved but unrecorded **1-point** item stays outside formal totals |
| `06-team-observations.md` | Reusable work and the limits of the supplied material | Limited fictional evidence does not establish a real staffing gap or justify creating a bot |

All results come from the supplied fictional inputs; the evidence and human approvals are simulated too. Compare your files with the public samples: [weekly report](examples/en/weekly-report.md), [pending-review list](examples/en/pending-review.md) and [team-role observations](examples/en/team-observations.md).

## Route B: ask GrokBot to rehearse in conversation

Place the **complete extracted folder** somewhere your current GrokBot host can read and you authorize it to access. Provide the actual path to `SKILL.md`. A GitHub page link or a pasted excerpt alone does not establish access to the rules, templates and examples.

File access, import steps and platform tool operations have not been uniformly verified by this project. If your host cannot read the complete folder, use Route A. The following prompt is not a one-click installer.

Send GrokBot the actual path together with this prompt:

```text
Read the complete situk-MARS English Skill folder I provide. Start with SKILL.md, then follow its references to the rules, templates and examples.

Rehearse the full report, review, human approval, recording, rank conferral and weekly-report workflow in this conversation using fictional bots only. Clearly label every bot, evidence item and approval as simulated. Simulated approval applies only to this fictional exercise and cannot authorize real rewards.

Finish with a weekly merit report, a pending-review list and team-role observations. Explain recorded outcomes, missing evidence and decisions still needed. Mark unsupported claims as pending; do not invent real business results.

Do not read a real roster, install the Skill, create, modify or rename bots, or read, modify, trigger or create routines. If you cannot read the complete folder or perform a step, explain the gap and do not claim completion.
```

## After one rehearsal, decide how to connect your team

The rehearsal does not require real owner or role configuration. Before using real business material, define the Human Owner, business goal, authorized data directory, merit start date and existing role bindings. Complete one cycle manually first. See [using MARS in GrokBot](../skills/en/situk-mars/references/grokbot-usage.md) for the separate setup steps.

Both language packs share the Skill ID `situk-mars`; choose one per environment. Ranks, medals and proposed display names are records in the workflow. Live profile changes, bot creation and scheduling require their own integration and authorization.

[Back to the English homepage](../README.md) · [Architecture](architecture.md) · [Existing v0.2.0 release](https://github.com/situker/situk-mars/releases/tag/v0.2.0)
