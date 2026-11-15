---
title: "How to set up a Mac"
type: how-to
owner: platform-owner
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-11
review_cadence: 180d
tags: [setup, laptop]
---

# How to set up a Mac

## Goal

A laptop that can run tests, harnesses, and tools, and reach your workstation,
with everything installed from Artifactory. No Homebrew, no Docker, and no
administrator rights needed.

## Steps

1. Install VS Code from the company's software portal. If you use JetBrains,
   install the Toolbox App from the portal too: it must be build
   {{ platform.dev.jetbrains_toolbox_build }}, the one the workstation image
   was built against, so do not update it on your own.
2. In Artifactory, open your profile and generate an identity token.
3. Run the team's bootstrap script, with your Artifactory address:

    ```sh
    ARTIFACTORY_URL={{ platform.dev.artifactory_url }} bash mac.sh
    ```

    It asks for your username and token once, then installs uv, Python
    {{ platform.dev.python_version }}, `just`, `ruff`, `pre-commit`,
    `nbstripout`, and the Google Cloud CLI into your home directory, all
    downloaded through Artifactory, and writes your token to `~/.netrc`.

4. Open a new terminal and sign in to Google Cloud:

    ```sh
    gcloud auth login
    gcloud auth application-default login
    ```

## Verify

```sh
uv --version
uv python list --only-installed
gcloud config list
```

In a project, `uv sync` installs from Artifactory with no errors.

## See also

- [Development environments](../methods/development/environments.md): what a
  laptop is for, and the rule that it never holds real data.
- [Artifactory](artifactory.md)

## Troubleshooting

- **401 from Artifactory.** The token in `~/.netrc` is wrong or expired.
  Generate a new one and replace that line.
- **`uv: command not found`.** Open a new terminal, or add `~/.local/bin` to
  your `PATH`.
