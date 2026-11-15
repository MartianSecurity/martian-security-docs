# Size an Evals installation

> Resources, volumes and limits of the martian-evals Helm chart, the one-process-per-run rule, and what is and is not measured.

Source: [Web version](https://docs.martiansecurity.ai/on-premises/sizing/)

Plan CPU, memory and storage for an installation of the `martian-evals` chart ([install](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/install.md)). This page gives the chart’s defaults, the rule that decides the backend’s memory, and the storage figures that have been measured.

**What is measured.** The storage and database figures below come from Martian Security’s load test of MLflow’s SQL store on PostgreSQL, the store this chart’s MLflow server uses. No load test of a whole installation of this chart has been run yet: response times through the API and the resources a run’s process uses are not measured. Start from the defaults and watch the installation as described in [operations](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#health-and-monitoring).

## Defaults

| Workload | Replicas | CPU request | Memory request | Memory limit | Volume | Values |
| --- | --- | --- | --- | --- | --- | --- |
| Backend, with its run and scoring processes | 1 | 500m | 1 GiB | 2 GiB | none | `backend.replicas`, `backend.resources` |
| Console | 1 | 50m | 64 MiB | 128 MiB | none | `frontend.replicas`, `frontend.resources` |
| MLflow | 1, fixed | 1 | 2 GiB | 4 GiB, 2 CPU | 20 GiB artifacts | `mlflow.resources`, `mlflow.workers`, `mlflow.artifacts.persistence.size` |
| PostgreSQL (bundled) | 1, fixed | 500m | 1 GiB | 2 GiB | 20 GiB data | `postgres.resources`, `postgres.size` |
| Migrate job, at install and upgrade | 1 | 100m | 256 MiB | 1 GiB | none | `backend.migration.resources` |

In total about 2 CPUs and 4 GiB of memory are requested, with memory limits of about 8 GiB, plus 40 GiB of volumes. The volume sizes are starting points; size them from the [storage figures](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/sizing.md#storage). Volumes use your default StorageClass unless you set `postgres.storageClassName` and `mlflow.artifacts.persistence.storageClassName`.

MLflow and PostgreSQL run as one pod each, and MLflow replaces its pod rather than rolling it, so each is briefly unavailable when it restarts. There is no failover; plan for this in your maintenance windows.

## One process per run

Each eval run and scoring job that the backend executes runs in a process of its own, started by the backend process that admitted it, inside the same container. MLflow keeps per-process state, so two organizations’ work must never share a process.

That has three consequences:

-   **Memory.** The backend container’s memory limit covers the API and every process it has started. When the limit is reached, Kubernetes stops the container, and with it every run in it. The memory of one run’s process is not measured yet. Raise `backend.resources.limits.memory` when several organizations run or score at the same time, and watch for restarts with the reason `OOMKilled`.
-   **Concurrency.** Each organization’s plan bounds how much work it has at once: **Enterprise**, the default, allows 5 runs and 5 scoring jobs in progress; **Community** allows 1 of each. A request beyond the bound is refused, not queued. The worst case for the backend is therefore 10 processes per active organization.
-   **Restarts.** A backend restart, for an upgrade, a values change or a crash, ends the processes it was running. Their runs and scoring jobs stay **running** until someone stops them. Change the installation when no work is in progress ([upgrades](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#upgrades)).

With this chart, most processes are scoring jobs on saved results. Runs from the SDK and CI execute in your own environment and are uploaded; they use no process in the backend.

A run stays with the backend replica that started it. The chart defaults to one replica.

## Storage

Most of the database is MLflow’s traces. Measured on MLflow’s SQL store on PostgreSQL 17, with traces of 5 spans and 1,000-character requests, responses and span payloads:

| Traces in a project | Database size | Per trace |
| --- | --- | --- |
| 10,000 | 180 MB | 18 KB |
| 100,000 | 1.7 GB | 17 KB |

-   Storage grows linearly, about **1.7 GB per 100,000 traces** of that shape. Larger traces take more: about 47 KB with 20 spans and 98 KB with 50 spans.
-   Read these as lower bounds. The test text compressed better than real traffic does.
-   PostgreSQL spent about 6 to 9 ms of CPU per trace written, so one core takes on the order of 100 traces a second before disk I/O, which was not measured.
-   Nothing deletes old traces. Plan the volume for the traces you keep, and grow it before it fills.

Run artifacts and review attachments are on the MLflow artifact volume or in your bucket. Their size depends on your use and is not measured.

## Starting points

-   **Evaluation of a few agents by one team:** the defaults.
-   **Several organizations scoring at once:** raise the backend’s memory limit first, by the processes you expect, and its CPU request.
-   **Many traces:** size the PostgreSQL volume from the storage figures, and give PostgreSQL more memory as the database outgrows it.
-   **Your own PostgreSQL:** the same figures apply to its `mlflow_tracking` database.

## Next

-   [Install](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/install.md)
-   [Operate](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md): backups, health, troubleshooting and upgrades.
