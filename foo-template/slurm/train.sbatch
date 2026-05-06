#!/bin/bash
#SBATCH --job-name=foo-train
#SBATCH --partition=gpu_p
#SBATCH --gres=gpu:A100:1            # pin GPU type for reproducibility
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64gb
#SBATCH --time=1-00:00:00            # 1 day; bump up to 7 for gpu_p
#SBATCH --output=/scratch/%u/runs/foo/_slurm/%x-%j.log
#SBATCH --error=/scratch/%u/runs/foo/_slurm/%x-%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=REPLACE@uga.edu

# --- env ---
cd $SLURM_SUBMIT_DIR
source setup_env.sh

# --- diagnostics into the slurm log ---
echo "host:    $(hostname)"
echo "gpu:     $(nvidia-smi -L)"
echo "commit:  $(git rev-parse HEAD)"
echo "modules: $(module list 2>&1 | tr '\n' ' ')"

# --- run ---
# Pass through any args to train.py: e.g.
#   sbatch slurm/train.sbatch model=fno seed=42
python scripts/train.py "$@"
