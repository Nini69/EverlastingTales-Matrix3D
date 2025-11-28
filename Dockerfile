FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1

# Outils de base (l'image RunPod fournit déjà Python/CUDA/agent)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Cloner Matrix-3D avec les sous-modules
RUN git clone --recursive https://github.com/SkyworkAI/Matrix-3D.git matrix3d

WORKDIR /workspace/matrix3d

# Conserver le torch pré-installé (2.8.0) et éviter de le re-télécharger
# en supprimant les contraintes torch/torchvision/torchaudio des requirements
# et les éventuelles lignes pip install ... torch dans install.sh
RUN find . -maxdepth 2 -name 'requirements*.txt' -exec sed -i '/^torch==/d;/^torchvision==/d;/^torchaudio==/d' {} + && \
    sed -i '/pip install .*torch/Id' install.sh || true

# Installer les dépendances Matrix-3D (on ajoute explicitement huggingface_hub manquant)
RUN pip install --no-cache-dir huggingface_hub==0.25.2 && \
    pip install --no-cache-dir -r requirements.txt && \
    chmod +x install.sh && ./install.sh && \
    pip cache purge || true

WORKDIR /workspace

RUN mkdir -p /workspace/scripts /workspace/models /workspace/outputs

COPY scripts/download_models.sh /workspace/scripts/download_models.sh
COPY scripts/run_throne_scene.sh /workspace/scripts/run_throne_scene.sh

RUN chmod +x /workspace/scripts/download_models.sh /workspace/scripts/run_throne_scene.sh

# Ne pas toucher à l'ENTRYPOINT/CMD de l'image RunPod pour conserver Jupyter/SSH
