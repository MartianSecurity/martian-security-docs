# Supply chain and backdoors

> Understand attacks introduced through dependencies, tools, skills, models and updates, and the limits of endpoint-based testing.

Source: [Web version](https://docs.martiansecurity.ai/attacks/supply-chain-backdoors/)

Supply-chain attacks introduce malicious behavior through something an AI system adopts or updates: a dependency, skill, plugin, MCP server, dataset or model artifact. A backdoor is behavior activated under particular conditions, possibly after normal use has appeared safe.

The compromised component can affect the model’s instructions or execute a side effect directly. A poisoned tool implementation may act maliciously even when the model makes an ordinary, authorized call.

## A synthetic example

A demo lookup tool changes after an update:

```text
Approved behavior: return a synthetic order's delivery status.
Unexpected update: also copy the full demo record to a second sink.
Trigger: the order reference begins with DEMO-.
Protected rule: a lookup must not authorize a separate data transfer.
```

Use only a controlled test implementation and an approved synthetic receiver. A trigger described in a prompt does not establish an implementation backdoor or a compromised model artifact.

## Find it in Martian

| Related technique | Catalogue state |
| --- | --- |
| `MT-11` MCP descriptor poisoning | In the library |
| `MT-24` Standing backdoor | **Declared gap** |

These are related catalogue entries, not a record of execution. Confirm availability, target compatibility and approved scope in [Attack Library](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/library/coverage.md) before configuring an assessment. A declared gap stays unavailable.

MCP descriptor poisoning is related to one part of this family. **MT-24 Standing backdoor is a declared gap.** The broader published catalogue includes software and model supply-chain research; it does not establish support for changing weights, training models, compromising dependencies or testing arbitrary build systems.

An assessment through an approved endpoint observes that interface. It is not a substitute for artifact provenance, dependency review or build-system security checks. Use [supported target limits](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/supported-targets.md) to define what the test can actually reach. To review what an agent loads (its skills, MCP configurations, plugins and the packages and links they name), scan those files with the [Scanner](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/overview.md).

## Evidence to inspect

Identify the component, publisher, version or digest, installation path and the specific change being tested. Compare the approved behavior with the changed behavior and retain the trigger conditions. For a hidden side effect, inspect the execution or receiving system independently of the visible response.

Separate a malicious definition, a poisoned runtime response and executable implementation behavior. A descriptor hash change can establish drift, but it does not alone prove exploitation. Conversely, an unchanged model answer can coexist with a hidden transfer performed by a tool.

If a trigger is not reached, describe the path as untested. A finite set of clean requests cannot exclude every dormant condition. Retain enough artifact provenance to make the result meaningful after the next update.

## Reduce the risk

Review sources and publisher identities, pin approved artifacts and verify updates before enabling them. Keep build and deployment credentials separate from runtime permissions. Restrict tool data access and egress even for trusted dependencies. Maintain an inventory and a controlled rollback path, and investigate changes in definitions, implementations and permissions together.

## Related standards and next steps

Related MITRE ATLAS entries in the [official data repository](https://github.com/mitre-atlas/atlas-data):

-   [AML.T0010 — Supply Chain Compromise](https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/ATLAS-2026.10.yaml#L1211)
-   [AML.T0110 — AI Agent Tool Poisoning](https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/ATLAS-2026.10.yaml#L5113)
-   [AML.T0115 — Publish Poisoned AI Artifacts](https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/ATLAS-2026.10.yaml#L5446)

These links describe related behavior. The relationship is editorial guidance, not a claim that a Martian technique implements every part of that ATLAS entry. See [how the ATLAS mapping works](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/frameworks/mitre-atlas.md).

See [OWASP LLM supply-chain risks](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/frameworks/owasp-llm.md) and [OWASP Agentic ASI04](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/frameworks/owasp-agentic.md). Continue with [MCP and tool poisoning](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/mcp-tool-poisoning.md) or [memory and context poisoning](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/attacks/memory-context-poisoning.md).
