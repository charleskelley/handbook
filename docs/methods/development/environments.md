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

Where the team writes code, and the rules that make every place the same.
All of these places are in dev, the environment where people act under their
own identity. None of them is production: see
[Path to production](path-to-production.md#two-environments) for the two
environments and how code gets from one to the other.

| Place | Use it for | Where it runs |
|---|---|---|
| **Cloud workstation** | Daily development: packages, pipelines, database work, anything touching data | A small cloud machine per person |
| **Laptop** | Tests, harnesses, tools, and small code that needs no real data | The laptop, with synthetic data only |
| **Research machine or batch job** | Work needing a lot of memory or a GPU | A large machine per person on request, or a job submitted to the training service |
| **Hosted notebook** | Exploration and research write-ups | A managed notebook instance running the team image |

## What makes them the same

Each project carries its own environment, so it is the same on a laptop, a
workstation, a research machine, and in CI:

- **The project file and the lockfile** pin every package. The lockfile
  covers every platform, so one lock resolves on an arm64 laptop and an x86
  cloud machine.
- **Python {{ platform.dev.python_version }}** is pinned in the project and
  installed by the package manager.
- **A settings file** holds the project's settings, and the code, the command
  line, and the editors' run configurations all read it. An editor's remote
  interpreter ignores shell setup, so nothing may depend on that. An example
  file is committed, the real one is not, and secrets never go in either:
  see [Secret manager](../../technology/secrets.md). The file also names the
  [tracking server](../../technology/mlflow.md), so a run logged from any of
  these places lands in the same experiment.
- **Each machine's package manager configuration** points at the artifact
  registry, for packages and for Python itself. The laptop setup, the
  workstation image, and the research machine's startup write it. Projects
  do not name a package index.

## Data never lands on a machine

Development can read production data, including personal data. So:

- **Datasets are created only in the warehouse or the governed bucket.**
  Each person has a dataset of their own in the warehouse, whose tables
  expire after {{ platform.dev.dev_table_expiry_days }} days, and a folder
  of their own in the dev bucket, whose files expire after
  {{ platform.dev.dev_scratch_expiry_days }} days. Anything worth keeping
  moves to a team dataset or the team folder.
- **Home disks and laptops hold code, environments, and caches.** Never a
  dataset, an extract, or a "temporary" data file.
- **Laptops never touch personal data.** Local work uses synthetic data.
- **Notebook outputs are stripped before commit**, because a displayed table
  is data written to git. A hook does it at commit, and CI rejects notebooks
  that still have outputs.
- **Tests use synthetic data.** Real rows never appear in fixtures or logs.
- **Models trained on personal data are governed data** and are stored like it.

## Cloud workstations

The default place to work. One {{ platform.dev.workstation_machine_type }}
workstation per person, created by the team's infrastructure code. See
[Cloud workstations](../../technology/cloud-workstations.md).

- **The image is rebuilt, never patched.** CI builds it, and every start
  recreates the container from it. Changes to tools go into the image.
- **The home disk persists, as a cache.** It is
  {{ platform.dev.workstation_home_disk_gb }}GB and holds your clones, your
  environments, and editor indexes, so restarts are fast. Nothing on it may
  be the only copy: push work-in-progress branches.
- **It stops itself** after {{ platform.dev.workstation_idle_minutes }} minutes
  idle, and after {{ platform.dev.workstation_max_hours }} hours running.
- **Editors connect over SSH.** VS Code is the default
  ([how to connect](../../technology/connect-vs-code.md)). JetBrains editors
  work the same way
  ([how to connect](../../technology/connect-jetbrains.md)).
- **You use your own identity for data.** You sign in to the cloud as
  yourself on the workstation. The workstation's service account can only
  read the artifact registry token.

Replace your workstation whenever the image changes, or every quarter. If
anything is lost, a rule above was broken, and it is cheaper to find out then.

## Laptops

For tests, harnesses, tools, and anything that needs no real data. The
[laptop setup](../../technology/set-up-a-mac.md) installs the package
manager, Python, tools, and the cloud's command line from the artifact
registry, and nothing comes from a public source. There is no container
engine, on purpose: laptops are arm64 and production is x86, so a local
image is either a different build or an emulated one, and the lockfile
already gives the same package versions.

## Research machines and batch jobs

For work too big for a workstation. A managed workstation costs more for
each core than a plain virtual machine, so large work runs elsewhere:

- **A batch job** (a training sweep, a large feature build) is submitted
  from the workstation to the
  [training service](../../technology/vertex-ai.md). It runs the same
  package code and stops when it finishes, and it looks like the production
  job it may become.
- **Interactive work** that needs memory or a GPU goes to a research
  machine, in a large-memory profile or a GPU profile. It stops at
  {{ platform.dev.research_vm_stop }}, and there is no option to turn that
  off. See [Research machines](../../technology/research-vms.md).

## Notebooks

Research only. A hosted notebook instance runs the team image built from the
same lockfile, so a notebook has the same packages as the project. A
notebook imports the project's package; the package never imports a
notebook. Results worth keeping move into the package with a test, and the
research run the production gate will reproduce is logged to the
[tracking server](experiment-tracking.md) with its fixture. See
[Start a hosted notebook](../../technology/start-a-workbench-notebook.md).

## Other languages

Python is wired end to end. Rust, Go, Node and TypeScript, Java, Scala for
distributed processing, and C, C++, and CUDA follow the same three-part
pattern when a project first needs them: a registry configuration pointing
at the artifact registry, a toolchain mirror, and a committed lockfile that
CI enforces. See
[Add a language toolchain](../../technology/add-a-language-toolchain.md).
