#!/bin/bash
# setup_env.sh — canonical environment for this project on Sapelo2.
#
# Usage:
#   source setup_env.sh           # activate existing venv
#   source setup_env.sh --create  # first-time: create venv and install deps
#
# This file is the ONLY supported way to activate the environment.
# If it stops working, fix it here, don't work around it in your shell rc.

set -e

VENV_PATH="$HOME/env/foo_pt2.6_py3.11"
CREATE_VENV=false
if [[ "$1" == "--create" ]]; then
    CREATE_VENV=true
fi

# --- module loads ---
# Pinned versions. Bump deliberately, not by accident.
module purge
module load nodejs/20.9.0-GCCcore-13.2.0
module load Python/3.11.5-GCCcore-13.2.0
module load CUDA/12.1.1
export PATH="$HOME/.npm-global/bin:$PATH"
# add other modules here as needed (e.g. cuDNN, NCCL)

# --- venv ---
if [[ "$CREATE_VENV" == "true" ]]; then
    if [[ -d "$VENV_PATH" ]]; then
        echo "venv already exists at $VENV_PATH; remove it first if you want to recreate"
        return 1 2>/dev/null || exit 1
    fi
    python -m venv "$VENV_PATH"
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip wheel
    pip install -e ".[dev]"
    pip freeze > requirements.lock
    echo "venv created at $VENV_PATH"
else
    if [[ ! -d "$VENV_PATH" ]]; then
        echo "venv not found at $VENV_PATH. Run: source setup_env.sh --create"
        return 1 2>/dev/null || exit 1
    fi
    source "$VENV_PATH/bin/activate"
fi

# --- env vars ---
# Refuse pip install outside a venv.
export PIP_REQUIRE_VIRTUALENV=true

# Project paths (override per-run if needed).
export FOO_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export FOO_DATA_DIR="${FOO_DATA_DIR:-/scratch/$USER/data/foo}"
export FOO_RUNS_DIR="${FOO_RUNS_DIR:-/scratch/$USER/runs/foo}"
export FOO_ARCHIVE_DIR="${FOO_ARCHIVE_DIR:-/project/REPLACE_LAB_NAME/$USER/foo}"

# W&B (only writes if WANDB_API_KEY is set; never put the key in this file)
export WANDB_PROJECT="${WANDB_PROJECT:-foo}"
export WANDB_DIR="${FOO_RUNS_DIR}"

# Quieter Hydra
export HYDRA_FULL_ERROR=1

# Reproducibility helpers
export PYTHONHASHSEED=0

echo "foo env active"
echo "  python:   $(which python)"
echo "  repo:     $FOO_REPO"
echo "  data:     $FOO_DATA_DIR"
echo "  runs:     $FOO_RUNS_DIR"
echo "  archive:  $FOO_ARCHIVE_DIR"
