# Review Red Team YAML

> Check local Red Team YAML syntax and version, and inspect the reports saved by an existing run.

Source: [Web version](https://docs.martiansecurity.ai/sdk/local-redteam-yaml/)

Red Team version 2 files use YAML. You can check the syntax of an existing file on your machine before reviewing the configuration or its recorded results.

## Read the file format

Use spaces for indentation. Keep fields at the same indentation when they belong to the same mapping. A dash starts a list item. Use quotes around text with a colon followed by a space, or text that YAML may read as a Boolean.

In a version 2 file the top-level `version: 2` setting is an integer. It identifies the file format. `martian --version` prints the installed package version separately.

## Check the syntax locally

With the [Local SDK environment](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-installation.md) active, run the check below from the directory containing the file. Replace `redteam.yaml` with its path if needed.

```sh
python - redteam.yaml <<'PY'
from pathlib import Path
import sys
import yaml

path = Path(sys.argv[1])
try:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
except yaml.YAMLError as error:
    location = getattr(error, "problem_mark", None)
    if location is not None:
        raise SystemExit(f"Invalid YAML at line {location.line + 1}, column {location.column + 1}.")
    raise SystemExit("Invalid YAML.")
except OSError as error:
    raise SystemExit(f"Could not read {path.name}: {error.strerror}.")

version = document.get("version") if isinstance(document, dict) else None
if type(version) is not int or version != 2:
    raise SystemExit("Expected a YAML mapping with version: 2.")
print("YAML parses and declares version 2.")
PY
```

Use the reported line and column to find an indentation or quoting error. This check reads the file and prints its syntax status. SDK field compatibility and run readiness require a separate review.

## Review saved results

Open **Red Team → Runs** in the [local UI](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-ui.md) and select the saved run. Read its scope, evidence, verdict and report before sharing results. For command-line report export and baseline comparison, see [Read saved Red Team evidence](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/sdk/local-cli.md#read-saved-red-team-evidence).
