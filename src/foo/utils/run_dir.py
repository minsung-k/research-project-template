"""Run directory layout and metadata stamping.

Every training run gets a directory like:

    /scratch/$USER/runs/foo/<exp_name>/<run_id>/
        config.yaml      # resolved Hydra config
        commit.txt       # git rev-parse HEAD + dirty?
        env.txt          # pip freeze + nvidia-smi + module list
        slurm.txt        # SLURM_JOB_ID, partition, GPU type
        train.log        # stdout
        metrics.csv      # epoch,train_loss,val_loss,...
        checkpoints/
        artifacts/

Call `stamp_run_dir(run_dir, cfg)` once at the start of training.
"""
from __future__ import annotations

import os
import socket
import subprocess
from pathlib import Path

from omegaconf import DictConfig, OmegaConf


def _run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        return f"<failed: {e}>"


def _git_info() -> str:
    sha = _run(["git", "rev-parse", "HEAD"])
    dirty = _run(["git", "status", "--porcelain"])
    branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return f"branch: {branch}\nsha: {sha}\ndirty:\n{dirty if dirty else '(clean)'}\n"


def _slurm_info() -> str:
    keys = [
        "SLURM_JOB_ID",
        "SLURM_JOB_NAME",
        "SLURM_JOB_PARTITION",
        "SLURM_NODELIST",
        "SLURM_ARRAY_JOB_ID",
        "SLURM_ARRAY_TASK_ID",
        "SLURM_GPUS_ON_NODE",
        "CUDA_VISIBLE_DEVICES",
    ]
    lines = [f"{k}={os.environ.get(k, '')}" for k in keys]
    lines.append(f"hostname={socket.gethostname()}")
    return "\n".join(lines) + "\n"


def _env_info() -> str:
    pip_freeze = _run(["pip", "freeze"])
    nvidia = _run(["nvidia-smi", "-L"])
    modules = _run(["bash", "-c", "module list 2>&1"])
    return (
        f"## nvidia-smi -L\n{nvidia}\n\n"
        f"## module list\n{modules}\n\n"
        f"## pip freeze\n{pip_freeze}\n"
    )


def stamp_run_dir(run_dir: Path | str, cfg: DictConfig) -> Path:
    """Create the run dir if needed and write all metadata files.

    Returns the run dir as a Path. Idempotent: safe to call on a resumed run
    (overwrites metadata files but does not touch checkpoints/).
    """
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "checkpoints").mkdir(exist_ok=True)
    (run_dir / "artifacts").mkdir(exist_ok=True)

    (run_dir / "config.yaml").write_text(OmegaConf.to_yaml(cfg, resolve=True))
    (run_dir / "commit.txt").write_text(_git_info())
    (run_dir / "slurm.txt").write_text(_slurm_info())
    (run_dir / "env.txt").write_text(_env_info())

    return run_dir
