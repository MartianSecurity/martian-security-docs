# The Scanner in a self-hosted installation

> What the Scanner does in an Enterprise installation in your own cluster, with outside lookups off by default, an allow-list or proxy, an imported advisory database and your own model endpoint.

Source: [Web version](https://docs.martiansecurity.ai/scanner/self-hosted/)

Current beta console · Security engineer of a self-hosted Enterprise installation · [Verification details](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md)

A self-hosted Enterprise installation runs the Scanner’s worker in your own cluster, next to the console and the backend. Your licence decides whether the installation has the Scanner, and your installation’s master admin turns it on for each organization.

## What differs from the hosted console

|  | Hosted Enterprise | Self-hosted Enterprise |
| --- | --- | --- |
| Outside lookups (registries, OSV, the addresses the files name) | On | **Off by default.** Every reference is reported as not attempted, its categories as not checked, and a gate that requires references to be followed fails |
| Limiting lookups | — | An allow-list of hosts, a proxy of yours (only with an allow-list), or both |
| Known vulnerabilities in packages | Asked of OSV | From OSV, or from an **imported advisory database** you build from OSV’s exports, which needs no outside route |
| Model analysis | Martian’s engine | **Your own OpenAI-compatible model endpoint**, if you name one. Without one, model analysis does not run, each scan says so, and findings reach at most evidence level 3 (resolved) |
| Where uploaded files are kept | Martian’s storage | A volume in your cluster or a bucket of yours |

A self-hosted installation has no sandbox, so the Scanner never runs an add-on there.

## Turn lookups on, or keep them limited

Your administrator sets these when installing:

-   **Lookups on.** The worker gets one way out: public addresses on ports 80 and 443, with every private, internal and cloud metadata address excluded.
-   **An allow-list.** Only the listed hosts are asked, for example `pypi.org`, `.npmjs.org` and `api.github.com`; a reference to any other host is reported as not attempted, naming the host.
-   **A proxy.** Requests go through your proxy, which must refuse internal addresses. The worker uses a proxy only together with an allow-list.

## Check packages with no outside route

Build an advisory database where there is internet, and give it to the installation:

```bash
martian-scanner advisory-db build --out advisories.db PyPI-all.zip npm-all.zip
```

`PyPI-all.zip` and `npm-all.zip` are OSV’s exports (`https://osv-vulnerabilities.storage.googleapis.com/PyPI/all.zip` and `.../npm/all.zip`). The `martian-scanner` command is in the Scanner’s worker image your administrator installed. Each finding from the database names it, when it was built and the exports it came from, so you can see how old the knowledge is. Build it again to refresh it.

## Next

-   [What the Scanner checks](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/overview.md)
-   [Limits, usage and data](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/scanner/limits-and-data.md)
