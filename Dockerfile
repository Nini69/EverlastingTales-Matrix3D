# syntax=docker/dockerfile:1.6
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

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

# Alias python -> python3
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

WORKDIR /workspace

# 2. Cloner Matrix-3D (avec sous-modules)
RUN git clone --recursive https://github.com/SkyworkAI/Matrix-3D.git matrix3d

WORKDIR /workspace/matrix3d

# 3. Installer torch + torchvision (versions conseillées)
# On force des timeouts/retries et on cache pip pour éviter de tout re-télécharger.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install --default-timeout=300 --retries 10 --progress-bar off \
      torch==2.7.0 torchvision==0.22.0

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
