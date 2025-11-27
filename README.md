# Matrix-3D Pipeline (Everlasting Tales)

Ce repo contient tout ce qu'il faut pour :

1. Builder une image Docker prête pour **Matrix-3D**.
2. Pousser l'image sur **GitHub Container Registry (GHCR)**.
3. Lancer Matrix-3D sur RunPod (ou autre GPU) pour générer :
   - une vidéo panoramique
   - une scène 3D en Gaussian Splats (.ply)
   - à partir d'un prompt texte (ex : *"a throne in a dreamlike room"*).

## Structure

- `Dockerfile` : image de base (CUDA + Python + Matrix-3D + scripts perso).
- `scripts/download_models.sh` : télécharge les modèles Matrix-3D depuis Hugging Face dans `/workspace/models`.
- `scripts/run_throne_scene.sh` : exemple de génération "room + throne".
- `.github/workflows/build-matrix3d-image.yml` : CI GitHub Actions pour builder/pusher l'image sur GHCR.

## Usage local rapide (sans RunPod)

```bash
# 1) Build l'image Docker localement
docker build -t matrix3d-local .

# 2) Lancer un container avec montage du dossier outputs
docker run --gpus all -it --rm \
  -v $PWD/outputs:/workspace/outputs \
  matrix3d-local
# Le script run_throne_scene.sh sera exécuté par défaut
```

Sur RunPod, on utilisera l'image `ghcr.io/<TON_USER_GITHUB>/matrix3d:latest`
et un volume persistant monté sur `/workspace/models` et `/workspace/outputs`.
