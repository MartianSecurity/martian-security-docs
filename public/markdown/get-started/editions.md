# Editions

> What Community, Enterprise and On-Premises include and leave out, and which parts are available, in beta, built or planned.

Source: [Web version](https://docs.martiansecurity.ai/get-started/editions/)

Martian Security comes in three editions. **Community** is open source and runs on your own machine. **Enterprise** is the hosted Martian Security console for teams. **On-Premises** is the same console run inside your own infrastructure, and it is planned.

Every item on this page carries one of these labels:

| Label | Meaning |
| --- | --- |
| **Available** | Released. You can use it today. |
| **Beta** | In the hosted beta console. Workspaces are by invitation. |
| **Built** | The code exists but is not released: it is not on PyPI and not in the hosted beta. It does not mean that your workspace or installation has it, and no date is promised. |
| **Planned** | Designed but not built. No date is promised. |
| — | Not part of that edition. |

## At a glance

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| Status | **Available**: the SDK on PyPI, with the local Evals UI from version 0.1.4 | **Beta** | **Planned** |
| Source and licence | Open source under Apache-2.0, in [MartianSecurity/martian-redteam](https://github.com/MartianSecurity/martian-redteam) | The hosted service. It uses the same open-source SDK | Under an agreement with Martian Security, with an offline licence file |
| Runs on | Your laptop, or a small server you run, for one user | Martian cloud | Your infrastructure |
| For | One engineer or a small team | Teams that share results and need control | Organizations that cannot send data out |
| How to start | [Community quickstart](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/quickstart.md) | [Request a workspace](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/access.md) | Email [founders@martiansecurity.ai](mailto:founders@martiansecurity.ai) |

The SDK is the `martian-sdk` package on PyPI. Its source repository holds the whole Evals core, including the code for review queues and Monitoring: every edition runs that code, and an edition’s entitlements decide which paid features it serves ([below](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/editions.md#what-separates-the-editions)). What Martian builds only for Enterprise and On-Premises is not in the repository.

## What each edition includes

### Evaluate

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| [Eval suites from one YAML file](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md): deterministic checks, LLM judges with your own model key, result files and CI exit codes | **Available** | **Available**: the same SDK | **Planned** |
| [Evaluations in Python and pytest](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/evaluations.md) | **Available** | **Available**: the same SDK | **Planned** |
| Evals UI | **Available**: `martian ui`, the console’s Evals pages on your machine for one user, with no login and the data in a local folder. Needs SDK 0.1.4 or later ([guide](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md), [quickstart](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/quickstart.md#5-see-the-result-in-the-local-evals-ui)) | **Beta**: the full console, with organizations and projects | **Planned**: the full console |
| Runs and results, comparison, traces and sessions, datasets, judges and scoring suites, quality issues and annotations in the UI | **Available**, with the local Evals UI | **Beta** | **Planned** |
| Runs and judges started from the UI on your own agent, model and key | **Available**, with the local Evals UI. The targets you define and their keys stay in its data folder | **Planned** | **Planned** |
| [Results from MLflow, promptfoo and Inspect AI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/mlflow.md) imported into the Evals UI | **Available**: SDK 0.1.4 or later | — | — |
| SDK results recorded against a tested revision: API keys and [CI sessions](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/ci.md) | — | **Beta** | **Planned** |

### Work as a team

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| [Review queues with assignment](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/human-reviews.md) (`review_queues`) | — | **Beta** | **Planned** |
| [Monitoring](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/suites-and-monitoring.md) (`monitoring`): scoring jobs and their scorecards across runs | — | **Beta** | **Planned** |
| Scoring of sampled production traces, scheduled regression runs and alerts (also under `monitoring`) | — | **Planned** | **Planned** |
| Organizations, projects and the four [roles](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/permissions.md): owner, admin, member and viewer | — | **Beta** | **Planned** |
| Single sign-on (`single_sign_on`): OIDC or SAML for each organization, verified email domains and password sign-in that an administrator can turn off. There is no identity-provider-initiated sign-in and no single logout | — | **Built** | **Built** |
| Audit log (`audit_log`): entries that nobody can change or delete, for sign-ins, permission changes and changes to eval objects, with search and export | — | **Built** | **Built** |
| Service accounts (`service_accounts`): identities for CI jobs and runners, each with a role, a scope of the organization or one project, an expiry and a key that can be rotated or revoked at once | — | **Built** | **Built** |
| Custom roles that separate developers from validators, and retention | — | **Planned** | **Planned** |

### Evidence

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| Export results | **Available**: JSONL, JSON summary and JUnit files. With SDK 0.1.4 or later, also CSV and JSON exports in the local Evals UI, and `martian evals export` for everything in its data folder | **Beta**: CSV and JSON exports | **Planned** |
| Evidence packs and sign-off records | — | **Planned** | **Planned** |

### Red Team

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| Red team runs with your own model: a version 2 run file, the attacker and judge called with your key, nothing sent to Martian and no account ([guide](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/redteam-local.md)) | **Built**: in the next SDK release | **Built**: the same SDK | **Planned** |
| Targets: a Python function, an HTTP endpoint or an MCP server, and a recording proxy for the agent’s tool calls | **Built** | **Built**: the same SDK; **Beta**: agents registered in the console | **Planned** |
| Evidence: a model’s verdict (suspected), text checks and canaries, tool calls and receipts (confirmed) | **Built** | **Built**: the same SDK | **Planned** |
| Red Team pages in `martian ui`: runs, reports, attempts and findings with status and comments | **Built** | — | — |
| Reports in JSON, Markdown, HTML, CSV, SARIF and JUnit, a CI gate by evidence level, pinned findings and run comparison | **Built** | **Built**: the same SDK | **Planned** |
| promptfoo red team configs and results, and garak probes against your agent ([guide](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/promptfoo-redteam.md)) | **Built** | **Built**: the same SDK | **Planned** |
| Attack generation and judging by Martian’s engine (`redteam_hosted_generation`) | — | **Beta**: the SDK’s probes with a workspace API key ([guide](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/redteam.md)) | **Planned**: attack generation on your own models |
| [Assessments](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/first-assessment.md) in a simulation environment (`redteam_environments`) and planned campaigns (`redteam_campaigns`) | — | **Beta**: in the hosted console | **Planned** |
| Custom limits and shared attack profiles | — | **Planned** | **Planned** |

### Delivery and support

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| Delivery | **Available**: `pip install` from PyPI, and a Docker image of the local Evals UI for one user on a small server, published as `ghcr.io/martiansecurity/martian-evals:<version>` ([how to run it](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md#6-run-the-ui-in-a-container)). It has no login and must not be exposed publicly | **Beta**: managed by Martian | **Built**: the offline licence file. **Planned**: Helm chart, air-gapped image bundle, a runner inside your network and a named deployment engineer |
| Support | **Planned**: community support in the public repository | **Planned**: priority support with an SLA | **Planned**: priority support with an SLA |

## What separates the editions

The Evals core serves every edition. What differs is what each edition supplies: who signs in, where the data lives, which paid features are on and how much may run at once.

### Where each edition runs

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| Who signs in | One user, with no login | The members of each organization | The members of each organization |
| Where the data lives | A folder on your machine, on SQLite. Nothing is sent to Martian | Martian’s hosted storage | Your infrastructure |
| What decides the edition | Nothing: it is always Community | The organization’s plan | A licence file signed by Martian and checked offline, with no licence server. Without a valid licence, or after its grace period, the installation is Community |

### Feature keys

The Evals UI shows a page only when the edition includes its feature key, and the API refuses a route of a missing feature with `403`.

| Feature key | Covers | Community | Enterprise | On-Premises |
| --- | --- | --- | --- | --- |
| `review_queues` | Review queues with an assignee, answering their items, and the library of review questions | No | Yes | Yes |
| `monitoring` | The Monitoring page, monitors on live traces, thresholds with alerts, and scheduled runs | No | Yes | Yes |
| `single_sign_on` | Single sign-on | No | Yes | Yes |
| `audit_log` | The audit log | No | Yes | Yes |
| `service_accounts` | Service accounts | No | Yes | Yes |
| `redteam_hosted_generation` | Attack generation and judging by Martian’s engine for SDK red team runs | No | Yes | Yes |
| `redteam_environments` | A red team run in a Martian simulation environment | No | Yes | Yes |
| `redteam_campaigns` | Planned red team campaigns started from the console | No | Yes | Yes |

Annotating one item or trace, and scoring one run, stay in every edition. A local red team run with your own model needs no key. `review_queues` and `monitoring` are in the open-source repository; the other keys are for features that exist only in Martian’s own product.

### Limits

Each edition sets how many runs and scoring jobs may be in progress at once. A launch over the limit is refused.

| Limit | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| Evaluation runs queued or running at once | 1 | 5 | No limit |
| Scoring jobs queued or running at once | 1 | 5 | No limit |
| Hosted red team generation and judging operations at once | — | 2 | No limit |

On your own machine you set the Community limit: `martian ui --concurrency 2` allows two of each. On-Premises has no limit of its own because its workers bound what runs at once.

## What Community leaves out

Community includes the whole Evals core except what a shared server needs or what Enterprise and On-Premises add:

-   Review queues and Monitoring.
-   Organizations, projects with several members and roles, single sign-on, the audit log and service accounts.
-   API keys and CI sessions, which record SDK results on a server.
-   The console’s Red Team assessments, simulation environments and planned campaigns, and attack generation by Martian’s engine. Local red team runs with your own model are Community.
-   Hosted storage, managed upgrades and priority support.

## Choose an edition

-   **Start on your own machine:** follow the [Community quickstart](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/quickstart.md). It needs no account.
-   **Share results as a team, or run Red Team assessments:** [request a workspace](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/access.md) in the hosted console.
-   **Keep all data inside your network:** On-Premises is planned. Email [founders@martiansecurity.ai](mailto:founders@martiansecurity.ai) to discuss your requirements.

The [verification record](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md) lists which guides have been walked through, against which release.
