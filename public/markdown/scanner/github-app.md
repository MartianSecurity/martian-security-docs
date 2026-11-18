# Scan pull requests with the GitHub App

> Connect the Martian Scanner GitHub App so every pull request and push to the default branch is scanned, with a check and one comment.

Source: [Web version](https://docs.martiansecurity.ai/scanner/github-app/)

> **Page qualification:** Current beta console · owner or admin; GitHub account admin · Walkthrough verification in progress. [Verification details](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md).

> **Walkthrough limits:** Written from the source at the commits listed, for the beta release that turns the Scanner on (MartianSecurity/martian-notes#527). Not yet walked through against the hosted beta console, and no screenshot is captured; the feature branches that add bundle retention, usage and the self-hosted chart (MartianSecurity/martian-notes#521 to #525) were not on main when it was written.

Guide in progress

This workflow has been reviewed against the implementation. A complete live walkthrough is still in progress.

The GitHub App scans pull requests and repositories on Martian’s side. It reads a pull request’s files with a token made for that one job, so no customer secret is in the pipeline, and pull requests from forks are scanned too.

## Before you start

-   Martian has turned on the Scanner and its GitHub App for your organization, with the number of repositories it may scan.
-   You are an owner or admin of the organization, and you can install apps on the GitHub account.

## Connect GitHub

1.  In the sidebar, open **Scanner → Integrations**.
2.  Select **Connect GitHub**. GitHub opens its install page for the Martian Scanner app.
3.  Choose the account and the repositories, and install. GitHub returns you to **Scanner → Integrations**, which connects the installation to your organization.
4.  Turn on each repository to scan, and set the folders to send (`.` for all) and how many hours after its last scan the default branch is scanned again without a push.

An installation made straight from GitHub, without **Connect GitHub**, is never connected to an organization and scans nothing.

## What happens on a pull request

-   The App posts a **Martian Scanner** check on the head commit. A pull request that changes no agent file passes without a scan.
-   The gate file `.martian/scan.yml` is read from the **base** commit, so a pull request cannot weaken its own gate ([the gate file](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/cli-and-ci.md#the-gate-file-martianscanyml)).
-   The repository’s agent files are scanned, not only the changed ones, so a file a changed one points at is scanned with it.
-   The check passes or fails with the gate’s reasons, a link to the scan and an annotation at each blocking finding. One comment on the pull request is edited on every later commit.
-   An organization over its limits, or without the App turned on, gets a neutral check that says why. It never blocks a merge.

A push to the default branch is scanned too, and that scan is the baseline later pull requests are compared with when `new_findings_only` is set.

## Disconnect

On **Scanner → Integrations**, disconnect the installation. Its repositories stop being scanned. Uninstalling the app on GitHub is yours to do.

## Next

-   [Limits, usage and data](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/limits-and-data.md)
