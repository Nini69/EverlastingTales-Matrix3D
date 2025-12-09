#!/usr/bin/env bash
set -e

REPO_DIR="/workspace/matrix3d"

echo "[Matrix3D] Downloading checkpoints..."
cd "${REPO_DIR}"

# Script officiel Matrix-3D : télécharge tous les modèles nécessaires
# On s'assure que le dossier checkpoints pointe vers le volume persistant
if [ -d "/workspace/data" ]; then
    echo "[Matrix3D] Setting up persistent checkpoints..."
    mkdir -p /workspace/data/checkpoints
    # Si le dossier checkpoints existe déjà (par git clone), on le déplace ou on le supprime s'il est vide
    if [ -d "checkpoints" ] && [ ! -L "checkpoints" ]; then
        if [ -z "$(ls -A checkpoints)" ]; then
            rmdir checkpoints
        else
            echo "[WARNING] 'checkpoints' directory exists and is not empty. Moving content to /workspace/data/checkpoints..."
            mv checkpoints/* /workspace/data/checkpoints/ || true
            rmdir checkpoints
        fi
    fi
    
    # Création du lien symbolique
    if [ ! -e "checkpoints" ]; then
        ln -s /workspace/data/checkpoints checkpoints
        echo "[Matrix3D] Symlink created: checkpoints -> /workspace/data/checkpoints"
    fi
fi

python code/download_checkpoints.py

echo "[Matrix3D] Checkpoints download finished."
