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

# 3. Nettoyer les contraintes torch/vision/numpy pour imposer nos versions CUDA 12.1
RUN find . -maxdepth 2 -name 'requirements*.txt' -exec sed -i '/^torch==/d;/^torchvision==/d;/^torchaudio==/d;/^numpy[><=]/d' {} + && \
    sed -i '/pip install .*torch/Id' install.sh || true

# 4. Forcer numpy<2, torch/torchvision cu121 et dépendances Matrix-3D (HF + diffusers + vision 3D)
RUN pip install --no-cache-dir "numpy<2" && \
    pip install --no-cache-dir torch==2.7.0 torchvision==0.22.0 --extra-index-url https://download.pytorch.org/whl/cu121 && \
    pip install --no-cache-dir huggingface_hub==0.34.0 transformers==4.38.2 "accelerate>=0.25" einops opencv-python open3d plotly dash && \
    pip install --no-cache-dir --no-deps git+https://github.com/huggingface/diffusers.git@main && \
    pip install --no-cache-dir -r requirements.txt && \
    chmod +x install.sh && ./install.sh || true

# 4bis. xformers peut être incompatible : on le désactive pour éviter les crashs
RUN pip uninstall -y xformers || true && pip cache purge || true
ENV XFORMERS_DISABLE_FLASH_ATTN=1

# 5. Revenir dans /workspace et ajouter nos scripts
WORKDIR /workspace
RUN mkdir -p /workspace/scripts /workspace/models /workspace/outputs

COPY scripts/download_models.sh /workspace/scripts/download_models.sh
COPY scripts/run_throne_scene.sh /workspace/scripts/run_throne_scene.sh

RUN chmod +x /workspace/scripts/download_models.sh \
             /workspace/scripts/run_throne_scene.sh

# 6. Dossiers pour modèles et sorties
RUN mkdir -p /workspace/models /workspace/outputs

# IMPORTANT : ne pas définir de CMD/ENTRYPOINT pour laisser l'agent RunPod (Jupyter/SSH) fonctionner.
