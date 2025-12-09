# Manifeste d'Installation Matrix3D (RunPod)

État des lieux consolidé pour éviter les régressions.

## 🏆 La configuration GAGNANTE (Validée)

Notre stratégie actuelle repose sur le "Socle PyTorch 2.1" qui permet d'utiliser Pytorch3D sans compilation.

| Composant           | Version Installée | Pourquoi cette version ?                                                                                 |
| :------------------ | :---------------- | :------------------------------------------------------------------------------------------------------- |
| **PyTorch**         | `2.1.0+cu121`     | **OBLIGATOIRE** pour utiliser le wheel Pytorch3D officiel. (La v2.5 forçait la compilation et échouait). |
| **PyTorch3D**       | `0.7.5`           | Installé via Wheel officiel Facebook (Compatible Torch 2.1).                                             |
| **HuggingFace Hub** | `0.24.7`          | **FIXÉ**. La v0.25+ cassait `cached_download`.                                                           |
| **Transformers**    | `4.38.2`          | **FIXÉ**. Downgradé car la version "Latest" utilisait des fonctions inconnues de Torch 2.1.              |
| **Kornia**          | `0.7.3`           | **FIXÉ**. La version récente crashait (`ImportError: build_laplacian_pyramid`).                          |
| **Diffusers**       | `Latest` (0.30+)  | Requis pour le modèle **Flux** (ne marche pas avec les vieilles versions).                               |
| **Accelerate**      | `Latest`          | **EN COURS DE FIX**. Requis à jour pour gérer la compatibilité Diffusers/Torch 2.1 (Erreur XPU).         |
| **Xformers**        | **DÉSINSTALLÉ**   | Causait des conflits de Symboles C++ avec Torch. Pas indispensable.                                      |

---

## 🛠️ Commandes de Référence

Si le Pod crashe et qu'il faut tout réinstaller, voici l'ordre exact :

### 1. Socle PyTorch 2.1

```bash
pip uninstall -y torch torchvision torchaudio xformers
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
```

### 2. PyTorch3D (Wheel Officiel)

```bash
pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu121_pyt210/download.html
```

### 3. Dépendances Fixées (HuggingFace & Utils)

```bash
pip install "huggingface_hub==0.24.7" "transformers==4.38.2" "kornia==0.7.3" accelerate rembg trimesh "imageio[ffmpeg]" scikit-image onnxruntime utils3d einops open3d plotly dash py360convert plyfile
```

---

## 🔴 Historique des Problèmes & Solutions

1.  **Erreur `nms` / `torchvision`**
    - _Cause_ : Mismatch entre Torch et Torchvision.
    - _Fix_ : Réalignement sur les versions 2.1.0 / 0.16.0.
2.  **Erreur `FluxIPAdapterMixin`**
    - _Cause_ : Diffusers trop vieux.
    - _Fix_ : Diffusers mis à jour (Latest).
3.  **Erreur `nvcc not found` (Compilation Pytorch3D)**
    - _Cause_ : Pas de compilateur sur le Pod.
    - _Fix_ : Abandon de la compilation -> Passage aux Wheels officiels (nécessitant Torch 2.1).
4.  **Erreur `AttributeError: 'xpu'` & `device_mesh`**
    - _Cause_ : Diffusers trop récent pour PyTorch 2.1.
    - _Fix Major_ : **Monkey Patch (V4)**. On simule TOUT : `xpu` complet + `torch.distributed.device_mesh`.
    - **Statut** : 🟢 **SUCCÈS** (Le script démarre et télécharge les modèles).
5.  **Erreur `ImportError: build_laplacian_pyramid` (Kornia)**

# Manifeste d'Installation Matrix3D (RunPod)

État des lieux consolidé pour éviter les régressions.

## 🏆 La configuration GAGNANTE (Validée)

Notre stratégie actuelle repose sur le "Socle PyTorch 2.1" qui permet d'utiliser Pytorch3D sans compilation.

| Composant           | Version Installée | Pourquoi cette version ?                                                                                 |
| :------------------ | :---------------- | :------------------------------------------------------------------------------------------------------- |
| **PyTorch**         | `2.1.0+cu121`     | **OBLIGATOIRE** pour utiliser le wheel Pytorch3D officiel. (La v2.5 forçait la compilation et échouait). |
| **PyTorch3D**       | `0.7.5`           | Installé via Wheel officiel Facebook (Compatible Torch 2.1).                                             |
| **HuggingFace Hub** | `0.24.7`          | **FIXÉ**. La v0.25+ cassait `cached_download`.                                                           |
| **Transformers**    | `4.38.2`          | **FIXÉ**. Downgradé car la version "Latest" utilisait des fonctions inconnues de Torch 2.1.              |
| **Kornia**          | `0.7.3`           | **FIXÉ**. La version récente crashait (`ImportError: build_laplacian_pyramid`).                          |
| **Diffusers**       | `Latest` (0.30+)  | Requis pour le modèle **Flux** (ne marche pas avec les vieilles versions).                               |
| **Accelerate**      | `Latest`          | **EN COURS DE FIX**. Requis à jour pour gérer la compatibilité Diffusers/Torch 2.1 (Erreur XPU).         |
| **Xformers**        | **DÉSINSTALLÉ**   | Causait des conflits de Symboles C++ avec Torch. Pas indispensable.                                      |

---

## 🛠️ Commandes de Référence

Si le Pod crashe et qu'il faut tout réinstaller, voici l'ordre exact :

### 1. Socle PyTorch 2.1

```bash
pip uninstall -y torch torchvision torchaudio xformers
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
```

### 2. PyTorch3D (Wheel Officiel)

```bash
pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu121_pyt210/download.html
```

### 3. Dépendances Fixées (HuggingFace & Utils)

```bash
pip install "huggingface_hub==0.24.7" "transformers==4.38.2" "kornia==0.7.3" accelerate rembg trimesh "imageio[ffmpeg]" scikit-image onnxruntime utils3d einops open3d plotly dash py360convert plyfile
```

---

## 🔴 Historique des Problèmes & Solutions

1.  **Erreur `nms` / `torchvision`**
    - _Cause_ : Mismatch entre Torch et Torchvision.
    - _Fix_ : Réalignement sur les versions 2.1.0 / 0.16.0.
2.  **Erreur `FluxIPAdapterMixin`**
    - _Cause_ : Diffusers trop vieux.
    - _Fix_ : Diffusers mis à jour (Latest).
3.  **Erreur `nvcc not found` (Compilation Pytorch3D)**
    - _Cause_ : Pas de compilateur sur le Pod.
    - _Fix_ : Abandon de la compilation -> Passage aux Wheels officiels (nécessitant Torch 2.1).
4.  **Erreur `AttributeError: 'xpu'` & `device_mesh`**
    - _Cause_ : Diffusers trop récent pour PyTorch 2.1.
    - _Fix Major_ : **Monkey Patch (V4)**. On simule TOUT : `xpu` complet + `torch.distributed.device_mesh`.
    - **Statut** : 🟢 **SUCCÈS** (Le script démarre et télécharge les modèles).
5.  **Erreur `ImportError: build_laplacian_pyramid` (Kornia)**

    - _Cause_ : La version de `kornia` installée (probablement 0.8+) a supprimé cette fonction.
    - _Fix_ : Downgrade vers `kornia==0.7.3`.
    - **Statut** : 🟢 **SUCCÈS**.

6.  **Erreur `AttributeError: torch.nn has no attribute RMSNorm`**

# Manifeste d'Installation Matrix3D (RunPod)

État des lieux consolidé pour éviter les régressions.

## 🏆 La configuration GAGNANTE (Validée)

Notre stratégie actuelle repose sur le "Socle PyTorch 2.1" qui permet d'utiliser Pytorch3D sans compilation.

| Composant           | Version Installée | Pourquoi cette version ?                                                                                 |
| :------------------ | :---------------- | :------------------------------------------------------------------------------------------------------- |
| **PyTorch**         | `2.1.0+cu121`     | **OBLIGATOIRE** pour utiliser le wheel Pytorch3D officiel. (La v2.5 forçait la compilation et échouait). |
| **PyTorch3D**       | `0.7.5`           | Installé via Wheel officiel Facebook (Compatible Torch 2.1).                                             |
| **HuggingFace Hub** | `0.24.7`          | **FIXÉ**. La v0.25+ cassait `cached_download`.                                                           |
| **Transformers**    | `4.38.2`          | **FIXÉ**. Downgradé car la version "Latest" utilisait des fonctions inconnues de Torch 2.1.              |
| **Kornia**          | `0.7.3`           | **FIXÉ**. La version récente crashait (`ImportError: build_laplacian_pyramid`).                          |
| **Diffusers**       | `Latest` (0.30+)  | Requis pour le modèle **Flux** (ne marche pas avec les vieilles versions).                               |
| **Accelerate**      | `Latest`          | **EN COURS DE FIX**. Requis à jour pour gérer la compatibilité Diffusers/Torch 2.1 (Erreur XPU).         |
| **Xformers**        | **DÉSINSTALLÉ**   | Causait des conflits de Symboles C++ avec Torch. Pas indispensable.                                      |

---

## 🛠️ Commandes de Référence

Si le Pod crashe et qu'il faut tout réinstaller, voici l'ordre exact :

### 1. Socle PyTorch 2.1

```bash
pip uninstall -y torch torchvision torchaudio xformers
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
```

### 2. PyTorch3D (Wheel Officiel)

```bash
pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu121_pyt210/download.html
```

### 3. Dépendances Fixées (HuggingFace & Utils)

```bash
pip install "huggingface_hub==0.24.7" "transformers==4.38.2" "kornia==0.7.3" accelerate rembg trimesh "imageio[ffmpeg]" scikit-image onnxruntime utils3d einops open3d plotly dash py360convert plyfile
```

---

## 🔴 Historique des Problèmes & Solutions

1.  **Erreur `nms` / `torchvision`**
    - _Cause_ : Mismatch entre Torch et Torchvision.
    - _Fix_ : Réalignement sur les versions 2.1.0 / 0.16.0.
2.  **Erreur `FluxIPAdapterMixin`**
    - _Cause_ : Diffusers trop vieux.
    - _Fix_ : Diffusers mis à jour (Latest).
3.  **Erreur `nvcc not found` (Compilation Pytorch3D)**
    - _Cause_ : Pas de compilateur sur le Pod.
    - _Fix_ : Abandon de la compilation -> Passage aux Wheels officiels (nécessitant Torch 2.1).
4.  **Erreur `AttributeError: 'xpu'` & `device_mesh`**
    - _Cause_ : Diffusers trop récent pour PyTorch 2.1.
    - _Fix Major_ : **Monkey Patch (V4)**. On simule TOUT : `xpu` complet + `torch.distributed.device_mesh`.
    - **Statut** : 🟢 **SUCCÈS** (Le script démarre et télécharge les modèles).
5.  **Erreur `ImportError: build_laplacian_pyramid` (Kornia)**

    - _Cause_ : La version de `kornia` installée (probablement 0.8+) a supprimé cette fonction.
    - _Fix_ : Downgrade vers `kornia==0.7.3`.
    - **Statut** : 🟢 **SUCCÈS**.

6.  **Erreur `AttributeError: torch.nn has no attribute RMSNorm`**

Notre stratégie actuelle repose sur le "Socle PyTorch 2.1" qui permet d'utiliser Pytorch3D sans compilation.

| Composant           | Version Installée | Pourquoi cette version ?                                                                                  |
| :------------------ | :---------------- | :-------------------------------------------------------------------------------------------------------- |
| **PyTorch**         | `2.1.0+cu121`     | **OBLIGATOIRE** pour utiliser le wheel Pytorch33D officiel. (La v2.5 forçait la compilation et échouait). |
| **PyTorch3D**       | `0.7.5`           | Installé via Wheel officiel Facebook (Compatible Torch 2.1).                                              |
| **PyTorch**         | `2.1.0+cu121`     | **OBLIGATOIRE** pour utiliser le wheel Pytorch3D officiel. (La v2.5 forçait la compilation et échouait).  |
| **PyTorch3D**       | `0.7.5`           | Installé via Wheel officiel Facebook (Compatible Torch 2.1).                                              |
| **HuggingFace Hub** | `0.24.7`          | **FIXÉ**. La v0.25+ cassait `cached_download`.                                                            |
| **Transformers**    | `Latest` (4.x)    | **MIS À JOUR**. Nécessite le **Monkey Patch V7** (PyTree Wrapper) pour fonctionner sur Torch 2.1.         |
| **Kornia**          | `0.7.3`           | **FIXÉ**. La version récente crashait (`ImportError: build_laplacian_pyramid`).                           |
| **Diffusers**       | `Latest` (0.30+)  | Requis pour le modèle **Flux**. Nécessite le **Monkey Patch V5** (XPU/DeviceMesh).                        |
| **Accelerate**      | `Latest`          | **MIS À JOUR**. Requis pour supporter `peft` et `diffusers` récents.                                      |
| **Xformers**        | **DÉSINSTALLÉ**   | Causait des conflits. Pas indispensable.                                                                  |

---

## 🛠️ Commandes de Référence

Si le Pod crashe et qu'il faut tout réinstaller, voici l'ordre exact :

### 1. Socle PyTorch 2.1

```bash
pip uninstall -y torch torchvision torchaudio xformers
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
```

### 2. PyTorch3D (Wheel Officiel)

```bash
pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu121_pyt210/download.html
```

### 3. Dépendances Fixées (HuggingFace & Utils)

```bash
pip install "huggingface_hub==0.24.7" "transformers==4.38.2" "kornia==0.7.3" accelerate rembg trimesh "imageio[ffmpeg]" scikit-image onnxruntime utils3d einops open3d plotly dash py360convert plyfile
```

---

## 🔴 Historique des Problèmes & Solutions

1.  **Erreur `nms` / `torchvision`**
    - _Cause_ : Mismatch entre Torch et Torchvision.
    - _Fix_ : Réalignement sur les versions 2.1.0 / 0.16.0.
2.  **Erreur `FluxIPAdapterMixin`**
    - _Cause_ : Diffusers trop vieux.
    - _Fix_ : Diffusers mis à jour (Latest).
3.  **Erreur `nvcc not found` (Compilation Pytorch3D)**
    - _Cause_ : Pas de compilateur sur le Pod.
    - _Fix_ : Abandon de la compilation -> Passage aux Wheels officiels (nécessitant Torch 2.1).
4.  **Erreur `AttributeError: 'xpu'` & `device_mesh`**
    - _Cause_ : Diffusers trop récent pour PyTorch 2.1.
    - _Fix Major_ : **Monkey Patch (V4)**. On simule TOUT : `xpu` complet + `torch.distributed.device_mesh`.
    - **Statut** : 🟢 **SUCCÈS** (Le script démarre et télécharge les modèles).
5.  **Erreur `ImportError: build_laplacian_pyramid` (Kornia)**

# Manifeste d'Installation Matrix3D (RunPod)

État des lieux consolidé pour éviter les régressions.

## 🏆 La configuration GAGNANTE (Validée)

Notre stratégie actuelle repose sur le "Socle PyTorch 2.1" qui permet d'utiliser Pytorch3D sans compilation.

| Composant           | Version Installée | Pourquoi cette version ?                                                                                 |
| :------------------ | :---------------- | :------------------------------------------------------------------------------------------------------- |
| **PyTorch**         | `2.1.0+cu121`     | **OBLIGATOIRE** pour utiliser le wheel Pytorch3D officiel. (La v2.5 forçait la compilation et échouait). |
| **PyTorch3D**       | `0.7.5`           | Installé via Wheel officiel Facebook (Compatible Torch 2.1).                                             |
| **HuggingFace Hub** | `0.24.7`          | **FIXÉ**. La v0.25+ cassait `cached_download`.                                                           |
| **Transformers**    | `4.38.2`          | **FIXÉ**. Downgradé car la version "Latest" utilisait des fonctions inconnues de Torch 2.1.              |
| **Kornia**          | `0.7.3`           | **FIXÉ**. La version récente crashait (`ImportError: build_laplacian_pyramid`).                          |
| **Diffusers**       | `Latest` (0.30+)  | Requis pour le modèle **Flux** (ne marche pas avec les vieilles versions).                               |
| **Accelerate**      | `Latest`          | **EN COURS DE FIX**. Requis à jour pour gérer la compatibilité Diffusers/Torch 2.1 (Erreur XPU).         |
| **Xformers**        | **DÉSINSTALLÉ**   | Causait des conflits de Symboles C++ avec Torch. Pas indispensable.                                      |

---

## 🛠️ Commandes de Référence

Si le Pod crashe et qu'il faut tout réinstaller, voici l'ordre exact :

### 1. Socle PyTorch 2.1

```bash
pip uninstall -y torch torchvision torchaudio xformers
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
```

### 2. PyTorch3D (Wheel Officiel)

```bash
pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu121_pyt210/download.html
```

### 3. Dépendances Fixées (HuggingFace & Utils)

```bash
pip install "huggingface_hub==0.24.7" "transformers==4.38.2" "kornia==0.7.3" accelerate rembg trimesh "imageio[ffmpeg]" scikit-image onnxruntime utils3d einops open3d plotly dash py360convert plyfile
```

---

## 🔴 Historique des Problèmes & Solutions

1.  **Erreur `nms` / `torchvision`**
    - _Cause_ : Mismatch entre Torch et Torchvision.
    - _Fix_ : Réalignement sur les versions 2.1.0 / 0.16.0.
2.  **Erreur `FluxIPAdapterMixin`**
    - _Cause_ : Diffusers trop vieux.
    - _Fix_ : Diffusers mis à jour (Latest).
3.  **Erreur `nvcc not found` (Compilation Pytorch3D)**
    - _Cause_ : Pas de compilateur sur le Pod.
    - _Fix_ : Abandon de la compilation -> Passage aux Wheels officiels (nécessitant Torch 2.1).
4.  **Erreur `AttributeError: 'xpu'` & `device_mesh`**
    - _Cause_ : Diffusers trop récent pour PyTorch 2.1.
    - _Fix Major_ : **Monkey Patch (V4)**. On simule TOUT : `xpu` complet + `torch.distributed.device_mesh`.
    - **Statut** : 🟢 **SUCCÈS** (Le script démarre et télécharge les modèles).
5.  **Erreur `ImportError: build_laplacian_pyramid` (Kornia)**

    - _Cause_ : La version de `kornia` installée (probablement 0.8+) a supprimé cette fonction.
    - _Fix_ : Downgrade vers `kornia==0.7.3`.
    - **Statut** : 🟢 **SUCCÈS**.

6.  **Erreur `AttributeError: torch.nn has no attribute RMSNorm`**

# Manifeste d'Installation Matrix3D (RunPod)

État des lieux consolidé pour éviter les régressions.

## 🏆 La configuration GAGNANTE (Validée)

Notre stratégie actuelle repose sur le "Socle PyTorch 2.1" qui permet d'utiliser Pytorch3D sans compilation.

| Composant           | Version Installée | Pourquoi cette version ?                                                                                 |
| :------------------ | :---------------- | :------------------------------------------------------------------------------------------------------- |
| **PyTorch**         | `2.1.0+cu121`     | **OBLIGATOIRE** pour utiliser le wheel Pytorch3D officiel. (La v2.5 forçait la compilation et échouait). |
| **PyTorch3D**       | `0.7.5`           | Installé via Wheel officiel Facebook (Compatible Torch 2.1).                                             |
| **HuggingFace Hub** | `0.24.7`          | **FIXÉ**. La v0.25+ cassait `cached_download`.                                                           |
| **Transformers**    | `4.38.2`          | **FIXÉ**. Downgradé car la version "Latest" utilisait des fonctions inconnues de Torch 2.1.              |
| **Kornia**          | `0.7.3`           | **FIXÉ**. La version récente crashait (`ImportError: build_laplacian_pyramid`).                          |
| **Diffusers**       | `Latest` (0.30+)  | Requis pour le modèle **Flux** (ne marche pas avec les vieilles versions).                               |
| **Accelerate**      | `Latest`          | **EN COURS DE FIX**. Requis à jour pour gérer la compatibilité Diffusers/Torch 2.1 (Erreur XPU).         |
| **Xformers**        | **DÉSINSTALLÉ**   | Causait des conflits de Symboles C++ avec Torch. Pas indispensable.                                      |

---

## 🛠️ Commandes de Référence

Si le Pod crashe et qu'il faut tout réinstaller, voici l'ordre exact :

### 1. Socle PyTorch 2.1

```bash
pip uninstall -y torch torchvision torchaudio xformers
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
```

### 2. PyTorch3D (Wheel Officiel)

```bash
pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu121_pyt210/download.html
```

### 3. Dépendances Fixées (HuggingFace & Utils)

```bash
pip install "huggingface_hub==0.24.7" "transformers==4.38.2" "kornia==0.7.3" accelerate rembg trimesh "imageio[ffmpeg]" scikit-image onnxruntime utils3d einops open3d plotly dash py360convert plyfile
```

---

## 🔴 Historique des Problèmes & Solutions

1.  **Erreur `nms` / `torchvision`**
    - _Cause_ : Mismatch entre Torch et Torchvision.
    - _Fix_ : Réalignement sur les versions 2.1.0 / 0.16.0.
2.  **Erreur `FluxIPAdapterMixin`**
    - _Cause_ : Diffusers trop vieux.
    - _Fix_ : Diffusers mis à jour (Latest).
3.  **Erreur `nvcc not found` (Compilation Pytorch3D)**
    - _Cause_ : Pas de compilateur sur le Pod.
    - _Fix_ : Abandon de la compilation -> Passage aux Wheels officiels (nécessitant Torch 2.1).
4.  **Erreur `AttributeError: 'xpu'` & `device_mesh`**
    - _Cause_ : Diffusers trop récent pour PyTorch 2.1.
    - _Fix Major_ : **Monkey Patch (V4)**. On simule TOUT : `xpu` complet + `torch.distributed.device_mesh`.
    - **Statut** : 🟢 **SUCCÈS** (Le script démarre et télécharge les modèles).
5.  **Erreur `ImportError: build_laplacian_pyramid` (Kornia)**

    - _Cause_ : La version de `kornia` installée (probablement 0.8+) a supprimé cette fonction.
    - _Fix_ : Downgrade vers `kornia==0.7.3`.

## 🚀 État Actuel : GÉNÉRATION EN COURS (Enfin !)

Tous les verrous ont sauté.

- **Monkey Patch V5** : Gère XPU, Device Mesh, RMSNorm.
- **Kornia Fix** : Gère l'erreur d'import.
- **Meta Tensor Fix** : Gère le chargement mémoire.

Notre stratégie actuelle repose sur le "Socle PyTorch 2.1" qui permet d'utiliser Pytorch3D sans compilation.

| Composant           | Version Installée | Pourquoi cette version ?                                                                                 |
| :------------------ | :---------------- | :------------------------------------------------------------------------------------------------------- |
| **PyTorch**         | `2.1.0+cu121`     | **OBLIGATOIRE** pour utiliser le wheel Pytorch3D officiel. (La v2.5 forçait la compilation et échouait). |
| **PyTorch3D**       | `0.7.5`           | Installé via Wheel officiel Facebook (Compatible Torch 2.1).                                             |
| **HuggingFace Hub** | `0.24.7`          | **FIXÉ**. La v0.25+ cassait `cached_download`.                                                           |
| **Transformers**    | `4.38.2`          | **FIXÉ**. Downgradé car la version "Latest" utilisait des fonctions inconnues de Torch 2.1.              |
| **Kornia**          | `0.7.3`           | **FIXÉ**. La version récente crashait (`ImportError: build_laplacian_pyramid`).                          |
| **Diffusers**       | `Latest` (0.30+)  | Requis pour le modèle **Flux** (ne marche pas avec les vieilles versions).                               |
| **Accelerate**      | `Latest`          | **EN COURS DE FIX**. Requis à jour pour gérer la compatibilité Diffusers/Torch 2.1 (Erreur XPU).         |
| **Xformers**        | **DÉSINSTALLÉ**   | Causait des conflits de Symboles C++ avec Torch. Pas indispensable.                                      |

---

## 🛠️ Commandes de Référence

Si le Pod crashe et qu'il faut tout réinstaller, voici l'ordre exact :

### 1. Socle PyTorch 2.1

```bash
pip uninstall -y torch torchvision torchaudio xformers
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
```

### 2. PyTorch3D (Wheel Officiel)

```bash
pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu121_pyt210/download.html
```

### 3. Dépendances Fixées (HuggingFace & Utils)

```bash
pip install "huggingface_hub==0.24.7" "transformers==4.38.2" "kornia==0.7.3" accelerate rembg trimesh "imageio[ffmpeg]" scikit-image onnxruntime utils3d einops open3d plotly dash py360convert plyfile
```

---

## 🔴 Historique des Problèmes & Solutions

1.  **Erreur `nms` / `torchvision`**
    - _Cause_ : Mismatch entre Torch et Torchvision.
    - _Fix_ : Réalignement sur les versions 2.1.0 / 0.16.0.
2.  **Erreur `FluxIPAdapterMixin`**
    - _Cause_ : Diffusers trop vieux.
    - _Fix_ : Diffusers mis à jour (Latest).
3.  **Erreur `nvcc not found` (Compilation Pytorch3D)**
    - _Cause_ : Pas de compilateur sur le Pod.
    - _Fix_ : Abandon de la compilation -> Passage aux Wheels officiels (nécessitant Torch 2.1).
4.  **Erreur `AttributeError: 'xpu'` & `device_mesh`**
    - _Cause_ : Diffusers trop récent pour PyTorch 2.1.
    - _Fix Major_ : **Monkey Patch (V4)**. On simule TOUT : `xpu` complet + `torch.distributed.device_mesh`.
    - **Statut** : 🟢 **SUCCÈS** (Le script démarre et télécharge les modèles).
5.  **Erreur `ImportError: build_laplacian_pyramid` (Kornia)**

    - _Cause_ : La version de `kornia` installée (probablement 0.8+) a supprimé cette fonction.
    - _Fix_ : Downgrade vers `kornia==0.7.3`.
    - **Statut** : 🟢 **SUCCÈS**.

6.  **Erreur `RuntimeError: DeviceMesh`**

    - _Cause_ : Mock incorrect (Class vs Module).
    - _Fix_ : Patch V13 (Correction du type).
    - **Statut** : 🟢 **SUCCÈS**.

7.  **Erreur `ImportError: templated_ring_attention`**

    - _Cause_ : Import Python résistant au mocking.
    - _Fix_ : **Patch V17 (Chirurgical)**. Modification directe du fichier `usp.py` de la librairie `xfuser`.
    - **Statut** : 🟢 **SUCCÈS**.

    - **Statut** : 🟢 **SUCCÈS**.

---

## 🏗️ Améliorations Template Docker (Rapport Codex)

Pour pérenniser l'environnement et réparer Jupyter automatiquement dans les futures versions de l'image Docker, voici les actions à intégrer au `Dockerfile` :

### 1. Fix du package `entrypoints` (Cassé dans l'image actuelle)

Le package `entrypoints` est corrompu, ce qui empêche Jupyter de démarrer.

**Action Dockerfile :**

```dockerfile
# Réparation entrypoints pour Jupyter
RUN rm -rf /usr/local/lib/python3.10/dist-packages/entrypoints* && \
    pip install --no-cache-dir -I entrypoints==0.4
```

### 2. Configuration Jupyter par défaut

Pour éviter de devoir passer des arguments complexes manuellement.

**Action Dockerfile :**

```dockerfile
# Création de la config Jupyter
RUN mkdir -p /root/.jupyter && \
    echo "c.ServerApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_server_config.py && \
    echo "c.ServerApp.port = 8888" >> /root/.jupyter/jupyter_server_config.py && \
    echo "c.ServerApp.open_browser = False" >> /root/.jupyter/jupyter_server_config.py && \
    echo "c.ServerApp.allow_root = True" >> /root/.jupyter/jupyter_server_config.py && \
    echo "c.ServerApp.token = 'codextoken'" >> /root/.jupyter/jupyter_server_config.py && \
    echo "c.ServerApp.password = ''" >> /root/.jupyter/jupyter_server_config.py
```

### 3. Commande de Démarrage (CMD)

Pour lancer Jupyter automatiquement au start du Pod.

**Action Dockerfile (CMD) :**

```dockerfile
CMD ["jupyter", "lab", "--config=/root/.jupyter/jupyter_server_config.py", "--no-browser", "--allow-root"]
```
