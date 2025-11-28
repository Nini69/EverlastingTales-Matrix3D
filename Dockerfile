# syntax=docker/dockerfile:1.6
# Image PyTorch déjà packagée avec torch/torchvision 2.7.0 / CUDA 12.1 pour éviter de re-télécharger les gros wheels
FROM pytorch/pytorch:2.7.0-cuda12.1-cudnn9-runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/usr/local/cuda/bin:${PATH}"

# 1. Linux + Python + utils (avec cache apt pour limiter les re-téléchargements)
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists \
    apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    ffmpeg \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Alias python -> python3 (certains runners n'ont que python3 en binaire)
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

WORKDIR /workspace

# 2. Cloner Matrix-3D (avec sous-modules)
RUN git clone --recursive https://github.com/SkyworkAI/Matrix-3D.git matrix3d

WORKDIR /workspace/matrix3d

# 3. Torch/torchvision déjà présents dans l'image de base (2.7.0 / 0.22.0).
# On laisse pip gérer uniquement les dépendances de Matrix-3D via install.sh.

# 4. Lancer le script d'installation Matrix-3D
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

# 7. Commande par défaut : télécharger les modèles puis générer la scène "throne"
CMD ["/bin/bash", "/workspace/scripts/run_throne_scene.sh"]
