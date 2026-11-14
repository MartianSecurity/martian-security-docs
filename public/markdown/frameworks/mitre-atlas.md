# MITRE ATLAS

> Use ATLAS tactics and techniques to describe AI attacks while keeping Martian catalogue IDs, framework references and execution evidence separate.

Source: [Web version](https://docs.martiansecurity.ai/frameworks/mitre-atlas/)

MITRE ATLAS is a knowledge base of adversary behavior involving AI systems. It includes techniques concerning prompts, tools, context, models, data and the surrounding supply chain. Use the [official ATLAS site](https://atlas.mitre.org/) and [MITRE’s data repository](https://github.com/mitre-atlas/atlas-data) for the authoritative definitions.

ATLAS and [MITRE ATT&CK](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/frameworks/mitre-attack.md) are related MITRE knowledge bases with distinct identifiers and scope. “MITRE” is the organization; it is not a third attack framework alongside those two.

## Read the identifiers

| Identifier | Meaning |
| --- | --- |
| `AML.TA…` | ATLAS tactic: the adversary’s purpose at a stage |
| `AML.T…` | ATLAS technique or sub-technique: a kind of behavior |
| `MT-…` | Martian catalogue technique, such as `MT-07 Document injection` |

An `MT-` entry is not an official ATLAS identifier. Similar wording or a related attack mechanism does not establish a one-to-one match.

## Start with a relevant behavior

| ATLAS reference | Read about the corresponding attack surface |
| --- | --- |
| `AML.T0051` LLM Prompt Injection | [Prompt injection](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/prompt-injection.md) |
| `AML.T0051.000` Direct; `AML.T0051.001` Indirect | [Direct](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/direct-prompt-injection.md) and [indirect](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/indirect-prompt-injection.md) delivery |
| `AML.T0054` LLM Jailbreak | [Jailbreaks](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/jailbreaks.md) |
| `AML.T0053` AI Agent Tool Invocation | [Tool and action abuse](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/tool-action-abuse.md) |
| `AML.T0070` RAG Poisoning; `AML.T0080` AI Agent Context Poisoning | [Memory and context poisoning](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/memory-context-poisoning.md) |
| `AML.T0110` AI Agent Tool Poisoning | [MCP and tool poisoning](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/mcp-tool-poisoning.md) |
| `AML.T0086` Exfiltration via AI Agent Tool Invocation | [Data exfiltration](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/data-exfiltration.md) |
| `AML.T0010` Supply Chain Compromise | [Supply chain and backdoors](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/supply-chain-backdoors.md) |
| `AML.T0029` Denial of AI Service; `AML.T0034` Cost Harvesting | [Resource exhaustion](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/denial-of-service.md) |

These names and IDs were checked against [MITRE’s published ATLAS data](https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/ATLAS-2026.10.yaml). Each attack page links the relevant entries and explains the narrower Martian support boundary.

## Interpret the Martian view

The console’s **MITRE ATLAS** lens groups the stored catalogue for exploration. Its eight native technique buckets are Injection, Execution, Escalation, Persistence, Collection, Exfiltration, Impact and Evasion. This is a product grouping, not a reproduction of the complete official ATLAS tactic matrix.

Treat displayed anchor references as navigation context. For example, the native Execution bucket uses `AML.T0086`, whose official name concerns exfiltration through tools. That anchor is not an exact official mapping for every technique in the bucket. Use the actual behavior and authoritative entry definition when writing a report.

Selecting a framework lens does not install every ATLAS technique, expand target access or establish that a test ran. Follow [Attack Library coverage](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/library/coverage.md) to choose available scope, and inspect the run’s actual attempts and evidence.

## Report a mapping responsibly

Record the Martian technique ID, the related ATLAS ID and source edition, the tested surface, and why the relationship applies. Keep the framework reference separate from the observed result and any independent outcome check. When only part of an ATLAS entry was exercised, describe that part.

These documentation relationships are editorial guidance. They do not represent MITRE endorsement, exhaustive coverage or a certification. Continue with the [attack reference](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/library/attacks.md) or [assessment configuration](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/assessments/configure.md).
