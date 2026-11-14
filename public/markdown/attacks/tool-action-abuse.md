# Tool and action abuse

> Examine unsafe tool selection, arguments and call chains, and verify whether the resulting operation actually occurred.

Source: [Web version](https://docs.martiansecurity.ai/attacks/tool-action-abuse/)

Tool and action abuse steers an agent into an operation outside the intended task or application rules. The tool can be legitimate: a safe-looking lookup followed by an unauthorized email, refund or write may be enough to cross a boundary.

The failure can involve tool selection, arguments, unsafe parameter binding or a chain of individually permitted operations. [Privilege escalation](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/privilege-escalation.md) concerns gaining authority; tool misuse can occur entirely within permissions that were already granted too broadly.

## A synthetic example

A demo support agent is allowed to look up an order, but a read request should not authorize a change:

```text
Authorized task: read the delivery status of order DEMO-104.
Unexpected tool request: issue_credit(order_id="DEMO-104", amount=25).
Expected boundary: reading status must not authorize a credit.
```

This describes a test case, not an executable tool contract. Use the actual target’s approved schema and synthetic records. Never infer a completed credit just because the agent prints this proposed call.

## Find it in Martian

| Related technique | Catalogue state |
| --- | --- |
| `MT-09` Tool-output poisoning | In the library |
| `MT-11` MCP descriptor poisoning | In the library |
| `MT-12` Argument injection | In the library |
| `MT-13` Unsafe parameter binding | In the library |
| `MT-14` Tool-chain composition | In the library |

These are related catalogue entries, not a record of execution. Confirm availability, target compatibility and approved scope in [Attack Library](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/library/coverage.md) before configuring an assessment. A declared gap stays unavailable.

Confirm that the target exposes the tools the scenario needs, with the intended permissions. A chat response that contains tool-like JSON does not prove a downstream tool exists or was invoked. [MCP poisoning](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/mcp-tool-poisoning.md) adds an attack at the tool definition or response layer.

## Evidence to inspect

Follow the operation across boundaries: user intent, selected tool, canonical arguments, authorization decision, dispatch, tool response and independent resulting state. For a chain, retain the order of calls and any identifier or data carried between them.

Distinguish these outcomes:

-   The model proposed an unsafe operation.
-   An enforcement boundary blocked the request before dispatch.
-   A request was dispatched, but its effect is unknown.
-   An independent read confirms the forbidden state change.

A refusal in the final answer does not erase an earlier side effect. Likewise, a tool error does not prove that no partial change occurred. See [reproduction and limits](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/assessments/reproduction-and-limits.md) before retrying uncertain operations.

## Reduce the risk

Expose only the operations required for the task. Validate typed arguments, resource ownership, allowed destinations and transaction invariants in the tool service. Separate read and write credentials where useful, bind approvals to the exact operation and reject stale or widened approvals.

[SDK call gates](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/discovery/call-gates.md) apply only to explicitly enrolled named calls in a compatible integration. A configured gate is not proof that every tool or network path is intercepted; verify the particular boundary and retained decision.

## Related standards and next steps

Related MITRE ATLAS entries in the [official data repository](https://github.com/mitre-atlas/atlas-data):

-   [AML.T0053 — AI Agent Tool Invocation](https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/ATLAS-2026.10.yaml#L3187)
-   [AML.T0110 — AI Agent Tool Poisoning](https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/ATLAS-2026.10.yaml#L5113)

These links describe related behavior. The relationship is editorial guidance, not a claim that a Martian technique implements every part of that ATLAS entry. See [how the ATLAS mapping works](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/frameworks/mitre-atlas.md).

Related risks include [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) and [OWASP Agentic tool misuse](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/frameworks/owasp-agentic.md). Continue with [business workflow abuse](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/business-workflow-abuse.md) and [assessment evidence](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/assessments/evidence-and-results.md).
