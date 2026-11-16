# Operate an Evals installation

> Back up and restore an installation of the martian-evals Helm chart, read its logs and health, troubleshoot it, and upgrade it or roll it back.

Source: [Web version](https://docs.martiansecurity.ai/on-premises/operations/)

> **Page qualification:** On-Premises Helm chart · platform engineer · Walkthrough verification in progress. [Verification details](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/reference/verification.md).

> **Walkthrough limits:** Reviewed against the martian-evals chart and the backend, frontend and MLflow sources it installs, at the revisions recorded as sources. The chart's own checks render every documented values variant and refusal. No install has been walked through on a Kubernetes cluster, so no step below is observed live. The backup and restore commands for the databases were run with docker exec in place of kubectl exec against a disposable PostgreSQL 17 holding a seeded backend database at migration 0050; the restored database kept its data, ownership and row-level security policies and the backend's seed ran on it. The upgrade paths and the rollback were tested by the backend's upgrade job, run locally because the private repository's CI is off: it upgrades a database seeded by the releases at schema 0048 and 0050 to the head with containers, checks that every row survives, that both backends serve the upgraded database, that a downgrade is refused and changes nothing, and that a restore of the database backup gives the earlier release back; the helm upgrade, helm rollback and kubectl exec commands themselves were not run on a cluster.

Guide in progress

This guide is reviewed against the chart and the services it installs. Its procedures have not yet been walked through on a cluster; the upgrade and rollback are tested with containers, not with Helm.

Keep an installation of the `martian-evals` chart ([install](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/install.md)) recoverable and healthy. The commands use the namespace and release name `martian-evals` and the bundled PostgreSQL; adjust them if yours differ.

## What to keep

| Data | Where | Holds |
| --- | --- | --- |
| `martian_backend` database | PostgreSQL | Organizations, users and sessions, agents and their encrypted credentials, API keys, and the Evals records: runs, case results, scores, scoring jobs, reviews, suites, dataset drafts and saved views |
| `mlflow_tracking` database | PostgreSQL | Traces, datasets, judges and run metadata |
| `mlflow_auth` database | PostgreSQL | MLflow’s accounts: one hidden service account and workspace per organization |
| Artifacts | The volume `martian-evals-mlflow-artifacts`, or your bucket | Run artifacts and review attachments |
| The Secrets | Your secret store | Database passwords, and the keys that decrypt the stored MLflow credentials, agent credentials, model keys and single sign-on client secrets. The licence Secret is also kept by Martian Security, who can issue it again |

A backup needs all of them, from the same moment. Without the original `EVALS_SECRET_ENCRYPTION_KEY`, `AGENT_SECRET_ENCRYPTION_KEY` and `SSO_SECRET_ENCRYPTION_KEY`, a restored database cannot read the credentials it stores, and without the original passwords the restored roles do not match the Secrets.

`helm uninstall` keeps the PostgreSQL volume, the artifact volume and the Secrets. Delete them yourself only to discard the data.

## Back up

Take a backup when no run or scoring job is in progress. `pg_dump` gives a consistent copy of each database, but not one across the three databases and the artifacts. Write it to a private directory; the dumps contain your evaluation data and password hashes.

```sh
umask 077
BACKUP="$HOME/martian-evals-backups/$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$BACKUP"
for db in martian_backend mlflow_tracking mlflow_auth; do
  kubectl -n martian-evals exec martian-evals-postgres-0 -- \
    pg_dump -U postgres -Fc "$db" > "$BACKUP/$db.dump"
done
kubectl -n martian-evals exec deploy/martian-evals-mlflow -- \
  tar -C /artifacts -cf - . > "$BACKUP/artifacts.tar"
ls -l "$BACKUP"
```

**Expected result.** Three non-empty `.dump` files and `artifacts.tar`. With artifacts in a bucket, skip the `tar` command and use your storage’s own versioning or copies. With your own PostgreSQL, dump the same three databases with your usual tools.

## Restore

Restore into an installation of the **same chart version and images** as the backup: the backend expects the database schema of its own release, and a restored database keeps the schema it was backed up at. In the shell you restore from, set `BACKUP` to the backup’s directory.

### 1\. Install with the same Secrets

In a new or emptied namespace, recreate the three Secrets with the backed-up values, then install with the same values file ([install](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/install.md#4-install)).

### 2\. Stop the backend and MLflow

Nothing may write while you restore:

```sh
kubectl -n martian-evals scale deploy/martian-evals-backend deploy/martian-evals-mlflow --replicas=0
```

### 3\. Replace each database with its dump

```sh
for db in martian_backend mlflow_tracking mlflow_auth; do
  kubectl -n martian-evals exec martian-evals-postgres-0 -- psql -U postgres -v ON_ERROR_STOP=1 \
    -c "DROP DATABASE $db WITH (FORCE)" -c "CREATE DATABASE $db OWNER $db" \
    -c "REVOKE ALL ON DATABASE $db FROM PUBLIC"
  kubectl -n martian-evals exec -i martian-evals-postgres-0 -- \
    pg_restore -U postgres --exit-on-error -d "$db" < "$BACKUP/$db.dump"
done
```

### 4\. Restore the artifacts and start the backend

```sh
kubectl -n martian-evals scale deploy/martian-evals-mlflow --replicas=1
kubectl -n martian-evals rollout status deploy/martian-evals-mlflow
kubectl -n martian-evals exec -i deploy/martian-evals-mlflow -- \
  tar -C /artifacts --no-overwrite-dir -xf - < "$BACKUP/artifacts.tar"
kubectl -n martian-evals scale deploy/martian-evals-backend --replicas=1
kubectl -n martian-evals rollout status deploy/martian-evals-backend
```

**Expected result.** Members sign in with their existing passwords and see their runs, datasets and traces. Runs that were in progress when the backup was taken show **running**; stop them.

## Health and monitoring

The chart adds no metrics endpoint. Watch the pods with your cluster’s own monitoring: restarts, memory against the limits (`OOMKilled`), CPU, and volume usage.

```sh
kubectl -n martian-evals get pods,jobs,pvc
kubectl -n martian-evals top pods
```

| Check | Healthy |
| --- | --- |
| Backend probes `/readyz` (database reachable) and `/healthz` | Pod `Ready`, restarts not growing in either container |
| MLflow probe `/health` | Pod `Ready` |
| PostgreSQL `pg_isready` | Pod `Ready`; data volume not close to full |
| An organization’s evaluation store | **Master admin → Invitations** shows **Evals: ready** on its row |
| The Evals schema | `kubectl -n martian-evals exec deploy/martian-evals-backend -c backend -- python -m app.evals_records current` prints the same revision twice, as `<revision> (head <revision>)` |
| The evals worker | The pod’s second container, `evals-worker`, is `Ready` with restarts not growing; its log starts with a line that it started. Without it a launched run stays queued |
| The licence | `kubectl -n martian-evals exec deploy/martian-evals-backend -c backend -- python -m app.licence status` prints the licence’s state as JSON and exits 0 only for `valid` or `grace` ([the licence](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#the-licence)) |

## Logs

```sh
kubectl -n martian-evals logs deploy/martian-evals-backend -c backend       # the API
kubectl -n martian-evals logs deploy/martian-evals-backend -c evals-worker  # the worker, and the run and scoring processes it starts
kubectl -n martian-evals logs deploy/martian-evals-mlflow
kubectl -n martian-evals logs statefulset/martian-evals-postgres
kubectl -n martian-evals logs job/martian-evals-migrate         # within ten minutes of it finishing
```

A run’s or scoring job’s process writes to the evals worker’s log. The migrate and seed jobs are deleted ten minutes after they finish, whether they succeeded or failed, and a successful upgrade-time migrate job or seed job at once. Read a job’s log within that time.

## Troubleshooting

| Symptom | Cause and action |
| --- | --- |
| The install times out | The migrate job has not completed. Read its log. A database it cannot reach, or a password that does not match, stops it |
| The seed job fails at install | The install ran without `--wait --wait-for-jobs`, so the seed ran before the schema existed. Run `helm upgrade` with `--wait --wait-for-jobs` and the same values |
| PostgreSQL’s first start fails with `division by zero` | A password in `martian-evals-postgres` or `martian-evals-mlflow` is shorter than 32 characters. On a new installation only, fix the Secret, delete the `data-martian-evals-postgres-0` volume and install again. This erases the database |
| MLflow restarts with `MLflow configuration rejected` | A key is missing from `martian-evals-mlflow`, a value is shorter than 32 characters or spans lines, or `mlflow.adminUsername` is not 8 to 128 of `A-Z a-z 0-9 _ . -` |
| The console loads but sign-in or every page fails | `/v1` does not reach the backend on the console’s host, or the console image is not the same-origin build. Check the Ingress and the image Martian Security gave you |
| Pages do not update live | The ingress controller does not pass the WebSocket upgrade on `/v1/ws` |
| A CI upload returns 413 | The ingress controller’s request size limit is below 4 MiB ([values](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/install.md#3-write-your-values-file)) |
| **Eval setup is unavailable; contact your administrator** | The organization’s evaluation store is not ready. Use **Complete eval setup** on its invitation row; check that MLflow is `Ready` and its log shows no authentication errors |
| The operator’s own organization shows the same error | Expected: the operator organization has no evaluation store. Use an invited organization |
| A run or scoring job stays **queued** | The evals worker is not running or not taking work. Check that the pod’s `evals-worker` container is `Ready` and read its log |
| A run or scoring job is **running** after a restart | A stopped worker gives its work back at once, and a killed one’s work is taken over after 30 seconds; the run then resumes after the cases it had finished. Work whose worker was killed three times is marked **failed** |
| Registering an agent, a model endpoint or an identity provider at an internal or `http://` address is refused | Add its host to `backend.managedTargetHosts` ([install](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/install.md#7-your-own-agents-and-models)) |
| Every organization is on the Community edition | No licence is in force. Run the licence check under [Health and monitoring](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#health-and-monitoring): `missing` means the Secret is not mounted or the file is absent, `invalid` that the image cannot verify the file, and `expired` that the grace period is over |
| Setting an OIDC client secret fails | The backend Secret has no `SSO_SECRET_ENCRYPTION_KEY` ([install](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/install.md#2-create-the-secrets)) |
| Launching a run from the console fails, or a model judge cannot run | A run needs a remote runner for an agent only your network reaches, and a model judge needs `backend.judge.enabled` and a provider key; the Red Team engine is not installed ([install](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/install.md#7-your-own-agents-and-models)). Record runs from the SDK and CI instead |
| Sign-in fails after a Secret value was changed | The database and stored credentials still use the first values. Restore the original values from your secret store |

## The licence

On the on-premises image, every organization’s edition comes from the licence file, never from an organization’s plan. The backend verifies the file offline, checks it at start-up and every five minutes, and compares its dates with the clock on every request:

| State | When | Edition |
| --- | --- | --- |
| `valid` | Between the licence’s issue and expiry dates | On-Premises, with the features and limits the licence lists |
| `grace` | For the licence’s grace days after expiry; each check logs a warning | On-Premises, as `valid` |
| `expired`, `not_yet_valid`, `missing`, `invalid` | After the grace period, before issue, no file at the path, or a file the image refuses | Community |

On the Community edition the paid features, review queues and Monitoring among them, are refused, every free feature keeps working, and reviews already recorded stay readable. A licence that is not in force never stops the backend from starting. To renew, replace the Secret’s file (`kubectl create secret generic martian-evals-licence --from-file=licence.json=<new file> --dry-run=client -o yaml | kubectl -n martian-evals apply -f -`); the API reads it again within five minutes and no restart is needed. No setting turns an on-premises image into a hosted one.

## Network use

The chart installs nothing that calls out by itself. What each part connects to:

| Part | Connects to |
| --- | --- |
| Backend API | PostgreSQL and MLflow in the release. Then only what an organization configures: its identity provider (single sign-on), the endpoint of a judge, and an agent’s address, which the API resolves and, for an agent, calls once to validate it |
| Evals worker | PostgreSQL and MLflow, and the model endpoint a judge names. A remote runner of yours calls an agent; the worker does not |
| MLflow | PostgreSQL and, if you chose object storage, your bucket |
| Console | Nothing. It serves static files |
| PostgreSQL, migrate and seed jobs | PostgreSQL only (the jobs) |

The chart sets what keeps it so: MLflow’s usage telemetry is off (`MLFLOW_DISABLE_TELEMETRY=true`) and MLflow’s model-price catalogue, which it downloads from github.com by default when a trace carries a model call, is not (`MLFLOW_MODEL_CATALOG_URI` is empty). With it empty no model call on a trace is priced. To price them, point `mlflow.modelCatalogUri` at a mirror of that catalogue inside your network. Invitation e-mail through a cloud mail service and the hosted red-team admission are off, and the chart sets no address for the Red Team engine, the Wiki or the sandbox orchestrator.

The chart adds NetworkPolicies for the pods that reach MLflow and PostgreSQL, and none for egress. A cluster that denies egress by default must let the backend and the worker reach PostgreSQL, MLflow, DNS and the endpoints above, and MLflow reach PostgreSQL and your bucket. Martian Security’s tests run the Evals core with the network blocked and fail on any outbound attempt; an installation of this chart on a cluster that denies egress has not been run yet.

## Upgrades

A release is identified by the backend’s schema revision. To see yours:

```sh
kubectl -n martian-evals exec deploy/martian-evals-backend -c backend -- alembic current
```

These are the supported upgrade paths. Each is tested by Martian Security’s CI with containers: a database seeded by the earlier release is upgraded, the backend serves its data, the earlier release’s backend serves the upgraded database again, and a backup of the earlier release restores.

| Installed schema | Upgrades to | Upgrade | Rollback |
| --- | --- | --- | --- |
| The release this chart installs | No later release yet |  |  |
| `0050` | The release this chart installs | Tested | Tested, with the [limits below](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#what-a-rollback-cannot-keep) |
| `0048` | The release this chart installs | Tested | Tested, with the [limits below](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#what-a-rollback-cannot-keep) |
| Earlier than `0048` |  | Not supported | Not tested |

`0048` and `0050` are backend releases before the one the chart installs. Upgrade only along a row of this table, to a chart and images that Martian Security gives you. When a release ships, its schema is added to the table.

### Upgrade

1.  Wait until no run or scoring job is in progress. A restart of the backend gives its work back to the queue, and the work resumes, but an upgrade under running work is not tested.
2.  [Back up](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#back-up) all three databases, the artifacts and the Secrets.
3.  Note the current Helm revision (`helm -n martian-evals history martian-evals`) and schema revision (`alembic current`, above). A rollback needs the Helm revision.
4.  Run `helm upgrade martian-evals ./martian-evals-<new version>.tgz --namespace martian-evals -f values.yaml --wait --wait-for-jobs --timeout 15m`. The migrate job runs before the new backend starts, while the current backend keeps serving. It takes seconds: about 20 s on an empty database and 20 to 25 s from `0048` or `0050` on a small one, almost all of it the Evals schema’s own steps. The larger the database, the longer the few migrations that read a whole table; the time on a large database has not been measured for every revision.
5.  Change the MLflow image only with Martian Security’s instructions for that release. A new MLflow release can need its database migrated while MLflow is stopped, and the chart does not do that step: MLflow refuses to start until it is done.

**Expected result.** `alembic current` prints the new revision with `(head)`, the Evals schema check under [Health and monitoring](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#health-and-monitoring) prints the same revision twice, and members sign in and see their runs.

### Roll back

Do not downgrade the database. The backend refuses to take its schema back below the audit log, evidence sign-offs and release gates, because those are records that must be kept, and a refused downgrade changes nothing. A rollback is one of two things, and both are tested.

**Run the previous release.** `helm rollback` does not change the database, so the previous backend starts on the upgraded database and ignores what it does not know. Use the Helm revision you noted before the upgrade:

```sh
helm -n martian-evals rollback martian-evals <previous Helm revision> --wait --timeout 15m
```

**Expected result.** The previous backend and worker are `Ready`, `alembic current` prints the upgraded revision, and members sign in and see their runs. Upgrade again when the cause is fixed.

**Restore the backup.** If the release changed the MLflow image, if the previous release does not enforce something you need ([below](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#what-a-rollback-cannot-keep)), or if you want the data as it was, restore the backup you took before the upgrade into the previous chart and images: run `helm rollback`, then [restore](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#restore) from step 2.

### What a rollback cannot keep

When the previous release runs on the upgraded database, what the newer one wrote stays in the database and is not shown by the older one:

-   **Evals work done after the upgrade:** runs launched or recorded through the console and the SDK, their results, scores, scoring jobs, reviews, suites, dataset drafts and saved views, and datasets published since. Runs uploaded by the CI gate stay.
-   **What the newer release added:** single sign-on settings, custom roles, provisioning, provider keys, the audit log, applications and release gates, evidence sign-offs, retention policies and holds, and remote runner keys.
-   **What the previous release does not enforce:** an organization that turned password sign-in off to require single sign-on can sign in with its password again, the audit log gets no new entries, and no retention pass deletes anything, until you upgrade again. Where that matters, restore the backup instead.
-   **MLflow** keeps whatever schema its image migrated to; the chart does not take it back.

Restoring the backup taken before the upgrade gives back everything as it was then, and loses everything since.

## Next

-   [Install](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/install.md)
-   [Size an installation](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/sizing.md)
