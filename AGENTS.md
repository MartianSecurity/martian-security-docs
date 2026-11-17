# Martian Security customer documentation

`AGENTS.md` and `.agents/skills/` are canonical. `CLAUDE.md` and `.claude/skills` are relative symlinks; edit the originals.

Implementation follows `PLAN_MARTIAN_SECURITY_DOCS.md` in the project vault and the current coverage matrix in quality/. Keep customer task guides accurate against the recorded product source revisions and observed real application behavior.

- Use the existing Hermes Astro/Starlight branding and native navigation/search/themes.
- Configure the Pages base only through site.config.mjs. Preserve strict local-link and sensitive-content checks.
- Every task guide needs its role/prerequisites, exact numbered UI steps, real relevant screenshots, expected results, failure/recovery limits and next links.
- Capture actual application states against a real backend. Do not fabricate screenshots, alter the DOM to invent features or intercept the behavior being verified.
- Customer screenshots must show Martian Security. Keep backend dependency UIs, including MLflow, out of published guides. Use copyable terminal output for local SDK workflows and distinguish it from recorded console runs.
- Never commit credentials, cookies, customer data, private deployment inventories or once-shown API tokens. Use synthetic fixtures and keep private evidence outside this repository.
- Update quality/coverage.json, quality/screenshots.json and quality/validation.json with honest provenance. Pending qualification is not complete.
- Run npm run build and npm run check. Run npm run check:release before declaring the end-to-end task complete.
- Actions remain SHA-pinned. PRs are ready for review. Product runtime changes belong in separate repositories.
- Guide, component, qualification or site-URL changes require `npm run docs:sync`; include its generated `public/markdown/`, `public/llms.txt`, `public/llms-full.txt` and `public/robots.txt` changes, then run the normal build/checks. Editing only this instruction file requires changed-path/link review and `git diff --check`.
- Preserve unrelated work and check the actual source revision. Do not commit, push, publish or deploy beyond the user's authorization. Existing qualification evidence applies only to the behavior and revision it actually exercised; list stale or missing evidence instead of promoting it to complete.
