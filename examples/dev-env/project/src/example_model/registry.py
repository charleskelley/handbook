"""The only module that knows where models live.

Model bytes go to a governed bucket in an open format, with a metadata file. The
Vertex AI Model Registry catalogs them by pointer. Changing registries changes
this file and nothing else.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version

import fsspec
import joblib

from example_model.config import Settings, TrainConfig


def package_version() -> str:
    try:
        return version("example-model")
    except PackageNotFoundError:
        return "unknown"


def artifact_uri(settings: Settings, model_version: str) -> str:
    return f"{settings.model_bucket.rstrip('/')}/{settings.model_name}/{model_version}"


def save(
    settings: Settings,
    model: object,
    metrics: dict[str, float],
    config: TrainConfig,
    model_version: str,
) -> str:
    """Write the model and its metadata. Returns the artifact URI."""
    uri = artifact_uri(settings, model_version)
    with fsspec.open(f"{uri}/model.joblib", "wb") as f:
        joblib.dump(model, f)
    metadata = {
        "model_name": settings.model_name,
        "model_version": model_version,
        "package_version": package_version(),
        "git_commit": settings.git_commit,
        "data": {"table": config.table, "as_of": config.as_of},
        "config": config.model_dump(),
        "reference_run_id": config.reference.run_id,
        "metrics": metrics,
        "created_at": datetime.now(UTC).isoformat(),
    }
    with fsspec.open(f"{uri}/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    return uri


def load(uri: str) -> object:
    with fsspec.open(f"{uri.rstrip('/')}/model.joblib", "rb") as f:
        return joblib.load(f)


def _model_resource(settings: Settings) -> str:
    """The registry ID is the model name, so versions and aliases are addressable."""
    return settings.model_name


def register(settings: Settings, uri: str, alias: str = "challenger") -> str:
    """Catalog a saved model in the Vertex AI Model Registry. Returns the version ID."""
    from google.api_core.exceptions import NotFound
    from google.cloud import aiplatform

    aiplatform.init(project=settings.gcp_project, location=settings.region)
    try:
        parent = aiplatform.Model(_model_resource(settings)).resource_name
    except NotFound:
        parent = None
    model = aiplatform.Model.upload(
        display_name=settings.model_name,
        model_id=None if parent else _model_resource(settings),
        parent_model=parent,
        artifact_uri=uri,
        serving_container_image_uri=settings.serving_image,
        version_aliases=[alias],
    )
    return model.version_id


def promote(settings: Settings, registry_version: str, alias: str = "champion") -> None:
    """Move an alias, such as champion, to a registered version."""
    from google.cloud import aiplatform

    aiplatform.init(project=settings.gcp_project, location=settings.region)
    registry = aiplatform.models.ModelRegistry(_model_resource(settings))
    registry.add_version_aliases([alias], registry_version)


def resolve(settings: Settings, alias: str = "champion") -> str:
    """The artifact URI of the version holding an alias."""
    from google.cloud import aiplatform

    aiplatform.init(project=settings.gcp_project, location=settings.region)
    return aiplatform.Model(f"{_model_resource(settings)}@{alias}").uri
