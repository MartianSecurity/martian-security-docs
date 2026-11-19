# Editions

> Compare available Community tools, the invitation-only Enterprise beta, and upcoming On-Premises deployments.

Source: [Web version](https://docs.martiansecurity.ai/get-started/editions/)

## At a glance

| Edition | Availability | How to start |
| --- | --- | --- |
| **Community** | **Available**. Open-source SDK and local UI for one user. | [Run the Community quickstart](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/quickstart.md). No account is needed. |
| **Enterprise** | **Invite-only beta**. Martian hosts the console and shared workspace. | [Request a workspace](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/access.md). |
| **On-Premises** | **Upcoming**. The console is planned for deployment in your infrastructure. | [Discuss your requirements](mailto:founders@martiansecurity.ai). |

**Available** means released for use. **Invite-only beta** means access through a hosted workspace, subject to its roles and configuration. **Upcoming** means there is no public release. A dash means the edition does not include the feature.

Community is published as [`martian-sdk` on PyPI](https://pypi.org/project/martian-sdk/) under the [Apache 2.0 license](https://github.com/MartianSecurity/martian-redteam). Enterprise users can install the same SDK for local work. The [SDK version guide](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/install-and-configure.md#sdk-versions-and-workflows) lists the Python and Docker releases.

## What each edition includes

### Evaluate

| Workflow | Community | Enterprise |
| --- | --- | --- |
| [YAML suites](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md) and [Python tests with pytest](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-pytest.md) | **Available** with the SDK | **Available** with the same SDK |
| [Runs, traces, comparisons, datasets, judges and scoring suites in the UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md) | **Available** in a local data folder | **Invite-only beta** in the console |
| [Run tests against your own targets from the local UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md#4-run-an-eval-from-the-ui) | **Available** with the target and provider settings you supply | Use the same local UI or [run a workspace evaluation](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/first-run.md) against an approved connection |
| [Import results from other tools](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/local-sdk.md#import-existing-results) | **Available** for MLflow, promptfoo and Inspect AI | — |
| [Record CI against an agent and Git revision](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/ci.md) | — | **Invite-only beta** |

### Work as a team

| Workflow | Community | Enterprise |
| --- | --- | --- |
| [Organizations, projects and workspace roles](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/permissions.md) | — | **Invite-only beta** |
| [Assigned review queues](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/human-reviews.md) | — | **Invite-only beta** |
| [Monitoring for saved runs](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/suites-and-monitoring.md) | — | **Invite-only beta** |
| Single sign-on, audit logs and service accounts | — | **Upcoming** |
| Scheduled regression runs, production monitoring and alerts | — | **Upcoming** |

### Export and share evidence

-   **Community · Available.** Export CSV and JSON from the UI or [export and restore the local Evals store](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md#export-and-restore-evals-records). The command line also produces JSONL, summary JSON and JUnit reports.
-   **Enterprise · Invite-only beta.** Share results in your workspace or export from [evaluation runs](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/results-and-scores.md) and [assessment history](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/history-and-exports.md).
-   **Enterprise · Upcoming.** Formal evidence packs and sign-off records.

### Red Team

| Workflow | Community | Enterprise |
| --- | --- | --- |
| [Local Red Team results and reports](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/redteam-local.md) | **Available** using your own models | **Available** with the same SDK |
| [Security assessments in the console](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/first-assessment.md) | — | **Invite-only beta** |
| [Workspace Red Team integration](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/redteam.md) | — | **Invite-only beta** with an enabled workspace |
| SDK-managed campaigns, sandbox-backed SDK runs, and publishing SDK Red Team runs to the console | — | **Upcoming** |

### Scan agent files

| Workflow | Community | Enterprise |
| --- | --- | --- |
| [Scan skills, MCP configurations and plugins](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/overview.md) | — | **Invite-only beta** for workspaces with Scanner access |
| [Scan pull requests through GitHub](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/github-app.md) | — | **Upcoming** |

The browser-based [single-file scan](https://www.martiansecurity.ai/scan/) is available without a workspace. [Scanner access and limits](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/overview.md#who-has-it).

## What separates the editions

|  | Community | Enterprise |
| --- | --- | --- |
| Sign-in | One user with no login | Workspace members sign in with assigned roles |
| Data | Local results in a folder you manage. Targets and judges can use services you configure. | Shared results in the hosted workspace |
| Access to team features | Individual runs and annotations | Shared projects, assigned reviews, monitoring, and CI sessions |

To run the local UI on a server, use the [Community Docker image](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md#6-run-the-ui-in-a-container) for one user and keep it private.

### Limits

The local UI defaults to one evaluation and one scoring job at a time. Set [`martian ui --concurrency`](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md#1-install-and-start-the-ui) to choose a different allowance. In a shared workspace, check the [workspace limits](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/limits.md).

## Upcoming deployment options

On-Premises is planned for organizations that need the console and data inside their infrastructure. [Plan for the Scanner in that deployment](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/self-hosted.md) or [contact Martian](mailto:founders@martiansecurity.ai) to discuss requirements.
