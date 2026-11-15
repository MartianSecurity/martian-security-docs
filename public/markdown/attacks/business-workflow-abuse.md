# Business workflow abuse

> Test refunds, credits and claims against persisted application rules rather than relying on the agent's reported success.

Source: [Web version](https://docs.martiansecurity.ai/attacks/business-workflow-abuse/)

Business workflow abuse breaks an application’s rules through operations that may look individually legitimate. Examples include repeated credits, stacked compensation, duplicate claims and attempts to move an exception past its approval boundary.

The important test is the business invariant: a rule about state that must hold across calls and sessions. An agent’s polite response, a valid API schema or an accepted tool request does not establish that the invariant held.

## A synthetic example

A demo order permits a total credit of 25 units, even if a customer asks several times:

```text
Order: DEMO-104
Maximum cumulative credit: 25 demo units
Initial credited total: 0
Forbidden result: two accepted credits of 25 make the total 50
Expected invariant: credited_total <= 25
```

This is an explanatory fixture, not a claim that a particular Martian sandbox uses this rule. Use the approved scenario’s actual invariant, starting state and supported outcome checks. Never substitute live money or customer records.

## Find it in Martian

| Related technique | Catalogue state |
| --- | --- |
| `MT-12` Argument injection | In the library |
| `MT-13` Unsafe parameter binding | In the library |
| `MT-14` Tool-chain composition | In the library |
| `MT-15` Approval-gate bypass | In the library |
| `MT-16` Confused deputy | In the library |
| `MT-30` Refund loop | In the library |
| `MT-31` Comp stacking | In the library |
| `MT-32` Price arbitrage | **Declared gap** |
| `MT-33` Duplicate claim | In the library |

These are related catalogue entries, not a record of execution. Confirm availability, target compatibility and approved scope in [Attack Library](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/library/coverage.md) before configuring an assessment. A declared gap stays unavailable.

The list includes refund loops, compensation stacking and duplicate claims. **MT-32 Price arbitrage is a declared gap.** The native `business` tag is a Martian grouping, not an OWASP identifier.

A meaningful test requires access to the relevant synthetic business system and a way to inspect its state. Endpoint-only output can establish a claimed or attempted operation; it cannot automatically establish that a refund, claim or balance changed.

## Verify the effect

Capture the relevant initial state, record identity and allowed operation. Retain request and transaction identifiers, arguments, responses and the final state read from the authoritative system. Compare cumulative effects across the relevant sequence, not just each call in isolation.

Check whether retries represent the same operation or a new operation. If dispatch succeeded but confirmation timed out, preserve the unknown result and inspect the receipt or ledger before resubmitting. A retry that creates another credit can itself change the state being measured.

When a supported scenario provides an independent outcome check or no-implant control, inspect that evidence and its scope. Do not label an effect verified solely because the attacker, target or another model says it happened. See [reproduction and limits](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/reproduction-and-limits.md).

## Reduce the risk

Enforce cumulative limits, uniqueness, resource ownership and approval requirements in the business service. Use transaction boundaries and idempotency appropriate to the operation. Bind approvals to the exact consequential arguments and verify them again at execution. Include regression cases for a repeated request and a changed request, while preserving unknown outcomes safely.

## Related standards and next steps

Related MITRE ATLAS entries in the [official data repository](https://github.com/mitre-atlas/atlas-data):

-   [AML.T0053 — AI Agent Tool Invocation](https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/ATLAS-2026.10.yaml#L3187)

These links describe related behavior. The relationship is editorial guidance, not a claim that a Martian technique implements every part of that ATLAS entry. See [how the ATLAS mapping works](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/frameworks/mitre-atlas.md).

The ATLAS relationship concerns tool invocation, not a dedicated official refund-loop technique. See [OWASP excessive agency](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/frameworks/owasp-llm.md), [tool and action abuse](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/tool-action-abuse.md) and [assessment results](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/assessments/evidence-and-results.md).
