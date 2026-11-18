# Scan from the command line and CI

> martian scan packs a folder's agent files, uploads them, waits for the scan and exits on the gate in .martian/scan.yml.

Source: [Web version](https://docs.martiansecurity.ai/scanner/cli-and-ci/)

> **Page qualification:** Current beta console · Developer with an API key holding scan:run and scan:read · Walkthrough verification in progress. [Verification details](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md).

> **Walkthrough limits:** Written from the source at the commits listed, for the beta release that turns the Scanner on (MartianSecurity/martian-notes#527). Not yet walked through against the hosted beta console, and no screenshot is captured; the feature branches that add bundle retention, usage and the self-hosted chart (MartianSecurity/martian-notes#521 to #525) were not on main when it was written.

Guide in progress

This workflow has been reviewed against the implementation. A complete live walkthrough is still in progress.

`martian scan` sends a folder’s agent files to the Scanner, waits for the scan, prints the findings and exits on the gate the server evaluates against the repository’s policy file. It is a thin client: the rules, the findings and the gate are all on the server.

## Before you start

-   A martian-sdk release that includes `martian scan`; 0.2.0 does not. Install it as in [installation and configuration](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/install-and-configure.md).
-   An organization with the Scanner turned on ([who has it](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/overview.md#who-has-it)), and an API key with **`scan:run`** and **`scan:read`**, issued by an owner or admin under **API Keys**.
-   `MARTIAN_API_URL` set to your Martian server and `MARTIAN_API_TOKEN` to the key.

## Scan a folder

```bash
martian scan --dry-run                         # list what would be sent and its digest; needs no token
martian scan                                   # the current folder's agent files
martian scan path/to/repo --sarif results/scan.sarif --json results/scan.json
martian scan --include 'skills/**' --include src/agent/ --kind agent_code --name support-agent
```

By default the command sends the files coding agents load: `AGENTS.md`, `CLAUDE.md` and `GEMINI.md`, MCP configurations (`.mcp.json`, `mcp.json`), the `.claude/`, `.cursor/`, `.agents/` and similar folders, Copilot instructions, and every folder that holds a `SKILL.md` or a `.claude-plugin/` folder, whole. Inside a Git work tree only files Git does not ignore are sent. A symbolic link that points out of the folder refuses the scan; the command never follows one.

| Option | Default | Meaning |
| --- | --- | --- |
| `FOLDER` | `.` | The folder to scan |
| `--include`, `-i` | the agent files | A pattern of files to send instead; repeatable |
| `--kind` | `repository` | `repository`, `skill`, `mcp_server`, `plugin`, `subagent`, `harness_config`, `agent_code` or `registry_entry` |
| `--name` | the repository, else the folder’s name | Scans of the same kind and name belong to one add-on |
| `--no-model-analysis` | analysis allowed | Keep file contents from any model, whatever the organization allows |
| `--timeout` | 600 | Seconds to wait for the scan |
| `--json PATH`, `--sarif PATH` | none | Write the server’s JSON or SARIF 2.1.0 export |
| `--policy PATH` | `.martian/scan.yml` | The gate policy file |
| `--default-branch NAME` | detected | The repository’s default branch, for the baseline |

## Exit codes

| Exit | Meaning |
| --- | --- |
| 0 | The gate passed |
| 1 | The gate failed: blocking findings or a coverage shortfall, with the reasons printed |
| 2 | No verdict: nothing to send, a link out of the folder, a refused policy file, missing or refused credentials, a refused upload, a failed scan, the timeout, or an export that could not be written |

## The gate file: `.martian/scan.yml`

```yaml
version: 1
paths: ["."]
include: [skills, mcp, plugins, subagents, harness-config]
external:
  follow: true
gate:
  fail_on: {evidence: structural, severity: high}
  new_findings_only: true
waivers:
  - {rule: REF-UNPINNED-PACKAGE, path: .mcp.json, reason: "Served from the internal mirror", expires: 2027-01-31}
```

| Field | Default | Meaning |
| --- | --- | --- |
| `paths` | `["."]` | What is sent, relative to the repository |
| `include` | all six families | `skills`, `mcp`, `plugins`, `subagents`, `harness-config`, `agent-code` |
| `external.follow` | `false` | Require the references to have been resolved, with none left not attempted unless `max_not_attempted_references` allows some |
| `gate.fail_on.evidence` | `inventory` | The least [evidence level](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/overview.md#evidence-levels) that blocks |
| `gate.fail_on.severity` | `info` | The least severity that blocks: `critical`, `high`, `medium`, `low` or `info` |
| `gate.fail_on.categories` | all | Only findings of these categories block |
| `gate.min_coverage` | none | Stages that must have run, the least evidence level reached, and at most so many skipped files or unresolved and not-attempted references |
| `gate.new_findings_only` | `false` | Block only on findings the default branch’s latest scan does not have |
| `waivers` | none | A finding of `rule` on exactly `path` does not block until `expires` (at most a year ahead), with a `reason` |

An unknown field anywhere is refused, so a misspelt threshold never passes silently. Without a file the gate is the strictest: every open finding blocks.

## In CI

-   **A CI session.** `martian ci --scan FOLDER` runs the same scan as one test of a [CI session](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/ci.md).
-   **GitHub Actions.** The scan action, `MartianSecurity/martian-redteam/.github/actions/scan`, runs `martian scan` with the token from the job’s environment and writes `scan.sarif` and `scan.json`; upload the SARIF to code scanning with `github/codeql-action/upload-sarif`. Run it on pushes to protected branches, not on pull requests: a customer token must not reach code nobody has reviewed. Pull requests are scanned by the [GitHub App](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/github-app.md).
-   Both exports quote the lines each finding is about. Keep `scan.json` out of artifacts others can download if the scanned files hold anything private.

## Next

-   [The GitHub App](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/github-app.md)
-   [Limits, usage and data](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/limits-and-data.md)
