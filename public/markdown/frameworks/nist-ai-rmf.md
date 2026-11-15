# NIST AI RMF

> Place Martian testing evidence within Govern, Map, Measure and Manage without treating a library lens as a complete risk program.

Source: [Web version](https://docs.martiansecurity.ai/frameworks/nist-ai-rmf/)

The [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) organizes risk work into **Govern, Map, Measure and Manage**. These functions apply across the lifecycle and inform one another. They are not four test suites or a mandatory sequence of steps.

The [NIST Playbook](https://airc.nist.gov/airmf-resources/playbook/) offers suggested actions. Use the official sources for their full scope; a red-team assessment supplies only part of the evidence a risk program needs.

## Use a concrete workflow

Consider a support agent connected to a synthetic order system. A useful application of the functions is:

| Function | Example decision or evidence |
| --- | --- |
| Govern | Assign the owner of the approval policy, testing authorization, risk acceptance and change review |
| Map | Identify users, data, tools, trust boundaries and the consequences of an unauthorized credit |
| Measure | Run a bounded compatible test and inspect actual attempts, scorer limits and independent state checks |
| Manage | Prioritize the observed failure, repair the relevant boundary, retain a regression case and review residual uncertainty |

These are applied examples for this workflow, not replacements for NIST’s categories and subcategories. Governance remains relevant throughout the other functions.

## Interpret the Martian lens

The current Attack Library has a **NIST** view using stored Map, Measure and Manage tags. It does not include a Govern bucket in that native technique lens. That is a limitation of the product grouping, not a change to the four-function framework.

Selecting the lens does not assess every AI RMF outcome or determine organizational maturity. A technique tagged Manage is not evidence that remediation, ownership or risk acceptance has already happened.

## Retain useful evidence

Connect the tested rule to the actual agent and environment, approved scope, relevant data boundaries and accountable owner. Keep the run and dataset revisions, attempts, scores, failed observations and outcome checks together where the workflow supports them.

After a failure, record the remediation and the conditions under which it was checked again. A successful retest of one case does not erase untested interfaces or unknown side effects. Preserve incomplete results so a later decision can account for them.

For ongoing evaluation, use [versioned datasets](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/datasets.md), [regression cases](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/regression-cases.md) and [comparisons](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/compare.md) where appropriate. Scoring quality and operational risk ownership remain separate responsibilities.

The framework relationship is guidance for organizing evidence, not a NIST endorsement or certification. Continue with [attack selection](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/library/attacks.md) and [reproduction and limits](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/reproduction-and-limits.md).
