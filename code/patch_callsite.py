import os

# --- PATCHER AUTOMATIQUE V29 (Call Site Fixes DUO) ---

# 1. Localiser le fichier infer_panorama.py
current_dir = os.path.dirname(os.path.abspath(__file__))
# Cible : code/MoGe/scripts/infer_panorama.py
target_rel = os.path.join(current_dir, "MoGe", "scripts", "infer_panorama.py")

if not os.path.exists(target_rel):
    target_rel = os.path.abspath("code/MoGe/scripts/infer_panorama.py")
    if not os.path.exists(target_rel):
        print(f"❌ Fichier non trouvé : {target_rel}")
        exit(1)

print(f"🎯 Cible identifiée : {target_rel}")

# 2. PATTERNS
# --- Pattern 1: unproject_cv (DEPTH FIX) ---
pat1_legacy = "utils3d.numpy.unproject_cv(uv,"
pat1_v27_broken = "utils3d.numpy.unproject_cv(uv, 1.0,"
# On utilise (uv[..., 0:1] * 0 + 1)
fix1 = "utils3d.numpy.unproject_cv(uv, (uv[..., 0:1] * 0 + 1),"

# --- Pattern 2: uv_to_pixel (WIDTH/HEIGHT KWARGS FIX) ---
# Original: pixels = utils3d.numpy.uv_to_pixel(spherical_uv, width=width, height=height).astype(np.float32)
pat2_legacy = "utils3d.numpy.uv_to_pixel(spherical_uv, width=width, height=height)"
# Fix: pixels = utils3d.numpy.uv_to_pixel(spherical_uv, (width, height))
fix2 = "utils3d.numpy.uv_to_pixel(spherical_uv, (width, height))"

# 3. LECTURE & PATCH
with open(target_rel, "r") as f:
    lines = f.readlines()

new_lines = []
patched_count = 0

for i, line in enumerate(lines):
    new_line = line
    
    # --- PATCH 1: unproject_cv ---
    if pat1_v27_broken in new_line:
        print(f"� Fix Unproject (V27->V28) L{i+1}")
        new_line = new_line.replace(pat1_v27_broken, fix1)
        patched_count += 1
    elif pat1_legacy in new_line and fix1 not in new_line and "depth" not in new_line:
        print(f"� Fix Unproject (Legacy->V28) L{i+1}")
        new_line = new_line.replace(pat1_legacy, fix1)
        patched_count += 1
        
    # --- PATCH 2: uv_to_pixel ---
    if pat2_legacy in new_line:
        print(f"� Fix UV_to_Pixel (V29) L{i+1}")
        new_line = new_line.replace(pat2_legacy, fix2)
        patched_count += 1
        
    new_lines.append(new_line)

# 4. Write Back
if patched_count > 0:
    with open(target_rel, "w") as f:
        f.writelines(new_lines)
    print(f"✅ SUCCÈS : {patched_count} correctifs appliqués (V29 Update).")
else:
    print("ℹ️ Aucun nouveau patch appliqué (Code déjà à jour ?).")
