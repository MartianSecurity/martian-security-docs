# Size an Evals installation

> Resources, volumes and limits of the martian-evals Helm chart, the one-process-per-run rule, and what is and is not measured.

Source: [Web version](https://docs.martiansecurity.ai/on-premises/sizing/)

Plan CPU, memory and storage for an installation of the `martian-evals` chart ([install](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/install.md)). This page gives the chart’s defaults, the rule that decides the backend’s memory, and the storage figures that have been measured.

**What is measured.** The storage and database figures below come from Martian Security’s load test of MLflow’s SQL store on PostgreSQL, the store this chart’s MLflow server uses. No load test of a whole installation of this chart has been run yet: response times through the API and the resources a run’s process uses are not measured. Start from the defaults and watch the installation as described in [operations](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#health-and-monitoring).

## Defaults

| Workload | Replicas | CPU request | Memory request | Memory limit | Volume | Values |
| --- | --- | --- | --- | --- | --- | --- |
| Backend API container | 1 | 500m | 1 GiB | 2 GiB | none | `backend.replicas`, `backend.resources` |
| Evals worker container, in the same pod, with the run and scoring processes | 1 | 250m | 768 MiB | 1536 MiB | none | `backend.worker.resources`, `backend.worker.concurrency` |
| Console | 1 | 50m | 64 MiB | 128 MiB | none | `frontend.replicas`, `frontend.resources` |
| MLflow | 1, fixed | 1 | 2 GiB | 4 GiB, 2 CPU | 20 GiB artifacts | `mlflow.resources`, `mlflow.workers`, `mlflow.artifacts.persistence.size` |
| PostgreSQL (bundled) | 1, fixed | 500m | 1 GiB | 2 GiB | 20 GiB data | `postgres.resources`, `postgres.size` |
| Migrate job, at install and upgrade | 1 | 100m | 256 MiB | 1 GiB | none | `backend.migration.resources` |

In total about 2.3 CPUs and 4.8 GiB of memory are requested, with memory limits of about 9.6 GiB, plus 40 GiB of volumes. The volume sizes are starting points; size them from the [storage figures](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/sizing.md#storage). Volumes use your default StorageClass unless you set `postgres.storageClassName` and `mlflow.artifacts.persistence.storageClassName`.

MLflow and PostgreSQL run as one pod each, and MLflow replaces its pod rather than rolling it, so each is briefly unavailable when it restarts. There is no failover; plan for this in your maintenance windows.

## One process per run

The API puts each eval run and scoring job in a queue in the backend’s database. The evals worker, a second container of the backend pod, takes work from the queue and runs each piece in a process of its own, inside that container. MLflow keeps per-process state, so two organizations’ work must never share a process.

That has four consequences:

-   **Memory.** The worker container’s memory limit (1536 MiB by default) covers the worker and every process it has started, each about 250 MB when it starts and more while it works. When the limit is reached, Kubernetes stops the container, and with it every run in it. The memory of a running process beyond its start is not measured yet. Raise `backend.worker.resources.limits.memory` before raising `backend.worker.concurrency`, and watch for restarts with the reason `OOMKilled`. The API container has its own limit and shares none of this.
-   **Concurrency.** `backend.worker.concurrency` (default 2) is how many runs and scoring jobs one worker runs at once, of any organizations; the others wait in the queue, oldest first, and a worker takes the next from the organization with the fewest running. The On-Premises edition sets no limit of its own, so the workers bound what runs at once, unless the licence lists `concurrent_runs` or `concurrent_scoring_jobs`: a launch or a scoring request that would put more than that many queued or running is refused. Without a licence in force an organization runs the Community edition, which allows 1 run and 1 scoring job queued or running.
-   **Restarts.** A restart of either container loses no run. A stopped worker gives its work back to the queue at once. A worker that was killed has its work taken over 30 seconds later. Either way the run resumes after the cases it had finished and calls your agent again for the case that was in flight. Work whose worker was killed three times is marked **failed**. Still, change the installation when no work is in progress ([upgrades](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md#upgrades)).
-   **Replicas.** Every backend pod has its own worker, and all workers take from the same queue, so `backend.replicas` above 1 adds capacity (CPU and memory for each pod) and no run is taken twice. MLflow and PostgreSQL stay single.

With this chart, most processes are scoring jobs on saved results. Runs from the SDK and CI execute in your own environment and are uploaded; they use no process in the backend.

## Storage

Most of the database is MLflow’s traces. Measured on MLflow’s SQL store on PostgreSQL 17, with traces of 5 spans and 1,000-character requests, responses and span payloads:

| Traces in a project | Database size | Per trace |
| --- | --- | --- |
| 10,000 | 180 MB | 18 KB |
| 100,000 | 1.7 GB | 17 KB |

-   Storage grows linearly, about **1.7 GB per 100,000 traces** of that shape. Larger traces take more: about 47 KB with 20 spans and 98 KB with 50 spans.
-   Read these as lower bounds. The test text compressed better than real traffic does.
-   PostgreSQL spent about 6 to 9 ms of CPU per trace written, so one core takes on the order of 100 traces a second before disk I/O, which was not measured.
-   Nothing deletes old traces until a retention policy is set. With a licence that includes retention, a member with the retention permission sets a maximum age, in days, for traces and for runs, for the organization or for a project, under **Organization → Retention**; the backend then deletes what is older, in batches, from every replica, one at a time per project. A legal hold stops deletion. Without a policy, plan the volume for every trace you keep, and grow it before it fills.

Run artifacts and review attachments are on the MLflow artifact volume or in your bucket. Their size depends on your use and is not measured.

## Starting points

-   **Evaluation of a few agents by one team:** the defaults.
-   **Several organizations scoring at once:** raise the backend’s memory limit first, by the processes you expect, and its CPU request.
-   **Many traces:** size the PostgreSQL volume from the storage figures, and give PostgreSQL more memory as the database outgrows it.
-   **Your own PostgreSQL:** the same figures apply to its `mlflow_tracking` database.

## Next

-   [Install](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/install.md)
-   [Operate](https://raw.githubusercontent.com/MartianSecurity/martian-security-docs/main/public/markdown/on-premises/operations.md): backups, health, troubleshooting and upgrades.
