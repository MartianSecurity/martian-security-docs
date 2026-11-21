# Read local SDK results through MCP

> Connect an MCP client to a local SDK project and validate Evals suites or deterministic checks using supplied data.

Source: [Web version](https://docs.martiansecurity.ai/sdk/local-mcp/)

Python SDK · Developer with a local MCP client

Local SDK preview

The `martian mcp` command requires the [preview SDK](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/local-sdk.md#open-the-preview-workbench) with both the `evals` and `mcp` extras.

Use `martian mcp` to let a local MCP client read saved Evals and Red Team results or check supplied data over stdio. It needs no Martian account or model key. Run it only in a client you trust with your local results.

## 1\. Connect your client

Use an MCP client that launches stdio servers. For a client with an `mcpServers` configuration, set the full path to the `martian` executable from your SDK environment and the data folder you use with `martian ui`.

```json
{
  "mcpServers": {
    "martian": {
      "command": "/path/to/venv/bin/martian",
      "args": ["mcp", "--data-dir", "/path/to/evals-data", "--project-id", "default"]
    }
  }
}
```

The server reads one project from a read-only store. Without overrides it uses the `default` project and the folder from `MARTIAN_EVALS_HOME` or `~/.martian/evals`. If the store needs initialization or an upgrade, open the folder in `martian ui` first. Configure a separate server entry for another project.

## 2\. Read saved records

| To read | Call |
| --- | --- |
| Evals or Red Team run IDs, states and counts | `list_runs` (defaults to `kind: "eval"`, use `kind: "redteam"` for scans) |
| An Evals run’s cases and recorded verdicts | `get_evaluation` |
| [Findings](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-findings.md) with triage state and filters | `list_findings` |
| One finding’s scan and attempt references, review decisions and verified fix links | `get_finding` |
| A saved scan’s [Remediation Report](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-remediation.md) | `get_remediation` |
| A baseline and follow-up’s recorded results and matched coverage | `compare_remediation` |

Start with a list and use a returned ID for the detail tool. Report listings support pagination. Convert the returned `next_cursor` to an integer and pass it as `offset` to retrieve the next page.

The tools return summaries and references. Open the workbench for raw case inputs and replies, reviewer names or review comments.

## 3\. Check a suite or a sample before a run

Use `"args": ["mcp", "--preview-only"]` for a client that only needs validation and deterministic checks. This starts without opening or creating a store.

-   `validate_suite` reads the native suite YAML in `suite_yaml`. You can supply CSV or JSONL as `case_data.text` to check case fields. To resolve the dataset path from a suite file on disk, run `martian evals validate evals.yaml` in the terminal.
-   `run_check` runs one deterministic check on the supplied sample. It takes `kind`, `options`, and `sample.output` with optional `sample.expectations`. It returns a `passed`, `failed` or `error` verdict with a reason.

For example, try these arguments to `run_check`.

```json
{
  "kind": "contains",
  "options": {"expectation": "branch"},
  "sample": {
    "output": "The central library opens at nine.",
    "expectations": {"branch": "central"}
  }
}
```

Expect `passed`. For a full evaluation see [Run Evals locally with a suite file](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md). To work with a Red Team target that speaks MCP, see [Review Red Team YAML](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-redteam-yaml.md).
