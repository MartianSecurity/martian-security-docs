# Run Python Evals with pytest

> Test a Python callback with pytest, assert scores, and save local results without a Martian workspace.

Source: [Web version](https://docs.martiansecurity.ai/sdk/local-pytest/)

Python SDK · Any developer; no Martian account is needed

Use pytest when your cases or assertions belong in Python. This example checks two support answers and writes a local evaluation record. You need Python 3.12 or newer and the [Local SDK installed](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-installation.md). The example needs no model key or Martian account.

## 1\. Write a prediction and an assertion

In your project folder, save this as `test_support.py`.

```python
import mlflow
from martian.evals import assert_checks, evaluate, exact_match


@mlflow.trace(name="support_agent", span_type="AGENT")
def predict(message: str) -> str:
    if "saturday" in message.casefold():
        return "Support opens at 10 a.m."
    return "Support opens at 9 a.m."


@mlflow.test
def test_support_hours():
    result = evaluate(
        data=[
            {
                "inputs": {"message": "When does weekday support open?"},
                "expectations": {"expected_response": "Support opens at 9 a.m."},
            },
            {
                "inputs": {"message": "When does Saturday support open?"},
                "expectations": {"expected_response": "Support opens at 10 a.m."},
            },
        ],
        predict_fn=predict,
        scorers=[exact_match],
    )
    assert_checks(result)
```

`predict` receives the fields under `inputs`. Replace its body with a call to your application when adding your own tests. The trace records each call, and `assert_checks` makes pytest fail if an expected score fails or is missing.

`exact_match` ignores capitalization and strips whitespace at the ends. Use an explicit `pass_if` rule for numeric metrics or custom labels. [See scoring criteria and judges](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/evaluations.md#judges-and-deterministic-checks).

## 2\. Run the test locally

With your project’s virtual environment active, run pytest through the SDK.

```sh
MARTIAN_EVALS_OFFLINE=1 \
MARTIAN_EVALS_STORE_DIR="$PWD/.martian-local-mlflow" \
martian evals run test_support.py -q
```

Expect **one passing test** and exit code `0`. That test evaluated both records. A mismatched answer makes the pytest test fail.

## 3\. Inspect the saved session

```sh
python -m json.tool .martian-local-mlflow/martian-session.json
```

Check that `state` and `upload` are both `offline`. The folder holds the recorded traces, inputs, expected answers and replies. Keep it private.

## Troubleshooting

-   For **`martian: command not found`**, activate the environment where you [installed the SDK](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-installation.md).
-   If an assertion fails, read the pytest output for the expected and actual values. Update your callback or correct the expected value in the case.

To share results tied to a published dataset and code revision, follow [Record Python Evals in a workspace](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/evaluations.md).
