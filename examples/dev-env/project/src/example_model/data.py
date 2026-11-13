"""Data access. Reads into memory only: datasets live in BigQuery or governed buckets."""

from __future__ import annotations

import hashlib

import pandas as pd

from example_model.config import Settings, TrainConfig


def load_frame(settings: Settings, table: str, as_of: str) -> pd.DataFrame:
    """Read one snapshot of a feature table from BigQuery.

    The frame remembers where it came from in ``frame.attrs``, so a tracked run
    can log the dataset without the caller repeating it.
    """
    from google.cloud import bigquery

    client = bigquery.Client(project=settings.gcp_project)
    job = client.query(
        f"SELECT * FROM `{table}` WHERE as_of_date = @as_of",
        job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("as_of", "DATE", as_of)]
        ),
    )
    frame = job.to_dataframe()
    frame.attrs["source"] = {"table": table, "as_of": as_of}
    return frame


def write_frame(settings: Settings, frame: pd.DataFrame, table: str) -> None:
    """Write results to a BigQuery table, replacing its contents."""
    from google.cloud import bigquery

    client = bigquery.Client(project=settings.gcp_project)
    config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    client.load_table_from_dataframe(frame, table, job_config=config).result()


def append_frame(settings: Settings, frame: pd.DataFrame, table: str) -> None:
    """Append rows to a BigQuery table, such as the prediction log."""
    from google.cloud import bigquery

    client = bigquery.Client(project=settings.gcp_project)
    # Feature columns are not in the table's Terraform schema: allow adding them.
    config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION],
    )
    client.load_table_from_dataframe(frame, table, job_config=config).result()


def query(settings: Settings, sql: str) -> pd.DataFrame:
    from google.cloud import bigquery

    return bigquery.Client(project=settings.gcp_project).query(sql).to_dataframe()


def _bucket(entity_id: object, seed: int) -> int:
    digest = hashlib.blake2b(f"{entity_id}:{seed}".encode(), digest_size=8).digest()
    return int.from_bytes(digest, "big") % 10_000


def split(frame: pd.DataFrame, config: TrainConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Deterministic train and holdout split by hashing the entity id.

    The same entity lands in the same partition in a notebook, on a workstation,
    and in the production pipeline, so the holdout can be saved as the fixture
    the gate scores, and production never trains on fixture rows.
    """
    cutoff = int(config.test_size * 10_000)
    buckets = frame[config.entity_id].map(lambda e: _bucket(e, config.seed))
    holdout = buckets < cutoff
    return frame[~holdout].reset_index(drop=True), frame[holdout].reset_index(drop=True)
