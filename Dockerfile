# syntax=docker/dockerfile:1.6
# Image RunPod avec agent + Jupyter (PyTorch 2.8.0, CUDA 12.x, Ubuntu 24.04)
FROM runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/usr/local/cuda/bin:${PATH}"

# 1. Linux + utils (avec cache apt pour limiter les re-téléchargements)
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists \
    apt-get update && apt-get install -y \
    git \
    ffmpeg \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# 2. Cloner Matrix-3D (avec sous-modules)
RUN git clone --recursive https://github.com/SkyworkAI/Matrix-3D.git matrix3d

WORKDIR /workspace/matrix3d

# 3. Installer les dépendances Python de Matrix-3D
RUN chmod +x install.sh && ./install.sh

# 4. Revenir dans /workspace et ajouter nos scripts
WORKDIR /workspace
RUN mkdir -p /workspace/scripts

COPY scripts/download_models.sh /workspace/scripts/download_models.sh
COPY scripts/run_throne_scene.sh /workspace/scripts/run_throne_scene.sh

RUN chmod +x /workspace/scripts/download_models.sh \
             /workspace/scripts/run_throne_scene.sh

# 5. Dossiers pour modèles et sorties
RUN mkdir -p /workspace/models /workspace/outputs

# IMPORTANT : ne pas définir de CMD/ENTRYPOINT pour laisser l'agent RunPod (Jupyter/SSH) fonctionner.
