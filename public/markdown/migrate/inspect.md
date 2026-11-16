# Move from Inspect AI

> Import the logs Inspect AI wrote as runs in the local Evals UI, then open, compare and review them. Needs SDK 0.1.4 or later.

Source: [Web version](https://docs.martiansecurity.ai/migrate/inspect/)

> **Page qualification:** Python SDK · Any developer with Inspect AI log files; no Martian account, API key or model key · Walkthrough partly verified. [Verification details](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md).

> **Walkthrough limits:** Every documented command ran against the SDK source at martian-redteam 08d2673. Inspect AI 0.3.290, in its own environment, wrote the sample logs: a three-sample task on Inspect's mock model answering from a table, scored with includes() and a numeric scorer, as two .eval logs (versions 1 and 2 of the table) and one .json log with two epochs. The .eval import printed the documented lines with exit 0 (2 passed / 1 failed, then 3 passed); the .json log imported as 6 cases. A log written with --no-log-samples was refused with the documented message, exit 2 and nothing imported. In martian ui the runs, the results table, a case's assessments, its trace (agent and model spans) and Compare (1 improved, 2 unchanged) were checked. Not verified: a published 0.1.4 package, logs with tool calls or model-graded scorers from a real provider, and logs of evals still running.

Partly verified guide

Every command on this page was run against the SDK source built for 0.1.4 (martian-redteam 08d2673), with sample projects made by Inspect AI 0.3.290. It was not run again on the later source or on the package published to PyPI.

Bring the logs your Inspect AI evals wrote into the local Evals UI. Each log becomes a run whose cases, scores and conversations you can open, compare with another run case by case, and review.

The importer reads log files only. It does not run Inspect tasks, and Inspect does not need to be installed next to the SDK. Keep running your tasks in Inspect and import their logs, or write new evals as [suite files](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md).

Needs SDK 0.1.4 or later

`martian evals import inspect` and the local Evals UI (`martian ui`) are in **martian-sdk 0.1.4**. The earlier 0.1.3 answers `No such command 'import'`.

## Before you start

-   Use **Python 3.12 or newer** and a macOS or Linux shell.
-   You need log files Inspect wrote, `.eval` or `.json`, for evals that have **finished** and that were logged **with their samples**.
-   You need no Martian account, API key or model key. The import reads files on your machine and writes to a local data folder (default `~/.martian/evals`); nothing is sent to Martian or to a model provider.
-   The data folder holds each sample’s input, reply and scores in clear text. Keep it as private as the logs.

## 1\. Install the SDK

From the folder that holds Inspect’s `logs` folder, create an isolated environment and install the SDK:

```sh
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade 'martian-sdk[evals]'
.venv/bin/martian --version
```

The first command must report Python 3.12 or newer. The last must print **0.1.4** or later. If it prints 0.1.3, stop here: that release has no importer.

## 2\. Import the logs

Name the log files. A wildcard takes every `.eval` log in the folder:

```sh
.venv/bin/martian evals import inspect logs/*.eval
```

The first time, log lines from the local evaluation store appear while it creates the data folder. Then each log prints one line. For two logs of a three-sample task named `faq`:

```text
2026-11-15T15-31-02-00-00_faq_SJf8QyeQAto7yqzZtu5bGd.eval: run inspect-faq-1, 3 cases: 2 passed, 1 failed, 0 errors, 0 without a verdict
2026-11-15T15-31-07-00-00_faq_6aAoMan7S5wPbpwYuaZUdx.eval: run inspect-faq-2, 3 cases: 3 passed, 0 failed, 0 errors, 0 without a verdict
Open them in the local Evals UI: martian ui
```

The exit code is **`0`**. Each run is named `inspect-`, the task’s name and a number that counts that task’s imported runs.

-   Import `.json` logs the same way, for example `logs/*.json`. One command can take both formats and any number of files.
-   Every file is read before anything is written. If one cannot be imported, the command exits **`2`**, says which file and why, and imports none of them.
-   Importing the same log again creates another run. Import each log once.
-   The log is not copied. The run records the log’s path and checksum, so keep the log file.
-   To import into a folder other than `~/.martian/evals`, add `--data-dir DIR`, or set `MARTIAN_EVALS_HOME`. Open the UI with the same folder.

## 3\. Open the runs

```sh
.venv/bin/martian ui
```

Your browser opens `http://127.0.0.1:7600/`. The UI has one user and no login; stop it with Ctrl+C in the terminal.

1.  **Runs** lists the imported runs in the **Default** project, with their pass rate and counts.
2.  Select a run. Its results table shows each sample’s input, the sample’s target as the expected answer, the model’s reply and the case’s verdict.
3.  Select a row’s **Inspect** button, which opens the case. The panel shows one assessment for each Inspect score. **View trace** shows the sample’s conversation as spans: one for each model reply and one for each tool call.
4.  Open **Compare**, choose two runs as **Baseline** and **Candidate**, and select **Compare runs**. Runs over the same samples pair case by case. In the example, `inspect-faq-2` improves one sample and leaves two unchanged.

Runs pair when their samples have the same IDs, inputs and targets, whatever their order. A run with more epochs pairs with a run with fewer on each sample’s first epoch.

## What maps where

| In Inspect AI | In the local Evals UI |
| --- | --- |
| A log: one task evaluated on one model | A run, named `inspect-<task>-<n>`. A log whose eval succeeded is **Completed**, one that ended in an error **Failed**, one cancelled **Cancelled** |
| A sample | A case, with the sample’s ID as the case ID |
| Each later epoch of a sample | Its own case, with the ID `<sample id> (epoch <n>)` |
| The sample’s input | The case’s input: the prompt text, or the chat messages |
| The sample’s target | The expected answer |
| The model’s completion | The reply |
| A score | An assessment, with the value Inspect recorded and its explanation as the reason |
| A score from a scorer that called a model | An LLM judge assessment, with that grading model as its source |
| The sample’s messages and tool calls | A trace, timed by Inspect’s model and tool events |
| Model token use and cost | The trace’s tokens, and its cost when every model reported one |
| Inspect’s metrics, such as accuracy | Kept in the run’s record. The run’s pass rate in the UI comes from its case verdicts |

Inspect’s score values become verdicts like this:

| Score value | Verdict |
| --- | --- |
| `C` (correct) or `true` | Pass |
| `I` (incorrect), `P` (partial), `N` (no answer) or `false` | Fail |
| A number, or other text | None. The value is kept and shown |
| A dictionary or a list | One assessment for each entry, named `<scorer>/<key>` or `<scorer>/<index>` |
| Not a number (Inspect’s unscored value) | No value, recorded as an error with Inspect’s reason |

A case’s verdict follows its sample and scores, in this order: an error when the sample failed, failed when any score fails, an error when a score is unscored, and passed when one passes. A case whose scores are only numbers or text has no verdict.

## What does not carry over

-   **Tasks, solvers and scorers.** Nothing in your Inspect code is converted or run. An imported run cannot be run again from the UI: its replies come from the log.
-   **Epoch reductions** that Inspect computed across a sample’s epochs.
-   **Each sample’s store and sandbox**, and events other than model calls, tool calls and spans. They stay in the log, which the run names.

## Failures and limits

-   **`No such command 'import'`:** the installed SDK is older than 0.1.4. See the note at the top of this page.
-   **`Importing Inspect logs needs martian-sdk[evals]`:** install the `evals` extra, as in step 1.
-   **`... has no samples: Inspect wrote it without them (--no-log-samples)`:** the log holds results without samples, so there is nothing to import. Run the eval again with samples logged. The command exits `2` and writes nothing.
-   **The eval has not finished:** a log of an eval that is still running is refused, and so is an `.eval` log whose process stopped before it wrote the log’s header. Import the log once the eval ends. A log of an eval that ended in an error, or was cancelled, imports as a failed or cancelled run.
-   **Another log format version:** the importer reads Inspect’s log format version 2 and refuses others.
-   **Exit code `2` with `Import failed:`:** the message names the file and the reason. Nothing was imported; fix or leave out that file and run the command again.

## Next

-   [Run evals locally with a suite file](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md): write new evals for your agent as a suite file.
-   [Move from MLflow](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/mlflow.md) and [Move from promptfoo](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/promptfoo.md) bring other tools’ results into the same data folder.
