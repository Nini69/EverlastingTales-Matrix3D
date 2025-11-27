#!/usr/bin/env bash
set -e

echo "[Matrix3D] === Throne scene generation ==="

MODELS_DIR="/workspace/models"
OUTPUT_DIR="/workspace/outputs/throne_scene"
REPO_DIR="/workspace/matrix3d"

mkdir -p "${MODELS_DIR}" "${OUTPUT_DIR}"

# 1) Télécharger les modèles si besoin
bash /workspace/scripts/download_models.sh

# 2) Aller dans le repo Matrix-3D
cd "${REPO_DIR}"

# Pour certains scripts Matrix-3D, les checkpoints sont attendus dans
# ./asset/checkpoints, etc. download_checkpoints.py gère déjà ça.
# On garde juste nos outputs personnalisés.
SCENE_OUT="${OUTPUT_DIR}"

PROMPT="a mysterious stone chamber with a central throne, dim dreamlike lighting, cinematic, highly detailed"

echo "[Matrix3D] Step 1: text -> panoramic image"
python code/panoramic_image_generation.py \
    --mode t2p \
    --prompt "${PROMPT}" \
    --output_path "${SCENE_OUT}"

# La structure attendue ensuite est :
#   ${SCENE_OUT}/pano_img.jpg
#   ${SCENE_OUT}/prompt.txt

echo "[Matrix3D] Step 2: panorama -> panoramic video (480p, low VRAM)"
VISIBLE_GPU_NUM=1
export VISIBLE_GPU_NUM

torchrun --nproc_per_node=${VISIBLE_GPU_NUM} code/panoramic_image_to_video.py \
    --inout_dir "${SCENE_OUT}" \
    --resolution 480 \
    --enable_vram_management

# Vidéo panoramique attendue :
#   ${SCENE_OUT}/pano_video.mp4

echo "[Matrix3D] Step 3: panoramic video -> 3D Gaussian Splats (.ply)"
python code/panoramic_video_to_3DScene.py \
    --inout_dir "${SCENE_OUT}" \
    --resolution 480

echo "[Matrix3D] Done!"
echo "[Matrix3D] Outputs are in: ${SCENE_OUT}"
echo "  - pano_img.jpg"
echo "  - pano_video.mp4"
echo "  - generated_3dgs_opt.ply (3D scene)"
