"""The production training pipeline on Vertex AI Pipelines.

The pipeline runs one step: the released container running `example-model train`.
It trains with the packaged config, checks the reproduction gate, saves the model
to the governed bucket, and registers it as challenger.
"""

# No `from __future__ import annotations`: KFP reads the component annotations as types.
from example_model.config import Settings


def compile_pipeline(image: str, path: str, env: dict[str, str] | None = None) -> str:
    from kfp import compiler, dsl

    @dsl.container_component
    def train_step(config: str, model_version: str):
        return dsl.ContainerSpec(
            image=image,
            command=["example-model"],
            args=["train", "--config", config, "--model-version", model_version, "--register"],
        )

    @dsl.pipeline(name="example-model-train")
    def train_pipeline(config: str = "train", model_version: str = "0"):
        task = train_step(config=config, model_version=model_version)
        for name, value in (env or {}).items():
            task.set_env_variable(name, value)

    compiler.Compiler().compile(train_pipeline, path)
    return path


def submit(
    settings: Settings, image: str, model_version: str, service_account: str, root: str
) -> str:
    """Compile and submit a pipeline run. Returns the run's resource name."""
    import tempfile

    from google.cloud import aiplatform

    aiplatform.init(project=settings.gcp_project, location=settings.region)
    with tempfile.TemporaryDirectory() as tmp:
        env = {
            "EXAMPLE_MODEL_GCP_PROJECT": settings.gcp_project or "",
            "EXAMPLE_MODEL_REGION": settings.region,
            "EXAMPLE_MODEL_MODEL_BUCKET": settings.model_bucket,
            "EXAMPLE_MODEL_SERVING_IMAGE": image,
            "EXAMPLE_MODEL_GIT_COMMIT": settings.git_commit or "",
        }
        if settings.tracking_uri:
            env["EXAMPLE_MODEL_TRACKING_URI"] = settings.tracking_uri
        if settings.experiment:
            env["EXAMPLE_MODEL_EXPERIMENT"] = settings.experiment
        env["EXAMPLE_MODEL_ENVIRONMENT"] = "production"
        spec = compile_pipeline(image, f"{tmp}/pipeline.json", env)
        job = aiplatform.PipelineJob(
            display_name=f"{settings.model_name}-train-{model_version}",
            template_path=spec,
            pipeline_root=root,
            parameter_values={"config": "train", "model_version": model_version},
        )
        job.submit(service_account=service_account)
    return job.resource_name
