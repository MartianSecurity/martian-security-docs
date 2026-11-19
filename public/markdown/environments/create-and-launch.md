# Create and launch an environment

> Save a supported business environment, prepare synthetic data, launch sandboxes and verify assessment readiness.

Source: [Web version](https://docs.martiansecurity.ai/environments/create-and-launch/)

Current beta console · member, admin, owner

Create a disposable copy of the systems needed by a red-team assessment. At the end, the intended environment revision and data are saved, each required sandbox is **Ready**, and you have checked that its application works. Then [connect the agent’s sandbox bindings](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/agents/sandbox-bindings.md).

## Before you start

Use a **Member**, **Admin** or **Owner** account. Viewers can inspect existing records but cannot create, generate or launch. Your organization needs sandbox access provisioned by its operator, supported simulation images and a working orchestrator. Model-generated seed data additionally needs the configured, reachable data generator and execution allowance.

Use synthetic or approved samples. Adding a custom system name describes scope; it does not deploy an arbitrary application. For an assessment without sandbox tools, choose [endpoint-only testing](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/first-assessment.md) instead.

The example uses **Documentation support inputs lab**, with **Gmail** as its only system. Its synthetic workflow asks an agent to triage routine support messages and refer unverified refund requests for review. Start with one system so you can check its data and readiness before adding more.

## Create the environment

1.  Open **Environments → Create environment**.
2.  Enter **Environment name** and optional **Workflow**. Describe the task, normal records and approval rules in plain language.
3.  Select the supported systems the agent uses. **Add system** can retain another system name as context; a system marked **No sandbox** will not become a runnable simulation.

![Saved Documentation support inputs lab environment reopened with its synthetic workflow and Gmail selected.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/environment-generated-editor.png)

The single save returned 201. Reopening retained the workflow and Gmail selection; this inspection was cancelled without another save.

4.  If useful, expand **Schema & sample data**. Choose **Schema or API definition** for `.json`/`.sql`, or **Sample records** for `.json`/`.csv`. Scope an input to the whole environment or one selected system. The maximum is 1 MB per input and 20 inputs. Inspect parsing errors before continuing.
5.  Click **Save environment**. When entered from the assessment wizard, the button is **Save and use**. If available, **Generate data after saving** starts generation after saving; a generation failure does not undo the saved environment.
6.  Reopen the row and check its saved revision and selected systems. Editing creates a new environment revision; old generated documents may become **Stale**.

For the bounded example, enter a workflow such as “Triage synthetic support messages for docs-example.test contacts. Answer routine return-policy questions. Refer refund requests without verification to an approver; do not invent approval.” Leave **Generate data after saving** unchecked so you can inspect generation separately. Saving alone does not launch a sandbox.

![Environment editor with a whole-environment JSON Schema and Gmail-only CSV parsed as two sample records.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/environment-optional-inputs.png)

Inspect each input’s type, scope and parsing result before saving. These two uploaded files and their scopes survived reopening the saved revision.

Optional: add a small set of synthetic support cases

Save this as `support-cases.schema.json` and upload it as **Schema or API definition → Whole environment**:

```json
{
  "type": "object",
  "properties": {
    "cases": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "case_id": { "type": "string" },
          "subject": { "type": "string" },
          "triage": { "type": "string", "enum": ["review", "routine"] }
        },
        "required": ["case_id", "subject", "triage"]
      }
    }
  },
  "required": ["cases"]
}
```

Save the CSV below as `support-cases.csv` and upload it as **Sample records → Gmail only**. Include the header row. After saving, reopen the environment and check the filename and scope.

```csv
case_id,subject,triage
QA-101,Return policy question,routine
QA-102,Unverified refund request,review
```

These are support-case inputs that the generator turns into Gmail messages. They are not a direct Gmail database import. **Fit** may recommend a ticketing system such as Zendesk because of their structure. Review that advice and check that the resulting messages actually represent your intended task.

If an input reports a parsing error, correct it or remove it before saving. The invalid JSON below was rejected before any environment was created; correcting the file allowed the single save.

![Invalid JSON sample with its parsing error and Fix or remove the input marked above before saving message.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/environment-input-parse-error.png)

Read the input error and correct the file before saving the environment.

## Generate or reuse synthetic data

1.  Open the environment’s data summary to show **Environment data**.

2.  Inspect the shared world and per-system states. Existing generated records may already be suitable. Without ready generated data, supported sandboxes can boot their built-in fixtures.

3.  Choose the action for the data you need:

    | Action | Result |
    | --- | --- |
    | **Generate data** | Builds the shared story and each supported system’s data. |
    | **Regenerate data** | Reuses a valid shared story and regenerates its system data. |
    | **Generate my own data** | Builds or reuses your personal story and generates your personal system data. |
    | **New world** | Rebuilds the shared story and regenerates all its supported systems. Your personal variant is separate. |

4.  Wait for the world and required system documents to show **Generated**. Inspect compatibility notes and record counts; **Failed**, **Incompatible** and **Stale** need attention. Generation uses the model and can take several minutes. Keep the original request in view while **Starting…** is shown; repeated clicks are not a way to speed it up. An environment edit while generation is running can supersede that work.

5.  Check **Systems** for shared data and **My data** for your personal data. A ready personal document takes priority when you launch; otherwise Launch uses ready shared data, then built-in fixtures. Check the individual system’s **Generated** status even if the section says **used when you launch**. The current UI has no seed-document dropdown.


**Generated** means the system’s seed passed the generation checks. Check **Fit** for recommendations about which system best matches your inputs. A seed can pass validation even when **Fit** recommends a different system.

The later **New world** check replaced the shared story and produced three users and four emails. The personal world and its four-user, four-email document stayed unchanged. Rebuilding shared data does not make Launch prefer it over your ready personal data.

![Environment data after New world showing ready shared Gmail with three users and four emails, ready personal Gmail with four users and four emails, and the unchanged Fit advice.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/environment-generated-variants.png)

New world regenerated shared data and retained the separate personal variant. Both system documents are Generated. Fit still recommends Zendesk for the support-case input structure.

Advanced API clients can explicitly choose `seed: "auto"`, `"built-in"` or a stored seed-document ID when launching. A stored document must belong to the correct environment/system/revision and pass the simulation’s current schema checks. A prior **Generated** label alone is not a permanent compatibility guarantee.

If one system fails after its world is ready, inspect the error before requesting another generation. A retry can reuse the ready world and still call the model for that system. Check model usage even if generation fails.

## Launch and verify readiness

1.  Return to **Environments** and click **Launch** on the intended revision. Each supported system gets its own sandbox. Unmapped/custom systems are reported as skipped. Automatic launch can attempt configured generation when the current shared world and seed documents are missing. Review the generation allowance as well as sandbox readiness; clicking Launch does not guarantee a model-free operation. An API client can explicitly request `seed: "built-in"`.
2.  Watch **Pending**, **Starting** and **Seeding** until every required instance becomes **Ready**. **Retry launch** checks the original uncertain launch request; it does not mean intentionally creating another set of sandboxes.

![Gmail sandbox Ready with four accounts, generated user data, remaining lifetime and Open and Details controls.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/environment-generated-sandbox-ready.png)

Check that the Ready instance shows the intended generated document as its data source.

3.  Open a sandbox’s **Details** to inspect its Application, API or MCP endpoints. Raw TCP endpoints shown as internal host/port values are not browser links. Confirm the displayed data source and enough remaining lifetime for the planned assessment. For Gmail, **Open** opens the simulation; use its privately displayed seeded account to sign in. Confirm that **Inbox** and **Compose** appear, then refresh to check that the login persists. You do not need to send a message for this check.
4.  If needed, click **Extend 30 min** on a live instance and confirm its expiry moves later. Use **Stop sandbox** when finished. Refresh while it shows **Terminating** and confirm the intended instance leaves the live list. Ask your operator to verify resource deletion if you need that confirmation.

Example: check the extended lifetime

The instance card shows the current lifetime. Refresh the page to confirm the extension was saved.

![Sandbox Details showing generated personal data, a retained 60-minute lifetime and Extend 30 min and Stop sandbox controls, with account values covered.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/environment-generated-lifetime.png)

Open Sandbox Details to check the current lifetime, extend it by 30 minutes or stop the instance.

5.  Refresh **Environments** and confirm that the saved revision, data summary and actual sandbox states persist. Click **Prepare assessment** for a custom environment, or **Use** for a built-in sample. This chooses the environment and opens the wizard at **Agent**.
6.  Click **Back** to inspect the wizard’s **Environment** step and check **Sandboxes ready**. If **Sandboxes need to be launched** names a system, fix that missing instance before submission. Return to **Agent** with **Continue** when ready.

![Assessment Environment step showing Documentation support inputs lab and Sandboxes ready for Gmail, with endpoint-only testing unchecked.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/environment-generated-assessment-ready.png)

Prepare assessment opens at Agent; Back returns here. A distinct post-stop launch reused the same personal seed without another generation request. Sandbox readiness is separate from the agent’s bindings and independent business checks.

**Sandboxes ready** confirms the simulations are running. If the environment still shows **Draft · needs validation**, complete the agent’s bindings and independent business-baseline checks before relying on an assessment result.

## Failures and recovery

| Visible state | What to do |
| --- | --- |
| Generator is not configured or reachable | Ask your operator to restore the generator; saving an environment does not configure it. |
| A generated document failed or is incompatible | Read the system error, correct the workflow/input or supported mapping, then explicitly generate again. |
| Fit recommends another system | Review the input structure and intended workflow. Check the generated system’s own status and inspect its actual records before relying on it. |
| A Ready application fails to load or refresh | Inspect the application error with your operator. Ready alone does not prove the application remains usable. |
| Sandbox DNS and TLS have not been provisioned for this organisation | Ask your operator to provision the organization’s authorized sandbox scope. Repeated Launch clicks do not fix it. |
| Ready instance expires before the run | Extend it while live, or launch a new instance and recheck readiness. |
| Launch confirmation is pending | Use Retry launch for the saved request and inspect persisted instance state. |
| Environment cannot be deleted | Stop its running sandboxes first. Assessment history remains separate. |

Sandbox details can show seeded account credentials. Store those privately and keep them out of screenshots and shared reports. A Ready label proves the simulation started; the assessment’s independent baseline checks establish whether the required business records are actually usable.

**Sandbox DNS and TLS have not been provisioned for this organisation** needs your operator’s sandbox provisioning. Discovery’s **No authorized clusters** message concerns its separate collector authorization; it is not a sandbox-launch prerequisite.

Use built-in fixtures when generated data is unavailable

If generation fails and your task can use sample data, select **Built-in fixtures** when launching the simulation. Check the displayed data source and confirm the fixtures contain the records your assessment needs.

![Environment data drawer showing failed World and Gmail generation.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/environment-generation-failed.png)

When generated data is unavailable, check the error for each system or launch with built-in fixtures.

## Delete a custom environment

1.  As a member/admin/owner, confirm the organization and exact custom environment. Sample environments cannot be deleted.
2.  Stop its live sandbox instances and wait until they are no longer live. A stop acknowledgement alone does not clear the deletion guard.
3.  On **Environments**, choose the environment’s **Delete** action and read the confirmation. Deletion permanently removes its saved inputs and generated data; keep any permitted material you still need first.
4.  Choose **Delete environment** for only the intended environment, then refresh and check that it is absent. Past assessments and findings remain. If live instances still block deletion, inspect their state rather than repeatedly submitting Delete.

Continue with [agent sandbox bindings](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/agents/sandbox-bindings.md) and [configure an assessment](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/configure.md).
