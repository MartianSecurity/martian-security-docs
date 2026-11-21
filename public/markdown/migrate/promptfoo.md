# Move from Promptfoo or Marsfoo

> Import saved Evals results, convert a config to native suite files, and review which verdicts can be compared.

Source: [Web version](https://docs.martiansecurity.ai/migrate/promptfoo/)

Python SDK · Any developer with promptfoo results or config files; no Martian account or API key; a model key only for a converted llm-rubric judge

Two commands move a promptfoo project. `martian evals import promptfoo` brings the results you already have into the local Evals UI, one run per provider. `martian evals convert promptfoo` turns your config’s tests into [suite files](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md) that `martian evals run` runs against your agent, wherever its assertions have an equivalent check, and lists everything it leaves out.

Neither command runs promptfoo or calls its providers, and promptfoo does not need to be installed next to the SDK.

For a promptfoo **red team** config or its results, see [Move a promptfoo red team](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/promptfoo-redteam.md).

Needs SDK 0.1.4 or later

The original walkthrough uses **martian-sdk 0.1.4**. For archive deduplication, additional provider and assertion support, and Compare, see [Migrate with the preview SDK](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/promptfoo.md#migrate-with-the-preview-sdk).

## Migrate with the preview SDK

These steps use the [preview SDK and matching workbench](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/local-sdk.md#open-the-preview-workbench). The import and conversion commands accept supported Marsfoo exports and configs under the same `promptfoo` subcommand.

### 1\. Import archived results

Use a version 3 results JSON archive. To include attachments, use an export made with `promptfoo export eval EVAL_ID --include-media -o results.json`. Keep the archive, local data folder and generated suites private because they can contain prompts, replies or attachments.

```sh
martian evals import promptfoo results.json --data-dir ./evals-data
```

Each provider becomes a saved run with its original case verdicts. Reimporting unchanged evidence reuses the runs and reviews. Changed evidence makes a separate snapshot. Use `--new-id` to create independent copies, including when you need comparison evidence available only to the preview importer.

Start the [preview workbench](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/local-sdk.md#open-the-preview-workbench) with `./evals-data`. Select **Evals → Runs**, open a run and select **Inspect** on a case. **View trace** opens the archived span tree when the export linked one. **Imported media** shows the case’s attachments, including unavailable references when the export omitted the bytes. **Overview** shows named and derived metrics when the archive includes them.

### 2\. Preview config conversion and grade the suite

```sh
martian evals convert promptfoo promptfooconfig.yaml --provider echo --strict --dry-run --output suite
```

Replace `echo` with the source provider’s exact ID or label. A plain `echo` provider uses the rendered prompt as the stored reply, with `providerOutput` taking precedence. Supported JSON POST and OpenAI-compatible chat configurations create native HTTP targets. You can use `--target agent.py:answer` for a trusted local Python adapter. Use `--all-providers` instead of selecting one provider or adapter to convert each supported provider into separate suites.

**Strict mode** exits with code **2** on unsupported settings or known scoring differences. **Dry run** lists the planned suites and writes no files. Review any listed omissions, remove `--dry-run` when ready, and run the suite paths printed by conversion. The single-provider example uses the same store as the imported results.

```sh
martian evals run suite/evals.yaml --data-dir ./evals-data
```

Conversion maps supported text and structured assertions, including literal JSON Schema, embedded JSON, [XML](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals-yaml.md#check-structured-replies-in-the-preview), word count and edit distance. It preserves supported provider and prompt selectors, assertion weights, test thresholds, one level of assertion sets, named metrics, and arithmetic derived metrics. The SDK reports custom code, unsupported schema rules and constraints, and configurations that need verdict review. If an unsupported assertion contributes to a weighted gate, best-effort conversion skips that test and strict conversion refuses it.

### 3\. Compare saved verdicts

In **Evals → Compare**, select the imported run as **Baseline**, the native run as **Candidate**, and choose **Compare runs**. For runs with different dataset identities, the preview verifies the shared cases’ rendered prompts, variables, effective deterministic checks, weights and thresholds before pairing verdicts. The **Case verdict** view labels verified comparisons and shows which cases were present on only one side.

An archived grade stays as recorded. In a comparison with verified check rules, a missing case verdict is incomparable. If any shared case lacks verified grading evidence or uses different rules, the entire cross-dataset comparison is unavailable. For example, a saved XML grade that disagrees with the native parser, or an embedded JSON schema referenced only by a file path, lacks the evidence required for that comparison. Model graders and custom transforms can also block verification.

The sections below show the original 0.1.4 walkthrough and its conversion limits.

## Before you start

-   Use **Python 3.12 or newer** and Bash or Zsh on macOS or Linux.
-   To import results, you need the JSON file that `promptfoo eval -o results.json` writes. Other output formats, and results files from promptfoo releases that wrote the older results table, are refused.
-   To convert a config, you need your `promptfooconfig.yaml` and a Python function that calls your agent.
-   You need no Martian account or API key. A converted suite needs a model key only if it keeps an `llm-rubric` assertion as an LLM judge; that judge sends each case to the model provider you choose.
-   The data folder (default `~/.martian/evals`) and the converted suite’s results hold prompts and replies in clear text. Keep them private.

## 1\. Install the SDK

In your promptfoo project’s folder, create an isolated environment and install the SDK:

```sh
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade 'martian-sdk[evals]'
martian --version
```

Check for Python 3.12 or newer and SDK **0.1.4** or later. Keep this environment active for the remaining commands.

The examples on this page use this config. It has one prompt, two versions of a bot as providers, and three tests:

```yaml
description: FAQ bot

prompts:
  - "Answer the customer briefly. Question: {{question}}"

providers:
  - id: file://provider.py:bot_v1
    label: bot-v1
  - id: file://provider.py:bot_v2
    label: bot-v2

defaultTest:
  assert:
    - type: not-icontains
      value: as an AI
    - type: latency
      threshold: 2000

tests:
  - description: opening hours
    vars:
      question: When do you open?
    assert:
      - type: icontains
        value: 9am
  - description: delivery
    vars:
      question: Do you deliver?
    assert:
      - type: regex
        value: "\\d+ km"
      - type: javascript
        value: output.length < 100
  - description: card payments
    vars:
      question: Can I pay by card?
    assert:
      - type: icontains
        value: card
      - type: levenshtein
        value: Yes, we take all major cards.
        threshold: 5
```

## 2\. Import your results

```sh
martian evals import promptfoo results.json
```

The first time, log lines from the local evaluation store appear while it creates the data folder. Then each provider in the file prints one line:

```text
results.json: provider bot-v1, run promptfoo-bot-v1-1, 3 cases: 2 passed, 1 failed, 0 errors
results.json: provider bot-v2, run promptfoo-bot-v2-1, 3 cases: 3 passed, 0 failed, 0 errors
Open them in the local Evals UI: martian ui
```

The exit code is **`0`**. Each run is named `promptfoo-`, the provider’s label (or its ID when it has none) and a number that counts that provider’s imported runs. Give every provider its own label: a file in which two providers share one is refused.

-   One command can take several results files. Every file is read before anything is written: if one cannot be imported, the command exits **`2`**, says which file and why, and imports none of them.
-   Importing the same file again creates more runs. Import each file once.
-   To import into a folder other than `~/.martian/evals`, add `--data-dir DIR`, or set `MARTIAN_EVALS_HOME`. Open the UI with the same folder.

## 3\. Open the runs

```sh
martian ui
```

Your browser opens `http://127.0.0.1:7600/`. The UI has one user and no login; stop it with Ctrl+C in the terminal.

1.  **Runs** lists one run for each provider in the **Default** project. The config’s `description` appears under each run’s name.
2.  Select a run. Each case’s input is the prompt with its vars filled in. The prompt text is the same under every provider, so the same test has the same case ID in every run of the file. The expected column shows the test’s assertions, and the verdict is promptfoo’s own verdict on that row.
3.  Select a row’s **Inspect** button, which opens the case. Each assertion promptfoo graded is an assessment that passed or failed, with promptfoo’s reason.
4.  Open **Compare**, choose the runs of two providers as **Baseline** and **Candidate**, and select **Compare runs**. Providers that ran the same tests on the same prompts pair case by case, whether they come from one results file or from two. A case on which a provider errored counts as **Not Comparable**.

## 4\. Convert your config

Write a Python file that calls your agent. The converted suite calls the function once per case with two keyword arguments, `prompt` (the prompt with the test’s vars filled in) and `vars` (the test’s vars), and grades the text it returns. This `agent.py` answers from a table; replace the body with a call to your application:

```python
REPLIES = {
    "When do you open?": "We open at 9am.",
    "Do you deliver?": "Yes, within 5 km.",
    "Can I pay by card?": "Yes, we take all major cards.",
}


def answer(prompt, vars):
    return REPLIES.get(vars["question"], "I don't know.")
```

Convert the config into a new folder:

```sh
martian evals convert promptfoo promptfooconfig.yaml --target agent.py:answer --output suite
```

The command prints the suite files it wrote and everything it did not convert:

```text
suite/evals.yaml: promptfoo tests 1, 3, 2 cases in cases.jsonl, checks not_icontains, latency, icontains
suite/evals-2.yaml: promptfoo tests 2, 1 cases in cases-2.jsonl, checks not_icontains, latency, regex
Not converted (also listed at the top of each suite file):
- providers[0] bot-v1 (file://provider.py:bot_v1): not called: the suite calls agent.py:answer instead
- providers[1] bot-v2 (file://provider.py:bot_v2): not called: the suite calls agent.py:answer instead
- tests[1].assert[1] javascript: runs custom code, which a suite file's built-in checks do not; write the rule as a custom Python scorer, `def scorer(inputs, outputs, expectations)` (name only the arguments it reads; `trace` too) returning True or False, a number, or a pair of either with a reason, and add it with `type: python` (`file:` and `function:`) by hand; this converter does not translate the code
- tests[2].assert[1] levenshtein: scores closeness to a reference text, or perplexity; no built-in check does
Run each with `martian evals run`, such as: martian evals run suite/evals.yaml
```

A suite file applies every check to every case, while promptfoo sets assertions per test. The converter therefore groups tests that need the same kinds of checks into one suite: `evals.yaml` with `cases.jsonl`, then `evals-2.yaml` with `cases-2.jsonl`, and so on. A check whose value differs between the tests of one suite, such as `icontains` above, reads the value from each case. The `defaultTest` assertions come first in every suite.

| Option | Effect |
| --- | --- |
| `--target FILE.py[:FUNCTION]` | The function each case calls, as above. Without a function name, it calls `target`. Without `--target`, a test’s `providerOutput` is graded as a stored reply, and a test without one is not converted |
| `--judge-model MODEL` | The model for `llm-rubric` assertions, such as `openai:/YOUR_JUDGE_MODEL`. Without it, `llm-rubric` is not converted |
| `--output DIR` | The folder for the suite and case files. A folder that already holds one of those files is refused, and nothing is written |

## 5\. Run the converted suites

Run each suite file:

```sh
martian evals run suite/evals.yaml
martian evals run suite/evals-2.yaml
```

The first suite prints this table and exits **`0`**:

```text
                       evals.yaml: 2 cases
┏━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Check         ┃ Passed ┃ Failed ┃ Errors ┃ Pass rate (95% CI) ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ not_icontains │ 2      │ 0      │ 0      │ 100% (34–100%)     │
│ latency       │ 2      │ 0      │ 0      │ 100% (34–100%)     │
│ icontains     │ 2      │ 0      │ 0      │ 100% (34–100%)     │
│ All checks    │ 2      │ 0      │ 0      │ 100% (34–100%)     │
└───────────────┴────────┴────────┴────────┴────────────────────┘
```

Each suite writes its result files next to it (`suite/results`, `suite/results-2`) and records a run in the local Evals UI. [Run evals locally with a suite file](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md) explains the results, exit codes and options.

## 6\. Replace what did not convert

Each item in the list needs a decision: rewrite it as a check, or leave it out. Custom code, such as the `javascript` assertion above, becomes a Python check. Write the rule as a function that takes the reply as `outputs` and returns `True` or `False`, in `suite/scorers.py`:

```python
def short_reply(outputs):
    return len(outputs) < 100
```

Add it at the end of the `checks` list in `suite/evals-2.yaml`, at the same indentation as the converted checks:

```yaml
- type: python
  name: short_reply
  file: scorers.py
  function: short_reply
```

The file path is relative to the suite file. Run the suite again:

```sh
martian evals run suite/evals-2.yaml
```

Because the checks changed, the earlier verdict is discarded and the case is graded again. The table gains a `short_reply` row with 1 passed. A Python check runs with your user’s full permissions, so review check files you did not write before you run them.

## What maps where

**Results.** Importing a results file maps it like this:

| In promptfoo results | In the local Evals UI |
| --- | --- |
| One provider | One run, named `promptfoo-<label>-<n>` |
| One test on one prompt | A case, `test <n>`. With several prompts, `test <n>, prompt <m>`, where the prompts are counted by their text and not by promptfoo’s numbering of each provider’s columns, so every provider’s run names the same test and prompt the same way; a later repeat adds `(repeat <k>)` |
| The rendered prompt and the vars | The case’s input |
| The test’s assertions | The case’s expected value |
| The provider’s output | The reply |
| promptfoo’s pass, fail or error for the row | The case’s verdict, so a test `threshold` counts as it did in promptfoo |
| Each graded assertion | An assessment named after its type, passed or failed, with promptfoo’s reason and numeric score. A second assertion of the same type is `<type> (2)`; one inside an `assert-set` is `assert-set/<type>` |
| A model-graded assertion or a red team grader | An LLM judge assessment |
| Latency, tokens and cost | The case’s trace |
| The config’s `description` | The run’s dataset name. The rest of the config is not copied |

**Assertions.** The converter turns an assertion into a check only when the check decides the same way:

| promptfoo assertion | Suite check |
| --- | --- |
| `contains`, `contains-all` | `contains`, case-sensitive |
| `icontains`, `icontains-all` | `contains` |
| `contains-any`, `icontains-any` | `contains` with `any_of: true`; case-sensitive for `contains-any` |
| `not-contains`, `not-contains-any` | `not_contains`, case-sensitive |
| `not-icontains`, `not-icontains-any` | `not_contains` |
| `regex`, `not-regex` | `matches`, `not_matches`, read as a Python regular expression |
| `equals`, `not-equals` with text, a number or a boolean | `matches`, `not_matches` on the whole reply |
| `starts-with`, `not-starts-with` | `matches`, `not_matches` at the start of the reply |
| `is-json` with no schema, or a schema of only `type: object` and `required` | `is_json`, with the required keys |
| `llm-rubric` with a text rubric | The `rubric` judge on `--judge-model`; one per suite, so a test’s second `llm-rubric` is listed |
| `latency` with a threshold above 0, with `--target` | `latency`: the call took at most that many milliseconds |
| `cost` with a threshold above 0, with `--target` | `cost`: the call cost at most that many US dollars |

`cost` reads the cost of the model calls your function makes, as the SDK traces them. A function that makes no traced model call gives the `cost` check an error.

## What does not carry over

The converter lists each of these, with the reason, in its output and at the top of every suite file:

-   **Providers.** They are never called; the suite calls your `--target` function.
-   **Custom code:** `javascript`, `python`, `ruby` and `webhook` assertions. Rewrite them as Python checks, as in step 6.
-   **Model-graded assertions other than `llm-rubric`**, such as `factuality`, `g-eval`, `answer-relevance` and the `context-` and `model-graded-` types, and `classifier`, `moderation` and `pi`.
-   **Similarity scores:** `similar`, `levenshtein`, `rouge-`, `bleu`, `gleu`, `meteor` and `perplexity`.
-   **Checks no suite check decides the same way:** `contains-json`; `is-json` with other schemas; `equals` with a JSON value; `is-refusal` and `not-is-refusal`; red team graders; tool-call and trajectory assertions; assertions on the provider’s trace or metadata; HTML, SQL and XML formats; `word-count`; `assert-set`, `select-best`, `max-score` and `human`. Where a check comes close, the list names it so you can add it by hand.
-   **Options that change a verdict:** `transform`, `contextTransform`, a `threshold` other than on `latency` and `cost`, `rubricPrompt`, `normalizeUnicode` and `config`, and values loaded with `file://` or using template logic beyond `{{ name }}`. The assertion is not converted. `weight`, `metric` and a grading `provider` do not change the verdict, so the assertion converts and the option is listed.
-   **Test settings:** a test’s `threshold`, `metadata`, `options`, `provider`, `providers`, `prompts` and `assertScoringFunction` are listed and not applied. A test whose var is a list or a `file://` reference is not converted.
-   **Config sections** such as `scenarios`, `redteam` and `evaluateOptions`.

From results files, only the config’s `description` is kept; the rest of the config section is not copied.

## Failures and limits

-   **`No such command 'import'` or `No such command 'convert'`:** the installed SDK is older than 0.1.4. See the note at the top of this page.
-   **`Importing promptfoo results needs martian-sdk[evals]`:** install the `evals` extra, as in step 1.
-   **Exit code `2` with `Import failed:`:** the file is not promptfoo’s JSON results of the current version, has no results, gives one provider the same case twice, or gives two providers one label. Nothing was imported.
-   **Exit code `2` with `Conversion failed:`:** the config cannot be read, the `--target` file does not exist, or the output folder already holds a file the converter would write. Choose a new `--output` folder.
-   **`Nothing written: no test converts.`:** none of the tests has an assertion that converts. Exit code `2`.
-   **Case-insensitive checks** compare with Python’s case folding, where promptfoo lowercases, so a few non-English letters can compare differently.

## Next

-   [Run evals locally with a suite file](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md): judges, result files and running the suite in CI.
-   [Move from MLflow](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/mlflow.md) and [Move from Inspect AI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/migrate/inspect.md) bring other tools’ results into the same data folder.
