# CLAUDE.md

Instructions for Claude Code working in this project.
Companion file `AGENTS.md` (for Codex) points at this one.

---

## What this project is

<!-- EDIT: 3–5 sentences. What's the research question? What's the approach? What's the success criterion? -->

This project applies deep learning to <PROBLEM DOMAIN>. The core question is <QUESTION>. We're testing <APPROACH>. Success looks like <METRIC / DELIVERABLE>.

## Where we run

We are on **GACRC Sapelo2** (UGA HPC). The agent runs in an OnDemand VS Code session on the `inter_p` partition. Training jobs are submitted to `gpu_p` via sbatch.

| Path                              | Purpose                       | Notes                          |
|-----------------------------------|-------------------------------|--------------------------------|
| `/home/$USER/projects/foo/`       | this repo, code, configs      | 200 GB quota, backed up        |
| `/scratch/$USER/runs/foo/`        | run outputs, checkpoints      | no quota, auto-deleted at 30 d |
| `/scratch/$USER/data/foo/`        | active datasets               | same as above                  |
| `/project/<lab>/$USER/foo/`       | archived results worth keeping | 1 TB, backed up                |

Code reads these via `FOO_REPO`, `FOO_RUNS_DIR`, `FOO_DATA_DIR`, `FOO_ARCHIVE_DIR` (set by `setup_env.sh`). Never hardcode paths.

## Hard rules — do not violate

1. **Never run `sbatch`, `scancel`, `git push --force`.** Write the command, print it, let the user run it.
2. **Never run `module purge` or change loaded modules** mid-session — silently breaks the active venv.
3. **Never `pip install` without saying so first.** All deps go through `pyproject.toml`; after editing it, run `pip install -e .` then `pip freeze > requirements.lock`.
4. **Never `rm` anything outside this repo.** `/scratch` and `/project` paths are never to be deleted by the agent.
5. **Never run `tar`, `gzip`, or large `cp`/`rsync` from this session.** Those operations belong on `xfer.gacrc.uga.edu`. Propose the command for the user to run there.
6. **Never put API keys, tokens, or passwords in code, configs, or this repo.** Read them from env vars (`os.environ`). If a key seems missing, ask the user.
7. **Do not remove `--gres=gpu:A100:1`** (or whatever GPU type the project has pinned) from sbatch templates. Mixed GPU types break reproducibility.
8. **Do not edit `RESEARCH_LOG.md` except to read it.** That's the user's journal.

## What the agent should do freely

- Read any file in the repo.
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

## Math + derivations

When the user asks for a derivation or to verify math:
- Show the steps, don't summarize. Flag hidden assumptions.
- If sign / index / sum-bound conventions are ambiguous, state which one you're using before solving.
- For physics terms (continuum mechanics, FEM, control), use the user's notation if given; otherwise default to standard textbook notation and say so.
- If you're unsure, say "I'm not sure" — don't guess.
- For load-bearing derivations (a new loss, a custom autograd, a numerical scheme), suggest the user run the same prompt past the secondary agent (Codex) for an independent derivation. Disagreement is a real signal.

## Working pattern

Every session, at the start:
1. Read this file.
2. Read `RESEARCH_LOG.md` (most recent entries) to learn the current state.
3. Run `git status` and `git log -5 --oneline` to see what changed since last session.
4. Ask the user what to focus on.

Every meaningful change:
1. Write tests first when feasible.
2. Run `pytest tests/ -x` after editing.
3. Show diffs before applying when changes touch >1 file or >50 lines.
4. Don't commit. Don't push. Tell the user when something is ready to commit and what the message should be.

## Current focus

<!-- EDIT WEEKLY. One short paragraph: what we're trying right now, what's on hold, what's broken / don't touch. -->

Setting up the project skeleton. Implementing the real dataset loader in `foo/data/` and replacing the placeholder MLP is the first milestone. The sweep machinery is wired but unused.
