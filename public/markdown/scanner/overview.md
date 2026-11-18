# What the Scanner checks

> The Skills / MCP / Plugin Scanner reads the files you give an agent and reports what is wrong with them, at a stated level of evidence and with the coverage of each scan.

Source: [Web version](https://docs.martiansecurity.ai/scanner/overview/)

> **Page qualification:** Current beta console · Any member of an Enterprise organization with the Scanner · Walkthrough verification in progress. [Verification details](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md).

> **Walkthrough limits:** Written from the source at the commits listed, for the beta release that turns the Scanner on (MartianSecurity/martian-notes#527). Not yet walked through against the hosted beta console, and no screenshot is captured; the feature branches that add bundle retention, usage and the self-hosted chart (MartianSecurity/martian-notes#521 to #525) were not on main when it was written.

Guide in progress

This workflow has been reviewed against the implementation. A complete live walkthrough is still in progress.

The Skills / MCP / Plugin Scanner is the third part of Martian Protect. It reads the files an agent is given (skills, MCP server configurations, plugins, sub-agents, hooks, settings, rules files and the agent’s own code) and reports what is wrong with them, including the indirect case: a clean `SKILL.md` that tells the agent to read and follow a link or a file that is not safe.

The Scanner checks the files you give an agent. It does not replace [Red Team](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/first-assessment.md), which tests what the agent does. A Scanner finding never starts a Red Team run; you start one on purpose.

## Who has it

The Scanner is in the **Enterprise** edition, in the hosted beta console, and in a self-hosted Enterprise installation ([self-hosted](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/self-hosted.md)). It is not in the open-source Community edition. Within Enterprise it is turned on for each organization by Martian, with its limits ([limits and data](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/limits-and-data.md)); ask your Martian contact to turn it on. Then:

-   owners, admins and members start scans, and every member reads them;
-   owners and admins triage findings, approve add-ons and change the Scanner’s settings;
-   an admin issues API keys with `scan:run` and `scan:read` for the [command line and CI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/cli-and-ci.md).

## What a scan reads

You upload a folder as a ZIP file, name a package or skill in a registry, or let the [GitHub App](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/github-app.md) send a repository. Each scan is of one **content digest**: the SHA-256 over every file’s path and hash. The same files give the same digest, so an approval names exactly the content it approved.

The scan runs in stages. Each stage that ran is listed in the result, and each that did not is too:

| Stage | What it does |
| --- | --- |
| Unpack, inventory, parse | Reads every file, hashes it, and works out what each one is and which agent clients load it. A file it could not read is listed, never treated as clean |
| Rules | Pattern and structural rules: dangerous commands and downloads, hidden text, hooks and settings that run commands, permissions, MCP server configuration, and data flows in the agent’s own code |
| References and resolve | Every link, repository, package, domain, image and command the files point at, and what the registries say about each: a package nobody has published, a domain anyone can register, a repository whose owner was deleted, a version with a known vulnerability |
| Fetch and assess | What the add-on tells the agent to read or run, fetched and judged against what the add-on says it is for. A model may add a finding; it never clears one |

## Evidence levels

Every finding states how strong its evidence is. A clean result means no findings at the levels the scan reached, with its coverage, at that time.

| Level | Name | Means |
| --- | --- | --- |
| 0 | Inventory | The file exists and is loaded by these clients |
| 1 | Pattern | A rule matched the text |
| 2 | Structural | The parsed structure shows it (a hook that runs a command, an unpinned server) |
| 3 | Resolved | A registry or address answered (the package does not exist; the domain is unregistered) |
| 4 | Assessed | A model, citing the passage, judged it outside the add-on’s purpose, and two passes agreed |
| 5 | Observed | It was seen when the add-on ran in a sandbox |
| 6 | Corroborated | An independent source agrees. Only level 6 is called malicious |

A scan whose organization does not allow sending content to a model stops at level 3, and says so.

## Coverage

Each result shows every category as **flagged** (a finding is in it), **clear** (every stage it needs ran and nothing was found) or **not checked** (a stage it needs did not run, or did not cover everything). A reference the Scanner did not ask about is **not attempted**, never clean, and a category that depends on it is not checked.

## Next

-   [Scan in the console](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/console.md)
-   [Scan from the command line and CI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/cli-and-ci.md)
-   [The GitHub App](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/github-app.md)
-   [Limits, usage and data](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/limits-and-data.md)
