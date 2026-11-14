# OWASP Agentic Top 10

> Understand official Agentic risk names, native Martian tags and the boundaries involved in tools, identity, memory and coordination.

Source: [Web version](https://docs.martiansecurity.ai/frameworks/owasp-agentic/)

The [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) focuses on risks in systems that plan, act and coordinate. It complements the [LLM Top 10](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/frameworks/owasp-llm.md) rather than replacing it.

## The official entries

| OWASP entry | Related reading in this reference |
| --- | --- |
| ASI01 Agent Goal Hijack | [Prompt injection](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/prompt-injection.md) |
| ASI02 Tool Misuse and Exploitation | [Tool and action abuse](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/tool-action-abuse.md) |
| ASI03 Identity and Privilege Abuse | [Privilege escalation](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/privilege-escalation.md) |
| ASI04 Agentic Supply Chain Vulnerabilities | [Supply chain and backdoors](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/supply-chain-backdoors.md) |
| ASI05 Unexpected Code Execution (RCE) | [Tool abuse](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/tool-action-abuse.md), with independent execution evidence |
| ASI06 Memory and Context Poisoning | [Memory and context poisoning](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/memory-context-poisoning.md) |
| ASI07 Insecure Inter-Agent Communication | [Multi-agent handoff boundaries](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/multi-agent-attacks.md) |
| ASI08 Cascading Failures | [Propagation across agents](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/multi-agent-attacks.md) |
| ASI09 Human-Agent Trust Exploitation | [Human manipulation](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/human-manipulation.md) |
| ASI10 Rogue Agents | [Multi-agent behavior](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/multi-agent-attacks.md) and [objective-related limits](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/reasoning-alignment-subversion.md) |

The names identify the official entries in the [OWASP publication](https://genai.owasp.org/download/52117/?tmstv=1765059207). The reading links are editorial relationships. They do not declare complete coverage or equate every attack on that page with the corresponding risk.

## Native tags use some different wording

Martian’s stored list currently includes `ASI02`, `ASI03`, `ASI04`, `ASI06`, `ASI07` and `ASI08`. Some console display labels are shorter or use different terminology from the official publication:

| Native label | Official entry to consult |
| --- | --- |
| ASI03 Privilege compromise | ASI03 Identity and Privilege Abuse |
| ASI07 Trust boundary | ASI07 Insecure Inter-Agent Communication |
| ASI08 Agent collusion | ASI08 Cascading Failures |

In particular, **Agent collusion is not the official name of ASI08**. Do not copy that display label into a report as an official definition. Inspect the actual scenario and evidence to decide which risk applies.

An absent `ASI01` or `ASI09` tag does not prove that an adjacent injection or approval technique is irrelevant. Conversely, a related technique does not establish comprehensive coverage of an official entry. `MT-36 Worker collusion` remains a declared gap.

## Define the boundary before selecting scope

For a tool test, identify the operation and authority. For an agent handoff, identify the sender, receiver, message provenance and scope. For a memory test, identify the store and later read. For a human approval, compare the displayed request with the exact action.

Use an approved synthetic scenario that actually exposes the required surface. Keep a proposed action, a dispatched call and an independently verified effect separate in the result. A passing judge or framework filter is not proof of enforcement at every boundary.

Continue with [Attack Library coverage](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/library/coverage.md), [the attack families](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/library/attacks.md) and [assessment evidence](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/assessments/evidence-and-results.md).
