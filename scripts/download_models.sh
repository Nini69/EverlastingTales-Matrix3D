#!/usr/bin/env bash
set -e

REPO_DIR="/workspace/matrix3d"

echo "[Matrix3D] Downloading checkpoints..."
cd "${REPO_DIR}"

# Script officiel Matrix-3D : télécharge tous les modèles nécessaires
python code/download_checkpoints.py

echo "[Matrix3D] Checkpoints download finished."
