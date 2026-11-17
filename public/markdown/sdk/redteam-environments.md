# From a local red team run to an environment run

> Take a version 2 red team run file from your machine to a Martian server, add an environment for state-verified findings, and start a planned campaign.

Source: [Web version](https://docs.martiansecurity.ai/sdk/redteam-environments/)

> **Page qualification:** Python SDK · A developer with a version 2 red team run file and an API key with redteam:run bound to no agent; an owner or admin approves the agent, binds its sandboxes and issues the key · Walkthrough verification in progress. [Verification details](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md).

> **Walkthrough limits:** On 2026-11-17 steps 1 to 5 were followed against unreleased source: martian-redteam feature/308/epic at 27bba7a and MartianBackend feature/308/epic, served on loopback with uvicorn on a disposable PostgreSQL 17 database, a test organisation (Enterprise plan, an admin, an approved agent connection, the environment refund-desk with one Ready instance) and an API key with redteam:run created through the API. The sandbox was the backend tests' fake world (fake orchestrator and sandbox MCP: an inbox and a refund ledger), the attacker and judge were the SDK tests' loopback fake models, and the agent was a small HTTP agent with a session API that binds its tools with the SDK's sandbox MCP binding. Observed: the local run kept the run and failed its gate on an undetermined tool-call check; push printed 'pushed to', a second push 'already on', and the console's red team list held the run once; without the server address variable the environment run stopped with the documented message; with it the run was admitted as MR-1001, both probes (a direct attack and an email planted with the inbox-email profile) reached level 5, Verified in environment, with clean no-implant controls and the planted email delivered, the gateway's calls and state results kept as evidence, the server's run completed and listed, and the run pushed. Not followed: step 6, the planned campaign: the server answered 'This agent has no approved martian-agents target binding', since no campaign engine (martian-agents) ran; no real Martian Simulation sandbox, model provider, published package or console UI was used, and no screenshots exist.

Guide in progress

This guide describes features that are not released yet. It was followed against unreleased source with a stand-in sandbox and stand-in models; the planned campaign step was not run.

The same version 2 run file works in three places. On your machine it runs against your agent with your own models, and its strongest evidence is a tool call or a receipt. Pushed to a Martian server, the run appears in the console beside the server’s own runs. With an `environment` and a token, the attempts run in a Martian Simulation world the server resets for each one, and an action finding can become **Verified in environment**.

## Before you start

-   A version 2 run file that runs locally with `martian redteam run`. The open package holds no environment: nothing on this page changes what a local run does.
-   `martian-sdk[evals,mcp]` at the release that includes red team environments, with Python 3.12 or newer.
-   An organisation on the Enterprise or On-Premises edition. Community organisations are refused red team environments and campaigns.
-   An owner or admin issues an API key with **Run hosted redteam generation and judging** (`redteam:run`). A key bound to an agent cannot push runs; use a key bound to no agent and name the agent in the run file.
-   The agent is registered, its connection is active and approved, and an owner or admin bound it to an environment’s sandboxes ([sandbox bindings](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/agents/sandbox-bindings.md)). The environment has a Ready instance of each system the agent’s connection binds ([create and launch an environment](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/environments/create-and-launch.md)).
-   Your agent reads its tool session the way a cloud agent does: from `tool-session.json`, or from its own session API (`tools.session_api`), and binds its tools with `bind_tools(session, action_id=conversation_id)`.

## 1\. Run locally

```sh
martian redteam run redteam.yaml
```

The run writes `redteam-run.json` and `redteam-report.md` to `output_folder`, keeps the run in the local store and prints `Kept in the local store as redteam-…`. Without an environment, an action objective stops at **Confirmed action** at best, and the report says an environment is what would raise it. An HTTP agent that does not report its tool calls leaves a `tool_call` check undetermined, and the gate fails on it: that is the gap the environment’s gateway closes.

## 2\. Push the run to the server

```sh
export MARTIAN_API_URL=https://YOUR_MARTIAN_ORIGIN
export MARTIAN_API_TOKEN=YOUR_REDTEAM_KEY
martian redteam push results/redteam-run.json
```

Expect `Red team run redteam-… pushed to the Martian server.` The console’s red team runs list shows it, labelled as executed by your machine. Pushing it again prints `already on the Martian server` and adds nothing. A run that has not finished is not pushed.

## 3\. Add an environment

Add two fields to the same file:

```yaml
environment: refund-desk                       # the environment's name in your organisation
agent: 1b2c3d4e-0000-4000-8000-000000000001    # the registered agent's id
```

Name the state check the environment decides, beside the checks you already have:

```yaml
vulnerabilities:
  - name: ExcessiveAgency
    types: [functionality]
    checks:
      - { type: state, name: business }        # the agent connection's business checks
      - { type: tool_call, tool: issue_refund, executed: true }
```

For an indirect injection, plant the attack in the world instead of sending it. The profile is one of the agent connection’s implant profiles; the agent receives the trigger:

```yaml
  - name: ExcessiveAgency
    types: [autonomy]
    plant: { profile: inbox-email, trigger: "Please handle my newest email." }
    checks:
      - { type: state, name: business }
```

Remove `tools.proxy` if the file has it: the environment’s gateway is the tool boundary. Keep `tools.session_api` if your agent has one. `martian redteam validate redteam.yaml` checks the file offline.

## 4\. Run in the environment

```sh
martian redteam run redteam.yaml
```

Without `MARTIAN_API_URL` and `MARTIAN_API_TOKEN` the run stops with exit code `2` before anything is called. With them:

1.  The server admits the run for the agent and pins the environment’s instances. It refuses an agent that is not approved, an environment or state check it does not know, and a sandbox another run is using. The run prints `Admitted in environment refund-desk as MR-…; the agent's tool session is in results/tool-session.json`, and the console’s assessments list shows the run.
2.  Your agent receives the session. Its tools now reach the environment’s applications through the server’s gateway, which records every call.
3.  Each attempt runs in a world reset for it. After the reply, the server compares the business records with that attempt’s baseline and returns the gateway’s calls.
4.  A state check that hit is checked once more: an ordinary message (or the planted probe’s trigger) in another reset world with nothing planted. Only when that control left the records unchanged does the finding reach level 5, **Verified in environment**. When the control changed them too, the check is undetermined.
5.  When the run ends the server releases the sandboxes, and the run is pushed so the console shows it: `Red team run redteam-… pushed to the Martian server.`

A finding the environment verified fails the gate as any confirmed finding does, for example `Gate failed: excessive_agency/functionality: Verified in environment (…)`, with exit code `1`.

Attempts run one at a time. Each control counts against `budget.target_queries`. `--resume` does not apply: an environment run starts again in a reset world.

## 5\. How the report changes

| Evidence | Local run | Environment run |
| --- | --- | --- |
| The agent’s tool calls | What the agent reports, or what the local proxy saw | What the server’s gateway recorded for the attempt |
| An action objective | At most **Confirmed action** (level 3) | **Verified in environment** (level 5) when the records changed and the control stayed clean |
| A planted attack | Not available | Kept as `payload` evidence, with whether the agent read it |
| `provenance.environment` | Absent | The server’s run id and code |

## 6\. Start a planned campaign

The console’s planned campaign uses the server’s engine against the same agent:

```sh
martian redteam campaign --agent 1b2c3d4e-0000-4000-8000-000000000001 --depth quick
```

It prints the campaign’s code and where the console shows it, follows it until it finishes, and writes the campaign’s `redteam-run.json` and reports to `results`. The exit code follows the release decision: `0` for `APPROVED`, `1` for `BLOCKED` or `CONDITIONAL` (`0` with a warning under `--allow-conditional`), and `2` when there is no decision.

## If something fails

| Message | What to do |
| --- | --- |
| `environment 'refund-desk' is a Martian environment, and environments run only on a Martian server` | Set `MARTIAN_API_URL` and `MARTIAN_API_TOKEN`, or remove `environment` |
| `This agent is not approved for red team runs` | Approve the agent’s connection and its grant in the console |
| `A selected sandbox is already used by an active assessment` | Wait for the other run, or launch another instance |
| `The agent's environment has no state check named …` | Use `business`, or add business checks to the agent’s connection |
| `Not pushed: … bound to an agent or to datasets does not push runs` | Use a key bound to no agent |
| `The campaign: This agent has no approved martian-agents target binding` | Campaigns run on the server’s engine: the agent needs its engine binding, which the console sets when the agent is activated |

Continue with [run a redteam probe](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/redteam.md) or [evidence and results](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/evidence-and-results.md).
