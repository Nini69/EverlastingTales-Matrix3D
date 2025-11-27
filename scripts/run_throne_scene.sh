#!/usr/bin/env bash
set -e

echo "[Matrix3D] Starting throne scene generation..."

# 1) S'assurer que les modèles sont présents
bash /workspace/scripts/download_models.sh

# 2) Aller dans le repo Matrix-3D
cd /workspace/matrix3d

# 3) Définir les dossiers d'entrées / sorties
export MATRIX3D_MODELS_DIR="/workspace/models"
export MATRIX3D_OUTPUT_DIR="/workspace/outputs/throne_scene"
mkdir -p "${MATRIX3D_OUTPUT_DIR}"

##############################################
# NOTE POUR CODEX :
# Adapter les commandes ci-dessous aux scripts
# réels du repo Matrix-3D (text -> pano -> video -> 3DGS).
##############################################

# Exemple pseudo-code (à adapter) :

PROMPT="a mysterious throne in a dimly lit, dreamlike stone chamber, cinematic, high detail"

echo "[Matrix3D] Step 1: text -> panorama image"
# Exemple : python tools/text_to_pano.py ...
# python tools/text_to_pano.py \
#   --prompt "${PROMPT}" \
#   --models_dir "${MATRIX3D_MODELS_DIR}" \
#   --output "${MATRIX3D_OUTPUT_DIR}/pano.png"

echo "[Matrix3D] Step 2: panorama -> panorama video"
# Exemple : python tools/pano_to_video.py ...
# python tools/pano_to_video.py \
#   --input "${MATRIX3D_OUTPUT_DIR}/pano.png" \
#   --models_dir "${MATRIX3D_MODELS_DIR}" \
#   --output "${MATRIX3D_OUTPUT_DIR}/pano_video.mp4"

echo "[Matrix3D] Step 3: video -> 3DGS (.ply)"
# Exemple : python tools/video_to_3dgs.py ...
# python tools/video_to_3dgs.py \
#   --input "${MATRIX3D_OUTPUT_DIR}/pano_video.mp4" \
#   --models_dir "${MATRIX3D_MODELS_DIR}" \
#   --output "${MATRIX3D_OUTPUT_DIR}/throne_3dgs.ply"

echo "[Matrix3D] Throne scene generation complete."
echo "[Matrix3D] Outputs should be in: ${MATRIX3D_OUTPUT_DIR}"
