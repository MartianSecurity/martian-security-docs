# Attack library

> Understand major AI attack families, find related Martian techniques and use MITRE ATLAS, OWASP and NIST references accurately.

Source: [Web version](https://docs.martiansecurity.ai/library/attacks/)

Choose an attack by the boundary you want to test: who supplies instructions, what the agent can read, which actions it can take, and what must remain protected. Each page explains the attack, a synthetic example, useful evidence and ways to reduce the risk.

The reference covers all **12 major families** in Martian’s published catalogue, with focused pages for common injection and workflow attacks. The catalogue and the selectable technique list are different views: a family can be documented without a dedicated runnable technique.

## Find the right attack

| Attack family | What to investigate |
| --- | --- |
| [Prompt injection](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/prompt-injection.md) | Untrusted instructions redirect the intended task |
| [Jailbreaks](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/jailbreaks.md) | A model is pushed past its safety policy |
| [Tool and action abuse](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/tool-action-abuse.md) | Tools perform an unauthorized or unsafe operation |
| [Memory and context poisoning](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/memory-context-poisoning.md) | Stored material changes later behavior |
| [Data exfiltration](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/data-exfiltration.md) | Protected information crosses an unauthorized boundary |
| [Privilege escalation](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/privilege-escalation.md) | The agent exercises authority the requester does not have |
| [Multi-agent attacks](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/multi-agent-attacks.md) | A malicious instruction or permission crosses an agent handoff |
| [Supply chain and backdoors](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/supply-chain-backdoors.md) | A compromised dependency, tool or artifact changes behavior |
| [Reasoning and alignment subversion](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/reasoning-alignment-subversion.md) | Manipulated objectives, feedback or reasoning steer decisions |
| [Guardrail and judge evasion](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/guardrail-judge-evasion.md) | A safety check or evaluator accepts an unsafe result |
| [Denial of service](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/denial-of-service.md) | Work consumes excessive time, tokens, money or capacity |
| [Human manipulation](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/human-manipulation.md) | The agent persuades a person to approve an unsafe action |

## Common starting points

[Direct prompt injection](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/direct-prompt-injection.md)Instructions arrive in the attacker's own message.

[Indirect prompt injection](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/indirect-prompt-injection.md)Instructions arrive inside a document, email or tool result.

[MCP and tool poisoning](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/mcp-tool-poisoning.md)Tool descriptions and responses become an instruction channel.

[Business workflow abuse](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/business-workflow-abuse.md)Refunds, credits and claims break application rules.

## Use security frameworks

These frameworks answer different questions. Their mappings help organize an assessment; selecting a framework does not run every associated attack or certify a system.

-   [MITRE ATLAS](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/frameworks/mitre-atlas.md) — adversary behavior against AI systems, including prompt injection, tools, memory and the AI supply chain.
-   [MITRE ATT&CK](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/frameworks/mitre-attack.md) — adversary behavior across enterprise, mobile and industrial environments; useful when AI abuse reaches conventional infrastructure.
-   [OWASP LLM Top 10](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/frameworks/owasp-llm.md) — application risk categories, including disclosure, output handling and excessive agency.
-   [OWASP Agentic Top 10](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/frameworks/owasp-agentic.md) — risks in planning, delegated identity, tools, memory and agent coordination.
-   [NIST AI RMF](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/frameworks/nist-ai-rmf.md) — a way to govern, understand, measure and manage risk across the lifecycle.

## Take a reference into an assessment

1.  State the protected rule and the observable failure. For example: a support agent must not credit more than the authorized amount for one order.
2.  Read the relevant attack page and confirm the required surface exists. A chat-only endpoint does not automatically provide document planting, memory editing or MCP descriptor control.
3.  [Find available techniques in Attack Library](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/library/coverage.md), then [configure the assessment](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/assessments/configure.md). Use an approved target, synthetic records and a bounded budget.
4.  Inspect [actual attempts and evidence](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/assessments/evidence-and-results.md). Separate a proposed action, a dispatched action and a verified effect. A timeout or unknown action remains unresolved.
5.  Retain the evidence and [add a regression case](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/evals/regression-cases.md) where the relevant behavior can be reproduced safely.

All examples in this reference are explanatory synthetic examples. They are not newly executed walkthroughs or ready-made Martian configuration files. Target support and execution limits are described in [supported targets](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/reference/supported-targets.md) and [reproduction and limits](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/assessments/reproduction-and-limits.md).

## Read catalogue states

The observed selectable list contains **36 techniques: 32 marked In the library and four Declared gaps**. The gaps are **MT-20 Session hijack**, **MT-24 Standing backdoor**, **MT-32 Price arbitrage** and **MT-36 Worker collusion**. Availability can differ by environment; confirm the live list before selecting scope.

Browse all 36 Martian techniques

| Related technique | Catalogue state |
| --- | --- |
| `MT-01` Direct instruction override | In the library |
| `MT-02` Roleplay framing | In the library |
| `MT-03` Crescendo escalation | In the library |
| `MT-04` Encoding obfuscation | In the library |
| `MT-05` Many-shot priming | In the library |
| `MT-06` Refusal suppression | In the library |
| `MT-07` Document injection | In the library |
| `MT-08` Email thread injection | In the library |
| `MT-09` Tool-output poisoning | In the library |
| `MT-10` Retrieval store poisoning | In the library |
| `MT-11` MCP descriptor poisoning | In the library |
| `MT-12` Argument injection | In the library |
| `MT-13` Unsafe parameter binding | In the library |
| `MT-14` Tool-chain composition | In the library |
| `MT-15` Approval-gate bypass | In the library |
| `MT-16` Confused deputy | In the library |
| `MT-17` Role inheritance | In the library |
| `MT-18` Delegation widening | In the library |
| `MT-19` Identity spoofing | In the library |
| `MT-20` Session hijack | **Declared gap** |
| `MT-21` Memory poisoning | In the library |
| `MT-22` Cross-session persistence | In the library |
| `MT-23` Summary laundering | In the library |
| `MT-24` Standing backdoor | **Declared gap** |
| `MT-25` Cross-tenant probe | In the library |
| `MT-26` PII surfacing | In the library |
| `MT-27` Bulk record extraction | In the library |
| `MT-28` Outbound mail egress | In the library |
| `MT-29` Canary confirmation | In the library |
| `MT-30` Refund loop | In the library |
| `MT-31` Comp stacking | In the library |
| `MT-32` Price arbitrage | **Declared gap** |
| `MT-33` Duplicate claim | In the library |
| `MT-34` Supervisor capture | In the library |
| `MT-35` Trust-edge injection | In the library |
| `MT-36` Worker collusion | **Declared gap** |

These are related catalogue entries, not a record of execution. Confirm availability, target compatibility and approved scope in [Attack Library](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/library/coverage.md) before configuring an assessment. A declared gap stays unavailable.

The published matrix also contains research counts across attack families and surfaces. Those counts are reference material, not a count of runnable tests, completed probes or unique verified findings. A technique can relate to more than one attack family.

Use **Copy page** to share a page’s Markdown, or choose **Copy agent link** for a public text link an agent can fetch. The [agent access guide](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/reference/using-with-agents.md) explains the page index and full documentation export.
