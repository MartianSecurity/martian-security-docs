# Run local Evals on pull requests

> Run a deterministic eval suite in GitHub Actions without a Martian account and read the result in the job summary.

Source: [Web version](https://docs.martiansecurity.ai/sdk/local-ci/)

Python SDK · Developer who can add a GitHub Actions workflow; no Martian account is needed

Check each pull request against a suite file and read the verdict in the GitHub Actions job summary. The example uses GitHub Actions and the [two-case support suite](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md#2-write-the-suite-file). Its target and checks run without a Martian account, target credentials, or a model key.

## 1\. Add your suite to the repository

Keep `evals.yaml`, `cases.jsonl`, and `agent.py` together. Run the suite with [the Local SDK](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-evals.md#3-run-the-suite) first. Keep the data synthetic when the workflow or its artifacts are public.

## 2\. Run the suite on pull requests

Save the workflow below as `.github/workflows/evals.yml`. It uses the SDK 0.3.1 Evals Action, which evaluates fresh results on each run. The job runs code from the pull request, so use the `pull_request` event with read-only permissions and no secrets.

```yaml
name: Evals
on: pull_request

permissions:
  contents: read

jobs:
  evals:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - name: Run the Evals suite
        id: evals
        uses: MartianSecurity/martian-redteam/.github/actions/evals@2459bee92fbcd01f9192eee60f1bdf38adac3c18 # v0.3.1
        with:
          suite: evals.yaml
          output: eval-results
      - name: Retain the summary and test report
        if: ${{ !cancelled() && steps.evals.outputs.results-written == 'true' }}
        uses: actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7.0.2
        with:
          name: eval-results
          path: |
            eval-results/summary.json
            eval-results/junit.xml
```

## 3\. Read the check and its reports

In the pull request’s **Checks** tab, open **Evals** and select the workflow run’s **Summary**. The support suite reports **2 passed, 0 failed, 0 errors**. Change `suite` to the relative path of your own suite when you are ready.

| Exit code | Meaning |
| --- | --- |
| `0` | Every case passed |
| `1` | At least one case failed a check |
| `2` | A case had no verdict or the configuration was invalid |

The artifact step retains `summary.json` and `junit.xml` when the invocation writes results, even on a failed gate. Review case IDs and failure reasons before sharing the reports. Raw replies and inputs can appear in `results.jsonl` and `mlflow.db`.

## Troubleshooting

-   If only a job summary appears, check its error message. A configuration error can occur before the action writes any results.
-   If you are upgrading from the action that posted pull-request comments, remove the `github-token` and `comment-author` inputs. The report now appears in the job summary.
-   Run tests that need a target or judge credential in a separate trusted workflow. To compare a pull request to the default branch, see [baseline setup for the Evals Action](https://github.com/MartianSecurity/martian-redteam/blob/v0.3.1/docs/gate-and-ci.md#compared-with-the-last-result-of-main).

For an evaluation record tied to an agent and Git revision in your Martian workspace, follow the [workspace CI guide](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/ci.md).
