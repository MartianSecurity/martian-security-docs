# Scan in the console

> Upload a folder, read the result by category, finding and evidence, and triage, approve and monitor what you scanned.

Source: [Web version](https://docs.martiansecurity.ai/scanner/console/)

> **Page qualification:** Current beta console · owner, admin or member (start); any member (read); owner or admin (triage, approve, delete stored files) · Walkthrough verification in progress. [Verification details](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md).

> **Walkthrough limits:** Written from the source at the commits listed, for the beta release that turns the Scanner on (MartianSecurity/martian-notes#527). Not yet walked through against the hosted beta console, and no screenshot is captured; the feature branches that add bundle retention, usage and the self-hosted chart (MartianSecurity/martian-notes#521 to #525) were not on main when it was written.

Guide in progress

This workflow has been reviewed against the implementation. A complete live walkthrough is still in progress.

Scan a skill, an MCP configuration, a plugin or a repository from the console and read what the Scanner found.

## Before you start

-   Your organization has the Scanner turned on ([who has it](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/overview.md#who-has-it)). Without it the **Scanner** group is not in the sidebar.
-   You are an owner, admin or member to start a scan; any member reads scans.
-   Have the folder ready, or a ZIP of it of at most 50 MiB (your organization’s limit may be lower).

## Start a scan

1.  In the sidebar, open **Scanner → New scan**.
2.  Under **Type**, choose what you are scanning: a skill, an MCP server, a plugin, a sub-agent, harness configuration, agent code or a repository.
3.  Under **Name**, give it a name. Scans of the same type and name belong to one add-on, so later scans are compared with earlier ones.
4.  Drop the folder or the ZIP file on the page, or choose it.
5.  Select **Start scan**. The result page follows the scan stage by stage.

A refused upload says why and names the limit it broke: the archive’s size, its number of files, or the organization’s scans for the day.

## Read the result

-   **Categories** shows each category as flagged, clear or not checked, with the stages a not-checked one is missing.
-   **Findings** lists each finding with its severity, evidence level, file and line. Select one to open the file with the cited lines marked.
-   **References** lists every link, package and repository the files point at, with what the registry answered, when, and when it is checked again.
-   **Coverage** lists the files that were skipped or not inspected and why.
-   **Download JSON** and **Download SARIF** export the scan.

## Triage, approve and monitor

1.  **Findings** across scans: an owner or admin accepts a finding (with a reason and an end date), waives it, or reopens it. Each action is in the audit log.
2.  **Policy** sets the severity of a rule for your organization, and the notifications for new findings, drift and voided approvals.
3.  **Add-ons** shows each add-on’s latest scan. An owner or admin **approves** the content digest of a completed scan. When the add-on’s content or what it points at changes, the approval is void and the add-on shows **changed since approval**.
4.  Add-ons from a registry are fetched again weekly, and what they point at is re-checked daily.

## Delete the stored files

The uploaded archive is kept for your organization’s retention period after its newest scan ([limits and data](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/limits-and-data.md#how-long-uploaded-files-are-kept)). An owner or admin can delete it sooner: open the scan, and under **This scan** select **Delete the stored files**. The scan and its findings stay.

## Next

-   [Scan from the command line and CI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/cli-and-ci.md)
-   [The GitHub App](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/github-app.md)
