# syntax=docker/dockerfile:1.6
# Image optimisée pour RunPod (Runtime CUDA 12.1 + Python 3.10 + Deps baked-in)
# Plus léger que runpod/pytorch-devel et évite de réinstaller CUDA via apt.
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1
ENV PATH="/usr/local/cuda/bin:${PATH}"
# Rediriger le cache HF vers le volume RunPod (sera monté au runtime)
ENV HF_HOME="/workspace/data/hf-cache"
ENV TRANSFORMERS_CACHE="/workspace/data/hf-cache"

# 1. Installer Python 3.10 et outils système essentiels
# On n'installe PAS cuda-toolkit via apt (déjà dans l'image ou inutile pour le runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3-pip \
    git \
    ffmpeg \
    wget \
    ca-certificates \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/python3.10 /usr/bin/python

WORKDIR /workspace

# 2. Copier et installer les dépendances Python (Baked-in !)
COPY requirements-matrix3d.txt /tmp/requirements-matrix3d.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements-matrix3d.txt && \
    rm -rf /root/.cache/pip

# 3. Cloner Matrix-3D
RUN git clone --recursive https://github.com/SkyworkAI/Matrix-3D.git matrix3d

WORKDIR /workspace/matrix3d

# 4. Nettoyage des requirements du repo pour éviter les conflits
# On a déjà installé ce qu'il faut, on empêche le script d'install de tout casser
RUN find . -maxdepth 2 -name 'requirements*.txt' -exec sed -i '/^torch==/d;/^torchvision==/d;/^torchaudio==/d;/^numpy[><=]/d' {} + && \
    sed -i '/pip install .*torch/Id' install.sh || true && \
    chmod +x install.sh && ./install.sh || true

# 4bis. Patch des scripts pour forcer float16 et optimiser VRAM
# - panoramic_image_generation.py : bfloat16 -> float16, retirer .to(device) car enable_model_cpu_offload gère le placement
# - panoramic_image_to_video.py : bfloat16/float32 -> float16
RUN sed -i 's/torch.bfloat16/torch.float16/g' code/panoramic_image_generation.py && \
    sed -i 's/).to(device)/)/' code/panoramic_image_generation.py && \
    sed -i 's/torch.bfloat16/torch.float16/g' code/panoramic_image_to_video.py && \
    sed -i 's/torch.float32/torch.float16/g' code/panoramic_image_to_video.py

# 5. Stub torch.xpu pour compatibilité diffusers récents
RUN python - <<'PY'
import pathlib, textwrap
sitecustomize = pathlib.Path('/usr/local/lib/python3.10/dist-packages/sitecustomize.py')
stub = textwrap.dedent('''
import torch, types
if not hasattr(torch, "xpu"):
    torch.xpu = types.SimpleNamespace(
        empty_cache=lambda: None,
        is_available=lambda: False,
        device_count=lambda: 0,
        manual_seed=lambda *args, **kwargs: None,
    )
''')
sitecustomize.write_text(stub)
PY

# 6. Setup scripts et dossiers
WORKDIR /workspace
RUN mkdir -p /workspace/scripts /workspace/models /workspace/outputs /workspace/data

COPY scripts/download_models.sh /workspace/scripts/download_models.sh
COPY scripts/run_throne_scene.sh /workspace/scripts/run_throne_scene.sh

RUN chmod +x /workspace/scripts/download_models.sh \
    /workspace/scripts/run_throne_scene.sh

# Pas de CMD spécifique, on laisse RunPod lancer son agent ou un sleep infinie si besoin
# (Note: l'image nvidia n'a pas l'agent RunPod pré-installé, mais RunPod l'injecte souvent.
# Si besoin d'accès SSH/Jupyter natif, il faudra peut-être installer openssh-server/jupyterlab)

# 7. Configuration pour RunPod (Jupyter)
# On expose le port 8888 et on lance JupyterLab par défaut
EXPOSE 8888
ENV JUPYTER_ALLOW_INSECURE_WRITES=true
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
