# OWASP LLM Top 10

> Use the OWASP LLM application risks to organize testing, with explicit limits on Martian tags and executable coverage.

Source: [Web version](https://docs.martiansecurity.ai/frameworks/owasp-llm/)

The [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) describes application risk categories. A category is broader than a single attack payload or executable test. Use it to ask what could fail, then choose a supported technique and define observable evidence.

## The 2025 risk categories

The names below identify the official OWASP entries. The Martian reading links are editorial starting points, not a complete crosswalk or a claim that every category is covered.

| OWASP entry | Start investigating |
| --- | --- |
| LLM01 Prompt Injection | [Untrusted instructions](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/prompt-injection.md) |
| LLM02 Sensitive Information Disclosure | [Protected data and destinations](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/data-exfiltration.md) |
| LLM03 Supply Chain | [Dependencies, tools and artifacts](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/supply-chain-backdoors.md) |
| LLM04 Data and Model Poisoning | [Poisoned context](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/memory-context-poisoning.md) and [training-related limits](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/reasoning-alignment-subversion.md) |
| LLM05 Improper Output Handling | [Unsafe tool arguments and actions](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/tool-action-abuse.md); also review the consuming application’s output handling |
| LLM06 Excessive Agency | [Tool scope](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/tool-action-abuse.md) and [delegated authority](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/privilege-escalation.md) |
| LLM07 System Prompt Leakage | Review what prompt content is exposed and whether it contains protected information |
| LLM08 Vector and Embedding Weaknesses | [Retrieval poisoning and access boundaries](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/memory-context-poisoning.md) |
| LLM09 Misinformation | Compare answers with authoritative data; inspect [scorer limits](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/guardrail-judge-evasion.md) |
| LLM10 Unbounded Consumption | [Time, cost and resource exhaustion](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/denial-of-service.md) |

Use [OWASP’s official risk pages](https://genai.owasp.org/llm-top-10/) for definitions and mitigations. For example, [LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) concerns agency granted to an application; it is not simply another name for a jailbreak.

## Read Martian’s tags accurately

The current selectable list uses `LLM01`, `LLM02` and `LLM08` on related entries. It also contains Agentic `ASI…` tags and the native `business` and `social` groupings. Those last two are Martian labels, not official OWASP IDs.

The **OWASP LLM + Agentic** library view filters and groups stored entries. It does not establish complete Top 10 coverage. In particular, documentation about supply chains, model poisoning, misinformation or resource exhaustion must not be read as proof that a corresponding dedicated test is selectable.

## Turn a category into a test

Write a concrete rule and outcome, such as “a viewer must not receive another synthetic tenant’s record.” Identify the actual retrieval or tool boundary, select a compatible available technique, and compare the result with that rule. Record any unsupported surface or missing observation explicitly.

Keep prompt disclosure distinct from data compromise: exposed instructions may reveal useful implementation details, but a claim of secret disclosure needs an actual protected value and an unauthorized reader. Likewise, an incorrect answer and a downstream execution flaw require different checks.

After a supported run, retain the underlying evidence with its OWASP reference. A framework label or a passing set of selected cases is not a security certification.

Continue with the [OWASP Agentic Top 10](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/frameworks/owasp-agentic.md), [Attack Library coverage](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/library/coverage.md) and [results and scores](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/evals/results-and-scores.md).
