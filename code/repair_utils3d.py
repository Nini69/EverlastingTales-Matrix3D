import os

# OFFENSIVE REPAIR V25: Pathfinding SANS IMPORT (Version Améliorée pour image_uv)
target_paths = [
    "/usr/local/lib/python3.10/dist-packages/utils3d/numpy/__init__.py",
    # Fallback paths
    "/usr/lib/python3.10/site-packages/utils3d/numpy/__init__.py",
    "/usr/local/lib/python3.8/dist-packages/utils3d/numpy/__init__.py"
]

target_file = None
for p in target_paths:
    if os.path.exists(p):
        target_file = p
        break

if not target_file:
    print("❌ Impossible de trouver utils3d/numpy/__init__.py.")
    print("Vérifiez l'emplacement de 'utils3d' avec 'pip show utils3d'.")
    exit(1)

print(f"🚑 Réparation V25 (No-Import) sur : {target_file}")

# 1. NETTOYAGE (On enlève les anciens patchs pour éviter les doublons)
try:
    with open(target_file, "r") as f:
        lines = f.readlines()
except Exception as e:
    print(f"❌ Erreur lecture : {e}")
    exit(1)

clean_lines = []
found_patch = False

for line in lines:
    if "PATCHED BY MATRIX3D" in line:
        found_patch = True
        break 
    clean_lines.append(line)

if found_patch:
    print("🧹 Ancien patch nettoyé.")
else:
    print("ℹ️ Code original préservé.")

# 2. INJECTION MULTIPLE (icosahedron + image_uv)
# Note: Pas de docstrings complexes (""") pour éviter SyntaxError.
safe_patch_v25 = """
# --- PATCHED BY MATRIX3D (V25) ---
import numpy as np

def icosahedron():
    # Helper: Creates Icosahedron
    t = (1.0 + 5.0**0.5) / 2.0
    verts = [
        [-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0],
        [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],
        [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1]
    ]
    faces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ]
    return np.array(verts, dtype=np.float32), np.array(faces, dtype=np.int32)

def image_uv(width, height, dtype=np.float32):
    # Helper: Get image space UV grid
    # Returns (width, height, 2) array with UV coordinates
    x = np.linspace(0.5, width - 0.5, width, dtype=dtype) / width
    y = np.linspace(0.5, height - 0.5, height, dtype=dtype) / height
    xx, yy = np.meshgrid(x, y)
    return np.stack([xx, yy], axis=-1)
"""

# Écriture
try:
    with open(target_file, "w") as f:
        f.writelines(clean_lines)
        f.write(safe_patch_v25)
    print("✅ SUCCÈS : Patch V25 appliqué (icosahedron + image_uv ajoutés).")
except Exception as e:
    print(f"❌ Erreur écriture : {e}")
