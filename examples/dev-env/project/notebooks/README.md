# Notebooks

Research only. Notebooks import `example_model`; they are never imported by it
and never run in a production pipeline.

- Outputs are stripped before commit (`nbstripout`, enforced in CI), because a
  displayed DataFrame is data written to git.
- Work you want to keep moves into `src/example_model/` with a test.
- Record the result you will promote with tracking turned on, then copy it into
  `reference` in `src/example_model/configs/train.yaml`.
