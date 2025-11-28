# syntax=docker/dockerfile:1.6
# Image RunPod avec agent + Jupyter (PyTorch 2.8.0, CUDA 12.1, Ubuntu 22.04)
FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1
ENV PATH="/usr/local/cuda/bin:${PATH}"

# 1. Linux + utils
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# 2. Cloner Matrix-3D (avec sous-modules)
RUN git clone --recursive https://github.com/SkyworkAI/Matrix-3D.git matrix3d

WORKDIR /workspace/matrix3d

# 3. Installer huggingface_hub explicitement avant les autres dépendances
RUN pip install --no-cache-dir huggingface_hub==0.25.2

# 4. Installer les dépendances Python de Matrix-3D via install.sh
RUN chmod +x install.sh && ./install.sh

# 5. Revenir dans /workspace et ajouter nos scripts
WORKDIR /workspace
RUN mkdir -p /workspace/scripts

COPY scripts/download_models.sh /workspace/scripts/download_models.sh
COPY scripts/run_throne_scene.sh /workspace/scripts/run_throne_scene.sh

RUN chmod +x /workspace/scripts/download_models.sh \
             /workspace/scripts/run_throne_scene.sh

# 6. Dossiers pour modèles et sorties
RUN mkdir -p /workspace/models /workspace/outputs

# IMPORTANT : ne pas définir de CMD/ENTRYPOINT pour laisser l'agent RunPod (Jupyter/SSH) fonctionner.
