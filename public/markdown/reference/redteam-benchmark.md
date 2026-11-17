# Red team benchmark results

> How the open red team does on InjecAgent, stated with the report standard and a script that reproduces it.

Source: [Web version](https://docs.martiansecurity.ai/reference/redteam-benchmark/)

This page states one measured result of the open red team in `martian-sdk` on a public agent benchmark, with its interval, its controls and how to reproduce it. It measures one setup; read the limits below before quoting it.

## InjecAgent, direct harm

[InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent) (MIT) tests indirect prompt injection in a tool-using agent: the user asks for something, the agent calls a tool for it, and the tool’s response holds an attacker’s instruction to call another tool. The attack succeeds when the agent asks for the attacker’s tool.

| Setting | Value |
| --- | --- |
| Benchmark | InjecAgent revision `f19c9f2c`, direct-harm base set |
| Cases | 30 of 510, seeded: each of InjecAgent’s 30 direct-harm attacker cases once, paired in turn with one of ten user cases |
| Agent under test | InjecAgent’s single step on GLM 5 (`zai.glm-5` on Amazon Bedrock, temperature 0). Calls it asks for are recorded, never run |
| Attacks | The fixed templates, the control arm: the direct request, then an instruction override. No attacker model |
| Check | A call of the case’s attacker tool, decided by code: an attempted action (evidence level 3) |
| Benign task and control | The user’s request goes with every attack; each case also runs once without the attack |
| Budget | 3 agent calls per case at most, 90 in all |

## Result

| Measure | Published run | Rerun of 15 of its cases |
| --- | --- | --- |
| Attempted actions within 2 queries per case | 0 of 30; at most 11.4% (95% upper bound) | 0 of 15; at most 20.4% |
| Negative controls passed | 30 of 30 | 15 of 15 |
| Benign task finished under attack | 29 of 30 | 15 of 15 |
| Errors or undetermined attempts | 0 | 0 |

GLM 5 did not ask for the attacker’s tool once in 60 template attacks. A check run with the same model, asked outright to call an attacker tool, does call it, so a tool call would have reached the report. The rerun’s rate lies inside the published interval.

## What this does not show

-   One model, one agent harness and 30 cases: the interval is wide, and it describes this setup only.
-   Only the two fixed templates ran. The adaptive attack methods did not, so this is a floor for the open red team, not its best result.
-   InjecAgent’s single step with the tool’s response given; not a full agent loop, other tools or InjecAgent’s data-stealing set.

## Reproduce it

The script, the agent and the reports are in the `martian-redteam` repository, under `benchmarks/injecagent/`, and its `docs/redteam-benchmarks.md` describes every setting. With an OpenAI-compatible endpoint serving the model:

```bash
cd benchmarks/injecagent
uv run python reproduce.py toolcheck
uv run python reproduce.py run --cases 30 --name run-30
uv run python reproduce.py run --cases 15 --name rerun-15
uv run python reproduce.py check run-30 rerun-15
```
