# Rapport RunPod / Matrix-3D

## Contexte
- Image GHCR utilisée : `ghcr.io/morinbakashabib-cloud/matrix3d:latest` (digest observé : `sha256:155a479a95…`).  
- Pods RunPod (RTX 4090, 24 Go) avec volume `/workspace/data`.  
- Le pod tire une image légère (17 Mo affichés au démarrage), signe que les dépendances Python ne sont pas incluses malgré le Dockerfile final.

## Dépendances installées manuellement (répétées sur plusieurs pods)
- `huggingface_hub` (0.25.2 puis 0.34.0)  
- `transformers` 4.38.2  
- `diffusers` 0.27.2 puis `main` (0.36.0.dev0)  
- `accelerate>=0.25`, `numpy<2`, `einops`, `opencv-python`, `open3d`, `plotly`, `dash`, `py360convert`, `scikit-image`, `sentencepiece`, `protobuf`, `plyfile`  
- Torch/vision rétrogradés à 2.2.0/0.17.0 pour tenter `pytorch3d` (échec de roue cu121) ; stub `matrix_to_quaternion` ajouté.  
- Stubs dans `sitecustomize.py` : `torch.xpu`, `torch.distributed.device_mesh`, alias `cached_download`, stub `matrix_to_quaternion`, etc.

## Erreurs rencontrées
- Modules manquants : `huggingface_hub`, `transformers`, `diffusers`, `open3d`, `plotly/dash`, `py360convert`, `scikit-image`, `plyfile`, `sentencepiece`, `protobuf`, `pytorch3d`, etc.  
- Accès HF gated : `Skywork/Matrix-3D`, `black-forest-labs/FLUX.1-dev` → besoin d’un token avec accès accordé.  
- Diffusers/torch : attributs `torch.xpu` et `device_mesh` manquants, `LayerNorm` half non supporté sur CPU, alias `cached_download` absent.  
- OOM GPU (24 Go) sur le chargement FLUX en float16. Tentatives en CPU float32 (lent).  
- Chemins modèles : les checkpoints locaux n’ont pas de `model_index.json` → `FluxPipeline.from_pretrained(/workspace/checkpoints)` impossible.  
- Scripts modifiés : suppression de `--mode/--output_path` → erreurs d’arguments dans `run_throne_scene.sh`.

## Pourquoi l’image ne contient pas tout
- Le Dockerfile final (commit `73c0008`) épingle toutes les deps et ajoute des stubs, mais l’image tirée (`sha256:155a479a95…`) semble issue d’un build antérieur minimal.  
- Résultat : chaque pod doit pip installer manuellement la pile ML + stubs.

## Saturation disque
- Pod Disk 60 Go saturé par : roues CUDA lourdes (torch/cu121), diffusers, open3d, checkpoints (~10+ Go).  
- Affichage “17 Mo” est une métrique overlay, mais l’espace se remplit après toutes les installations.

## Recommandations
1) **Rebuild/push** l’image GHCR à partir du Dockerfile final (deps + stubs) et vérifier le digest, puis **forcer le pull** sur un nouveau pod (credential GHCR `read:packages`).  
2) Restaurer/adapter `panoramic_image_generation.py` (original) et `run_throne_scene.sh` ; supprimer les options obsolètes ou supporter `--mode/--output_path`.  
3) Accès HF : s’assurer que le token possède l’accès à `black-forest-labs/FLUX.1-dev` (ou utiliser un modèle public alternatif).  
4) Réduire la conso VRAM : `torch_dtype=float16`, `TORCH_CUDA_ALLOC_CONF=expandable_segments:True`, résolution plus basse si possible. En dernier recours, CPU float32 (lent) ou modèle plus léger.  
5) Disque : augmenter le Pod Disk ou nettoyer les caches/roues après install.

## Commande utile pour la taille du workspace
- `du -sh /workspace`  
- `du -sh /workspace/* | sort -h`

## Workspace téléchargé (C:\Users\Administrateur\Downloads\workspace)
- Contenu : seulement `matrix3d/` et `scripts/`. Taille totale ~0,11 Go (`matrix3d` ~0,11 Go, `scripts` ~0 Go).  
- Sous-dossiers `matrix3d` (approx) : `asset` ~52 Mo, `submodules` ~35 Mo, `data` ~20 Mo, `code` ~7 Mo.  
- Aucun checkpoint lourd ni outputs dans cet export (pas de `.ckpt/.safetensors/.bin` trouvés). Cela confirme que les checkpoints téléchargés dans les pods (Skywork/Matrix-3D, Wan-AI, FLUX, etc.) n'ont pas été récupérés dans ce workspace (probablement stockés ailleurs ou sur un volume éphémère non inclus).  
- Conclusion : le bundle téléchargé correspond essentiellement au code et aux assets légers, pas aux modèles/outputs générés.

## Inventaire apt (matrix3d_apt_packages.txt)
- Base Ubuntu 22.04 + stack CUDA 12.1 complète : `cuda-command-line-tools-12-1`, `cuda-compiler-12-1`, `cuda-cudart-dev-12-1`, `cuda-nvcc-12-1`, `cuda-libraries-12-1`, `nvidia-cublas-12-1` etc.  
- Outils build : `build-essential`, `gcc/g++-11`, `cmake` (via deps), `git`, `python3.10-dev`, `ffmpeg`, `nginx` (pour RunPod UI), `opencl/ocl-icd`, `libgl1`, `libegl`, `libx11`, etc.  
- Rien d’exotique manquant côté système : le déficit venait bien du Python/pip, pas d’apt.

## Inventaire pip (matrix3d_pip_freeze.txt)
- PyTorch stack par défaut de l’image : `torch==2.7.0`, `torchvision==0.22.0`, `torchaudio==2.2.0`, `triton==3.3.0`, `numpy==2.2.6`. Cette combo est incompatible avec certaines libs installées plus tard (pytorch3d absent pour cu121 + torch 2.7.0, et numpy 2.2.x casse des wheels).  
- Pas de `diffusers`, `transformers`, `huggingface_hub` dans ce freeze initial, ce qui confirme qu’ils ne sont pas baked dans l’image.  
- Présence de `einops==0.8.1`, `fsspec==2024.2.0`, `httpx/httpcore`, mais absence de `open3d`, `plyfile`, `sentencepiece`, `protobuf` récent, `pytorch3d`, etc.  
- Conclusion : le set pip de base ne suffit pas pour Matrix-3D ; il faut tout réinstaller (et souvent rétrograder) à chaque pod, d’où les multiples erreurs “ModuleNotFoundError” et conflits de versions.

## Extraits / points saillants supplémentaires
- Pytorch3D : impossible à installer en cu121 + torch 2.7.0 ; aucune wheel publiée pour cette combo. Tentatives via `https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu121_pyt220/...` -> 403 ou “No matching distribution”. Workaround bricolé : stub `matrix_to_quaternion` pour éviter le crash, mais fonctionnalités 3D incomplètes.
- FLUX.1-dev (gated HF) : besoin d’un token autorisé. Avec token, chargement possible mais très lourd : OOM 24 Go en float16 GPU ; en CPU float16 erreur LayerNorm half ; CPU float32 passe mais très lent. Ajouter `torch_dtype=float16`, `low_cpu_mem_usage`, `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` peut aider, sinon réduire la résolution ou choisir un modèle plus léger.
- Tokenizers/sentencepiece/protobuf : erreurs “Cannot instantiate tokenizer from slow version” et “requires protobuf” résolues en installant `sentencepiece` + `protobuf` récents.
- Cached_download / torch.xpu / device_mesh : diffusers/transformers récents attendent `cached_download` dans huggingface_hub et `torch.xpu`/`torch.distributed.device_mesh`. Des stubs ont été ajoutés via `sitecustomize.py` pour débloquer l’import, mais ce n’est qu’un contournement. Un vrai fix serait de builder l’image avec des versions alignées (ex. torch 2.2.x + diffusers 0.27.x + huggingface_hub 0.25.x) ou d’attendre une release compatible torch 2.7.
- OOM récurrent : le flux complet (t2p -> vidéo -> 3D) dépasse ~24 Go VRAM. Pistes : `--resolution 480`, `--enable_vram_management`, `torch_dtype=float16`, pas de multi-GPU (VISIBLE_GPU_NUM=1), nettoyage `torch.cuda.empty_cache()`, et si besoin `expandable_segments:True`.
- Scripts CLI : le script amont a été modifié à plusieurs reprises ; certaines options `--mode/--output_path` n’existent plus dans `panoramic_image_generation.py`, d’où les erreurs “unrecognized arguments”. Il faut aligner `run_throne_scene.sh` sur la CLI réelle (prompt + seed, et gérer les chemins via variables d’env ou arguments propres au repo).
