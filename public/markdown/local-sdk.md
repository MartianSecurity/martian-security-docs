# Local SDK

> Choose a guide for installing the Martian SDK, running local Evals, inspecting results, or importing existing runs.

Source: [Web version](https://docs.martiansecurity.ai/local-sdk/)

Run evaluations and inspect saved results on your machine with the Martian SDK. The Community quickstart uses deterministic checks and needs no Martian account or model key.

| I want to | Start here |
| --- | --- |
| Install the SDK and try two example runs | [Community quickstart](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/quickstart.md) |
| Evaluate a Python function or HTTP target with a YAML suite | [Run evals locally with a suite file](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md) |
| Write checks in Python and run them with pytest | [Run Python Evals with pytest](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-pytest.md) |
| Open, compare, export, or restore runs | [Use the local Evals UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md) |
| Find saved local Red Team reports | [Read the report in the local UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/redteam-local.md#5-read-the-report-in-the-ui) |
| Check a pull request with a deterministic suite | [Run local Evals on pull requests](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ci.md) |

## Install the Local SDK

Use Python 3.12 or newer. From your project folder in Bash or Zsh, create a virtual environment and activate it.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade 'martian-sdk[evals]'
martian --version
```

In each new terminal, run `source .venv/bin/activate` from the same folder before using `martian`. The [SDK version guide](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/install-and-configure.md#sdk-versions-and-workflows) lists the Python package and container releases separately.

## Import existing results

Bring runs into the local UI from [MLflow](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/mlflow.md), [promptfoo](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/promptfoo.md), or [Inspect AI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/inspect.md).

To connect the same SDK to a shared workspace and record CI sessions, see [Install and configure the SDK](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/install-and-configure.md).
