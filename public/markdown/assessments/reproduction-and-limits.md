# Understand reproduction and coverage limits

> Distinguish observed replies, independently verified effects, clean reproduction, negative controls and incomplete coverage.

Source: [Web version](https://docs.martiansecurity.ai/assessments/reproduction-and-limits/)

Current beta console · viewer, member, admin, owner

Use the strongest retained evidence for the question you are answering. A reproducible reply, an executed tool call and a reproducible change in a restored business world support different conclusions.

## Before you start

Any tenant role can inspect a retained run it can access. You need an actual run with its recorded scope, verification receipts and coverage. Independent business verification additionally requires a sandbox-backed target with approved checks; an endpoint-only run cannot create missing world-state evidence after the fact.

## Review the reproduction claim

The [glossary](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/glossary.md) defines oracle, world epoch, carrier/implant and no-implant control. These terms identify different evidence checks; they are not interchangeable labels for a passed run.

1.  Open the run and read **Security outcome** separately from **Assessment execution**. A completed bounded search may have findings, no findings or inconclusive coverage; completion does not certify the agent.

2.  Open a verification row or the versioned **Verification receipts** section. Inspect its retained status and evidence. In artifact-backed reviews, the policy can retain verdict metadata without the verifier body. For a canonical finding, open **Findings → Recorded detail** to inspect the saved verification fields, repetition counts and control result. A legacy verification panel can display these as labeled fields.

3.  For a business effect, open **Outcome checks** and compare independently read baseline/after values. Check that repeated worlds were restored to an equivalent baseline and used distinct observed world epochs. Reusing a mutated world cannot establish clean reproduction.

4.  Inspect the control when required. For a chat probe, compare the replay request with its benign control message. For a prepared scenario, also check whether removing the implant removes the effect. A passing chat control alone does not establish attribution to an implant.

5.  Check the finding’s actual verification status after refresh. Martian only presents cleanly reproduced findings as verified when the recorded reproduction conditions are satisfied.


## Interpret the states

| Recorded result | Interpretation |
| --- | --- |
| Verified / cleanly reproduced | The recorded successful repetitions, trusted evidence and required controls met the admitted reproduction boundary. Read the specific scope and receipts. |
| Consistent / state dependent | Similar behavior or a positive observation exists, but the required evidence tier or clean-world boundary was not established. It needs further verification. |
| Unverifiable / untested | No trusted oracle or required evidence source could establish reproduction. This is uncertainty, not a pass. |
| Not reproducible | The recorded repetitions did not meet the reproduction threshold within this run’s scope. It does not prove the behavior is impossible. |
| Negative control skipped after negative repeats | Trusted repetitions were negative, so the runtime omitted a control that could not turn them positive. A skipped control is not a passed one. |

The normal profiles request two verification repetitions and two successful reproductions. The run’s admitted profile and receipts remain authoritative. Exact regression replay can require its control even after negative repeats.

## Example: two successful repetitions and a passing control

1.  Open **Findings → Recorded detail**. To read a cleanly reproduced result like the one shown here, check the saved `verification` object for the number of repetitions, how many succeeded, and whether the negative control passed.

```json
{
  "status": "verified",
  "reproduction_status": "reproduced_clean",
  "repetitions": 2,
  "successful_reproductions": 2,
  "negative_control_passed": true
}
```

![MR-1009 completed with four agent requests, seven model calls and a finding labeled reproduced clean.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/clean-reproduction-finding.png)

The finding records reproduced clean. Its 4 agent requests include the original probe, two positive repetitions and one executed benign control.

2.  Open **Outcome checks**. Compare the before and after records for each repetition and the control. Check for distinct world epochs and matching baseline-equivalence digests. A passing control should have its own receipt recording **No violation observed**.

![Independent payment world receipts show violations in restored epochs five and six, and no violation for the executed control in epoch seven.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/clean-reproduction-world-control.png)

The two repeated worlds show Violation observed; the executed benign control shows No violation observed. All three retain the same baseline-equivalence digest.

3.  Compare the retained messages to see whether each repetition used the original wording. Use the structured receipt and independent records to resolve any discrepancy with the model-generated summary.
4.  In **Recorded review → Verification receipts**, check for separate rows for the verification result and control. A redacted review may include only verdict metadata. Include the finding detail, review revision and independent receipts when sharing the result.

**Largest cleanly reproduced sandbox refund** can show **Unavailable** when verification checks a transaction count without measuring a monetary amount. Use the verification receipt for reproduction counts and the independent ledger for the observed business effect.

## Separate evidence from interpretation

1.  Read the **Verifier narrative (model-generated)** as an interpretation. It may disagree with independent world receipts.
2.  For tool use, distinguish a catalogue advertisement, an attempted call, a gateway refusal, an error and an executed call. Execution alone still does not establish the intended downstream effect.
3.  For state-changing objectives, use independent before/after records rather than the target’s statement that it completed an action. A strong text match can establish disclosure in a reply, but not an unobserved payment or permission change.
4.  For imported history, retain its original provenance. It does not represent a fresh execution in the current deployment.

If **Outcome captured** and **After-state digest** are **Pending**, the saved evidence only establishes the starting state. Check the [baseline and outcome fields](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/agents/sandbox-bindings.md#example-a-passed-baseline-with-no-outcome-verdict) before drawing a conclusion about business impact.

![Outcome checks with a ready starting receipt, five ledger records, two met baseline conditions, pending after-state and unavailable cleanly reproduced refund.](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/media/screenshots/assessment-outcome-checks.png)

Both baseline prerequisites passed. Outcome captured and After-state digest remain Pending, and no complete comparison or refund verdict exists. The duplicated-refund sentence describes the configured check.

## Observed effect and failed repetition are different results

Keep the initial [before-and-after comparison](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/agents/sandbox-bindings.md#example-a-completed-independent-business-comparison) with the later verification receipts. When verification records **Not reproduced**, report the original observed effect and the unsuccessful repetitions separately. Use the retained messages and baseline digests to identify what changed between observations. Report a control as skipped when its receipt shows it never ran.

## Check coverage before deciding what to do

Review selected versus executed techniques, budget exhaustion, skipped work, missing records, failed knowledge lookups, dropped customer events and any pending evidence delivery. **Attempts held** needs a complete attempt count and blocked classification; a run with no tested attempts has no meaningful held ratio.

The depth selector reports ceilings, not a promise that every allowance will be used. Default Light/Normal/Deep profiles allow at most 30/90/180 target requests and 100/300/700 model calls respectively, subject to workspace/server caps. Prepared scenarios use one search trigger and their admitted verification budget; browser setup also consumes requests.

**Largest cleanly reproduced sandbox refund** is the largest independently observed sample among this run’s retained clean repetitions. It is not an expected production loss, loss ceiling, incident probability or proof of savings from a call gate.

If evidence is insufficient, keep the result inconclusive, fix the missing prerequisite and explicitly schedule an appropriate new bounded assessment. Reading, comparing or exporting saved evidence does not fill missing execution coverage.

Next: [inspect evidence](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/evidence-and-results.md), [find and export retained runs](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/history-and-exports.md), or [review platform limits](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/limits.md).
