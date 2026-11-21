# Evals suite YAML

> Build an evals.yaml file, look up suite fields and checks, and run it against an agent or saved replies.

Source: [Web version](https://docs.martiansecurity.ai/sdk/local-evals-yaml/)

An Evals suite connects a [case file](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-datasets.md#1-write-case-files-for-a-yaml-suite) to a list of checks. Save it as `evals.yaml` and use the [Local SDK](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-installation.md) to run it.

## Write a suite file

```yaml
data: cases.jsonl
target:
  file: agent.py
  function: answer
checks:
  - type: contains
    name: mentions_opening_time
    expectation: opening
output: results
```

`data` points to the cases and `target` selects the function returning replies. Each item under `checks` is a separate check. `expectation: opening` reads the `opening` value from each case. Paths are relative to the suite file. Indent nested settings with spaces and prefix list items with `-`.

The [local suite walkthrough](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md#2-write-the-suite-file) provides matching cases and a Python function. Run it with `martian evals run evals.yaml`.

## Suite fields

| Key | Meaning |
| --- | --- |
| `data` | Required path to a JSON Lines or CSV case file |
| `checks` | Required list of one or more checks with unique names |
| `case_gate` | Optional [weighted case scoring](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals-yaml.md#score-a-case-with-weighted-checks). Without it, all checks must pass |
| `target` | Python `file` and `function`, or an [HTTP target](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals-yaml.md#http-target). Omit it to grade saved replies |
| `judge` | Model settings for [LLM checks](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md#6-add-an-llm-judge). Use `model` and optionally `inference_params`, `max_retries`, and `rate_limit_wait_seconds` |
| `output` | Results folder. Defaults to `results` |
| `input_key` | Argument name for a case’s plain `input`. Defaults to `message` |
| `concurrency` | Cases processed at once. Defaults to 4 |
| `repeats` | Attempts per case. Defaults to 1 |
| `combine` | How repeated results are combined. The default `all` requires all attempts to pass |

The runner rejects unknown keys. For prompt or model matrices, saved responses, and run limits, see the [SDK’s suite documentation](https://github.com/MartianSecurity/martian-redteam/blob/v0.4.0/docs/evals.md#run-a-suite-file-locally).

## HTTP target

Use these keys under `target` to send cases to your own HTTP endpoint.

| Key | Meaning |
| --- | --- |
| `url` | Required HTTP or HTTPS address without inline credentials |
| `body` | Required JSON body for the POST. Use `{{input}}`, `{{inputs.NAME}}`, or `{{uuid}}` in string values |
| `headers` | Optional headers |
| `response_path` | Optional dotted path to the reply. An index selects a list item, as in `choices.0.message.content`. Without a path, the SDK grades the raw response text |
| `timeout_seconds` | Per-request timeout. Defaults to 120 seconds |

A body value made entirely of a placeholder keeps the source value’s type. Use `${NAME}` in the URL or a header value to read a setting from your environment. [Configure a URL target](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md#8-test-an-agent-behind-an-http-endpoint).

## Deterministic checks

These checks evaluate replies without calling a judge.

| `type` | Settings | Passes when |
| --- | --- | --- |
| `contains` | `values` or `expectation`. Optional `any_of` and `case_sensitive` | The reply contains the expected text |
| `not_contains` | `values` or `expectation`. Optional `case_sensitive` | The reply contains none of the given strings |
| `matches` | `pattern` | The regular expression is found in the reply |
| `not_matches` | `pattern` | The regular expression is absent from the reply |
| `is_json` | Optional `required_keys` | The reply is valid JSON and contains any required keys |
| `json_schema` | `schema` and optional `embedded: strict` | The reply matches the schema. In embedded mode, any matching object in the reply passes |
| `word_count` | `min_words`, `max_words`, or both. Optional `negate` | The reply meets the inclusive word-count bounds |
| `levenshtein` | `values` or `expectation`. Optional `max_edits` and `negate` | The reply is within the edit limit of at least one reference |

Use SDK 0.4.0 or later for `embedded: strict`, `word_count`, and `levenshtein`.

Use `values` for text shared across all cases, or `expectation` to select a per-case value. For `contains`, all values must be present unless you set `any_of: true`. Text matching ignores case unless you set `case_sensitive: true`. A check name must differ from the expectation key it reads. [All deterministic checks](https://github.com/MartianSecurity/martian-redteam/blob/v0.4.0/docs/evals.md#deterministic-checks).

### Check structured replies

SDK 0.4.0 and later support `is_xml` for well-formed XML. Save the example below as `catalog-evals.yaml`.

```yaml
data: catalog-cases.jsonl
checks:
  - type: is_xml
    name: second_book_title
    required_elements: [catalog.book.1.title]
output: results-catalog
```

Save one reply in `catalog-cases.jsonl`.

```json
{"id":"catalog","input":"List two titles as XML.","output":"<catalog><book><title>First</title></book><book><title>Second</title></book></catalog>"}
```

Run `martian evals run catalog-evals.yaml` and expect one passing case. Paths start at the root. The zero-based index `1` selects the second `book` sibling. Set `fragment: true` to look for well-formed XML in surrounding prose or a code fence. Set `negate: true` to require the condition to fail.

### Score a case with weighted checks

Use SDK 0.4.0 or later. This suite requires an object with a string title inside a reply. It gives that check three times the weight of the word-count check. Each check keeps its own verdict, and the overall case passes at a weighted score of 0.75 or higher.

Save as `weighted-evals.yaml`.

```yaml
data: weighted-cases.jsonl
checks:
  - type: json_schema
    name: has_title
    embedded: strict
    schema:
      type: object
      required: [title]
      properties:
        title: {type: string}
  - type: word_count
    name: concise
    max_words: 10
case_gate:
  threshold: 0.75
  weights: {has_title: 3}
output: results-weighted
```

Save these records as `weighted-cases.jsonl`. The suite grades the saved replies without calling an agent or a model.

```json
{"id":"short","input":"Return a catalog entry.","output":"Catalog entry follows. {\"title\":\"Atlas\"}"}
{"id":"long","input":"Return a catalog entry.","output":"Here is the requested catalog entry with the title supplied for this branch: {\"title\":\"Atlas\"}"}
{"id":"wrong-type","input":"Return a catalog entry.","output":"Here is an entry: {\"title\":42}"}
```

```sh
martian evals run weighted-evals.yaml --data-dir ./evals-data
```

Expect two passing cases and one failing case, with exit code `1`. The long reply earns 0.75 because the schema check passed. The reply with the numeric title earns 0.25 because only the word-count check passed. [Weighted gates and assertion sets](https://github.com/MartianSecurity/martian-redteam/blob/v0.4.0/docs/evals.md#weighted-case-gates)

## Grade saved replies

To evaluate replies you already have, save this record as `saved-cases.jsonl`.

```json
{"id":"weekday-hours","input":"When does weekday support open?","output":"Support opens at 9 a.m.","expectations":{"opening":"9 a.m."}}
```

Save this as `saved-evals.yaml` next to it.

```yaml
data: saved-cases.jsonl
checks:
  - type: contains
    name: mentions_opening_time
    expectation: opening
output: results-saved
```

```sh
martian evals run saved-evals.yaml
```

Expect one passing case. The reply comes from `output`, and this check needs no agent or model call. Keep all recorded replies in the case file when omitting `target`.

## Fix configuration errors

-   If the YAML parser reports a line and column, check indentation, missing quotes, and the dash before each check.
-   If the runner reports an unknown field, check its spelling and nesting. For example, `expectation` belongs to a check and `expectations` belongs to a case.
-   If a check reports a missing expectation, add that key to each relevant case or use shared `values`.

See the [CLI command reference](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-cli.md) for run flags and result paths.
