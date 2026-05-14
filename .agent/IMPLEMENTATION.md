# IMPLEMENTATION.md

Cluster setup, runtime conventions, and code style for this repo.
**Read this** when writing or running code, proposing sbatch, doing EDA
on disk data, or installing dependencies. For methodology / framing /
literature / brainstorm / spec work (no code), you don't need this file.

`CLAUDE.md` (project root) covers research-process methodology, universal
hard rules, and session protocol. This file covers everything below that
layer.

## Where we run

We are on **GACRC Sapelo2** (UGA HPC). The agent runs in an OnDemand VS Code session on the `inter_p` partition. Training jobs are submitted to `gpu_p` via sbatch.

| Path                              | Purpose                       | Notes                          |
|-----------------------------------|-------------------------------|--------------------------------|
| `/home/$USER/projects/foo/`       | this repo, code, configs      | 200 GB quota, backed up        |
| `/scratch/$USER/data/foo/`        | active datasets               | no quota, auto-deleted at 30 d |
| `/scratch/$USER/runs/foo/`        | run outputs, checkpoints      | same as above                  |
| `/project/<lab>/$USER/foo/`       | archived results worth keeping | 1 TB, backed up                |

Code reads these via `FOO_REPO`, `FOO_RUNS_DIR`, `FOO_DATA_DIR`, `FOO_ARCHIVE_DIR` (set by `setup_env.sh`). Never hardcode paths.

If the dataset is small enough to live in `/home` (a few GB, fits the 200 GB quota with room to spare), put it under `${FOO_REPO}/data/` and point `FOO_DATA_DIR` at it. Bigger datasets stay on `/scratch`.

## Cluster / runtime hard rules

1. **Never run `sbatch`, `scancel`.** Write the command, print it, let the user run it.
2. **Never run `module purge` or change loaded modules** mid-session — silently breaks the active venv.
3. **Never `pip install` without saying so first.** All deps go through `pyproject.toml`; after editing it, run `pip install -e .` then `pip freeze > requirements.lock`.
4. **Never run `tar`, `gzip`, or large `cp`/`rsync` from this session.** Those operations belong on `xfer.gacrc.uga.edu`. Propose the command for the user to run there.
5. **Do not remove `--gres=gpu:A100:1`** (or whatever GPU type the project has pinned) from sbatch templates. Mixed GPU types break reproducibility.

## What the agent can do freely

- Edit code in `src/foo/`, `scripts/`, `tests/`, `configs/`.
- Run `pytest`, `ruff`, short Python sanity checks (small tensors, CPU).
- Inspect run output dirs on `/scratch` (read-only).
- Read `nvidia-smi`, `squeue -u $USER`, `sacct -u $USER`, `seff <jobid>`.
- Propose sbatch scripts and the exact `sbatch` command to run them.

## How to run things

```bash
# activate env (always)
source setup_env.sh

# tests
pytest tests/ -x

# quick local train (CPU)
python scripts/train.py trainer.max_epochs=1 trainer.use_wandb=false

# real training run (submit, don't run inline)
sbatch slurm/train.sbatch model=mlp seed=0

# parallel sweep — generates configs, prints sbatch command
python scripts/sweep.py configs/sweep/<spec>.yaml
```

Hydra notes:
- Override at CLI: `python scripts/train.py model=fno optimizer.lr=1e-4 seed=0`
- Multirun: `python scripts/train.py -m seed=0,1,2 model=mlp,fno`
- Named experiments: `python scripts/train.py +experiment=ablation_v1`
- Run output dir is `${FOO_RUNS_DIR}/${exp_name}/<date>_<user>_<exp>_seed<n>/`.

## Code conventions

- **PyTorch** is the default. Device handling: `device = "cuda" if torch.cuda.is_available() else "cpu"` — never hardcode `"cuda"`.
- **Variable names match math** where reasonable: `x`, `y`, `u` for vectors/fields; `A`, `K` for matrices/operators; uppercase for tensors of rank ≥ 2; suffix `_b` for batched.
- **New models** → `src/foo/models/<name>.py`, register in `models/__init__.py`.
- **New losses** → `src/foo/losses/<name>.py`, register in `losses/__init__.py`.
- **New datasets** → `src/foo/data/<name>.py`. The class takes `data_dir: str` from config, not from a hardcoded path.
- **Tests required** for any function doing non-trivial math (custom autograd, PDE residuals, FEM ops, numerical integration).
- **Type hints** on public functions. Don't bother on tight inner loops.
- **Logging**: `logging.getLogger(__name__)`, not `print`.
- Format: ruff handles it. Run `ruff format .` and `ruff check . --fix` before committing.

## Every meaningful code change

1. Write tests first when feasible.
2. Run `pytest tests/ -x` after editing.
3. Show diffs before applying when changes touch >1 file or >50 lines.
4. Don't commit. Don't push. Tell the user when something is ready to commit and what the message should be.
