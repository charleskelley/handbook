---
title: "How to add a language toolchain"
type: how-to
owner: platform-owner
audience: [mle, de]
status: draft
last_reviewed: 2026-11-11
review_cadence: 365d
tags: [languages, artifactory]
---

# How to add a language toolchain

## Goal

Use a language other than Python, with the same guarantees: dependencies and the
toolchain come from Artifactory, the lockfile is committed, and CI refuses to
build if it is out of date.

## Steps

1. **Ask for the repositories.** The Artifactory owner adds a remote for the
   language's registry and its toolchain downloads, a dev and a release local
   repository, and the two virtual repositories, in the same shape as Python.
2. **Point the registry config at Artifactory, and the toolchain installer at its
   mirror.** Put the config in the workstation image or the research VM startup
   script, not in your home directory.
3. **Commit the lockfile, and build in CI with the frozen flag.**

| Language | Registry config | Toolchain mirror | Lockfile | CI flag |
|---|---|---|---|---|
| Node and TypeScript | `.npmrc` registry | Node download mirror for fnm or nvm | `package-lock.json` or `pnpm-lock.yaml` | `npm ci`, `pnpm install --frozen-lockfile` |
| Rust | `~/.cargo/config.toml` source replacement | `RUSTUP_DIST_SERVER` | `Cargo.lock` | `cargo build --locked` |
| Go | `GOPROXY` | `GOTOOLCHAIN`, which uses the same proxy | `go.sum` | `go build -mod=readonly` |
| Java | Gradle init script or Maven `settings.xml` | JDK from a generic remote | Gradle lockfiles | `--locked` builds with dependency verification |
| Scala, Spark on Dataproc only | Coursier and sbt resolvers | Coursier mirror | sbt lock plugin | Check the lock in CI |
| C and C++ | Conan remote | Compilers from the OS image | `conan.lock` | `conan install --lockfile` |
| CUDA | Python wheels from a PyTorch index remote | Toolkit from NVIDIA's apt repository, through a Debian remote | `uv.lock` | `uv sync --locked` |

For speeding up Python, prefer Rust with PyO3 and maturin: it produces an
ordinary wheel, and Cargo already locks. Use C or C++ to wrap an existing
library or write CUDA kernels, building wheels with scikit-build-core and
cibuildwheel in CI. Scala is used only for Spark jobs, where the Dataproc runtime
sets the Scala version.

## Verify

On a fresh workstation or research VM, a clean build succeeds with no access to
the public registry, and CI fails if the lockfile is edited out of step with the
manifest.

## See also

- [Artifactory](artifactory.md)
- [Development environments](../methods/development/environments.md)
