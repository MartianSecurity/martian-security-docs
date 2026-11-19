# Method and measured results

> How the Scanner finds direct and indirect issues, what each evidence level means, what it does not claim, and its measured precision and recall on its labelled corpus.

Source: [Web version](https://docs.martiansecurity.ai/scanner/method/)

Current beta console · Anyone evaluating or using the Scanner

This page says how the Skills / MCP / Plugin Scanner reaches each finding, what a finding at each evidence level may and may not mean, and how accurate it is on the corpus it is measured on. Every number here comes from the Scanner’s accuracy report for the release this page describes. A number from another corpus, or from a scan with fewer stages, can be very different.

## Direct issues: what the files themselves say

The Scanner reads every file of an add-on, not only `SKILL.md`: scripts, reference documents, MCP server configurations, plugin and marketplace manifests, hooks, settings, sub-agents, rules files, lockfiles and the agent’s own source code. Nothing it reads is run. Each file is parsed into the facts a client would act on (the commands a hook runs, the servers an MCP configuration starts, the tools a skill pre-approves, the agent a framework builds), each citing a file and a line.

Rules then look for what is wrong in the text and in those facts:

-   **Pattern rules** match text: a download piped to a shell, a read of `~/.aws/credentials`, an instruction that tells the agent to hide something. The rules for hidden instructions match the text as a model reads it, with invisible characters removed and look-alike letters folded.
-   **Structural rules** test the parsed facts: a hook that runs a command when a session starts, a setting that turns off approval, an MCP server that is not pinned.
-   **Code rules** read agent source without running it: a tool whose input reaches a shell, model output that reaches execution, an agent that can delegate to an ungated action.

Zip and tar archives inside the add-on are opened, one level deep, and their members read the same way. A file the Scanner could not read (too large, binary, an archive it does not open) is listed in the scan’s coverage, never treated as clean.

## Indirect issues: what the files point at

A `SKILL.md` can be clean and still tell the agent to read and follow a page, or run a package, that is not safe. The Scanner follows the chain in seven steps, and each step states what it found and where it stopped:

1.  **Extract every reference, with its role.** Every link, repository, package, domain, container image, cloud host, local path and command the files name, and what the agent is told to do with it: follow it (instruction source), run it (executed code), install it (dependency), read it (data), or nothing (link).
2.  **Ask who is behind it.** GitHub, the package registries, the domain registries, DNS and the MCP Registry are asked about each reference, and every answer is kept as a receipt: what was asked, from where, when, and what came back. A repository whose owner was deleted, a package name nobody has published or a domain anyone can register is reported as a name that can be claimed. The Scanner never claims it.
3.  **Fetch what it points at, safely.** Only public addresses, every redirect checked again, with caps on size and time. A fetch cut at a cap is partial, never complete.
4.  **Judge the content against the add-on’s stated purpose.** A model is asked whether the fetched content asks the agent for something outside what the add-on says it is for: reading credentials, sending data out, switching off approval, hiding from the user, fetching and running more code. Every answer must quote the passage it relies on, the quotation is checked again, and more than half of the passes must agree. The model may add a finding. It can never clear or lower one.
5.  **Check whether the Scanner was shown something else.** Each instruction source is fetched as the Scanner and as an agent-like client, and a difference is reported.
6.  **Record a hash and check again.** What was fetched is hashed, and a change since the last scan is reported. References are checked again on their own schedule between scans.
7.  **Say what could not be checked.** A reference ends as resolved, does not exist, unresolved (with the reason) or not attempted. Unresolved and not attempted are never clean.

An organization can turn off sending content to a model. Its scans then stop at level 3, and say so.

## Evidence levels

Each finding carries the highest level its evidence reached:

| Level | What was observed | The finding may say | It must not say |
| --- | --- | --- | --- |
| 0\. Inventory | The add-on was parsed | It references X, runs Y, is pinned or not | Anything about risk |
| 1\. Pattern | Text or code matches a rule | A pattern linked to this behavior is here | “Malicious”, or that the behavior happens |
| 2\. Structural | A deterministic check of the parsed facts | This is so, with the values shown | Intent |
| 3\. Resolved | A reference was checked at a stated time from a stated place | At that time it did not exist, redirected, or was registered on this date | That it has been or will be exploited |
| 4\. Assessed | Linked content was fetched, hashed and judged against the stated purpose | This content asks for Z, outside the stated purpose | That an agent will comply |
| 5\. Observed | The add-on ran in a sandbox with decoy credentials | In N of M runs it did this | That a clean run means safe |
| 6\. Corroborated | A lower level plus an independent match or a human review | “Malicious” or “compromised” |  |

## What a result means, and what it does not claim

A clean result means: no findings at the levels the scan reached, with the coverage it states, at the time it ran. It is not a verdict that the add-on is safe.

-   **A category is clear only when every stage it needs ran.** Otherwise it is not checked, and the result says which stage did not run.
-   **A sandbox run proves presence, never absence.** An add-on that did nothing in a run may act later or elsewhere.
-   **Every cap is a way to hide.** A file over the size limit, an archive the Scanner does not open, a fetch cut at its cap: each is listed, and the categories that depend on it are not reported clear.
-   **A claimable name can be wrong.** GitHub does not say whether a freed name is retired, so “this owner name can be claimed” can be wrong for a once-popular repository.
-   **The model can miss.** Published defenses against prompt injection aimed at a model judge have been broken under adaptive attack. That is why the model can only add findings and why its findings stand on a quoted passage.
-   **The Scanner reads files, not accounts or machines.** Connectors and skills held in a vendor’s account, and what is installed on a developer’s laptop, are not seen.

## How accuracy is measured

The Scanner is scored on a labelled corpus kept with its source. Each sample is a folder scanned as one unit and labelled with the categories a correct scan reports for it. A category whose ground truth is not settled for a sample is marked uncertain and not scored.

| Samples | Benign | Harmful | What they are |
| --- | --- | --- | --- |
| 40 | 40 | 0 | Martian’s own skills, including eight that describe attack techniques in plain words, as hard negatives |
| 9 | 5 | 4 | Martian’s demonstration MCP server and agent: its defensive prompts, and deliberately weak twins of them |
| 4 | 4 | 0 | Public skills from Anthropic’s Apache-2.0 plugin directory |
| 36 | 16 | 20 | Synthetic samples written for the corpus: harmful ones for each content category, and benign twins of them |
| 9 | 1 | 8 | Indirect-case fixtures: clean add-ons that point at a deleted repository owner, a renamed owner, an unpublished package, a look-alike domain, a page that changes after the scan, a page that cloaks, a five-hop chain to an unpublished package, an unregistered MCP host, and one benign twin |
| 37 | 0 | 37 | Bypass fixtures: one inert sample for each published way past a skill or MCP scanner that Martian’s research records (40 classes, some sharing a sample) |
| 14 | 0 | 14 | Attack-library fixtures: one inert sample for each mechanism of the attack records on agent add-ons in Martian’s attack library |
| **149** | **66** | **83** |  |

The indirect-case fixtures are offline: each carries recorded answers from the registries and the pages it names, and the model’s analysis is replayed from recorded answers of the Scanner’s analysis model. No live network or model is used when the corpus is scored.

For each sample and category, the labels determine whether a finding counts as a true or false positive. With no finding, the category counts as a true or false negative only when the scan checked it. When a required stage did not run, the category counts as **not checked**.

## Measured results

Per category. TP, FP, FN and TN are counts of samples. “Not checked” is the number of harmful and benign samples on which the scan did not check the category: the resolve and fetch categories are checked only where there is something to resolve, and prompt injection only where the model analysis ran.

| Category | TP | FP | FN | TN | Not checked (harmful / benign) | Precision | Recall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Supply chain | 23 | 0 | 0 | 2 | 0 / 118 | 23 of 23 | 23 of 23 |
| Distribution credibility | 1 | 0 | 0 | 2 | 0 / 144 | 1 of 1 | 1 of 1 |
| External instruction source | 4 | 0 | 0 | 3 | 3 / 138 | 4 of 4 | 4 of 4 |
| Server integrity | 1 | 0 | 0 | 5 | 1 / 142 | 1 of 1 | 1 of 1 |
| Prompt injection | 5 | 0 | 0 | 60 | 5 / 78 | 5 of 5 | 5 of 5 |
| Data exfiltration | 8 | 0 | 0 | 134 | 0 / 0 | 8 of 8 | 8 of 8 |
| Excessive actions | 5 | 0 | 1 | 141 | 0 / 0 | 5 of 5 | 5 of 6 |
| Hidden behavior | 28 | 0 | 0 | 117 | 0 / 0 | 28 of 28 | 28 of 28 |
| Unsafe configuration | 13 | 0 | 0 | 135 | 0 / 0 | 13 of 13 | 13 of 13 |
| Agent code weakness | 5 | 0 | 0 | 142 | 0 / 0 | 5 of 5 | 5 of 5 |

Per evidence level. A finding is true or false by the same labels; recall at a level counts the expected categories caught at that level or above.

| Level | True findings | False findings | Recall at or above |
| --- | --- | --- | --- |
| 0\. Inventory | 5 | 0 | 99% |
| 1\. Pattern | 44 | 0 | 96% |
| 2\. Structural | 62 | 0 | 67% |
| 3\. Resolved | 8 | 0 | 20% |
| 4\. Assessed | 23 | 0 | 16% |
| 5\. Observed | 0 | 0 | 0% |
| 6\. Corroborated | 0 | 0 | 0% |

Most harmful samples carry their problem in their own text or structure, so most are caught at levels 1 and 2; few have a reference to resolve or content to fetch, which is why recall at levels 3 and 4 is low.

No rule that runs by default reported a category on a benign sample that the sample is not labelled for.

## What these numbers are, and are not

-   **They are bound to this corpus.** Published evaluations of other scanners show the same engine scoring under 10% or over 90% recall depending on the corpus and the mode. These numbers say how the Scanner does on these samples, not on the add-ons you will scan.
-   **The counts are small.** Several categories have one to eight harmful samples. “5 of 5” is not evidence of no misses in general, and no false positive on 66 benign samples is not a false-positive rate for the field.
-   **Most samples are Martian’s.** The harmful samples were written for the corpus (the bypass and attack-library fixtures reproduce published techniques as inert samples), and most benign ones are Martian’s own skills and agents. Third-party sets of real malicious add-ons are not in it: their terms forbid redistribution or they hold working malware, so they are listed by name and not scored.
-   **The indirect case is measured on fixtures we built.** No public dataset labels a clean add-on that points at hostile or claimable content, so the nine fixtures are the only indirect-case measurement there is. They replay recorded answers; a live registry or page can answer differently.
-   **Level 4 is measured on recorded answers of one model.** A live model, or another model, can flag more or less.
-   **The resolve and fetch categories are checked only where there is something to resolve,** and prompt injection only where the model analysis ran. On the other samples they are not checked, which is why their “not checked” counts are high.
-   **Levels 5 and 6 are not measured.** The corpus has no sandbox runs and no corroborated samples.

## Known limits

What the stages that exist cannot see. Each is reported as not checked, skipped or not inspected where it applies; none is reported clear.

-   **Natural-language attacks.** Patterns catch known phrasings only. A ciphered, translated, paraphrased or payload-less instruction, or one split across tool descriptions, needs the model analysis; where it did not run, prompt injection is not checked. A data-exfiltration instruction in plain words with no path or command is not caught by a rule.
-   **Behavior at run time.** A trigger that waits for a date, an environment or a number of calls, and a payload decided at run time, are seen only by running the add-on. A trigger whose payload is in the files is caught by the payload’s rule.
-   **Remote content.** A remote MCP server is listed under one client identity; an answer that differs by identity or by number of calls is not compared.
-   **Across files.** Values are followed inside one file. A download to a fixed path run by another file is caught; other data passed between files is not followed.
-   **Opaque content.** Archives are opened one level deep, and 7-Zip, RAR, zstandard and lone gzip streams not at all; binary data, PDFs and legacy Office documents are not read. Each is listed as not inspected.
