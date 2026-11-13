---
title: "How to request, replace, or release a research VM"
type: how-to
owner: platform-owner
audience: [ds, mle]
status: draft
last_reviewed: 2026-11-11
review_cadence: 180d
tags: [compute, terraform]
sources:
  - "examples/dev-env/infra/envs/dev/terraform.tfvars.example"
---

# How to request, replace, or release a research VM

## Goal

A large-memory or GPU VM for interactive work, created, replaced, or removed
through the team's Terraform.

## Steps

1. Check that a Vertex AI custom job will not do: batch work belongs there.
2. In the infrastructure repository, add a `research_vm` entry to your user in
   the dev variables:

    ```hcl
    --8<-- "examples/dev-env/infra/envs/dev/terraform.tfvars.example"
    ```

    `sam` gets a 128GB CPU VM and `kim` a GPU VM.
3. Open a merge request. Once it is applied, connect as on
   [Connect VS Code](connect-vs-code.md).
4. **To replace it:** push everything, then ask for it to be recreated.
   **To release it:** remove your entry.

## Verify

`gcloud compute instances list --project={{ platform.dev.gcp_dev_project }}`
shows `research-<name>`, and you can connect through IAP.

## See also

- [Research VMs](research-vms.md)
- [Development environments](../methods/development/environments.md)
