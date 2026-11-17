# Real qualification, screenshots and evidence

## Establish what is being qualified

Record the exact guide task, interface, customer role, organization, source/runtime revisions and prerequisites. Use an authorized synthetic QA scope and bounded representative work. Check the real owning API and UI, without intercepting/mocking the behavior being verified. Local, CI, isolated compatibility QA and hosted beta are separate environments.

Inspect the important success and failure/permission paths at the cheapest reliable level. For changed API behavior, real endpoints and persisted side effects matter; a health check or mocked unit result is not an API smoke test. For UI journeys, click through the real backend, check visible results and reload retention, and inspect failed responses and console errors. A screenshot alone proves neither execution nor persistence. Do not build a large permanent test suite for a prose or cosmetic change.

Keep the original request identity when an observation times out. Inspect that request before retrying. New intent, a read-only refresh and a retry of an uncertain state-changing operation are different actions. Use a new bounded run only when it is actually a separate authorized test, not to make an older uncertain action look resolved.

## Capture protocol

1. Use the real Martian console or released Martian local UI, synthetic data, a genuine customer role and the supported product viewport. The current registry convention is **1440 × 1000** for application captures; recheck the validator before changing that standard.
2. Navigate normally, inspect the fresh UI snapshot and use actual labels. Scroll/focus is allowed; changing DOM text, styling, counters, backend responses or feature flags to invent a screen is not. Correct a bad locator rather than blaming the product without evidence.
3. Wait for the actual state, fonts and image decoding. A lazy image's first blank screenshot is a timing observation; retain the failed check, then capture the settled actual image. A manual website login succeeding does not qualify the native browser executor.
4. Close once-shown secret disclosures. Exclude credentials, invitations, authorization headers, cookies and customer data. Native privacy masks, when truly needed for unrelated background names, must be disclosed and cannot hide the state being qualified. Prefer naturally safe views.
5. Save the direct capture privately first. View every proposed published image at readable size and inspect text/metadata. Do not publish a low-contrast payload screenshot just because its JSON exists; use another truthful, readable view and record the UI defect.
6. Inspect PNG integrity, dimensions, SHA-256 and metadata; copy only the reviewed asset into `public/media/screenshots/`. The helper's successful byte check does not set `reviewedForSecrets` or establish authenticity.
7. Register it in `quality/screenshots.json`, reference it through `<Screenshot id="..." />`, and include that ID in the guide's `screenshots` array. Preserve existing required IDs during evidence completion. If intentionally recapturing changed UI, record the new revision/hash and retain the prior evidence in history.
8. Verify caption, alt text, full-size link, actual deployed bytes and placement beside the corresponding action. A full-size popup must show the expected native dimensions.

Representative registry entry (values must come from the actual capture):

```json
{
  "id": "guide-action-result",
  "file": "guide-action-result.png",
  "alt": "What this actual screen shows",
  "caption": "Action, expected result and scope",
  "width": 1440,
  "height": 1000,
  "guideSteps": ["guide/id: named step"],
  "environment": "Named synthetic QA scope",
  "role": "Actual customer role",
  "capturedAt": "ACTUAL_ISO_TIMESTAMP",
  "sourceRevisions": {"frontend": "ACTUAL_COMMIT", "backend": "ACTUAL_COMMIT"},
  "sourceMatchesDeployment": "What was matched and any patch/parity boundary",
  "validationStatus": "Actual workflow, reload, response/error and privacy review",
  "reviewedForSecrets": true,
  "sha256": "ACTUAL_FILE_SHA256"
}
```

This is a schema illustration, not a captured record. Keep relevant SDK/Agents/Evals/patch revisions when they affected the result. Do not insert invented fields or placeholders into the real registry.

## Interpret assessment evidence correctly

| Observation | It establishes |
| --- | --- |
| Catalogue entry/selected technique | Requested scope or available content, not executed coverage |
| Completed execution | Bounded work ended; not a security pass |
| Model critic/narrative | Interpretation or hypothesis; it can disagree with structured independent receipts |
| Target says it acted | A reply, not an independently observed business-state change |
| Before-only ready baseline | Prerequisites, not an after-state/outcome verdict |
| Independent before/after violation | A scoped observed effect; not automatically clean reproduction |
| Required clean repetitions plus executed passing control | The recorded reproduction boundary, for those requests/baselines/evidence |
| Skipped control after negative repeats | A skipped control, never a passed one |
| Review published or download restored | Saved evidence became available; no new execution or improved verdict |
| Reply consistency | Text behavior; it cannot supply missing state evidence for a payment/permission objective |

For clean business reproduction, compare distinct observed epochs, the same seed and equivalent baselines, independent positive before/after reads, actual replay messages and the executed benign/no-implant control. The normal profiles previously required two repetitions/two successes; the actual admitted profile remains authoritative. Do not reduce the threshold or select an unrelated oracle to obtain a screenshot.

A chat benign control and a prepared-scenario no-implant attribution test answer different questions. A generic verification message may differ from the original request; say so. Exact replay requires a reviewed exact message from its sealed, attributed one-turn source. Recipe approval does not execute it, approve a release policy, or authorize deployment. A global unattributed Backend finding cannot be retrofitted with guessed source attribution.

**Quantified impact is narrower than reproduction.** Count-based duplicate-refund checks can reproduce a business violation while the dollar-sample summary stays unavailable. Its zero qualifying monetary samples need not mean zero successful verification repetitions. Never turn a synthetic observed sample into a production loss ceiling, incident probability, forecast or measured Call Gate savings.

## Saved review and exports

Read execution, verdict, review delivery, source coverage and Native telemetry delivery separately. A frozen revision may retain its original coverage label after live delivery advances. Reports JSON, legacy trace JSON, domain outcomes and redacted review ZIPs have different content and pagination; do not call them interchangeable complete evidence.

Modern artifact-backed verification rows intentionally can retain verdict metadata with an empty display body. Full verification fields can belong to the canonical finding; legacy labeled verification panels are another interface. Write instructions for the actual mode tested. A product payload panel with poor contrast is a separate defect, not a reason to fabricate readable UI in its screenshot.

For a real review ZIP, verify more than HTTP 200/content type or a `PK` prefix:

- Complete body/end directory, readable archive and CRC for every entry.
- Exact selected revision and manifest digest; correct organization, campaign and export scope.
- Expected complete entry set, every declared part's byte count and SHA-256, and parseable JSON.
- Retained revision and content after real UI refresh; test the actual browser download as well as a direct authenticated read when qualifying the download journey.

Keep redacted exports private unless explicitly selected and reviewed for publication. A partial stream or timeout is not a valid archive. Reading the same immutable export again is not a model/target retry, but it does not erase the earlier failed download. Preserve that distinction in the record.

## Other important boundaries

- Actual Viewer denial, foreign-organization isolation and anonymous denial need genuine identities/requests. Never relabel a platform administrator as a customer Owner because a role string looks similar.
- Dataset draft authoring, publication, read-only Martian sources, editable copies and immutable versions have different permissions and behavior. Reopening and native readback matter.
- Saved-output scoring, suites, reviews and comparisons are distinct from running the target again. Record canonical verdicts versus supplementary feedback, policy/version compatibility, paired/unpaired records and filtered export scope.
- Discovery inventory, observed runtime reports, cooperative SDK Call Gate, one-shot capture, continuous sensors and network containment previews are different workflows. Report attribution/omission counts, degraded state and unknown kernel loss; successful delivery or a stopped sensor is not complete network capture or enforcement.
- Actual revoke/acknowledgment/expiry behavior is separate from configured enrollment. Provider resource disappearance from an ordinary list is not independent proof of deletion.
- Record failed HTTP responses, actual page exceptions, console errors and expected navigation aborts separately. React profiler `TIMESTAMP` output is not by itself a console error. Do not claim zero network failures if navigation-aborted requests were observed.
