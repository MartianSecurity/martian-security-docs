# Human manipulation

> Inspect deceptive agent messages and approval requests against the exact action a person is being asked to authorize.

Source: [Web version](https://docs.martiansecurity.ai/attacks/human-manipulation/)

Human manipulation uses an agent’s apparent credibility to influence a person’s decision. A misleading summary, fabricated authority claim, deceptive citation or incomplete approval prompt can induce someone to authorize an action they would otherwise reject.

The trust boundary is the person’s understanding and consent. Requiring approval helps only when the interface communicates the real operation, resource, destination and consequence clearly enough to make that approval meaningful.

## A synthetic example

The proposed operation sends a complete demo record to a new recipient, but its approval summary describes a routine lookup:

```text
Displayed summary: "Approve checking the delivery status."
Actual proposed operation: send the full demo order to a new inbox.
Expected boundary: approval must describe and bind the exact action.
```

This fixture can be inspected without deceiving a real person. An AI-simulated reader review is useful for finding confusing wording, but it does not establish how real users behave or measure a successful social-engineering campaign.

## Find related techniques in Martian

| Related technique | Catalogue state |
| --- | --- |
| `MT-15` Approval-gate bypass | In the library |
| `MT-19` Identity spoofing | In the library |

These are related catalogue entries, not a record of execution. Confirm availability, target compatibility and approved scope in [Attack Library](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/library/coverage.md) before configuring an assessment. A declared gap stays unavailable.

Approval-gate bypass and identity spoofing are related entries. They do not establish support for sending phishing messages, contacting employees or running a human-subject test. The native `social` tag is a Martian grouping, not an OWASP risk identifier.

## Evidence to inspect

Compare what the person would see with the full canonical operation. Inspect the recipient, data scope, amount, resource and any changed arguments. Retain the source of authority claims and citations so the reviewer can verify them independently.

Separate a generated deceptive message, a message actually displayed, a recorded approval and a completed downstream action. Do not claim that a human was persuaded when no participant or approval record exists. If the task is an interface review, report the observed ambiguity and its potential consequence.

For workflows that genuinely require participant testing, define authorization, participant handling and the safe synthetic task before contacting anyone. Documentation examples do not grant that authorization.

## Reduce the risk

Show consequential arguments directly in the approval interface. Make sensitive changes and destination differences visible, and bind approval to the exact operation rather than a free-form model summary. Keep untrusted claims and citations identifiable. Offer an independent way to verify the source, and require renewed approval after a meaningful change.

Test whether a first-time reader can explain the action and its consequence from the displayed screen. Follow that review with the actual permitted workflow checks; a beautiful approval dialog does not establish that its backend enforces the same scope.

## Related standards and next steps

Related MITRE ATLAS entries in the [official data repository](https://github.com/mitre-atlas/atlas-data):

-   [AML.T0067 — LLM Trusted Output Components Manipulation](https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/ATLAS-2026.10.yaml#L3602)
-   [AML.T0052 — Phishing](https://github.com/mitre-atlas/atlas-data/blob/main/dist/v6/ATLAS-2026.10.yaml#L3012)

These links describe related behavior. The relationship is editorial guidance, not a claim that a Martian technique implements every part of that ATLAS entry. See [how the ATLAS mapping works](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/frameworks/mitre-atlas.md).

See [OWASP Agentic ASI09 Human-Agent Trust Exploitation](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/frameworks/owasp-agentic.md). Continue with [privilege escalation](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/privilege-escalation.md) and [business workflow abuse](https://raw.githubusercontent.com/MorningHQ/martian-security-docs/main/public/markdown/attacks/business-workflow-abuse.md).
