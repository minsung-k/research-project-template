"""Pre-generate per-run configs for a SLURM array sweep.

Usage:
    python scripts/sweep.py configs/sweep/<spec>.yaml

Spec format (yaml):
    base:
      +experiment: ablation_v1     # base composition
    grid:                          # cartesian product of these
      seed: [0, 1, 2]
      optimizer.lr: [1.0e-3, 3.0e-4, 1.0e-4]
      model.hidden_dims: [[64,64], [128,128], [256,256]]
    name: lr_seed_v1               # sweep name (goes into the dir)
    array:
      max_concurrent: 8

Writes:
    /scratch/$USER/runs/foo/sweeps/<date>_<name>/
        sweep_spec.yaml            # the spec used
        configs/run_0000.yaml      # one resolved config per cell
        configs/run_0001.yaml
        ...
        submit.sh                  # the sbatch command to run

Then run the printed `sbatch ...` command. The sweep script does not submit
for you — that's a deliberate handoff point so you (or the agent) can review
before launching dozens of GPU-hours.
"""
from __future__ import annotations

import argparse
import datetime as dt
import itertools
import os
import sys
from pathlib import Path

import yaml


def expand_grid(grid: dict) -> list[dict]:
    keys = list(grid.keys())
    values = [grid[k] for k in keys]
    return [dict(zip(keys, combo)) for combo in itertools.product(*values)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", type=Path, help="path to sweep spec yaml")
    args = ap.parse_args()

    spec = yaml.safe_load(args.spec.read_text())
    name = spec["name"]
    base = spec.get("base", {})
    grid = spec["grid"]
    max_concurrent = spec.get("array", {}).get("max_concurrent", 4)

    cells = expand_grid(grid)
    n = len(cells)
    if n == 0:
        print("error: empty grid", file=sys.stderr)
        return 1

    runs_root = Path(os.environ.get("FOO_RUNS_DIR") or f"/scratch/{os.environ['USER']}/runs/foo")
    date = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    sweep_dir = runs_root / "sweeps" / f"{date}_{name}"
    cfg_dir = sweep_dir / "configs"
    cfg_dir.mkdir(parents=True, exist_ok=True)

    # Save the spec verbatim
    (sweep_dir / "sweep_spec.yaml").write_text(args.spec.read_text())

    # Each per-run config is a tiny override yaml; train.py composes the rest.
    for i, cell in enumerate(cells):
        run_cfg: dict = {}
        run_cfg.update(base)
        # Flatten dotted overrides into nested dicts that Hydra will merge
        for dotted, val in cell.items():
            cur = run_cfg
            parts = dotted.split(".")
            for p in parts[:-1]:
                cur = cur.setdefault(p, {})
            cur[parts[-1]] = val
        # Tag run with its index so logs are findable
        run_cfg["exp_name"] = f"{name}_run{i:04d}"
        (cfg_dir / f"run_{i:04d}.yaml").write_text(yaml.safe_dump(run_cfg, sort_keys=False))

    # Print the sbatch command for the user to run.
    end = n - 1
    cmd = (
        f"sbatch --export=SWEEP_DIR={sweep_dir},ALL "
        f"--array=0-{end}%{max_concurrent} "
        f"slurm/sweep_array.sbatch"
    )
    (sweep_dir / "submit.sh").write_text(cmd + "\n")
    print(f"wrote {n} configs to {cfg_dir}")
    print()
    print("review the configs, then run:")
    print(f"  {cmd}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
