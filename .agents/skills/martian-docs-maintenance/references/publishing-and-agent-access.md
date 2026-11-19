# Build, agent exports and GitHub Pages

## Source and build contract

Read the current package scripts and workflow. This repo uses **npm and its committed lockfile**. Use the configured Node version. Install dependencies through the package manager when needed; preserve lockfiles and reviewed SHA-pinned Actions. Do not update dependencies merely to maintain a local skill.

For a guide, rendered component, qualification record or site-URL change:

```sh
npm ci
npm run docs:sync
npm run build
npm run check
git diff --check
```

Skip reinstalling unchanged dependencies when already prepared. Keep dependent steps sequential. Run `npm run check:release` when auditing completion and before declaring full end-to-end qualification. For a skill-only or agent-instruction-only edit, use the repo's narrower changed-path/link/skill checks; no paid or hosted run is needed.

`docs:sync` rebuilds rendered articles and updates committed `public/markdown/`, `llms.txt`, `llms-full.txt` and `robots.txt`. `build` generates output but rejects stale committed agent exports. Include all generated changes belonging to the edit. Do not hand-edit derived Markdown or repair a mismatch by weakening the exporter/checker. Inspect removed stale assets and links when a guide is renamed.

Use the existing checks for links/anchors/assets, qualifications, examples, exact code payloads, source notices, captions, secure links and Mermaid. Do not add repetitive tests for prose. Rerun passed suites when subsequent changes affect their inputs, not as a substitute for finishing publication.

## Local browser acceptance

Serve the production build with the existing preview command on a known free port. If the installed CLI supports an independent-preview/lock option, verify its help and use it; do not kill another preview to obtain the default port. Record your own process/session and stop only that process after qualification.

For affected routes, use real browser controls to check:

1. Desktop/light and narrow/dark layout, readable text/callouts/tables/code, decoded images and no document-wide overflow. Add minimum-width/keyboard focus checks when a shared component changes.
2. Code Copy equals the original executable payload byte-for-byte, including indentation, quotes and literal fences. Line wrapping, terminal prompts or comment removal must not silently change it. Check keyboard access and visible success/error feedback for copy-control changes.
3. Copy page equals the generated full Markdown, including audience context, product limits, verification link, screenshots and exact code. Check the actual agent-link action and raw destination when changing sharing behavior.
4. Full-size images open the expected native dimensions and actual asset; screenshots are individually viewed.
5. Real search input finds a new meaningful phrase, result navigation works and a nested guide survives full refresh.
6. Browser page errors, failed HTTP responses, failed requests and unexpected console errors are inspected. Retain the original failure if a later focused check passes.

Do not use an automated search locator failure as proof the site search is broken. Inspect the current dialog, actual result/anchor and existing UI before changing product code or tests.

## Agent-ready contract

The site is static HTML with public no-login/no-JavaScript Markdown alternatives, per-page discovery links, an agent index, and the complete reference. Inspect `PageActions.astro`, `src/lib/agent-links.mjs`, the exporter and its tests before changing it.

Current behavior learned from source:

- Human actions: **Copy page**, **More page actions → Copy agent link**, **View Markdown** and **Agent index**.
- Conversion starts from rendered HTML. It preserves audience context and the verification link, exact executable code, original Mermaid source, captions and secure public asset and guide links.
- Exported discovery and mirror URLs receive content-digest cache-busting queries. Preserve those queries; version/release notices are not the cache key.
- Clipboard preload and a synchronous fallback preserve user activation on HTTP local previews. Replacing it with an untested async-only Clipboard API call can break local copying.
- Custom-domain HTML/TLS works in ordinary clients while an individual external agent fetcher can still fail or serve cached raw-main text. Test the actual reader when possible; compare exact current bytes, try the supported raw mirror, and use an immutable commit URL to establish which revision was read. A tool internal error is not proof of an origin outage, and mirror success is not proof every agent can fetch canonical HTML.

Test both human and agent representations after changing shared layout. Check the evidence on the verification page and in `quality/`.

## Publication and concrete review

Use the current user's actual authorization. Local skill creation does not authorize a docs publication. When publication is requested or already authorized:

1. Inspect a clean intended change set, preserve unrelated work and record the reviewed head/tree and affected file hashes. Commit only task files. Do not include support plans, raw QA exports or private logs.
2. Push a ready-for-review PR. Address actual findings, verify required checks and inspect current review threads. Report honestly if there was only self-review and no external review submission.
3. Merge only the reviewed head using the GitHub tool's expected-head option or CLI equivalent when the connector cannot provide it. Do not bypass required CI or override a failing gate to finish docs.
4. Verify the actual main-branch workflow's build **and deploy** jobs and the GitHub Pages environment. A connector that lists only PR runs may need a narrow GitHub CLI fallback for main Pages runs. A PR's skipped deploy job is expected, not publication.
5. Verify merged content/tree and source synchronization; inspect actual public pages/assets/Markdown/downloads over trusted HTTPS. Compare public bytes to the reviewed built files, not just a status code.
6. Repeat the relevant browser acceptance against production. Check real nested refresh, search, full-size images, page/code copying and both themes/layouts.
7. Report public URL, repository/PR or commit, guide coverage, exact validation and remaining gaps. Publication can be complete while the overall qualification goal is incomplete.

Private-repo Actions billing failures can prevent jobs from starting while the public docs workflow works. A failure with zero executed steps is not a product-test failure and not a reason to rerun paid QA. Do not silently waive required checks. An approved private Backend PR merge is still conditional on those checks; successful docs Pages publication does not authorize beta deployment.

## Domains and HTTPS

Use `site.config.mjs` as the single origin/base source. A custom-domain site uses its actual root base; a project Pages URL may require a project base. Never globally remove prefixes based on one local screenshot. Check assets, Markdown, search, diagrams, downloads, sibling links and deep routes after any change.

Read current GitHub Pages settings, DNS and redirects when a domain task requires them. Historical registrar/CNAME/certificate notes can drift. Trusted HTTPS must pass without `--insecure`; expired local Python CA bundles and actual certificate errors are different problems. Prefer a client with a working trusted system CA store, and fix the trust setup rather than disabling verification.

The earlier organization transfer left some legacy website URLs unavailable while raw GitHub aliases still worked. Recheck before making claims, and use canonical current links. Do not recreate domains/repos or change DNS without the appropriate task authorization.

## Helper commands and meaning

Run `scripts/docs_maintenance.py --help` from the skill directory. Examples:

```sh
python3 scripts/docs_maintenance.py audit --repo /path/to/docs --baseline-ref REVIEWED_BASE
python3 scripts/docs_maintenance.py inspect-png /path/to/direct-capture.png
python3 scripts/docs_maintenance.py verify-published --repo /path/to/docs --site https://docs.martiansecurity.ai --path /assessments/reproduction-and-limits/ --path /markdown/assessments/reproduction-and-limits.md --path /llms.txt
```

`audit` exits nonzero for invalid/missing registered captures or a requested preservation comparison that detects changed/removed original requirements or capture records. Intentional recaptures/feature changes require reviewing the diff; the helper does not authorize a rollback or freeze the guide's old contract forever. Partial guides are reported, not silently promoted.

`inspect-png` checks CRC/dimensions and reports metadata chunk names without exposing their payload. It flags text/EXIF metadata for review. It cannot validate the depicted state, screenshot provenance, privacy or readability.

`verify-published` defaults to `repo/dist`. Supply `--expected-root repo/public` only for a deliberate check of tracked static files, which does not establish HTML/build correctness. Paths are site-relative and must remain within the expected directory. HTTPS and redirect trust remain enforced; curl configuration files are disabled so they cannot inject credentials or weaken the request. A payload mismatch or fetch failure fails the check. The helper performs only GETs and local reads, with an optional exclusive private JSON report; it does not run npm, commit, deploy, mutate a backend or decide that a whole site is usable.
