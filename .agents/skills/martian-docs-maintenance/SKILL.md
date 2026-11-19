---
name: martian-docs-maintenance
description: Maintain Martian Security's customer documentation repository, Hermes-based design, real walkthroughs and screenshots, agent-readable exports, and GitHub Pages publication. Use for changes or audits of martian-security-docs and docs.martiansecurity.ai. Product runtime fixes and SDK releases remain separate work with their own authorization.
---

# Martian Docs Maintenance

Maintain an accurate, usable customer site whose published behavior and qualification claims match the evidence. This skill captures the decisions and failure modes learned while building the site; it grants no deployment, spending, recovery or product-change permission.

## Start from the owning source

Locate the actual `martian-security-docs` checkout; inspect its branch, working-tree state and relevant remote ref. Read its `AGENTS.md`, `README.md`, `package.json`, `site.config.mjs`, workflow and affected `quality/` records. Repository `.agents/skills/` is canonical; `.claude/skills` is an alias, not a second copy to maintain.

Use current task instructions and existing session authorization. Proceed within already authorized scope without asking again. Historical approvals, local credentials, an old successful run and this skill are not new authorization. Preserve unrelated work; use an isolated worktree when needed. Never repair dirty checkouts with a reset or broad cleanup.

Treat content, source review, executable examples, real application qualification and public deployment as distinct evidence. Do not reuse old counts, release versions, cloud sessions or availability claims without checking their owning source. [Verification history](references/verification-history.md) illustrates why this matters; it is dated evidence, not a current checklist result.

## Choose the needed reference

| Work | Read |
| --- | --- |
| Guide edits, design, ownership and quality-file updates | [Repo and standards](references/repo-and-standards.md) |
| Real walkthroughs, screenshots, evidence interpretation or archive checks | [Qualification and screenshots](references/qualification-and-screenshots.md) |
| Commands, generated Markdown, copying, local checks or Pages deployment | [Publishing and agent access](references/publishing-and-agent-access.md) |
| Authentication, QA services, transports, sandboxes or recovery blockers | [Runtime QA lessons](references/runtime-qa-lessons.md) |
| SDK/CI examples, local UI, migrations, attacks or framework coverage | [SDK and attack library](references/sdk-and-attack-library.md) |

Read only the relevant references. Ordinary prose, design and skill edits do not require AWS, a running product stack, paid models or a deployment.

## Essential workflow

1. Establish the customer task and change scope. Inspect the implementation that owns its UI labels, API contract, roles and release availability. Fetch current library documentation through Context7 when library behavior is needed; use primary sources for SDK/framework facts. Record exact source revisions and material uncertainty.
2. Make the smallest complete change. Preserve the Hermes foundation, logo-only navbar, readable callouts and copyable code. Keep normal SDK installation evergreen, retaining versions where compatibility or historical evidence needs them. Keep audience metadata and a verification link in agent exports. Record walkthrough status in the verification record.
3. Maintain the evidence contract. Task guides retain purpose, role/prerequisites, exact actions, relevant real screenshots, expected results, failure/recovery limits and next links. Update the affected coverage, screenshot, source and validation records together. Do not trim required stages, relabel pending checks, or replace a failed observation to obtain a pass. Legitimate workflow changes need an explicit, explained requirement diff.
4. Validate at the appropriate level. For guide/component/qualification/URL changes, use the repo's `docs:sync`, production build and normal checks. Inspect affected desktop/light and narrow/dark docs, copying, full-size images, search and nested refresh. Application journeys use the product's actual supported viewport and real backend. Skill-only changes need skill/helper validation, not model runs.
5. Publish only within the user's authorization. Use a ready PR, address findings, verify required CI and merge the reviewed head. Check the main Pages build/deploy and actual public bytes and browser behavior. A green PR build, successful push or correct local preview is not a public deployment.
6. Report what changed, exact checks and environment, the live URL/revision when published, and concrete remaining gaps. Call an AI-simulated novice review what it is; a human Mom Test needs a real participant. Update the existing project/skill note in the user's vault when applicable, following that vault's scoped commit/push rules.

`npm run check` permits incomplete walkthroughs recorded in the coverage matrix. `npm run check:release` audits full qualification. For incremental publication, record the scope that was verified and report remaining checks.

## Read-only helpers

The Python 3.11+ stdlib helper has no build, commit, push, merge, runtime, quota or recovery operation:

```sh
python3 scripts/docs_maintenance.py audit --repo /path/to/martian-security-docs
python3 scripts/docs_maintenance.py audit --repo /path/to/martian-security-docs --baseline-ref REVIEWED_BASE
python3 scripts/docs_maintenance.py inspect-png /path/to/capture.png
python3 scripts/docs_maintenance.py verify-published --repo /path/to/martian-security-docs --site https://docs.martiansecurity.ai --path / --path /reference/verification/ --path /llms.txt
```

Run these from this skill directory or use the script's absolute path. `audit` reports current counts and optional requirement/capture changes; existing repository validators remain authoritative. A baseline preservation failure requires review, not automatic rollback. `inspect-png` checks bytes, dimensions and metadata, not authenticity, readability or privacy. `verify-published` compares an explicitly supplied expected artifact with trusted HTTPS responses; it does not prove CI, browser usability or application behavior. See the publishing reference for options and failure semantics.

Keep credentials and raw private QA evidence outside the public repo and skill. Stop an ambiguous target/model mutation, inspect the original request/action and preserve its records before considering a new intent. Never clear unknown usage, protected reservations, containers or volumes to finish a screenshot.
