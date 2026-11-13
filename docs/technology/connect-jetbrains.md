---
title: "How to connect JetBrains to a workstation or research VM"
type: how-to
owner: platform-owner
audience: [ds, mle, de]
status: draft
last_reviewed: 2026-11-11
review_cadence: 180d
tags: [jetbrains, editors]
sources:
  - "examples/dev-env/ssh/config.example"
  - "examples/dev-env/workstation-image/Dockerfile"
  - "examples/dev-env/workstation-image/210_jetbrains.sh"
  - "https://www.jetbrains.com/help/toolbox-app/jetbrains-gateway-migrations-guide.html"
  - "https://www.jetbrains.com/help/toolbox-app/offline-remote-development-in-the-toolbox-app.html"
---

# How to connect JetBrains to a workstation or research VM

## Goal

PyCharm or DataGrip with its backend running on the cloud machine, through the
JetBrains Toolbox App. Needs a Professional licence.

JetBrains Gateway is being replaced by the Toolbox App and will be deprecated,
so this page does not use it. The backend is already in the workstation image,
and the Toolbox App on your laptop must be build
{{ platform.dev.jetbrains_toolbox_build }} to match it: install it from the
software portal and leave updates to the portal.

## Steps

1. Set up `~/.ssh/config` as in [Connect VS Code](connect-vs-code.md), and for a
   workstation, start the tunnel. The Toolbox App uses your system `ssh`, so the
   tunnel port and the IAP `ProxyCommand` work as they do for VS Code.
2. In the Toolbox App, open the drop-down next to the menu, choose **SSH**, and
   create a connection to `workstation` or `research-<name>`.
3. Open the connection's **Tools** tab. PyCharm is listed as installed, from
   `/opt/jetbrains/pycharm` in the image. Open it, then open your clone on the
   remote machine from the **Projects** tab or **File | Open**.
4. Set the interpreter to the project's `.venv/bin/python` after `uv sync`.
5. In each run configuration, set **Paths to ".env" files** to the project's
   `.env`. Remote interpreters do not load your shell setup.

If a full PyCharm 2026.3 or later is installed locally, **File | Connect to
Remote** inside it does the same as steps 2 and 3. Research VMs are built from
the Terraform image, not the workstation image, so there the Toolbox App
installs the backend itself: that needs the VM to reach Artifactory's
`jetbrains` repository, and takes a few minutes the first time.

### Where the code lives

With a remote backend, your clone lives on the cloud machine's home disk. The laptop has
no copy, and git is the only way code moves between the two. To test something
on the laptop:

1. On the cloud machine, commit to your feature branch and push. Work-in-progress
   commits are fine on a feature branch.
2. On the laptop, pull that branch into a separate local clone, run `uv sync`,
   and run the tests. The laptop needs [Set up a Mac](set-up-a-mac.md) first so
   `uv` installs from Artifactory, and the lockfile then gives it the same
   versions as the cloud machine.
3. Push from the laptop and pull on the cloud machine before switching back.

Keep one clone in charge of each branch at a time. Editing both copies at once
is where most of the conflicts come from. If a piece of work is mostly local,
such as a small tool or harness, make the laptop the main clone for that branch
and use the cloud machine only to run things.

Only tests that use synthetic data run on the laptop. Dev can read personal
data, so no extract of real data comes down to a laptop. Anything that needs
BigQuery or real data runs on the cloud machine.

### Remote backend or an SSH interpreter

The other way to use the cloud machine from JetBrains is a local PyCharm with an
**SSH remote interpreter**. The source then lives on the laptop, and PyCharm
copies it to the cloud machine through a deployment mapping before each run.

| | Remote backend | Local IDE with SSH interpreter |
|---|---|---|
| Where the source lives | Cloud machine | Laptop |
| Where the IDE's indexing memory sits | Cloud machine | Laptop |
| How code reaches the other side | Git push and pull | Automatic upload on save or run |
| Main risk | Two clones drift if both are edited | The uploaded copy drifts from the local one |
| Fits | Most work, large projects, database work | Small repos you mostly edit and test locally |

Use the remote backend by default. Use the SSH interpreter for a small repository where you
want to edit and run tests locally and only occasionally run on the cloud
machine. Set the deployment mapping's remote path to a directory under your
home, and treat that copy as disposable: commit and push from the laptop.

## Verify

A run configuration prints the cloud machine's hostname, and a query in the
database tool reaches BigQuery with your own identity.

## See also

- [Cloud Workstations](cloud-workstations.md)
- [Research VMs](research-vms.md)

## Troubleshooting

- **The backend is slow to start the first time.** It is indexing. The index
  lives in your home directory, which persists, so later starts are fast.
- **The Toolbox App tries to download an agent or a backend.** Your Toolbox
  App build does not match the image's Agent, or the startup script did not
  register the backend. Check **About** in the Toolbox App against
  {{ platform.dev.jetbrains_toolbox_build }}, then restart the workstation.
