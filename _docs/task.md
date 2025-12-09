# Débogage de l'erreur d'inférence Matrix3D

- [x] Localiser le code source de `moge`
- [x] Analyser `fix_runpod.sh`
- [x] Identifier la cause de `RuntimeError` (Shapes) & `ValueError` (Resize)
- [x] Corriger l'incompatibilité de forme de tenseur (Shapes / Device) [VALIDÉ]
- [x] Corriger la première erreur de dimensions (`log_distance_map`)
- [x] Corriger la seconde erreur de dimensions (`panorama_pred_mask`)
- [x] Corriger le crash de sauvegarde (`points.exr`)
- [x] Script `repair_matrix_final.py` mis à jour localement
- [x] Exécuter la réparation sur RunPod via commandes `echo` ligne par ligne (ÉCHOUÉ - Syntax Errors)
- [ ] **NOUVELLE STRATÉGIE : Transfert de fichier direct**
  - [x] Créer le script `final_patch.py` propre localement (sans hacks echo)
  - [x] Uploader ce fichier sur RunPod (via Script `auto_deploy_v2.py` SSH Direct)
  - [x] Exécuter `python final_patch.py` sur le serveur (Automatisé)
- [ ] **VÉRIFICATION & MONITORING**
  - [x] Récupérer les logs distants (Vérifié visuellement par l'utilisateur via Jupyter)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [-] Exécuter la commande finale dans le Web Terminal (SUSPENDU PAR L'UTILISATEUR)
- [ ] Résoudre le problème de téléchargement lent (ModelScope -> Hugging Face)
- [ ] Vérifier le correctif final

- [ ] **TENTATIVE 3 : CLEAN START (MODÈLES OFFICIELS)**
  - [ ] Créer le script `install_clean.sh` avec TOUTES les dépendances connues (`rembg`, `utils3d`, `trimesh`...)
  - [ ] Nettoyer le workspace RunPod (Git Reset Total)
  - [/] Installer les dépendances manquantes (`rembg`...)
  - [x] Fixer `huggingface_hub` (ImportError incompatible)

# Débogage de l'erreur d'inférence Matrix3D

- [x] Localiser le code source de `moge`
- [x] Analyser `fix_runpod.sh`
- [x] Identifier la cause de `RuntimeError` (Shapes) & `ValueError` (Resize)
- [x] Corriger l'incompatibilité de forme de tenseur (Shapes / Device) [VALIDÉ]
- [x] Corriger la première erreur de dimensions (`log_distance_map`)
- [x] Corriger la seconde erreur de dimensions (`panorama_pred_mask`)
- [x] Corriger le crash de sauvegarde (`points.exr`)
- [x] Script `repair_matrix_final.py` mis à jour localement
- [x] Exécuter la réparation sur RunPod via commandes `echo` ligne par ligne (ÉCHOUÉ - Syntax Errors)
- [ ] **NOUVELLE STRATÉGIE : Transfert de fichier direct**
  - [x] Créer le script `final_patch.py` propre localement (sans hacks echo)
  - [x] Uploader ce fichier sur RunPod (via Script `auto_deploy_v2.py` SSH Direct)
  - [x] Exécuter `python final_patch.py` sur le serveur (Automatisé)
- [ ] **VÉRIFICATION & MONITORING**
  - [x] Récupérer les logs distants (Vérifié visuellement par l'utilisateur via Jupyter)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [-] Exécuter la commande finale dans le Web Terminal (SUSPENDU PAR L'UTILISATEUR)
- [ ] Résoudre le problème de téléchargement lent (ModelScope -> Hugging Face)
- [ ] Vérifier le correctif final

- [ ] **TENTATIVE 3 : CLEAN START (MODÈLES OFFICIELS)**
  - [ ] Créer le script `install_clean.sh` avec TOUTES les dépendances connues (`rembg`, `utils3d`, `trimesh`...)
  - [ ] Nettoyer le workspace RunPod (Git Reset Total)
  - [/] Installer les dépendances manquantes (`rembg`...)
  - [x] Fixer `huggingface_hub` (ImportError incompatible)
  - [x] Fixer `diffusers` (FluxIPAdapterMixin missing)
  - [x] Fixer `torchvision` (Update sync)
  - [x] Fixer `xformers` (Désinstallation)
  - [x] **PIVOT MAJOR : Downgrade PyTorch 2.1.0** (Fait)

# Débogage de l'erreur d'inférence Matrix3D

- [x] Localiser le code source de `moge`
- [x] Analyser `fix_runpod.sh`
- [x] Identifier la cause de `RuntimeError` (Shapes) & `ValueError` (Resize)
- [x] Corriger l'incompatibilité de forme de tenseur (Shapes / Device) [VALIDÉ]
- [x] Corriger la première erreur de dimensions (`log_distance_map`)
- [x] Corriger la seconde erreur de dimensions (`panorama_pred_mask`)
- [x] Corriger le crash de sauvegarde (`points.exr`)
- [x] Script `repair_matrix_final.py` mis à jour localement
- [x] Exécuter la réparation sur RunPod via commandes `echo` ligne par ligne (ÉCHOUÉ - Syntax Errors)
- [ ] **NOUVELLE STRATÉGIE : Transfert de fichier direct**
  - [x] Créer le script `final_patch.py` propre localement (sans hacks echo)
  - [x] Uploader ce fichier sur RunPod (via Script `auto_deploy_v2.py` SSH Direct)
  - [x] Exécuter `python final_patch.py` sur le serveur (Automatisé)
- [ ] **VÉRIFICATION & MONITORING**
  - [x] Récupérer les logs distants (Vérifié visuellement par l'utilisateur via Jupyter)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [-] Exécuter la commande finale dans le Web Terminal (SUSPENDU PAR L'UTILISATEUR)
- [ ] Résoudre le problème de téléchargement lent (ModelScope -> Hugging Face)
- [ ] Vérifier le correctif final

- [ ] **TENTATIVE 3 : CLEAN START (MODÈLES OFFICIELS)**
  - [ ] Créer le script `install_clean.sh` avec TOUTES les dépendances connues (`rembg`, `utils3d`, `trimesh`...)
  - [ ] Nettoyer le workspace RunPod (Git Reset Total)
  - [/] Installer les dépendances manquantes (`rembg`...)
  - [x] Fixer `huggingface_hub` (ImportError incompatible)
  - [x] Fixer `diffusers` (FluxIPAdapterMixin missing)
  - [x] Fixer `torchvision` (Update sync)
  - [x] Fixer `xformers` (Désinstallation)
  - [x] **PIVOT MAJOR : Downgrade PyTorch 2.1.0** (Fait)
  - [x] Installer `pytorch3d` (Fait via Wheel)
  - [x] Fixer `transformers` (Downgrade 4.38.2)
  - [x] Fixer `accelerate` (Mise à jour insuffisante)
  - [x] **Ultra-Fix Final** : Monkey Patch V4 (XPU + Device Mesh) [SUCCÈS]
  - [x] Fixer `kornia` (Downgrade 0.7.3)
  - [x] **Ultra-Fix V5** : Monkey Patch RMSNorm (Alias LayerNorm) [SUCCÈS]
  - [x] **Fix Meta Tensor** : Injection `low_cpu_mem_usage=False` (Syntaxe OK)
  - [x] **Fix PEFT** : Installer `peft` (Manquant pour LoRA)
  - [x] **Fix Accelerate** : Update (`pip install -U accelerate`)
  - [x] **Fix Transformers** : Update (Requis par Accelerate/Flux)

# Débogage de l'erreur d'inférence Matrix3D

- [x] Localiser le code source de `moge`
- [x] Analyser `fix_runpod.sh`
- [x] Identifier la cause de `RuntimeError` (Shapes) & `ValueError` (Resize)
- [x] Corriger l'incompatibilité de forme de tenseur (Shapes / Device) [VALIDÉ]
- [x] Corriger la première erreur de dimensions (`log_distance_map`)
- [x] Corriger la seconde erreur de dimensions (`panorama_pred_mask`)
- [x] Corriger le crash de sauvegarde (`points.exr`)
- [x] Script `repair_matrix_final.py` mis à jour localement
- [x] Exécuter la réparation sur RunPod via commandes `echo` ligne par ligne (ÉCHOUÉ - Syntax Errors)
- [ ] **NOUVELLE STRATÉGIE : Transfert de fichier direct**
  - [x] Créer le script `final_patch.py` propre localement (sans hacks echo)
  - [x] Uploader ce fichier sur RunPod (via Script `auto_deploy_v2.py` SSH Direct)
  - [x] Exécuter `python final_patch.py` sur le serveur (Automatisé)
- [ ] **VÉRIFICATION & MONITORING**
  - [x] Récupérer les logs distants (Vérifié visuellement par l'utilisateur via Jupyter)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [-] Exécuter la commande finale dans le Web Terminal (SUSPENDU PAR L'UTILISATEUR)
- [ ] Résoudre le problème de téléchargement lent (ModelScope -> Hugging Face)
- [ ] Vérifier le correctif final

- [ ] **TENTATIVE 3 : CLEAN START (MODÈLES OFFICIELS)**
  - [ ] Créer le script `install_clean.sh` avec TOUTES les dépendances connues (`rembg`, `utils3d`, `trimesh`...)
  - [ ] Nettoyer le workspace RunPod (Git Reset Total)
  - [/] Installer les dépendances manquantes (`rembg`...)
  - [x] Fixer `huggingface_hub` (ImportError incompatible)

# Débogage de l'erreur d'inférence Matrix3D

- [x] Localiser le code source de `moge`
- [x] Analyser `fix_runpod.sh`
- [x] Identifier la cause de `RuntimeError` (Shapes) & `ValueError` (Resize)
- [x] Corriger l'incompatibilité de forme de tenseur (Shapes / Device) [VALIDÉ]
- [x] Corriger la première erreur de dimensions (`log_distance_map`)
- [x] Corriger la seconde erreur de dimensions (`panorama_pred_mask`)
- [x] Corriger le crash de sauvegarde (`points.exr`)
- [x] Script `repair_matrix_final.py` mis à jour localement
- [x] Exécuter la réparation sur RunPod via commandes `echo` ligne par ligne (ÉCHOUÉ - Syntax Errors)
- [ ] **NOUVELLE STRATÉGIE : Transfert de fichier direct**
  - [x] Créer le script `final_patch.py` propre localement (sans hacks echo)
  - [x] Uploader ce fichier sur RunPod (via Script `auto_deploy_v2.py` SSH Direct)
  - [x] Exécuter `python final_patch.py` sur le serveur (Automatisé)
- [ ] **VÉRIFICATION & MONITORING**
  - [x] Récupérer les logs distants (Vérifié visuellement par l'utilisateur via Jupyter)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [-] Exécuter la commande finale dans le Web Terminal (SUSPENDU PAR L'UTILISATEUR)
- [ ] Résoudre le problème de téléchargement lent (ModelScope -> Hugging Face)
- [ ] Vérifier le correctif final

- [ ] **TENTATIVE 3 : CLEAN START (MODÈLES OFFICIELS)**
  - [ ] Créer le script `install_clean.sh` avec TOUTES les dépendances connues (`rembg`, `utils3d`, `trimesh`...)
  - [ ] Nettoyer le workspace RunPod (Git Reset Total)
  - [/] Installer les dépendances manquantes (`rembg`...)
  - [x] Fixer `huggingface_hub` (ImportError incompatible)
  - [x] Fixer `diffusers` (FluxIPAdapterMixin missing)
  - [x] Fixer `torchvision` (Update sync)
  - [x] Fixer `xformers` (Désinstallation)
  - [x] **PIVOT MAJOR : Downgrade PyTorch 2.1.0** (Fait)

# Débogage de l'erreur d'inférence Matrix3D

- [x] Localiser le code source de `moge`
- [x] Analyser `fix_runpod.sh`
- [x] Identifier la cause de `RuntimeError` (Shapes) & `ValueError` (Resize)
- [x] Corriger l'incompatibilité de forme de tenseur (Shapes / Device) [VALIDÉ]
- [x] Corriger la première erreur de dimensions (`log_distance_map`)
- [x] Corriger la seconde erreur de dimensions (`panorama_pred_mask`)
- [x] Corriger le crash de sauvegarde (`points.exr`)
- [x] Script `repair_matrix_final.py` mis à jour localement
- [x] Exécuter la réparation sur RunPod via commandes `echo` ligne par ligne (ÉCHOUÉ - Syntax Errors)
- [ ] **NOUVELLE STRATÉGIE : Transfert de fichier direct**
  - [x] Créer le script `final_patch.py` propre localement (sans hacks echo)
  - [x] Uploader ce fichier sur RunPod (via Script `auto_deploy_v2.py` SSH Direct)
  - [x] Exécuter `python final_patch.py` sur le serveur (Automatisé)
- [ ] **VÉRIFICATION & MONITORING**
  - [x] Récupérer les logs distants (Vérifié visuellement par l'utilisateur via Jupyter)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [x] Confirmer le succès ou diagnostiquer l'échec précis (Fichier `final_patch.py` présent et correct)
  - [-] Exécuter la commande finale dans le Web Terminal (SUSPENDU PAR L'UTILISATEUR)
- [ ] Résoudre le problème de téléchargement lent (ModelScope -> Hugging Face)
- [ ] Vérifier le correctif final

- [ ] **TENTATIVE 3 : CLEAN START (MODÈLES OFFICIELS)**
  - [ ] Créer le script `install_clean.sh` avec TOUTES les dépendances connues (`rembg`, `utils3d`, `trimesh`...)
  - [ ] Nettoyer le workspace RunPod (Git Reset Total)
  - [/] Installer les dépendances manquantes (`rembg`...)
  - [x] Fixer `huggingface_hub` (ImportError incompatible)
  - [x] Fixer `diffusers` (FluxIPAdapterMixin missing)
  - [x] Fixer `torchvision` (Update sync)
  - [x] Fixer `xformers` (Désinstallation)
  - [x] **PIVOT MAJOR : Downgrade PyTorch 2.1.0** (Fait)
  - [x] Installer `pytorch3d` (Fait via Wheel)
  - [x] Fixer `transformers` (Downgrade 4.38.2)
  - [x] Fixer `accelerate` (Mise à jour insuffisante)
  - [x] **Ultra-Fix Final** : Monkey Patch V4 (XPU + Device Mesh) [SUCCÈS]
  - [x] Fixer `kornia` (Downgrade 0.7.3)
  - [x] **Ultra-Fix V5** : Monkey Patch RMSNorm (Alias LayerNorm) [SUCCÈS]
  - [x] **Fix Meta Tensor** : Injection `low_cpu_mem_usage=False` (Syntaxe OK)
  - [x] **Fix PEFT** : Installer `peft` (Manquant pour LoRA)
  - [x] **Fix Accelerate** : Update (`pip install -U accelerate`)
  - [x] **Fix Transformers** : Update (Requis par Accelerate/Flux)
  - [x] **Ultra-Fix V7** : Monkey Patch PyTree Wrapper (Ignore arguments) [SUCCÈS]
  - [/] **ÉTAPE 1 : Génération Panorama** (Bloqué par fichier manquant)
  - [x] **Download Models** : `python code/download_checkpoints.py` [SUCCÈS]
  - [x] **Fix LoRA Path** : `cp checkpoints/flux_lora/checkpoints/text2panoimage...` [SUCCÈS]
  - [x] **Ultra-Fix V8** : Monkey Patch SDPA (GQA compat) [SUCCÈS]
  - [x] **ÉTAPE 1 : Génération Panorama** (COMPLÉTÉE 50/50 - IMAGE OK)
  - [/] **ÉTAPE 2 : Panorama -> Vidéo** (Erreur DeviceMesh)
  - [x] **Fix Step 2** : Patch V13 (DeviceMesh Module fix)
  - [x] **Fix Step 2** : Patch V17 (Library Surgical Fix)
  - [x] **Fix Env** : Revert PyTorch 2.1.0
  - [ ] **ÉTAPE 2 : Panorama -> Vidéo** (Exécution Finale)
  - [ ] **ÉTAPE 3 : Vidéo -> 3D** (`panoramic_video_to_3DScene.py`)
