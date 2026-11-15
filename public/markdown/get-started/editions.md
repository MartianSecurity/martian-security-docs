# Editions

> What Community, Enterprise and On-Premises include, and which parts are available, in beta or planned.

Source: [Web version](https://docs.martiansecurity.ai/get-started/editions/)

Martian Security comes in three editions. **Community** is free and runs on your own machine. **Enterprise** is the hosted Martian Security console for teams. **On-Premises** is the same console run inside your own infrastructure, and it is planned.

Every item on this page carries one of these labels:

| Label | Meaning |
| --- | --- |
| **Available** | Released. You can use it today. |
| **Beta** | In the hosted beta console. Workspaces are by invitation. |
| **Planned** | Designed but not released. No date is promised. |
| — | Not part of that edition. |

## At a glance

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| Status | **Available**: the SDK on PyPI | **Beta** | **Planned** |
| Price | Free | Contact us | Contact us |
| Runs on | Your laptop or your own server | Martian cloud | Your infrastructure |
| For | One engineer or a small team | Teams that share results and need control | Organizations that cannot send data out |
| How to start | [Community quickstart](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/quickstart.md) | [Request a workspace](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/access.md) | Email [founders@martiansecurity.ai](mailto:founders@martiansecurity.ai) |

The SDK is the `martian-sdk` package on PyPI, licensed Apache-2.0. A public source repository for Community is **Planned**.

## What each edition includes

### Evaluate

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| [Eval suites from one YAML file](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md): deterministic checks, LLM judges with your own model key, result files and CI exit codes | **Available** | **Available**: the same SDK | **Planned** |
| [Evaluations in Python and pytest](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/evaluations.md) | **Available** | **Available**: the same SDK | **Planned** |
| Evals UI | **Planned**: the console’s Evals pages on your machine, one user, no login | **Beta**: the full console, with organizations and projects | **Planned**: the full console |
| Runs and results, comparison, traces and sessions, datasets, judges and scoring suites, quality issues and annotations in the UI | **Planned**, with the local Evals UI | **Beta** | **Planned** |
| Judges run from the UI on your own model and key | **Planned** | **Planned** | **Planned** |
| SDK results recorded against a tested revision: API keys and [CI sessions](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/ci.md) | — | **Beta** | **Planned** |

### Work as a team

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| [Review queues with assignment](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/human-reviews.md) | — | **Beta** | **Planned** |
| [Monitoring](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/suites-and-monitoring.md): scoring jobs and their scorecards across runs | — | **Beta** | **Planned** |
| Scoring of sampled production traces, scheduled regression runs and alerts | — | **Planned** | **Planned** |
| Organizations, projects and the four [roles](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/permissions.md): owner, admin, member and viewer | — | **Beta** | **Planned** |
| Single sign-on, custom roles that separate developers from validators, audit log, retention and service accounts | — | **Planned** | **Planned** |

### Evidence

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| Export results | **Available**: JSONL, JSON summary and JUnit files | **Beta**: CSV and JSON exports | **Planned** |
| Evidence packs and sign-off records, with a [mapping to the EU AI Act and model-risk guidance](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evidence/requirement-mapping.md) | — | **Planned** | **Planned** |

### Red Team

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| Red Team | **Planned**: local probes, with a monthly limit on hosted attack generation | **Beta**: [assessments](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/first-assessment.md) in the hosted console | **Planned**: attack generation on your own models |
| Custom limits and shared attack profiles | — | **Planned** | **Planned** |

### Delivery and support

|  | Community | Enterprise | On-Premises |
| --- | --- | --- | --- |
| Delivery | **Available**: `pip install` from PyPI. **Planned**: a Docker image for single-user self-hosting | **Beta**: managed by Martian | **Planned**: Helm chart, air-gapped image bundle, a runner inside your network, an offline licence file and a named deployment engineer |
| Support | **Planned**: community support in the public repository | **Planned**: priority support with an SLA | **Planned**: priority support with an SLA |

## Where the paid line is

Features that one engineer needs are free. Features that a team, a manager or a risk function needs are paid.

Two Evals features are paid: **review queues with assignment** and **Monitoring**. Enterprise and On-Premises include them; Community does not. No other Evals feature is paid, so the local Evals UI, when released, includes every other Evals page.

Community also leaves out what needs a shared server or belongs to another product area: API keys and CI sessions, organizations and team pages, and the console’s Red Team assessments and simulation environments.

## Choose an edition

-   **Start on your own machine:** follow the [Community quickstart](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/quickstart.md). It needs no account.
-   **Share results as a team, or run Red Team assessments:** [request a workspace](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/access.md) in the hosted console.
-   **Keep all data inside your network:** On-Premises is planned. Email [founders@martiansecurity.ai](mailto:founders@martiansecurity.ai) to discuss your requirements.

The [verification record](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md) lists which guides have been walked through, against which release.
