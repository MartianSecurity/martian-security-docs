# Limits, usage and data

> The Scanner's limits, where owners and admins read their organization's usage, and what is stored of scanned content and for how long.

Source: [Web version](https://docs.martiansecurity.ai/scanner/limits-and-data/)

> **Page qualification:** Current beta console · owner or admin (usage, retention, deletion); any member (limits) · Walkthrough verification in progress. [Verification details](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md).

> **Walkthrough limits:** Written from the source at the commits listed, for the beta release that turns the Scanner on (MartianSecurity/martian-notes#527). Not yet walked through against the hosted beta console, and no screenshot is captured; the feature branches that add bundle retention, usage and the self-hosted chart (MartianSecurity/martian-notes#521 to #525) were not on main when it was written.

Guide in progress

This workflow has been reviewed against the implementation. A complete live walkthrough is still in progress.

## Limits

Martian sets your organization’s Scanner limits when it turns the Scanner on:

| Limit | Default | When it is reached |
| --- | --- | --- |
| Scans a day | 200 | An upload, a CI scan or a GitHub App scan is refused (`429`) with the limit named, and the GitHub App’s check is neutral |
| Largest upload | 50 MiB | The upload is refused (`413`) with the limit |
| Files in one upload | 5,000 entries, 10 MiB per file, 200 MiB unpacked | The upload is refused with the limit |
| Model analysis requests in one scan | 24 | The scan’s later passes are listed as not run |
| Repositories for the GitHub App | 10 | Repositories over it get a neutral check |

An organization may also start at most 30 scans a minute, and an API key 10 a minute and 500 a day.

## Usage

Owners and admins see what the organization’s scanning used over the last 30 days under **Scanner → Settings → Usage**: scans by state, scans today against the daily limit, files read, references resolved and not attempted, model calls and tokens, and the bundles stored. Every figure is counted from the scans themselves.

## How long uploaded files are kept

| What is stored | How long |
| --- | --- |
| The uploaded or fetched archive (the bundle) | Your organization’s retention after its newest scan: 30 days unless an owner or admin changes it under **Scanner → Settings → Uploaded files** (1 to 3,650 days) |
| Each scan’s record: the file list with each file’s hash, the coverage, the references and what the registries answered | While the organization exists |
| Findings, each with an excerpt of at most 1,000 characters of the line a rule matched | While the organization exists. They are what gates, approvals and triage were decided on |
| Pages, files and repositories the Scanner fetched | Not stored. They are hashed, and the scan’s working folder is removed when it ends |

-   When a bundle’s retention ends it is deleted from storage; the scan and its findings stay. The same files can be scanned again by uploading them again.
-   An owner or admin deletes a scan’s stored files at once from the scan’s page (**Delete the stored files**). Every scan of the same files shares them. The deletion is in the audit log.
-   A legal hold on the organization stops every deletion while it holds.
-   Deleting the organization deletes its stored files and its Scanner records. Its audit log is kept.

## Next

-   [What the Scanner checks](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/overview.md)
-   [Self-hosted](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/self-hosted.md)
