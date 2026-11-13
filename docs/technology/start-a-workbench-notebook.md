---
title: "How to start a Workbench notebook"
type: how-to
owner: mle-lead
audience: [ds, mle]
status: draft
last_reviewed: 2026-11-11
review_cadence: 180d
tags: [notebooks, vertex]
sources:
  - "examples/dev-env/project/notebook-image/Dockerfile"
---

# How to start a Workbench notebook

## Goal

A Vertex AI Workbench notebook with the same packages as your project, for
research.

## Steps

1. Use the project's notebook image, which CI rebuilds from the lockfile on
   every main commit: `<artifactory-host>/docker-dev-local/<project>-notebook:latest`.
2. Create a Workbench instance in {{ platform.dev.gcp_dev_project }} with that
   image as its custom container, idle shutdown on, and no public IP.
3. Clone the project in JupyterLab's terminal and install it in editable mode,
   so notebooks import the package. The image already holds every dependency,
   so this downloads nothing:

    ```sh
    uv pip install --python python3 --no-deps --no-build-isolation -e .
    ```

4. Turn on tracking for runs you may promote: set
   `EXAMPLE_MODEL_EXPERIMENT` to the experiment name.
5. Run `nbstripout --install` once in the clone. It sets a git filter, so
   outputs never reach a commit.

```dockerfile
--8<-- "examples/dev-env/project/notebook-image/Dockerfile"
```

## Verify

In a notebook, `import example_model` works, and the versions of the main
packages match `uv.lock`.

## See also

- [Path to production](../methods/development/path-to-production.md): why
  notebooks never run in production.
- [Vertex AI](vertex-ai.md)
