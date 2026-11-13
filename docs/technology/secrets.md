---
title: "Secret manager"
type: platform
owner: platform-owner
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-11
review_cadence: 180d
tags: [secrets, security]
---

# Secret manager

## What it is for

The only place secrets live. Code never reads a secret from a file in a
repository, a `.env` file, or a notebook. The secret manager of record is
{{ platform.components.secrets.product }}.

## Architecture

```mermaid
flowchart LR
    C[{{ platform.components.secrets.product }}] -- sync --> S[GCP Secret Manager]
    S --> W[Workstations and research VMs]
    S --> R[Cloud Run and pipelines]
    S --> M[Artifact Registry mirrors]
```

Secrets are kept in {{ platform.components.secrets.product }} and synced into
GCP Secret Manager, where Google workloads read them with their service account.
Whether the sync is available depends on the {{ platform.components.secrets.product }}
license: *[unverified: needs source]*. Without it, code reads the secret
manager of record directly, behind the same small function.

## How we use it

- **Workloads** read secrets from GCP Secret Manager with their service account.
- **People** do not handle machine secrets. Artifactory uses your own identity
  token; data uses your own Google identity.
- **CI** holds no secrets: it exchanges identity tokens.
- **Local code** reads settings from `.env` and secrets from the secret manager,
  so the same code runs everywhere.

## Limits and quotas

None that affect the team: *[unverified: needs source]*.

## Owner and support path

Owner: {{ platform.components.secrets.owner }}. Support:
{{ platform.components.secrets.support_channel }}.

## Runbooks

- **A token expired.** Rotate it in {{ platform.components.secrets.product }};
  the sync updates Secret Manager, and machines pick it up at their next start.
- **A secret was committed.** Rotate it first, then remove it from history.
