# Local SDK

> Choose a guide for installing the Martian SDK, running local Evals, inspecting results, or importing existing runs.

Source: [Web version](https://docs.martiansecurity.ai/local-sdk/)

Run evaluations and inspect saved results on your machine with the Martian SDK. The Community quickstart uses deterministic checks and needs no Martian account or model key.

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
| Review and export findings across saved scans | [Review and triage local findings](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-findings.md) (preview) |
| Export a remediation plan and verify a fix | [Read and verify remediation reports](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-remediation.md) (preview) |
| Read local results from an MCP client | [Connect to the local SDK over MCP](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-mcp.md) (preview) |
| Check a pull request with a deterministic suite | [Run local Evals on pull requests](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ci.md) |

## Install the Local SDK

Use Python 3.12 or newer. Follow [Install with pip](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-installation.md#install-with-pip) or [Install with uv](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-installation.md#install-with-uv) from your project directory.

## Open the preview workbench

For the preview guides, install a candidate wheel in an isolated environment. Replace `PREVIEW_WHEEL.whl` with the supplied wheel’s filename. For MCP, use `[evals,mcp]` in the install command. [SDK change under review](https://github.com/MartianSecurity/martian-redteam/pull/318)

Use a new data folder for the preview. To try it with existing runs, stop every process writing to your current data folder, copy the entire folder, and open the copy in the preview. The candidate can upgrade the local database schema.

```sh
python -m pip install '/path/to/PREVIEW_WHEEL.whl[evals]'
martian ui --data-dir ./evals-data --ui-dir /path/to/workbench
```

Point `--ui-dir` at the matching workbench build’s folder containing `index.html` and `assets/`. With a candidate wheel that already bundles that workbench, start it with `martian ui --data-dir ./evals-data`. The workbench footer shows the build revision.

## Import existing results

Bring runs into the local UI from [MLflow](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/mlflow.md), [Promptfoo or Marsfoo](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/promptfoo.md), or [Inspect AI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/inspect.md).

To record results in a shared workspace, see [Configure the SDK for a workspace](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/install-and-configure.md).
