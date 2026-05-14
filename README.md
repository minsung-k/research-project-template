# foo

One-paragraph description of this project: research question, approach, target deliverable.

## Quickstart (Sapelo2)

```bash
# First time only:
git clone <repo-url> ~/projects/foo
cd ~/projects/foo
source setup_env.sh --create

# Every session:
cd ~/projects/foo
source setup_env.sh

# Sanity check:
pytest tests/ -x

# Local debug train (no GPU, tiny config):
python scripts/train.py trainer.max_epochs=1

# Submit a real training job:
sbatch slurm/train.sbatch model=mlp seed=0

# Launch a sweep:
python scripts/sweep.py configs/sweep/lr_seed.yaml
# (then run the printed sbatch command)
```

## Layout

```
configs/        Hydra configs (model, dataset, optimizer, trainer, experiment, sweep)
src/foo/        Importable package — all real logic lives here
scripts/        Thin entry points: train.py, sweep.py, evaluate.py
slurm/          sbatch templates for Sapelo2 gpu_p
tests/          pytest, no GPU needed
notebooks/      Exploration only — never the source of a result
notes/          Research-process phase artifacts (problem.md, litreview.md, …)
.agent/         Claude Code / Codex skills, subagents, prompts, HANDOFF.md
```

## Conventions

- Code in `/home/$USER/projects/foo`. Run output in `/scratch/$USER/runs/foo`. Archive in `/project/<lab>/$USER/foo`.
- New models go in `src/foo/models/` and get registered in `models/__init__.py`.
- Variable names match math symbols where reasonable (lowercase math vars; uppercase for tensors of dim ≥ 2).
- Tests are required for any function with non-trivial math.
- Commit `requirements.lock` when deps change.

## See also

- `CLAUDE.md` / `AGENTS.md` — agent instructions (methodology, hard rules, working pattern).
- `.agent/IMPLEMENTATION.md` — cluster paths, runtime rules, code conventions.
- `RESEARCH_LOG.md` — running journal of what was tried and what's next.
- `.agent/HANDOFF.md` — live state of in-flight work; outgoing agent overwrites.
- `slurm/README.md` — partition/template details.
