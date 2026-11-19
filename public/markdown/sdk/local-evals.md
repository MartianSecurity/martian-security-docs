# Run evals locally with a suite file

> Run an eval suite from one YAML file on your own machine, using deterministic checks and LLM judges with your own model key.

Source: [Web version](https://docs.martiansecurity.ai/sdk/local-evals/)

Python SDK · Any developer; no Martian account; own model key for LLM judges

Write a suite for your own agent by combining a YAML file, test cases, and checks. The example evaluates support hours with two deterministic cases. If you have never run an eval, start with the [Community quickstart](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/get-started/quickstart.md).

## 1\. Set up your project

Open a project folder where you can save a suite and test cases together. Use Python 3.12 or newer and [install the Local SDK](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/local-sdk.md#install-the-local-sdk). Keep your virtual environment active.

The deterministic example needs no account or model key. When your target calls an external service or you [add an LLM judge](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md#6-add-an-llm-judge), those services receive the inputs they need.

## 2\. Write the suite file

Save `evals.yaml` in the project folder. Paths are relative to this file.

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

Save two cases in `cases.jsonl`, one JSON object per line. Each case’s `expectations.opening` provides the text that must appear in its reply.

```json
{"id":"weekday-hours","input":"When does weekday support open?","expectations":{"opening":"9 a.m."}}
{"id":"saturday-hours","input":"When does Saturday support open?","expectations":{"opening":"10 a.m."}}
```

Create `agent.py` with a function that accepts the case input as `message` and returns a string.

```python
def answer(message: str) -> str:
    if "saturday" in message.casefold():
        return "Support opens at 10 a.m. on Saturdays."
    return "Support opens at 9 a.m. on weekdays."
```

Replace the function body with a call to your application when using this pattern for your own agent. If your agent already exposes an API, use an [HTTP target](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md#8-test-an-agent-behind-an-http-endpoint).

## 3\. Run the suite

```sh
martian evals run evals.yaml
```

Expect **2 passed, 0 failed, 0 errors** and exit code `0`. Use the printed run code to find the result in the [local Evals UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md).

| Exit code | Meaning |
| --- | --- |
| `0` | Every case passed every check |
| `1` | At least one case failed a check |
| `2` | A case had no verdict, or the suite configuration was invalid |

## 4\. Read the results

The suite writes these files in `results`.

| File | Content |
| --- | --- |
| `results.jsonl` | Inputs, replies, case verdicts, and the reason for each check |
| `summary.json` | Pass, fail and error counts, with pass rates and 95% intervals |
| `junit.xml` | CI report with separate failures and errors |
| `verdicts.json` | Verdicts and fingerprints for comparison, without inputs or replies |
| `mlflow.db` | Evaluation data, including traces |

```sh
python -m json.tool results/summary.json
```

Read `results.jsonl` when a case fails or has no verdict. It contains inputs and replies in clear text, like the evaluation database. Keep both private. Review failure reasons in JUnit reports before sharing them.

## 5\. Rerun a suite

A rerun can reuse saved verdicts with matching fingerprints. The fingerprint covers the case, the checks, the target, and the SDK version. Use a different output folder to compare a candidate with your original result, and use `--fresh` to evaluate every selected case.

```sh
martian evals run evals.yaml --fresh --output results-candidate
```

Open **Compare** in the [local Evals UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md#compare) to pair results by case ID.

## 6\. Add an LLM judge

Use a judge when a check depends on the meaning of a reply. Copy `evals.yaml` to `evals-with-judge.yaml`. Keep `data` and `target` from the original file. Add `judge` and update `checks` and `output`.

```yaml
judge:
  model: "openai:/YOUR_JUDGE_MODEL"
  inference_params:
    temperature: 0
checks:
  - type: contains
    name: mentions_opening_time
    expectation: opening
  - type: rubric
    name: answers_the_question
    rubric: Pass when the reply clearly states when support opens on the day asked about.
output: results-judge
```

1.  Replace `YOUR_JUDGE_MODEL` with a model you have access to.
2.  Set your provider’s key in your environment. Test inputs, replies, and criteria go to this provider.

| Provider | `judge.model` | Environment |
| --- | --- | --- |
| OpenAI | `openai:/<model>` | `OPENAI_API_KEY` |
| OpenAI-compatible endpoint | `openai:/<model>` | `OPENAI_API_KEY` and `OPENAI_API_BASE` set to the endpoint’s `/v1` address |
| Amazon Bedrock OpenAI-compatible endpoint | `openai:/<Bedrock model ID>` | `OPENAI_API_KEY` set to a Bedrock API key and `OPENAI_API_BASE` set to the regional endpoint |

For example, use `https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1` for an enabled model in that region. [Generate a short-term Bedrock key](https://docs.aws.amazon.com/bedrock/latest/userguide/api-keys-generate.html).

3.  Run the copy and read the judge’s reason for each case in `results-judge/results.jsonl`.

```sh
martian evals run evals-with-judge.yaml
```

The suite file supports three judge types. Use at most one of each type in a suite.

| `type` | Criteria | What the judge decides |
| --- | --- | --- |
| `rubric` | `rubric`: one piece of text | Pass or fail against the rubric as a whole |
| `guidelines` | `guidelines`: a list of rules | Each rule is complied with, violated or not applicable; any violation fails |
| `conditions` | `conditions`: a list of `{question, fail_when}` | The judge answers each yes/no question; you decide whether `yes` or `no` fails |

Criteria written in the suite file apply to every case. A case can carry its own instead, under the same key in its `expectations`.

For a rule-by-rule explanation, replace the rubric check with this `guidelines` check:

```yaml
  - type: guidelines
    name: answers_about_support
    guidelines:
      - "State the opening time for the day the customer asked about."
```

For an explicit yes/no question, use `conditions`. Quote `"yes"` and `"no"` so YAML reads them as strings:

```yaml
  - type: conditions
    name: mentions_an_opening_time
    conditions:
      - question: "Does the reply state a support opening time?"
        fail_when: "no"
```

These snippets replace one item under `checks`; keep the suite’s `data`, `target` and `judge` settings. Use a new output folder or `--fresh` after changing the check.

A judgment that is invalid or uncertain is reported as an **error**, never as a pass. If the provider rate-limits, the judge waits as long as the provider asks, for up to `judge.rate_limit_wait_seconds` (default 300, at most 3600), separately from the retries. Server errors and connection failures are retried up to five times by default (`judge.max_retries`). It never asks again after receiving a judgment.

## 7\. Run it in CI

Use [Run local Evals on pull requests](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ci.md) for a read-only GitHub Actions workflow that uses this suite.

To keep a result tied to an agent and Git revision in a shared workspace, follow [Record CI results in a workspace](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/ci.md).

## 8\. Test an agent behind an HTTP endpoint

Copy the suite to `evals-http.yaml`. Keep the same cases and checks. Replace `target` with the URL, body, and response field for your endpoint. Set `output: results-http` to keep it separate from the function-based run.

```yaml
target:
  url: "http://127.0.0.1:8765/chat"
  headers:
    Authorization: "Bearer ${AGENT_API_KEY}"
  body:
    message: "{{input}}"
    session: "{{uuid}}"
  response_path: reply
```

Set `AGENT_API_KEY` in the shell that runs the suite if the endpoint needs it. For an endpoint without authentication, omit `headers`. Start your agent, then run the HTTP suite.

```sh
martian evals run evals-http.yaml
```

The SDK sends a JSON `POST` for each case. This example reads the returned text from a field such as `{"reply":"Support opens at 9 a.m. on weekdays."}`. For a chat-completions response, use `choices.0.message.content`. For a downloadable localhost agent and its dataset, see [Run an eval from the UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md#4-run-an-eval-from-the-ui).

-   **Placeholders** are filled into `body` for each case. `{{input}}` is the case’s `input`. `{{inputs.NAME}}` is one value from a case’s `inputs` object. `{{uuid}}` is a new random ID, for agents that keep a conversation per session. The body must use `{{input}}` or `{{inputs.NAME}}`.
-   **Secrets stay in your environment.** `${NAME}` in `url` or in a header value is replaced from the environment when the suite loads. Only the name is in the suite file, and the value is not written to the result files. `${NAME}` is not replaced inside `body`.
-   **Case text is sent as written.** `${...}` or `{{...}}` inside a case’s input reaches your agent unchanged.
-   **One request per case.** There is no retry, redirects are not followed, and proxy settings from the environment are not used.

A URL target cannot be combined with `file` or `function`. Keep using a Python function when your agent needs another HTTP method, a body that is not JSON, several calls per case, or a secret inside the body.

The example token `demo-token` only shows how a credential is passed. Use `https` for any endpoint that is not on your own machine or network, and review a suite file from someone else before running it with your credentials loaded: the file chooses where your cases and headers are sent.

## Reference

### Suite file

| Key | Required | Meaning |
| --- | --- | --- |
| `data` | Yes | Path to a `.jsonl` or `.csv` file of cases |
| `checks` | Yes | One or more checks, described below |
| `target` | No | `file` and `function` of the code under test, or a [URL target](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md#url-target) in SDK 0.1.4 or later. Omit it to grade replies stored in the data file |
| `judge` | For LLM judges | `model`, optional `inference_params` (`temperature`, `top_p`, `max_tokens`, `seed`), `max_retries` (0 to 10) and `rate_limit_wait_seconds` (at most 3600) |
| `concurrency` | No | Cases run at the same time; default 4 |
| `output` | No | Results folder; default `results` |
| `input_key` | No | Name of the argument passed to the target for a plain `input`; default `message` |

Unknown keys are rejected, so a misspelt setting stops the run with exit code `2`. SDK 0.1.4 and later also read a matrix of prompts and models, repeated attempts, conversations, run limits and a cache of model calls; the [SDK’s Evals documentation](https://github.com/MartianSecurity/martian-redteam/blob/main/docs/evals.md#run-a-suite-file-locally) describes them.

### URL target

Available in SDK 0.1.4 or later. These keys go under `target` in place of `file` and `function`.

| Key | Required | Meaning |
| --- | --- | --- |
| `url` | Yes | An `http` or `https` address, without credentials in it. `${NAME}` is read from the environment |
| `body` | Yes | The JSON body of the `POST`. Its string values can use `{{input}}`, `{{inputs.NAME}}` and `{{uuid}}` |
| `headers` | No | Request headers. `${NAME}` in a value is read from the environment |
| `response_path` | No | Dotted path to the reply in a JSON response; a number selects an item in a list. Without it, the whole response text is the reply |
| `timeout_seconds` | No | Limit for one request, from 1 to 600; default 120 |

A body value that is only a placeholder keeps the input’s type, so a number in `inputs` is sent as a number.

### Data file

| Format | Fields |
| --- | --- |
| JSONL | One object per line. `input` (a string) or `inputs` (an object passed to the target as keyword arguments). Optional `id`, `output` and `expectations` |
| CSV | Columns `input`, and optionally `id` and `output`. Every other column becomes an expectation of that name |

Give every case its own `id`; without one, the line number is used. To grade replies you already have, put each one in `output` and leave `target` out of the suite file. A data file with stored outputs cannot be combined with a `target`. There is no row limit.

### Deterministic checks

These make no model call and give the same answer every time. The table lists common checks. SDK 0.1.4 and later have more, such as `equals`, `starts_with`, `length`, `json_schema`, `no_secrets`, `no_personal_data` and `latency`; the [SDK’s list of deterministic checks](https://github.com/MartianSecurity/martian-redteam/blob/main/docs/evals.md#deterministic-checks) gives each with its options.

| `type` | Settings | Passes when |
| --- | --- | --- |
| `contains` | `values`, or `expectation`; `any_of`; `case_sensitive` | The reply contains every value, or at least one with `any_of: true` |
| `not_contains` | `values`, or `expectation`; `case_sensitive` | The reply contains none of the values |
| `matches` | `pattern` | The regular expression is found anywhere in the reply |
| `not_matches` | `pattern` | The regular expression is not found in the reply |
| `is_json` | `required_keys` | The reply is valid JSON; with keys, a JSON object that has each one |

`values` is a list written in the suite file. `expectation` names a key in each case’s `expectations` holding one string or a list of strings. Matching ignores case unless `case_sensitive: true`. Give a check a `name` when you use the same type twice; names must be unique and must differ from the expectation key the check reads.

### Run options

| Option | Effect |
| --- | --- |
| `--output DIR` | Choose the output folder |
| `--concurrency N` | Run up to N cases at once (default 4) |
| `--limit N` | Run only the first N cases |
| `--fresh` | Check every selected case again |
| `--data-dir DIR` | Choose the UI data folder for the saved run. Defaults to `MARTIAN_EVALS_HOME` or `~/.martian/evals` |

## Failures and limits

-   **Exit code `2` before any case runs:** the suite file is invalid, a path is wrong, or the target file cannot be imported. The message names the field or file.
-   **A case with no verdict:** the target raised an error, a check could not find its expectation value, or a judge returned no usable judgment. The case is counted under **Errors**, the run exits `2`, and a rerun tries that case again.
-   **URL target, before any case runs:** a `${NAME}` variable that is not set stops the run with exit code `2` and names the setting and the variable, for example `Eval run failed: target.headers.Authorization needs the environment variable AGENT_API_KEY`. An invalid target, such as a body with no input placeholder or an unknown placeholder, is rejected the same way.
-   **URL target, during the run:** a status outside 2xx, a timeout, an address that cannot be reached, or a response with no value at `response_path` gives that case no verdict, and the run exits `2`. The case’s `error` in `results.jsonl` says why, and the command prints a count for each reason after the table. For HTTP 401, check the credentials in `target.headers`. For a connection error, confirm the service is running and check `target.url`. The reason never includes the address, a header or the response body. A Python function target reports only `the target call failed`.
-   **Judges can be wrong.** Calibrate a rubric on replies you know should pass and fail before relying on it, and prefer a deterministic check wherever the text itself decides.
-   **Judge calls cost money and leave your machine.** Each LLM check uses your provider for each case; multiple judges and transport retries add requests.
-   **Rate limits:** if errors persist after the retries, lower `--concurrency` or raise `judge.max_retries`.
-   **Not a platform record.** A local run has no Martian session, agent attribution or tested revision. It is a development and pull-request check, not a release gate recorded by Martian.
-   **Private files:** do not publish `results.jsonl` or `mlflow.db` as public artifacts.

Continue with [Python Evals with pytest](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-pytest.md) for Python assertions or [local CI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ci.md) to run a suite on pull requests.
