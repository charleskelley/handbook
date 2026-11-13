---
title: "How to connect VS Code to a workstation or research VM"
type: how-to
owner: platform-owner
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-11
review_cadence: 180d
tags: [vscode, editors]
sources:
  - "examples/dev-env/ssh/config.example"
---

# How to connect VS Code to a workstation or research VM

## Goal

VS Code on your laptop, with the editor's server, your code, and the
interpreter on the cloud machine. This is the team's default.

## Steps

1. Install the **Remote - SSH** extension.
2. Add the team's entries to `~/.ssh/config`, replacing the placeholders and
   your OS Login username:

    ```text
    --8<-- "examples/dev-env/ssh/config.example"
    ```

3. **Workstation:** start it, then start the tunnel in a terminal and leave it
   running, as the comment above shows.
4. In VS Code, run **Remote-SSH: Connect to Host** and choose `workstation` or
   `research-<name>`.
5. Open your clone on the remote machine, run `uv sync`, and choose
   `.venv/bin/python` as the interpreter.
6. Settings come from `.env`, which the Python extension reads by default.

## Verify

In the VS Code terminal, `hostname` shows the cloud machine, and
`uv run python -c "import sys; print(sys.prefix)"` shows the project's `.venv`.

## See also

- [Cloud Workstations](cloud-workstations.md)
- [Research VMs](research-vms.md)
- [Connect JetBrains](connect-jetbrains.md)

## Troubleshooting

- **Connection refused on port 2222.** The workstation tunnel is not running,
  or the workstation is stopped.
- **Permission denied on a research VM.** Check the OS Login username, and that
  the Terraform change granting you access has been applied.
