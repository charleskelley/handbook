# Development environment and path to production: skeleton

A working skeleton for the practices in the handbook's
[Development environments](../../docs/methods/development/environments.md) and
[Path to production](../../docs/methods/development/path-to-production.md) pages.
The pages quote these files. In a real organization each top-level directory is
its own repository.

| Directory | What it is | Handbook page |
|---|---|---|
| `bootstrap/` | Mac setup with no Homebrew: uv, Python, tools, gcloud, all from Artifactory | Set up a Mac |
| `workstation-image/` | The Cloud Workstations image and the CI job that builds it | Cloud Workstations |
| `mlflow-image/` | The MLflow server image and the CI job that builds it | MLflow |
| `infra/modules/mlflow/` | The tracking server: Cloud Run, Cloud SQL, artifact bucket | MLflow, Experiment tracking |
| `ALTERNATIVE-vertex-experiments.md` | The fallback if the MLflow server is not approved | DR-0003 |
| `project/src/example_model/{score,serve,performance,monitoring,report}.py` | Prediction log, lookup service, labeled performance, Model Monitoring, Evidently | Model monitoring, Path to production |
| `ssh/` | SSH entries for a workstation tunnel and IAP research VMs | Connect VS Code, Connect JetBrains |
| `infra/modules/artifactory/` | Dev and release local repositories, remotes, virtual repositories | Artifactory |
| `infra/modules/registry-mirror/` | Artifact Registry pull-through cache of Artifactory, for Google runtimes | Artifactory |
| `infra/modules/workstations/` | One workstation per person, home disk as cache | Cloud Workstations |
| `infra/modules/user-data/` | Per-person BigQuery dataset and governed bucket folder, with expiry | Development environments |
| `infra/modules/research-vm/` | Large-memory and GPU VMs that always stop on a schedule | Research VMs |
| `infra/envs/` | The dev project, the prod project, and Artifactory | |
| `project/` | An ML project: package, tests, notebook rules, Dockerfile, GitLab pipeline | Path to production |

## Placeholders

Every value a fork must replace is an obvious placeholder: `artifactory.example.com`,
`your-dev-project`, `your-prod-project`, `example.com` emails, the
workload identity provider number `000000000000`, and the JetBrains versions
`0.0.0.00000` and `pycharm-0000.0` in `workstation-image/.gitlab-ci.yml`. Search
for them before use.

## What has been checked

- `project/`: the tests pass (including the tracking and gate tests against a
  SQLite MLflow store, and the Evidently report build), ruff is clean, the wheel builds with the config inside
  it, the MLflow plugin entry point resolves, the Vertex AI pipeline compiles,
  and the Vertex AI SDK calls in `registry.py` and `pipeline.py` exist with the
  arguments used.
- `infra/`: every file parses as HCL, and every module call matches the
  module's variables. **`terraform validate` has not been run**, so resource
  attribute names against the provider schemas are unchecked. Run
  `terraform init -backend=false && terraform validate` in each `envs/`
  directory first.
- Shell scripts pass a syntax check. The startup script template was rendered
  and checked.
- `.gitlab-ci.yml` parses as YAML. It has not run in GitLab.

## What to confirm with your platform before relying on it

1. **JFrog OIDC from GitLab.** `scripts/ci/artifactory-auth.sh` uses the JFrog
   Platform token exchange endpoint. Confirm your JFrog version supports an
   OIDC integration for GitLab, and the provider name.
2. **Artifact Registry remote repository to Artifactory.** Confirm the image
   path form through the mirror (`<mirror>/<artifactory-repo>/<image>`) with one
   test pull.
3. **The PyPI layout in Artifactory.** `scripts/ci/promote.py` copies
   `<package>/<version>/` between local repositories. Check one published
   release's path.
4. **Egress.** Workstations and research VMs have no external IP. They reach
   Artifactory through Cloud NAT or private connectivity.
5. **The perimeter.** A VPC Service Controls perimeter around the dev project
   is assumed and is not in this Terraform: it is set at the organization level.
6. **JetBrains versions.** The workstation image bakes in the Toolbox Agent and
   the PyCharm backend from `download.jetbrains.com` through Artifactory.
   Confirm the PyCharm archive path from the JetBrains releases API, and that
   the software portal ships the Toolbox App build the image was built with:
   the Agent and the App must match exactly.
7. **Cloud Run accepts user identity tokens.** `mlflow_auth.py` sends the
   token from `gcloud auth print-identity-token` for people. Cloud Run accepts
   gcloud user tokens for IAM-authenticated services; confirm with one `curl`
   from a workstation before the first run is logged.
8. **Cloud SQL private IP.** The MLflow module puts the database on the VPC,
   which needs Private Services Access configured on the network. Cloud Run
   reaches it through the Cloud SQL connector volume either way.
9. **Model Monitoring inputs.** `monitoring.py` passes a BigQuery query as the
   training dataset and as the scheduled baseline, and the prediction log with
   `timestamp_field` as the target. The SDK signatures accept this; confirm a
   first scheduled run completes.
10. **Cloud Scheduler to Cloud Run jobs.** The schedules call the Cloud Run
    Jobs `run` API with the scheduler service account. The jobs must exist
    (the deploy job creates them) before the IAM bindings apply.
11. **Prediction log schema.** Feature columns are added on first append with
    `ALLOW_FIELD_ADDITION`. Changing a feature's type later needs a new table.
12. **`pandas<3`.** Pinned because Evidently 0.7 does not import under pandas 3.
    Lift the pin when it does.
13. **`uv.lock`.** Not committed here, because a lock made against public PyPI
   records the wrong index. Run `uv lock` once against your Artifactory and
   commit it; CI uses `--locked`.
