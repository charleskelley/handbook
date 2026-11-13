"""Vertex AI Model Monitoring v2: drift between the training snapshot and the prediction log.

Created when a version is promoted to champion. The baseline is the training
snapshot the version was trained on; the target is the prediction log, a daily
window. Feature drift and prediction drift only: attribution needs the model to
be served on Vertex AI, and it is not. Alerts go to the configured emails.
"""

from __future__ import annotations

from example_model.config import Settings, TrainConfig


def schema(config: TrainConfig):
    from vertexai.resources.preview import ml_monitoring

    spec = ml_monitoring.spec
    return spec.ModelMonitoringSchema(
        feature_fields=[spec.FieldSchema(name=f, data_type="float") for f in config.features],
        prediction_fields=[spec.FieldSchema(name="score", data_type="float")],
        ground_truth_fields=[spec.FieldSchema(name=config.target, data_type="categorical")],
    )


def baseline_query(config: TrainConfig) -> str:
    return f"SELECT * FROM `{config.table}` WHERE as_of_date = DATE '{config.as_of}'"


def ensure_monitor(settings: Settings, config: TrainConfig, registry_version: str) -> str:
    """Create the monitor and its schedule for a model version, once. Returns the monitor name."""
    import vertexai
    from vertexai.resources.preview import ml_monitoring

    spec = ml_monitoring.spec
    vertexai.init(project=settings.gcp_project, location=settings.region)
    display_name = f"{settings.model_name}-v{registry_version}"
    existing = [m for m in ml_monitoring.ModelMonitor.list() if m.display_name == display_name]
    if existing:
        return existing[0].resource_name

    drift = spec.DataDriftSpec(default_numeric_alert_threshold=config.monitoring.drift_threshold)
    objective = spec.TabularObjective(feature_drift_spec=drift, prediction_output_drift_spec=drift)
    output = spec.OutputSpec(gcs_base_dir=f"{settings.reports_bucket.rstrip('/')}/model-monitoring")
    notify = spec.NotificationSpec(user_emails=settings.alert_emails, enable_cloud_logging=True)

    monitor = ml_monitoring.ModelMonitor.create(
        display_name=display_name,
        model_name=settings.model_name,
        model_version_id=registry_version,
        model_monitoring_schema=schema(config),
        training_dataset=spec.MonitoringInput(query=baseline_query(config)),
        tabular_objective_spec=objective,
        output_spec=output,
        notification_spec=notify,
    )
    monitor.create_schedule(
        display_name=f"{display_name}-daily",
        cron=config.monitoring.schedule,
        baseline_dataset=spec.MonitoringInput(query=baseline_query(config)),
        target_dataset=spec.MonitoringInput(
            table_uri=f"bq://{settings.gcp_project}.{settings.predictions_table}",
            timestamp_field="scored_at",
            window="24h",
        ),
        tabular_objective_spec=objective,
        output_spec=output,
        notification_spec=notify,
    )
    return monitor.resource_name
