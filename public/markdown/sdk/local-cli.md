# CLI command reference

> Look up Martian commands for local Evals, starting the UI, importing results, and reviewing saved reports.

Source: [Web version](https://docs.martiansecurity.ai/sdk/local-cli/)

Run these commands from the terminal where you [installed the SDK](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-installation.md). In a uv project, you can prefix a command with `uv run`. For example, use `uv run martian --version`.

## Check the version and options

| Task | Command |
| --- | --- |
| Print the SDK version | `martian --version` |
| List command groups | `martian --help` |
| List evaluation commands | `martian evals --help` |
| Show options for a subcommand | `martian evals export --help` |

Use the help for your installed release when a flag differs from a guide. Replace capitalized placeholders like `FILE` or `DIR` with your paths and quote paths that contain spaces.

## Run evaluations and open the UI

| Task | Command |
| --- | --- |
| Run a [YAML suite](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals-yaml.md) | `martian evals run evals.yaml` |
| Grade every case again and save a separate result | `martian evals run evals.yaml --fresh --output results-candidate` |
| Try a small set before running the whole suite | `martian evals run evals.yaml --limit 2` |
| Choose how many cases run at once | `martian evals run evals.yaml --concurrency 2` |
| Run the [local pytest example](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-pytest.md) | `MARTIAN_EVALS_OFFLINE=1 martian evals run test_support.py -q` |
| Start the [local UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md) | `martian ui` |
| Open a specific data folder and port | `martian ui --data-dir ./evals-data --port 7601` |
| Start the UI without opening a browser | `martian ui --no-open` |

`martian evals run evals.yaml --data-dir ./evals-data` puts the saved run in the folder opened by `martian ui --data-dir ./evals-data`. Without an override, both use `MARTIAN_EVALS_HOME`, or `~/.martian/evals` if it is unset. The suite’s result files and the UI data folder serve different purposes.

For a YAML suite, exit code `0` means all selected cases passed. Code `1` means a check failed. Code `2` means a configuration error or a missing verdict. Use the [suite guide](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md#4-read-the-results) to inspect the results.

## Import, export, and move results

| Task | Command |
| --- | --- |
| List supported import formats | `martian evals import --help` |
| Export from the [local UI store](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md#export-and-restore-evals-records) | `martian evals export ./evals-export --data-dir ./evals-data` |
| Restore an export to an empty data folder | `martian evals import martian ./evals-export --data-dir ./restored-evals` |
| Copy an [MLflow store](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/mlflow.md) | `martian evals import mlflow SOURCE` |
| Import [promptfoo results](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/promptfoo.md) | `martian evals import promptfoo FILE` |
| Import [Inspect AI logs](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/inspect.md) | `martian evals import inspect LOG` |
| Convert a promptfoo evaluation config to suite files | `martian evals convert promptfoo CONFIG` |

Use [Create and import Evals datasets](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-datasets.md) for test cases such as JSON Lines or CSV. The commands above move recorded runs, stores, or tool-specific configurations.

## Look up advanced Evals commands

| Task | Command |
| --- | --- |
| Find options for saving matrix prompt versions | `martian evals prompts push --help` |
| Check how a suite grades canned replies | `martian evals audit --help` |
| Inspect a completed run for signs of grader gaming | `martian evals inspect-cheating --help` |
| Find options for constructing conversation cases | `martian evals personas --help` |
| Find options for comparing simulated and recorded conversations | `martian evals fidelity --help` |

## Read saved Red Team evidence

| Task | Command |
| --- | --- |
| Re-export an existing local run’s report | `martian redteam report RUN` |
| Compare stored baseline and candidate results | `martian redteam compare BASELINE CANDIDATE` |
| See which output formats are available | `martian redteam report --help` |

See [Read a saved report in the UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/redteam-local.md#5-read-the-report-in-the-ui) or [Review Red Team YAML](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-redteam-yaml.md).

### Findings and remediation commands in the preview

| Task | Command |
| --- | --- |
| Find open confirmed findings | `martian redteam findings list --status open --evidence confirmed` |
| Look up an inventory finding and its review history | `martian redteam findings show FINDING_ID` |
| Save a review decision | `martian redteam findings triage FINDING_ID --status accepted --comment "Reviewed with the owner"` |
| Export the scan’s PDF | `martian redteam report RUN --pdf -o review` |
| Draft a revised system prompt from a report | `martian redteam harden-prompt RUN system-prompt.txt -o candidate-prompt.txt` |
| Gate on any remediation regression | `martian redteam verify-remediation BASELINE FOLLOW_UP --fail-on-regression -o verification` |
| Start a read-only MCP connection to one project | `martian mcp --data-dir ./evals-data --project-id default` |
| Start MCP with just suite validation and deterministic checks | `martian mcp --preview-only` |

See the [Findings](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-findings.md), [Remediation](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-remediation.md) and [MCP](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-mcp.md) guides for required builds, outputs and limits.

## Commands that use a workspace

Use `martian evals push --help` to see options for [sending finished runs](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md#7-send-runs-to-a-martian-server). For `martian ci` and SDK credentials, see [Workspace SDK and CI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/install-and-configure.md).
