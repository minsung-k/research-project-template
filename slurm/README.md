# SLURM templates

GACRC Sapelo2 sbatch templates. Edit `--mail-user` before first use.

## `train.sbatch` — single training run

```bash
sbatch slurm/train.sbatch model=fno seed=0 trainer.max_epochs=200
```

Args after the script name pass through to `python scripts/train.py`.

## `sweep_array.sbatch` — parallel hyperparameter sweep

Two-step pattern (see `scripts/sweep.py`):

```bash
# 1. Generate the configs for the sweep
python scripts/sweep.py configs/sweep/lr_seed.yaml

# 2. The sweep script prints the sbatch command, e.g.:
sbatch --export=SWEEP_DIR=/scratch/$USER/runs/foo/sweeps/2026-05-06_lr_seed,ALL \
       --array=0-23%8 slurm/sweep_array.sbatch
```

## Partitions used

| Partition  | Walltime | Use for                                 |
|------------|----------|-----------------------------------------|
| `gpu_p`    | 8 days   | normal training runs (this project)     |
| `inter_p`  | 12 h     | Claude Code / Codex agent host (no GPU) |

## What to NEVER do

- Run `module purge` mid-session — silently changes the Python under your venv.
- Submit without specifying `--gres=gpu:A100:1` (or whichever you've pinned). Without it you can land on P100, V100S, A100, L4, or H100 and get bitwise-different results.
- Forget that `/scratch` auto-deletes at 30 days. Move keepers to `/project`.
