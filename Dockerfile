FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Éviter les questions interactives
ENV DEBIAN_FRONTEND=noninteractive

# 1. Linux + Python + utilitaires
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

# 2. Cloner le repo Matrix-3D officiel
RUN git clone https://github.com/SkyworkAI/Matrix-3D.git matrix3d

WORKDIR /workspace/matrix3d

# 3. Installer les dépendances Python de Matrix-3D
# (Codex pourra ajuster si le repo fournit un autre fichier)
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 4. Retour dans /workspace et ajout de nos scripts custom
WORKDIR /workspace

# Créer le dossier scripts dans l'image
RUN mkdir -p /workspace/scripts

# Copier les scripts depuis le repo git
COPY scripts/download_models.sh /workspace/scripts/download_models.sh
COPY scripts/run_throne_scene.sh /workspace/scripts/run_throne_scene.sh

RUN chmod +x /workspace/scripts/download_models.sh \
             /workspace/scripts/run_throne_scene.sh

# 5. Dossiers de travail pour les modèles et les sorties
RUN mkdir -p /workspace/models /workspace/outputs

# 6. Commande par défaut : télécharger les modèles puis lancer la scène "throne"
CMD ["/bin/bash", "/workspace/scripts/run_throne_scene.sh"]
