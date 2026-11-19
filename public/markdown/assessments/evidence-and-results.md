# Inspect assessment evidence and results

> Read reports, trace turns, findings, probe coverage and independent outcome checks at the correct evidence level.

Source: [Web version](https://docs.martiansecurity.ai/assessments/evidence-and-results/)

Current beta console · viewer, member, admin, owner

Inspect what an assessment tested, what it observed and how strongly a finding is supported. A useful result includes the actual scope and coverage, not just a verdict badge.

## Before you start

Use any signed-in role with access to the organization’s run. Complete or retain a bounded assessment and know its run code. Use **Recorded review** for versioned review content when available. Other runs show the legacy trace controls.

## Read the report and run summary

1.  At the wizard’s **Report** step, inspect **Verdict**, **Attempts held**, **Exposed value**, findings and the displayed-page count. A blank held ratio can mean no tested attempts or incomplete coverage; do not treat it as 100% protection.
2.  Click **Open trace**. Read **Security outcome** and **Assessment execution** separately. **INCONCLUSIVE** means the evidence does not support a security pass; zero findings also does not establish a pass.

![Completed MR-1002 with INCONCLUSIVE security outcome](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/first-assessment-trace-overview.png)

The report shows execution state, security outcome, request counts and findings.

3.  Check **Attempts**, **Blocked**, **Verified**, **Unverified**, **Agent requests**, **Model calls** and **Displayed findings**. Read the exhaustion reason and any retained error. Requested techniques are scope; they are not a count of completed target attempts.
4.  Inspect **Probe coverage** when available. Check selected, attempted, skipped or incomplete coverage before drawing a conclusion about a technique.

![Attempted disclosure probe with unverifiable outcome and actual call counts](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/assessment-coverage.png)

One outcome-data probe was attempted. Its unverifiable outcome and 3/30 target, 15/100 model usage are separate from the five requested technique labels.

If a **Release recommendation** appears, read its recorded policy and reason separately. **PENDING** with **None approved** means no customer-approved release policy was available. An execution result or finding does not authorize deployment.

## Inspect the actual conversations and actions

1.  In a legacy run, open **Trace**. Use **Tree** to follow campaign, conversation, turn and verification rows, or **Timeline** for timestamped runtime/customer events. **Filter rows**, **Expand all** and **Collapse** change the view rather than the assessment.
2.  Select a turn and compare **Attacker message**, **Customer agent reply** and **Observed actions**. A request to call a tool, an executed gateway call and a confirmed business effect are different evidence.
3.  Read the turn critic or verifier narrative as model-generated interpretation. For a state-changing outcome, inspect independent receipts rather than treating the narrative as the final authority.

![Recorded attacker message and actual teaching-target refusal in Turn 1](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/first-assessment-trace.png)

Select a retained turn to compare the actual attacker message, customer reply and action journal. The critic below is model interpretation, not an independent oracle.

4.  In **Recorded review**, select a **Review revision** and inspect **Conversations**, **Turns**, **Runtime timeline**, **Observed gateway calls**, **Verification receipts** and **Evidence references**. **Native spans** shows retained native trace details when available. **Customer reported events** are customer instrumentation, not independent proof of effect.
5.  Use **Refresh review** to select a newer published revision. Published revisions pin their content; reading, exporting or retrying a review does not rerun target execution.

### Example: read a redacted turn

In **Recorded review**, open **Turns** and select a turn. Check the **target response** and its exported-content label. A redacted response may show `[REDACTED]` in place of withheld text.

![First retained turn with redacted target response, credential\_scrubbed status, exported byte counts and twelve loaded turn records.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/assessment-modern-redacted-turn.png)

The actual target response contains \[REDACTED\] instead of the fixture’s token-shaped test string. The critic rationale is model interpretation. This on-screen read does not establish a successful ZIP download.

Redaction describes what the export contains. Read **Security outcome** and the critic’s explanation separately.

## Inspect findings and independent outcomes

Inspect the [business-state comparison](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/agents/sandbox-bindings.md#example-a-completed-independent-business-comparison) to see the independent before and after records for a finding.

![Completed synthetic payment assessment with one business-state finding, 17 agent requests and 59 model calls.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/payment-completed-independent-outcome.png)

Outcome checks shows the observed business violation and the independent before-and-after comparison.

1.  Open **Findings** and inspect each finding’s title, severity, verification status, evidence and technique attribution. Page through the results: **Displayed findings** is not necessarily the total run count.

2.  When present, open **Outcome checks**. Compare before/after business records, repeated-world receipts and the no-implant control. Use **Scenario setup** to inspect the prepared carrier and readback for a scenario run.

    **Ready** can mean the starting state was captured. If **Outcome captured** and **After-state digest** are pending, the comparison is incomplete.


![Outcome checks with a ready starting receipt, five ledger records, two met baseline conditions, pending after-state and unavailable cleanly reproduced refund.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/assessment-outcome-checks.png)

Both baseline prerequisites passed. Outcome captured and After-state digest remain Pending, and no complete comparison or refund verdict exists. The duplicated-refund sentence describes the configured check.

3.  Read **Reproduction status**, **Repetitions**, **Successful reproductions**, **Target calls** and **Negative control** in verification details. A skipped control is not a passed control. If the same violation occurs without an implant, the scenario’s carrier attribution is not established.
4.  Check missing-knowledge notices, truncated payloads, dropped customer events and evidence availability. A missing event/reference cannot prove no action or relevant attack existed.
5.  Refresh the page and reopen the saved run to verify that the selected evidence, findings and final execution state persist.

![Knowledge and skills shows zero reviewed references and one activated skill](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/assessment-knowledge.png)

Six visible lookup stages retained no reviewed references. One activated canonical skill is recorded with a Content digest control; missing references do not prove no relevant attack is known.

**Knowledge & skills** shows activated skills and reviewed references when available. Use **Probe coverage** to distinguish an attempted probe with an unverifiable outcome from a verified result.

## Read an MCP endpoint example

1.  Open the saved MCP assessment. Confirm its agent, **Assessment execution** and **Security outcome**.

![Martian Security MCP assessment MR-1001 showing completed execution, an inconclusive security outcome, three agent requests and sixteen model calls.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/assessment-mcp-result.png)

Check execution and security outcome separately. This synthetic MCP result was recovered by an operator after an uncertain admission; it does not establish a security pass.

2.  In **Trace**, select a turn. Read the customer reply and the action’s **Journal** to see whether the call completed.

![The actual first MCP turn with its attacker message, refusal, action identity and prepared to submitted to completed journal.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/assessment-mcp-turn.png)

Compare the actual request, reply and action journal. This turn belongs to the same operator-reconciled MCP campaign; a refusal is separate from independent outcome verification.

3.  Open **Probe coverage**. Check the outcome and calls for the selected probe. The run summary counts calls across the whole assessment.

![MCP disclosure probe coverage showing attempted and unverifiable, three target calls, fifteen probe model calls and one inconclusive recorded attempt.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/assessment-mcp-coverage.png)

Read the probe outcome and its own counters. This operator-reconciled campaign attempted the disclosure probe but retained no decisive verified result.

4.  Use **Download legacy JSON evidence** when you need the saved trace and coverage. See the [export guide](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/history-and-exports.md) for the available formats.

## Read a cleanly reproduced business finding

1.  In **Findings**, check the reproduction label. Open **Recorded detail** for the saved verification data.
2.  Open **Outcome checks** and compare the independent records for each repetition and the negative control.
3.  In **Recorded review → Verification receipts**, read the retained verdict and control outcome. Use the finding’s **Recorded detail** for the full verification data.
4.  To retain the selected revision, [download its redacted review](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/history-and-exports.md#download-and-check-the-redacted-review).

See [reproduction and evidence limits](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/reproduction-and-limits.md) for how to interpret repeated outcomes and controls.

## Read a completed browser assessment

1.  Open the saved run and confirm its target. Read **Assessment execution** and **Security outcome** separately. The example shows **Completed** execution with an **INCONCLUSIVE** outcome.

![Martian Security MR-1006 showing completed browser execution, an inconclusive security outcome, four agent requests and twelve model calls.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/browser-completed-coverage-refreshed.png)

The bounded browser assessment completed, but its evidence did not support a security pass. The saved result survived a full reload.

2.  Open **Probe coverage**. Read the probe’s outcome and reason. Compare the probe’s calls with the assessment totals to see how much of the admitted scope ran.

![Martian Security browser disclosure probe showing attempted coverage, an unverifiable outcome, two target calls and eight model calls.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/browser-completed-probe-detail.png)

Probe counters cover this disclosure probe. The campaign summary also includes setup and other work; an attempted probe is not a verified finding.

3.  Check **Website access** and the retained target revision. **Configured website account** describes website sign-in. Use independent checks for any claimed business effect.
4.  Open **Recorded review** and confirm availability and the selected revision.

![Recorded review showing its saved revision and two retained turns.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/browser-recovered-review.png)

A published Recorded review lets you inspect the saved turns even when the security outcome is inconclusive.

5.  Use [Download redacted review](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/history-and-exports.md#download-and-check-the-redacted-review) to retain a copy of the selected revision.

## Read a browser run that needs attention

1.  Open the saved trace. Read **Assessment execution**, **Security outcome** and the reason in **Waiting on a decision**. The example shows **Needs attention** with **No verdict recorded**.

![Saved browser run showing Waiting on a decision, an uncertain fresh-conversation timeout, Needs attention and No verdict recorded.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/assessment-browser-needs-attention.png)

Preserve the original action for inspection. Successful website sign-in and setup messages did not produce a completed probe or a security verdict.

2.  Open **Probe coverage**. **Scheduled** with **No outcome recorded** means the probe has no verdict. Setup requests and probe requests are counted separately.

![Browser probe coverage showing Scheduled, No outcome recorded, zero of thirty probe target calls and zero of one hundred probe model calls.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/assessment-browser-coverage.png)

The disclosure goal was scheduled, with no probe outcome recorded. These probe counters exclude the campaign’s earlier neutral setup messages.

3.  Refresh to see the latest evidence for the same run. Use **Download legacy JSON evidence** to retain the available trace.
4.  If an action is uncertain, preserve the run code and inspect the original action before choosing a recovery. Use **The action did not execute** when you have evidence for that decision.

## Exports and limitations

**Download report** exports run/finding JSON. The trace’s legacy JSON download includes its currently displayed findings page; read its pagination flags. Artifact-backed **Recorded review** can offer **Download redacted review** when a published revision is available. See [history and exports](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/history-and-exports.md) for the differences.

A finding can require human verification even when it has a severe consequence label. Endpoint-only textual consistency does not establish that a real payment, permission or record changed. A **Largest cleanly reproduced sandbox refund** value is an observed synthetic sample for this run, not a production loss forecast or measured call-gate saving.

Continue with [reproduction and evidence limits](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/reproduction-and-limits.md) and [retained history](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/history-and-exports.md).
