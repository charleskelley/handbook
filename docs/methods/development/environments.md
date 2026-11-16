---
title: "Development environments"
type: general
owner: mle-lead
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-11
review_cadence: 180d
tags: [environments, development]
---

# Development environments

Where the team writes code, and the rules that make every place the same. There
are three ways of working. One set of files in each project makes all three
identical, and none of them is production: see
[Path to production](path-to-production.md) for how code gets there.

| Way of working | Use it for | Where it runs |
|---|---|---|
| **Cloud Workstation** | Daily development: packages, pipelines, database work, anything touching data | A small cloud machine per person, in the dev project |
| **Laptop** | Tests, harnesses, tools, and small code that needs no real data | The laptop, with synthetic data only |
| **Research VM or Vertex AI job** | Work needing a lot of memory or a GPU | A large VM per person on request, or a Vertex AI custom job |
| **Workbench notebook** | Exploration and research write-ups | A Vertex AI Workbench instance running the team image |

## What makes them the same

Each project carries its own environment, so it is the same on a laptop, a
workstation, a research VM, and in CI:

- **`pyproject.toml` and `uv.lock`** pin every package. The lockfile covers every
  platform, so one lock resolves on an arm64 Mac and an x86 Linux VM.
- **Python {{ platform.dev.python_version }}** is pinned in `.python-version` and
  installed by uv.
- **`.env`** holds settings, read by the code itself, by `uv run --env-file .env`,
  and by VS Code and PyCharm run configurations. IDE remote interpreters ignore
  shell setup, so nothing may depend on it. `.env.example` is committed, `.env`
  is not, and secrets never go in either: see
  [Secret manager](../../technology/secrets.md). It also names the
  [MLflow server](../../technology/mlflow.md), so a run logged from any of the
  three places lands in the same experiment.
- **Each machine's uv configuration** points at Artifactory for packages and for
  Python itself. The Mac bootstrap, the workstation image, and the research VM
  startup script write it. Projects do not name an index.

## Data never lands on a machine

Development can read production data, including personal data. So:

- **Datasets are created only in BigQuery or the governed bucket.** Each person
  has a dataset, `dev_<name>`, whose tables expire after
  {{ platform.dev.dev_table_expiry_days }} days, and a folder in the dev bucket,
  `users/<name>/`, whose files expire after
  {{ platform.dev.dev_scratch_expiry_days }} days. Anything worth keeping moves
  to a team dataset or the `team/` folder.
- **Home disks and laptops hold code, environments, and caches.** Never a
  dataset, an extract, or a "temporary" Parquet file.
- **Laptops never touch personal data.** Local work uses synthetic data.
- **Notebook outputs are stripped before commit**, because a displayed DataFrame
  is data written to git. A pre-commit hook does it and CI rejects notebooks
  that still have outputs.
- **Tests use synthetic data.** Real rows never appear in fixtures or logs.
- **Models trained on personal data are governed data** and are stored like it.

## Cloud Workstations

The default place to work. One {{ platform.dev.workstation_machine_type }}
workstation per person, created by the team's Terraform. See
[Cloud Workstations](../../technology/cloud-workstations.md).

- **The image is rebuilt, never patched.** CI builds it, and every start
  recreates the container from it. Changes to tools go into the image.
- **`/home` persists, as a cache.** It is {{ platform.dev.workstation_home_disk_gb }}GB
  and holds your clones, `.venv`, and editor indexes, so restarts are fast.
  Nothing on it may be the only copy: push work-in-progress branches.
- **It stops itself** after {{ platform.dev.workstation_idle_minutes }} minutes
  idle, and after {{ platform.dev.workstation_max_hours }} hours running.
- **Editors connect over SSH.** VS Code is the default
  ([how to connect](../../technology/connect-vs-code.md)). JetBrains works
  the same way through the Toolbox App, with the PyCharm backend already in the
  image ([how to connect](../../technology/connect-jetbrains.md)).
- **You use your own identity for data.** Run `gcloud auth login` and
  `gcloud auth application-default login` on the workstation. The workstation's
  service account only reads the Artifactory token.

Replace your workstation whenever the image changes, or every quarter. If
anything is lost, a rule above was broken, and it is cheaper to find out then.

## Laptops

For tests, harnesses, tools, and anything that needs no real data. No Homebrew
and no Docker: the [Mac setup](../../technology/set-up-a-mac.md) installs uv,
Python, tools, and the Google Cloud CLI from Artifactory. Docker is left out on
purpose: laptops are arm64 and production is x86, so a local image is either a
different build or an emulated one, and uv's lockfile already gives the same
package versions.

## Research VMs and Vertex AI jobs

For work too big for a workstation. Workstations charge a management fee per
vCPU, which makes large machines much dearer than plain VMs, so large work runs
elsewhere:

- **A batch job** (a training sweep, a large feature build) goes to a Vertex AI
  custom job from the workstation. It runs the same package code and stops when
  it finishes, and it looks like the production job it may become.
- **Interactive work** that needs memory or a GPU goes to a research VM: CPU
  profiles with 128GB or 256GB, or a GPU profile. It stops at
  {{ platform.dev.research_vm_stop }}, and there is no option to turn that off.
  See [Research VMs](../../technology/research-vms.md).

## Notebooks

Research only. A Workbench instance runs the team image built from the same
lockfile, so a notebook has the same packages as the project. A notebook imports
the project's package; the package never imports a notebook. Results worth
keeping move into the package with a test, and the research run the production
gate will reproduce is logged to [MLflow](experiment-tracking.md) with its
fixture. See
[Start a Workbench notebook](../../technology/start-a-workbench-notebook.md).

## Other languages

Python is wired end to end. Rust, Go, Node and TypeScript, Java, Scala for Spark
on Dataproc, and C, C++, and CUDA follow the same three-part pattern when a
project first needs them: a registry config pointing at Artifactory, a toolchain
mirror, and a committed lockfile that CI enforces. See
[Add a language toolchain](../../technology/add-a-language-toolchain.md).
