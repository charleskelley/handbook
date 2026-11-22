---
title: "DR-0001: Production runs only CI-built artifacts from the artifact registry"
type: decision-record
owner: mle-lead
audience: [all]
status: draft
last_reviewed: 2026-11-11
review_cadence: 365d
tags: [production, artifacts, ci]
---

# DR-0001: Production runs only CI-built artifacts from the artifact registry

## Context

The team develops on laptops, cloud workstations, research machines, and
notebooks, in several languages, and deploys to one cloud. Without a rule,
anything that works on one of those machines can reach production: a notebook on a schedule, a
container built on a laptop, or an image saved from a VM. Each is hard to
reproduce, hard to audit, and impossible to rebuild after the machine is gone.
Security also requires that machines do not download from public registries.

## Decision

1. Every external input comes through the artifact registry: packages,
   toolchains, OS packages, base images, and pretrained models.
2. Production runs only artifacts built by CI from a commit: packages and
   containers built from them. CI publishes to dev repositories, tests the
   published artifact, and promotes the same bytes to release repositories.
   Production reads only the release repositories.
3. No machine image is ever saved and run in production.
4. No notebook runs in a production pipeline.

## Alternatives considered

- **Everything inside the cloud's ML platform.** Fewer products, but the ML
  platform has no development environment for packaged code, and it does not
  replace the organization's artifact registry and CI, which production
  rules need on any platform. We use the ML platform for the ML-specific
  parts.
- **One local repository per type, with releases told apart by version.**
  Simpler, but the separation rests on discipline, not permissions.
- **Scheduled notebooks in production**, as some large teams do. Rejected: hidden
  state and untested code paths, and notebooks resist review.
- **Saved VM images for production machines.** Rejected: they capture whatever
  was on the machine, and cannot be rebuilt from source.

## Consequences

- Every project needs a lockfile, a package build, and the standard pipeline.
  The project template provides them.
- The cloud's runtimes pull through a cache of the artifact registry kept
  inside the cloud, which must be maintained.
- A release takes a tag and a pipeline run, even for a small fix.
- Untested code cannot reach production by mistake, and every release can be
  traced to a commit and an approval.

## Status

Proposed
