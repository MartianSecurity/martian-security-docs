# Move from MLflow

> Copy an MLflow tracking store into the local Evals UI: experiments, traces, assessments, evaluation datasets and evaluation runs. Needs SDK 0.1.4.

Source: [Web version](https://docs.martiansecurity.ai/migrate/mlflow/)

> **Page qualification:** Python SDK · Any developer with read access to the MLflow tracking store's database; no Martian account, API key or model key · Walkthrough partly verified. [Verification details](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md).

> **Walkthrough limits:** Every documented command ran against the SDK source at martian-redteam 08d2673 with sample tracking stores that MLflow itself wrote (one experiment with three application traces, two in a session, a person's feedback, an LLM judge's feedback, an expectation, a three-record evaluation dataset, two mlflow.genai.evaluate runs with a code scorer, and a training run with only a parameter and a metric). The 3.18.0 SQLite store's dry run, copy and second copy printed the documented reports with exit 0, and its SHA-256 was unchanged. A 3.16.1 store was refused with exit 2 and nothing written; its copy upgraded with the SDK's mlflow db upgrade imported with the same counts. A store on PostgreSQL 17 (postgres extra) passed the dry run and copy from an environment variable URL, with the password never printed; without the extra the documented message and exit 2 appeared. --experiment, an unknown experiment, an http:// server address and an mlruns folder behaved as documented. In martian ui the project, traces, the two-turn session, both runs, Compare (1 improved, 2 unchanged) and the dataset were checked. Not verified: a published 0.1.4 package, stores from MLflow 2.x, the upgrade of a Postgres copy, and spans kept in a remote artifact store.

Partly verified guide

Every command on this page was run against the SDK source built for 0.1.4 (martian-redteam 08d2673), with sample projects made by MLflow 3.18.0 and 3.16.1. It was not run again on the later source or on the package published to PyPI.

If your team traced and evaluated an agent with MLflow, copy its tracking store into the local Evals UI. Each experiment becomes a project, with its traces, the feedback and expectations on them, its evaluation datasets and its evaluation runs. You can then compare runs case by case and review results without a Martian account.

The import is a **copy**. It reads the store over a connection that cannot write and never changes it, so your MLflow keeps working as before. Changes made in MLflow later are not seen until you copy again.

Needs SDK 0.1.4 or later

`martian evals import mlflow` and the local Evals UI (`martian ui`) are in **martian-sdk 0.1.4**. The earlier 0.1.3 answers `No such command 'import'`.

## Before you start

-   Use **Python 3.12 or newer** and a macOS or Linux shell.
-   You need the store’s **database**: the SQLite file, usually `mlflow.db`, or the Postgres database your MLflow server writes to (its `--backend-store-uri`). The import does not read an MLflow server’s address (`http://...`) or MLflow’s file store (an `mlruns` folder with no database).
-   The store must be at the **schema version MLflow 3.18.0 writes**, the MLflow the SDK installs. A store from an older MLflow is refused until you upgrade a copy ([step 3](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/mlflow.md#3-copy-and-upgrade-an-older-store)). A store from a newer MLflow is refused until an SDK release supports it.
-   Traces whose spans MLflow kept as artifact files are read only when those files are on this machine.
-   You need no Martian account, API key or model key. Nothing is sent to Martian or to a model provider.
-   The copy holds your traces’ inputs and outputs in clear text, in a local data folder (default `~/.martian/evals`). Keep that folder as private as the store itself.

## 1\. Install the SDK

In an empty folder, or the folder that holds `mlflow.db`, create an isolated environment and install the SDK:

```sh
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade 'martian-sdk[evals]'
.venv/bin/martian --version
```

The first command must report Python 3.12 or newer. The last must print **0.1.4** or later. If it prints 0.1.3, stop here: that release has no importer.

For a store on Postgres, install the `postgres` extra instead of `evals`. It includes everything in `evals` and the Postgres driver:

```sh
.venv/bin/python -m pip install --upgrade 'martian-sdk[postgres]'
```

## 2\. Check the store with a dry run

Point the importer at the database file. `--dry-run` checks the schema version, reads everything and reports what it would copy, without writing anything:

```sh
.venv/bin/martian evals import mlflow mlflow.db --dry-run
```

For a store with one experiment, `faq-bot`, that holds application traces, an evaluation dataset, two evaluation runs and one training run, it prints:

```text
Read sqlite:////path/to/mlflow.db: MLflow schema revision f4a9b2c7d1e6, the one mlflow-skinny 3.18.0 reads.
To copy (nothing was written, --dry-run):
  experiment 1 as project faq-bot: 9 traces, 2 runs
    run mlflow-bot-v1 (completed): 3 cases: 2 passed, 1 failed, 0 errors, 0 without a verdict
    run mlflow-bot-v2 (completed): 3 cases: 3 passed, 0 failed, 0 errors, 0 without a verdict
  dataset faq-questions: 3 cases
Not copied:
  experiment Default (0): no traces or runs
  run tune-threshold (faq-bot): no traces; MLflow keeps its 1 parameter and 1 metric
```

The exit code is **`0`**. **Not copied** names everything the copy leaves out and why. Here the training run is left out because it has only a parameter and a metric; [What is not copied](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/mlflow.md#what-is-not-copied) lists every case.

To copy some experiments only, add `--experiment` with an experiment’s name or ID, once for each.

For a Postgres store, keep the database URL in an environment variable, for example `MLFLOW_DB_URL`, set the way you handle other credentials, and pass it in quotes:

```sh
.venv/bin/martian evals import mlflow "$MLFLOW_DB_URL" --dry-run
```

The URL has the form `postgresql://USER:PASSWORD@HOST:5432/DATABASE`. The importer prints it with the password replaced by `***`, and runs every transaction read-only.

## 3\. Copy and upgrade an older store

Skip this step if the dry run succeeded. A store an older MLflow wrote stops the dry run with exit code **`2`** and a message that starts like this:

```text
Import failed: sqlite:////path/to/mlflow.db has MLflow schema revision b7e2c1a4d9f3, which an older MLflow wrote: mlflow-skinny 3.18.0 reads revision f4a9b2c7d1e6 and would have to migrate the store, ...
```

Reading it would mean migrating it, and after a migration the older MLflow can no longer open the store. Upgrade a **copy** instead, with the MLflow that the SDK installed into `.venv`:

```sh
cp mlflow.db mlflow-copy.db
.venv/bin/mlflow db upgrade sqlite:///mlflow-copy.db
.venv/bin/martian evals import mlflow mlflow-copy.db --dry-run
```

The original `mlflow.db` is unchanged; use `mlflow-copy.db` in the next step. Do not upgrade the store your MLflow server uses unless that server already runs MLflow 3.18.0. For a Postgres store, make the copy with your usual backup and restore tools, then upgrade and import the copy.

## 4\. Copy the store

Run the same command without `--dry-run`:

```sh
.venv/bin/martian evals import mlflow mlflow.db
```

The first time, log lines from the local evaluation store appear while it creates the data folder. The report then ends with the counts it wrote:

```text
Copied:
  experiment 1 as project faq-bot: 9 traces, 2 runs
    run mlflow-bot-v1 (completed): 3 cases: 2 passed, 1 failed, 0 errors, 0 without a verdict
    run mlflow-bot-v2 (completed): 3 cases: 3 passed, 0 failed, 0 errors, 0 without a verdict
  dataset faq-questions: 3 cases, version 1
  New: 1 project, 1 dataset, 9 traces, 7 scores, 1 annotation, 7 expectations, 2 runs, 6 case results
Not copied:
  experiment Default (0): no traces or runs
  run tune-threshold (faq-bot): no traces; MLflow keeps its 1 parameter and 1 metric
Open them in the local Evals UI: martian ui
```

Running the command again copies only what is new. Everything an earlier copy wrote is left as it was and reported on a separate line:

```text
  New: nothing
  There from an earlier copy, left as they were: 1 project, 1 dataset, 9 traces, 2 runs
```

To copy into a folder other than `~/.martian/evals`, add `--data-dir DIR`, or set `MARTIAN_EVALS_HOME`. Open the UI with the same folder.

## 5\. Open the copy in the local Evals UI

```sh
.venv/bin/martian ui
```

Your browser opens `http://127.0.0.1:7600/`. The UI has one user and no login; stop it with Ctrl+C in the terminal.

1.  Choose the experiment’s name in the **Project** list at the top left. MLflow’s `Default` experiment is the **Default** project.
2.  Open **Traces** to see the copied traces with their spans. **Group by session** groups the turns MLflow recorded with a session ID.
3.  Open **Runs**. Each MLflow evaluation run is a run named `mlflow-` and the run’s name. Select one to see each case’s input, expected answer, reply and verdict. A row’s **Inspect** button opens the case with its assessments and trace.
4.  Open **Compare**, choose two runs as **Baseline** and **Candidate**, and select **Compare runs**. Two runs over the same evaluation dataset pair case by case. In the example store, `mlflow-bot-v2` improves one case and leaves two unchanged.
5.  Open **Datasets** to see each evaluation dataset, with one case per record.

## What maps where

| In MLflow | In the local Evals UI |
| --- | --- |
| An experiment | A project with the same name. The `Default` experiment is the Default project |
| A trace | A trace with its spans, session, user, tags, token use and cost, under MLflow’s trace ID |
| A person’s feedback | An annotation, as a person’s annotation in the UI is recorded |
| An expectation | An expected value on the trace, with no verdict |
| Feedback from an LLM judge or from code | An assessment, with the judge’s model or the scorer’s name as its source |
| A feedback value | Kept as it is. `true` and `yes` pass, `false` and `no` fail; numbers and other text have no verdict |
| An evaluation dataset | A dataset, one case per record, kept under the record’s ID |
| An evaluation run with traces | A run named `mlflow-<run name>`: one case per trace, with that run’s judge and code feedback as the case’s assessments. The run’s metrics, parameters and dataset are kept in its record |

A case’s verdict follows its trace and assessments, in this order: an error when the trace failed, failed when any assessment fails, an error when an assessment has an error, and passed when one passes. A case whose assessments are only numbers or text has no verdict.

## What is not copied

The report lists each of these under **Not copied**:

-   Deleted experiments and runs, and runs still running.
-   Runs without traces, such as training runs with only parameters and metrics.
-   Feedback that a later correction overrode. The correction is copied.
-   Dataset records without inputs.
-   Spans kept in an artifact store that is not a file on this machine. The trace is copied without them.
-   Registered scorers, labeling schemas, review queues, logged models, registered models and prompts. The local Evals UI has no place for them.

Run artifacts and MLflow’s own `mlflow.*` tags are not copied either. A copied run cannot be run again from the UI: its outputs come from the store.

## Failures and limits

-   **`No such command 'import'`:** the installed SDK is older than 0.1.4. See the note at the top of this page.
-   **`Copying an MLflow store needs martian-sdk[evals]`:** install the `evals` or `postgres` extra, as in step 1.
-   **Exit code `2` with `Import failed:`:** the store was refused, and nothing was written. The message says why: an older or newer schema version, an MLflow server address (copy from its database instead), a folder instead of a database file, an experiment name that does not exist, or experiments in MLflow workspaces other than the default one, which are not supported.
-   **A Postgres URL fails:** without the `postgres` extra, the message says so. Install it as in step 1.
-   **Project limit:** the copy refuses to start if it would create more than 25 projects besides the Default project. Copy fewer experiments with `--experiment`.
-   **A copy that stops part way** leaves its unfinished run marked failed, or cancelled when you interrupted it. Running the copy again adds what else is missing but leaves that run as it is. For a complete copy of it, copy the store into a new data folder.
-   **Copied assessments are dated by the copy.** MLflow’s original creation time is kept with each one.

## Next

-   [Run evals locally with a suite file](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md): write new evals for your agent as a suite file.
-   [Move from promptfoo](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/promptfoo.md) and [Move from Inspect AI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/inspect.md) bring other tools’ results into the same data folder.
