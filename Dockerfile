FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Linux + Python + utils
RUN apt-get update && apt-get install -y \
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
RUN pip install --upgrade pip && \
    pip install torch==2.7.0 torchvision==0.22.0

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
