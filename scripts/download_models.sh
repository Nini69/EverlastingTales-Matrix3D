#!/usr/bin/env bash
set -e

MODELS_DIR="/workspace/models"

echo "[Matrix3D] Using models dir: ${MODELS_DIR}"

mkdir -p "${MODELS_DIR}"
cd "${MODELS_DIR}"

##############################################
# NOTE POUR CODEX :
# 1) Lire le README de https://github.com/SkyworkAI/Matrix-3D
# 2) Identifier les checkpoints nécessaires pour :
#    - génération pano image
#    - pano vidéo
#    - reconstruction 3D / 3DGS
# 3) Ajouter ici les commandes de téléchargement si les fichiers n'existent pas.
##############################################

# Exemple de structure (A ADAPTER avec les vrais noms de fichiers) :

download_if_missing () {
  local url="$1"
  local filename="$2"

  if [ ! -f "${filename}" ]; then
    echo "[Matrix3D] Downloading ${filename} ..."
    wget -O "${filename}" "${url}"
  else
    echo "[Matrix3D] ${filename} already exists, skipping."
  fi
}

# EXEMPLES (FAUX NOMS, À REMPLACER) :
# download_if_missing "https://huggingface.co/Skywork/Matrix-3D/resolve/main/pano_480p.ckpt" "pano_480p.ckpt"
# download_if_missing "https://huggingface.co/Skywork/Matrix-3D/resolve/main/video_480p.ckpt" "video_480p.ckpt"
# download_if_missing "https://huggingface.co/Skywork/Matrix-3D/resolve/main/recon_3dgs.pt" "recon_3dgs.pt"

echo "[Matrix3D] Models download/check complete."
