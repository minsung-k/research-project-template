"""Train entry point. Thin wrapper around the training loop in foo.training.

Usage:
    # local sanity check (CPU is fine for the placeholder)
    python scripts/train.py model=mlp seed=0

    # multirun sweep (Hydra -m)
    python scripts/train.py -m model=mlp seed=0,1,2 optimizer.lr=1e-3,1e-4

    # named experiment
    python scripts/train.py +experiment=ablation_v1
"""
from __future__ import annotations

import logging
from pathlib import Path

import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf

from foo.utils import set_seed, stamp_run_dir

log = logging.getLogger(__name__)


@hydra.main(version_base="1.3", config_path="../configs", config_name="config")
def main(cfg: DictConfig) -> float:
    # Hydra has already created hydra.run.dir; we use it as our run dir.
    run_dir = Path(hydra.core.hydra_config.HydraConfig.get().runtime.output_dir)
    stamp_run_dir(run_dir, cfg)

    log.info("Run dir: %s", run_dir)
    log.info("Config:\n%s", OmegaConf.to_yaml(cfg))

    set_seed(cfg.seed, deterministic=cfg.trainer.deterministic)

    # Instantiate components from config.
    model = instantiate(cfg.model)
    # `_partial_: true` in optimizer.yaml means this returns a callable
    # that we bind to params now.
    optimizer = instantiate(cfg.optimizer)(model.parameters())

    log.info("Model:\n%s", model)
    log.info("Optimizer: %s", optimizer)

    # ---- training loop goes here ----
    # Replace with your real loop, calling into foo.training.
    # For the template we just verify the pieces import and instantiate.
    val_metric = 0.0
    log.info("Template train.py is a stub. Implement the loop in foo.training.")

    return val_metric  # Hydra optuna sweeper picks this up if used


if __name__ == "__main__":
    main()
