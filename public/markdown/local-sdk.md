# Local SDK

> Install the Martian SDK, run local Evals, triage security findings, verify fixes, or migrate saved results.

Source: [Web version](https://docs.martiansecurity.ai/local-sdk/)

Run evaluations and inspect saved results on your machine with the Martian SDK. The Community quickstart uses deterministic checks and needs no Martian account or model key.

## New in SDK 0.4.0

-   **Findings.** Review evidence across saved scans, record triage, and export CSV, SARIF, or NeMo Guardrails bundles. [Review and triage local findings](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-findings.md)
-   **Remediation Reports.** Open a prioritized plan, export it as HTML or PDF, draft a prompt change, and record a verified fix after a follow-up scan with matching coverage. [Read and verify remediation reports](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-remediation.md)
-   **Promptfoo and Marsfoo migration.** Preview supported config conversion, import saved verdicts, traces and media, and compare the imported runs against native runs with compatible grading rules. Reimporting unchanged archives preserves their reviews. [Migrate from Promptfoo or Marsfoo](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/promptfoo.md#migrate-with-the-current-sdk)
-   **Deterministic checks.** Validate XML and embedded JSON, measure word count and edit distance, and use weighted checks in a suite. [Evals suite YAML](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals-yaml.md#deterministic-checks)
-   **Local MCP.** Read saved run records and reports through a local stdio client. Use preview mode to validate a suite or run a deterministic check on supplied data. [Connect to the local SDK over MCP](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-mcp.md)
-   **Workbench tables.** Column dividers run through the headers and rows of the bundled UI. [See the Runs table](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md#runs)

## Choose a guide

| I want to | Start here |
| --- | --- |
| Install the SDK with pip or uv | [Installation](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-installation.md) |
| Try two example runs | [Community quickstart](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/quickstart.md) |
| Write test cases or import them into the local UI | [Create and import Evals datasets](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-datasets.md) |
| Find fields and examples for suite files | [Evals suite YAML](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals-yaml.md) |
| Review the syntax of an existing Red Team file | [Review Red Team YAML](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-redteam-yaml.md) |
| Look up a command | [CLI command reference](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-cli.md) |
| Evaluate a Python function or HTTP target with a YAML suite | [Run evals locally with a suite file](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md) |
| Write checks in Python and run them with pytest | [Run Python Evals with pytest](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-pytest.md) |
| Open, compare, export, or restore runs | [Use the local Evals UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md) |
| Find saved local Red Team reports | [Read the report in the local UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/redteam-local.md#5-read-the-report-in-the-ui) |
| Check a pull request with a deterministic suite | [Run local Evals on pull requests](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ci.md) |

## Install the Local SDK

Use Python 3.12 or newer. Follow [Install with pip](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-installation.md#install-with-pip) or [Install with uv](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-installation.md#install-with-uv) from your project directory.

## Open the bundled workbench

Install or upgrade to SDK 0.4.0 or later to use local Findings and Remediation Reports. Install both the `evals` and `mcp` extras if you plan to [connect an MCP client](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-mcp.md).

```sh
python -m pip install --upgrade 'martian-sdk[evals]'
martian ui --data-dir ./evals-data
```

The SDK can upgrade a local database when it opens the data folder. Before upgrading an existing store, stop the processes writing to it and copy the entire folder. Open the copy to confirm your saved runs and reviews. The workbench footer shows the bundled UI revision.

## Import existing results

Bring runs into the local UI from [MLflow](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/mlflow.md), [Promptfoo or Marsfoo](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/promptfoo.md), or [Inspect AI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/inspect.md).

To record results in a shared workspace, see [Configure the SDK for a workspace](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/install-and-configure.md).
