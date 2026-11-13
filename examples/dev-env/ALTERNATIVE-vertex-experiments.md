# Fallback: experiment tracking on Vertex AI Experiments

Use this if the MLflow server (one Cloud Run service and one Cloud SQL
instance, `infra/modules/mlflow/`) is not approved. It keeps everything the
handbook says about fixtures, the reference run, the gate, and the feature rule,
and swaps only the tracker. Written so that a later session, human or
assistant, can carry it out from this file and the current `project/`.

## What does not change

- `data.split`, `features.py`, `fixture.py`, `gate.py`, `train.py`: the fixture
  is still the holdout with scores in the governed bucket, the gate still checks
  metric tolerance and rank agreement, the reference block in `train.yaml` has
  the same fields.
- `example-model reference <run_id>` still writes the reference block and still
  refuses dirty or fixture-less runs.
- The handbook pages: replace "MLflow" with "Vertex AI Experiments" on
  `experiment-tracking.md`, remove `technology/mlflow.md` and its nav entry,
  restore the Experiments row and the research-runs edge on `vertex-ai.md`, and
  rewrite DR-0003's decision to this fallback with MLflow as the alternative
  considered.

## What changes

### `tracking.py`

Same public surface (`run`, `Run.params`, `Run.metrics`, `Run.dataset`,
`Run.fixture`, `runs`, `reference_from_run`, `standard_tags`, `git_state`),
implemented on `google.cloud.aiplatform`:

| MLflow | Vertex AI Experiments |
|---|---|
| `mlflow.set_tracking_uri`, `set_experiment` | `aiplatform.init(project, location, experiment=settings.experiment or model_name)` |
| `mlflow.start_run(run_name, tags)` | `aiplatform.start_run(run_name)`; tags become params with a `tag_` prefix, because runs have no tags |
| `mlflow.log_params` / `log_metrics` | `aiplatform.log_params` (float, int, str only: stringify the rest) / `aiplatform.log_metrics` |
| `mlflow.log_input(from_pandas(...))` | No dataset API: log `table`, `as_of`, row count, and a content digest of the frame (`fixture.digest`) as params |
| `mlflow.search_runs(experiment_names=[...])` | `aiplatform.get_experiment_df(experiment)`; columns are `param.*` and `metric.*` |
| `mlflow.get_run(run_id).data` | `aiplatform.ExperimentRun(run_name, experiment=...)`, then `.get_params()` and `.get_metrics()` |
| run id | The run name. Make it unique: `f"{name}-{datetime.now(UTC):%Y%m%d%H%M%S}"` |
| artifacts | Not available without a TensorBoard instance. Save the statsmodels summary or a loss curve next to the fixture in the bucket and log its URI as a param |

Drop the `mlflow_auth.py` plugin and its entry point; Vertex uses Application
Default Credentials. Drop the `track` extra and move the tracker into the `gcp`
extra (`google-cloud-aiplatform` is already there). Remove `mlflow` from the dev
group.

### Settings and environment

`Settings.tracking_uri` goes; `experiment` stays. `.env.example` keeps
`EXAMPLE_MODEL_EXPERIMENT` and drops the tracking URI. The CI train job sets
`EXAMPLE_MODEL_EXPERIMENT` instead of `EXAMPLE_MODEL_TRACKING_URI`;
`pipeline.py` already forwards `EXAMPLE_MODEL_EXPERIMENT`. The production
training service account needs `roles/aiplatform.user` in the project that holds
the experiment. Decide whether that is the dev project (research and production
runs side by side, cross-project access) or the prod project (two experiments,
one per project); side by side is better for the gate's audit trail.

### Tests

The tracking and CLI tests use a SQLite MLflow store. Vertex has no local store,
so replace them with tests against a fake: a small in-memory `aiplatform` stub
with `init`, `start_run`, `log_params`, `log_metrics`, `get_experiment_df`, and
`ExperimentRun`, patched into `tracking` with `monkeypatch`. Keep the same
assertions: tags present, dataset params present, `reference_from_run` refuses
dirty runs and runs without a fixture, the CLI writes the config and keeps its
comments.

### Infrastructure

Delete `infra/modules/mlflow/`, `mlflow-image/`, the `mlflow` module call and
the `mlflow_image_tag` variable in `infra/envs/dev/`, the `mlflow_url` output,
and the `random` provider. Keep `team_readers` on the user-data module: the
production training account still reads fixtures. Add `roles/aiplatform.user`
for that account in whichever project holds the experiment.

### Facts and pages

Remove the `mlflow` component and `platform.dev.mlflow_url` from
`facts/platform.yaml`. On `experiment-tracking.md`, state what is lost and the
workaround: no dataset digest (logged as params instead), no artifacts without
TensorBoard (saved beside the fixture), comparison in `get_experiment_df` and
the console rather than a compare view, and `autolog()` available through
`aiplatform.autolog()` for scikit-learn and statsmodels with the same
reservations.

## Verify before relying on it

- `aiplatform.start_run`, `log_params`, `log_metrics`, `get_experiment_df`, and
  `ExperimentRun.get_params` / `get_metrics` exist with these signatures in the
  pinned `google-cloud-aiplatform`.
- Parameter and metric count limits per run, which Google's docs do not state.
- Whether a run name may be reused across experiments.
