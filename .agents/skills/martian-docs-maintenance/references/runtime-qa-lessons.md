# Runtime QA and recovery lessons

Use this reference only when a documentation task actually requires new runtime qualification or diagnosis. Do not launch a stack, request AWS login, invoke models, reset worlds or run a recovery procedure merely to verify prose.

## Scope, identity and prerequisites

- Check the real application readiness, identity and tenant before a bounded run. A genuine non-platform-admin Owner, Member and Viewer exercise different boundaries. Existing authentication in one Backend is not proof it works in another QA Backend.
- Use actual source/runtime revisions. A source archive can be pinned, a container can include a narrow backport, and UI/backend dependencies can differ. Verify relevant served/container files when consequential; describe exact matched files and the baseline guard retained. Never label this full-main or hosted parity.
- Interfaces and identity modes are independent: HTTP, MCP and native browser; endpoint-only and sandbox-backed; anonymous, configured website access and a synthetic signed-in fixture. A website account is not an independently attested customer identity. A fixture rejecting `test_identity` does not qualify synthetic sign-in.
- A scenario/assurance catalogue returning 503 or a workspace without a compatible source does not qualify a prepared scenario. Do not fake a catalogue, downgrade a required fixture or claim selecting a pack executed it. Continue other authorized work and state the actual missing prerequisite.
- Model/API spending authorization applies to its actual session/scope. Prior unlimited spending for bounded synthetic QA is historical context, not a reusable grant for every future skill invocation. Ask only for genuinely missing authorization, not something already provided.

## Authentication and local infrastructure

Check a fresh identity/readiness request before diagnosing a model run. AWS login/exported credentials can expire independently of a Chrome session. Verify the actual profile, model permission and expiration; successful GitHub login does not restore Bedrock. Do not print keys or token-bearing sign-in URLs into docs/skills.

If an AWS refresh is needed and the user must perform the interactive sign-in, ask once, keep that request pending and continue independent work. After the user says done, verify identity before starting. Do not repeatedly replace a pending request or reopen duplicate sign-in tabs. A stale temporary authorization URL is not reusable.

Docker Desktop, an isolated Lima daemon and Kubernetes are separate surfaces. Inspect the actual Docker context/socket, compose project, network namespace, image and mount ownership. A VM loopback port may require a dedicated host forward. A failed Docker command or inaccessible UI does not authorize factory reset, deletion of containers/volumes, daemon restart or termination of shared forwards. Ask for the necessary user unlock/restore action if that is the real blocker.

Record your own preview/browser/tunnel/forward processes and verify command, start identity and working directory before stopping them. Preserve other sessions and shared services. Avoid process-wide kill patterns and cleanup of unknown worlds/volumes. Keep read-only credential refresh separate from automatic target/model work.

## Temporary transport failures

Quick Tunnel URLs can expire or return NXDOMAIN/530 while an old metrics value still reports a connection. Verify actual public DNS/trusted HTTPS health and the target's real protocol. Preserve the original failed run and action identities.

When rotating a transport within an approved QA scope:

1. Prove the relevant campaign/actions are terminal or otherwise safely quiescent; inspect outstanding usage, leases and action journals.
2. Rotate only the owned process. A metrics-port collision can kill a new tunnel; inspect its exact log and health before using its URL.
3. Reconcile every affected origin: Backend public origin, seed-download origin, Native telemetry origin, callback/management base and the actual target endpoint may be configured separately. One working health URL does not prove all clients use it.
4. Active connection endpoints can be immutable. Use supported registration/revision/binding/validation/approval for a genuinely new connection rather than editing DB endpoints or silently changing the tested target artifact.
5. Recreate only the necessary owned service on the same qualified image when a configuration change requires it, preserving mounts/custody. Inspect startup replay semantics before a restart.

Do not change trust requirements or allow arbitrary HTTP to get past an HTTPS contract. A host Python CA problem can coexist with successful trusted system curl/browser checks.

## Sandboxes, seeds and action certainty

A visible seed/account catalogue is not proof that a launched instance loaded it. Use the published document/seed selected for the tutorial, actual launch/readback, relevant seeded sign-in and world readiness. Shared and personal generation, a ready story and a ready projected dataset are distinct states. One saved schema/import should not accidentally trigger generation or relaunch.

For world-state objectives, verify starting prerequisites before admission. A successful probe mutates its world: another run can correctly fail preflight on that state. A supported reset of an owned completed world can restore a baseline; it is not a release of usage or quota. Record new epochs and equivalent baselines. Check live ownership/terminal action receipts first. Never reset an active/uncertain world to manufacture clean reproduction.

Expired/deleted sandbox state, a tenant CPU limit and review-storage capacity are different blockers. Do not raise quotas, delete unrelated instances or free protected reservations to get a new run admitted. A failed preflight can retain its own reservation; no Native execution does not automatically authorize manual release.

HTTP 202 can acknowledge work whose observation times out; query the original request before retrying. Persist original request/intent IDs and exclusive mutation guards privately, with redacted outputs. Distinguish `started`, `completed`, `uncertain` and actual idempotent replay semantics. An unknown target action or provider usage stays unknown and conservatively accounted until a supported, evidenced resolution exists.

## Review-only recovery

Recovery is product behavior. Read the owning repo's current instructions, existing implementation/runbook and the user's concrete authorization. Do not add fallback logic, alter frozen identities, deploy a private product patch or commit it under docs publication approval. Make a separate concrete issue/ready PR when authorized. Existing approval for a named fix should not be requested again within that scope, but does not authorize an unrelated repair or beta deployment.

Lessons from the actual review pipeline:

- Completed execution, Native telemetry completion, source capture, review publication and reservation cleanup advance independently. Inspect the correct authoritative record; do not rerun the model to repair an export.
- Frozen files have immutable campaign, policy, binding, source, manifest, descriptor, byte-count and SHA identities. An installed redaction-ruleset upgrade is not permission to rewrite the original policy fingerprint. Authenticate the original frozen contract.
- A reconcile response's HTTP 200 is not proof it inspected or advanced anything. Inspect the actual state, receipt and persisted parts. A fresh matching provider read does not establish why an earlier conflict occurred.
- Existing guarded frozen-export replay must verify scope, completed/frozen state, no open observations, exact canonical spool digest, actor authorization and exclusive writer custody. It is not a target/model retry. Read the shipped procedure before using it; this reference is not authorization to invoke it.
- A narrowly scoped, attributed reinspection can acknowledge already-present matching bytes. Confirmed absence and a new uncertain-write reissue are separate decisions. Do not combine recovery flags, infer absence from an ambiguous read, blindly repeat provider writes or let a stale worker release a replacement owner's lease.
- A replay grant is time-bound and exact-spool scoped; a loss acknowledgment waives missing evidence and is not verified publication. Never use the latter to fill a screenshot or call an export complete.
- Normal verified publication/cleanup can release only its own expected review reservation. Retain earlier failed/unknown reservations and compare original execution/budget/action records before and after. A startup discovery pass can encounter other spools; verify its guards before restarting.
- Native summary `attempts` may be an integer; the full checkpoint has the interaction/verification arrays. Use the actual schema instead of iterating a summary as a full proof. Inspect `target_response`, candidate message and action metadata, not guessed key names.

Stop on unknown outcomes or changed custody. Capture a non-secret, concrete blocker and continue independent docs work. Do not issue repeated sign-in requests for a billing, catalogue, policy, capacity or product-contract problem.

## Keep customer and operator instructions separate

Public guides describe supported customer controls and tell readers when an operator is needed. Private actor identities, workload keys, native spool paths, SQL queries, replay grants, deployment inventories and credential-forwarding details stay in private operational evidence/runbooks. A recovery verified only with operator assistance must not be marketed as customer self-service.
