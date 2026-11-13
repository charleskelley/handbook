"""Command line entry points. Production runs these inside the released container."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from example_model.config import Settings, load_config


def _train(args: argparse.Namespace) -> None:
    from example_model import data, gate, registry, tracking
    from example_model.train import train

    settings = Settings()
    config = load_config(args.config)
    frame = data.load_frame(settings, config.table, config.as_of)
    with tracking.run(settings, f"train-{args.model_version}", stage="production") as run:
        run.dataset(frame)
        run.params(**config.params, reference_run_id=config.reference.run_id)
        result = train(config, frame)
        run.metrics(**result.metrics)
        if args.register:
            run.metrics(**gate.check_reproduction(result, config.reference, config))
        uri = registry.save(settings, result.model, result.metrics, config, args.model_version)
        run.params(artifact_uri=uri)
    print(f"saved {uri} {result.metrics}")
    if args.register:
        print(f"registered version {registry.register(settings, uri)}")


def _reference(args: argparse.Namespace) -> None:
    """Write a research run's fixture and metrics into the config's reference block."""
    import re

    import yaml

    from example_model import tracking

    block = yaml.safe_dump({"reference": tracking.reference_from_run(Settings(), args.run_id)})
    if args.write:
        path = args.write
        text = path.read_text()
        head = re.split(r"(?m)^reference:.*$", text, maxsplit=1)[0]
        path.write_text(head + block)
        print(f"wrote reference for run {args.run_id} to {path}")
    else:
        print(block, end="")


def _score(args: argparse.Namespace) -> None:
    from example_model.score import score

    rows = score(Settings(), load_config(args.config), args.input_table, args.output_table)
    print(f"scored {rows} rows")


def _promote(args: argparse.Namespace) -> None:
    """Make a registered version the champion and start watching it. A person runs this."""
    from example_model import monitoring, registry

    settings = Settings()
    registry.promote(settings, args.version)
    name = monitoring.ensure_monitor(settings, load_config(args.config), args.version)
    print(f"champion is version {args.version}; monitor {name}")


def _performance(args: argparse.Namespace) -> None:
    from example_model import performance

    metrics = performance.run(Settings(), load_config(args.config), args.days)
    print(metrics.to_string(index=False) if not metrics.empty else "no labeled predictions yet")


def _report(args: argparse.Namespace) -> None:
    from example_model import report

    print(f"report written to {report.run(Settings(), load_config(args.config), args.days)}")


def _serve(args: argparse.Namespace) -> None:
    import uvicorn

    from example_model.serve import production_app

    uvicorn.run(production_app(), host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))


def _submit(args: argparse.Namespace) -> None:
    from example_model.pipeline import submit

    name = submit(Settings(), args.image, args.model_version, args.service_account, args.root)
    print(f"submitted {name}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="example-model")
    commands = parser.add_subparsers(required=True)

    train = commands.add_parser("train", help="train from a config")
    train.add_argument("--config", default="train")
    train.add_argument("--model-version", required=True)
    train.add_argument(
        "--register", action="store_true", help="check the gate and register (production)"
    )
    train.set_defaults(func=_train)

    reference = commands.add_parser(
        "reference", help="record a research run as the one production must reproduce"
    )
    reference.add_argument("run_id")
    reference.add_argument(
        "--write",
        type=Path,
        help="config file to update, e.g. src/example_model/configs/train.yaml",
    )
    reference.set_defaults(func=_reference)

    score = commands.add_parser("score", help="batch score a table")
    score.add_argument("--config", default="train")
    score.add_argument("--input-table", required=True)
    score.add_argument("--output-table", required=True)
    score.set_defaults(func=_score)

    promote = commands.add_parser("promote", help="make a version the champion and monitor it")
    promote.add_argument("--config", default="train")
    promote.add_argument("--version", required=True, help="registry version ID")
    promote.set_defaults(func=_promote)

    performance = commands.add_parser("performance", help="metrics from labeled predictions")
    performance.add_argument("--config", default="train")
    performance.add_argument("--days", type=int, default=7)
    performance.set_defaults(func=_performance)

    report = commands.add_parser("report", help="write an Evidently report to the bucket")
    report.add_argument("--config", default="train")
    report.add_argument("--days", type=int, default=7)
    report.set_defaults(func=_report)

    serve = commands.add_parser("serve", help="serve the latest batch predictions over HTTP")
    serve.set_defaults(func=_serve)

    submit = commands.add_parser("submit-training", help="submit the training pipeline")
    submit.add_argument("--image", required=True)
    submit.add_argument("--model-version", required=True)
    submit.add_argument("--service-account", required=True)
    submit.add_argument("--root", required=True, help="pipeline root, a gs:// path")
    submit.set_defaults(func=_submit)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
