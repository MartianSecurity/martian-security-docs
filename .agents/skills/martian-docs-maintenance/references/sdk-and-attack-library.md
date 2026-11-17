# SDK, CI, local UI and attack references

## Released SDK truth

Inspect the current PyPI distribution, actual installed help/source, downloadable examples and owning SDK docs before changing commands or compatibility claims. Use the existing local SDK release skill when a task actually concerns release/provenance operations. This docs-maintenance skill does not publish packages or container images.

Use an isolated environment and the complete ZIP served by the built/public site. Run the exact documented commands, retaining files together and their relative paths. A source-checkout command or a schema that accepts a field is not proof it exists or works in the released package.

Record release/wheel digest, example archive/source digest, test environment, actual outputs/exits and the relevant service/provider scope. Normal customer install commands stay evergreen (`pip install --upgrade 'martian-sdk[evals]'` when appropriate). Versions belong in real minimum compatibility requirements and historical verification, with release history linked to [PyPI](https://pypi.org/project/martian-sdk/#history), rather than a large announcement for every release.

Do not preserve an obsolete minimum merely because a previous run used it. The SDK changed from no local UI to released local UI and container support during this project; the current source/registry must decide availability. Conversely a later release does not automatically inherit an earlier hosted CI/judge/redteam qualification.

### Modes that must stay distinct

| Mode | Required distinction |
| --- | --- |
| Local suite with deterministic checks | Can be account/model-key free; an intentional failure is not a setup error |
| Local LLM judge | Inputs, replies and criteria reach the selected provider; real routing/permission/error behavior must be checked |
| Local Evals UI | Customer-facing SDK UI on its data folder, not the MLflow dependency UI |
| Container local UI | Published image pulled/run with the documented tag; persistence, interface/host checks and auth boundary need their own evidence |
| Persisted Evals / hosted redteam / combined CI | Correct platform key/scopes, organization readiness, actual API support and retained results; local success alone is insufficient |
| Runtime reporter / MCP binding / cooperative Call Gate | Separate enrollment, credentials, policy/acknowledgment and enforcement scope; not network isolation |
| Import/migration from MLflow, Promptfoo or Inspect | Real import, readback, traces/dataset/run provenance and unsupported mappings; not blanket ecosystem feature parity |

Check first failing run, result files/failing record, resume/fresh/corrected run and relevant error exits. Resume behavior changed across SDK releases, including source/target fingerprints; do not promise that a changed agent reuses the same prior results. Compare actual installed help and file behavior.

Missing environment variables, wrong HTTP tokens, stopped targets, unsupported judge routing, provider denial and rate-limit waiting are different tests. A configured wait limit accepted by the schema does not prove real 429/retry waiting. Native `bedrock:/...` routing once failed while an OpenAI-compatible Bedrock route worked; recheck the current release before repeating either claim, and preserve the actual tested route/model scope.

Never publish API-key values or once-shown disclosures. Explain platform credentials separately from a callback's model/provider keys. Configuration origin/transport restrictions, `.env` loading, scopes, timeouts and redirect/proxy behavior come from the released implementation, not a remembered snippet. Placeholders must be obviously placeholders and not accidentally embedded in a runnable verified command.

The local UI data folder and exported results can contain clear-text inputs/replies. Do not expose it casually while capturing a tutorial. A loopback/no-login server and a remotely exposed container are different deployment boundaries; document the actual binding, allowed Host behavior and persistence tested. A pulled container or successful health read is not a completed local-UI walkthrough.

## Attack library and frameworks

Use `quality/attack-library.json`, the actual enabled catalogue, native attack-family/operator support and Wiki mappings as the owning implementation. Reconcile taxonomy names, technique IDs, eligible target surfaces and actual execution evidence separately. A framework mapping or requested MT-ID does not prove an operator ran.

The established architecture has one page per major attack family, focused pages for important direct/indirect injection, tool/MCP and business-workflow attacks, plus framework guides and a hub. Do not reduce this to a single undifferentiated list or duplicate every page's content in the framework guide.

Each attack page should provide:

- Plain-language behavior and boundary at risk.
- An original synthetic example, prerequisites and applicable surface/interface.
- Related actual technique IDs, enabled/disabled/declared-gap limits and evidence needed to establish an outcome.
- Defenses/mitigations grounded in the behavior and links to a supported next task.
- Direct primary references and exact framework identifiers/version when verified.

MITRE **ATLAS** (AI/ML adversary techniques) and **ATT&CK** are separate catalogues. OWASP LLM and Agentic lists and NIST AI RMF serve different purposes. Do not invent equivalence, universal coverage, certification or compliance because a page has a cross-reference. Recheck primary authoritative sources when updating their facts or versions; retain clear citations close to the claim. Do not copy another vendor's attack prose/prompts wholesale.

An enabled technique, disabled declared gap, available scenario, reviewed Wiki route, threat-intelligence feed and observed target interaction are different product states. "No live feed connected" should remain a real empty state, not a fabricated feed screenshot. Prepared scenarios additionally need compatible catalogue services, bindings/implant profiles, approved sources and independently checked worlds. The attack reference can explain a concept while clearly saying the current workflow cannot execute it.
