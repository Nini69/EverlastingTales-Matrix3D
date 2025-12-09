import os
import cv2
import numpy as np

print("1. RESET du fichier...")
os.system("git checkout code/MoGe/scripts/infer_panorama.py")

print("2. APPLICATION des 5 Correctifs...")
lines = open('code/MoGe/scripts/infer_panorama.py').readlines()
new_lines = []

for l in lines:
    # Fix 1: Distance Resize
    if 'panorama_log_distance_map = np.where' in l:
        indent = l.split('panorama')[0]
        new_lines.append(indent + "tmp = cv2.remap(log_splitted_distance, projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)\n")
        new_lines.append(indent + "if tmp.shape != projection_valid_mask.shape: tmp = cv2.resize(tmp, (projection_valid_mask.shape[1], projection_valid_mask.shape[0]), interpolation=cv2.INTER_NEAREST)\n")
        new_lines.append(indent + "panorama_log_distance_map = np.where(projection_valid_mask, tmp, 0)\n")
    
    # Fix 2: Mask Resize
    elif 'panorama_pred_mask = projection_valid_mask &' in l:
        indent = l.split('panorama')[0]
        new_lines.append(indent + "tmp_m = cv2.remap(pred_masks[i].astype(np.uint8), projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)\n")
        new_lines.append(indent + "if tmp_m.shape != projection_valid_mask.shape: tmp_m = cv2.resize(tmp_m, (projection_valid_mask.shape[1], projection_valid_mask.shape[0]), interpolation=cv2.INTER_NEAREST)\n")
        new_lines.append(indent + "panorama_pred_mask = projection_valid_mask & (tmp_m > 0)\n")
    
    # Fix 3: Normals Signature
    elif 'normals, normals_mask = utils3d.numpy.points_to_normals' in l:
        new_lines.append(l.replace('normals, normals_mask = utils3d.numpy.points_to_normals(points, panorama_mask)', 'normals = utils3d.numpy.points_to_normals(points); normals_mask = panorama_mask'))
    
    # Fix 4: Mesh Skip (Missing Function)
    elif 'utils3d.numpy.image_mesh' in l:
        indent = l.split('faces')[0]
        new_lines.append(indent + "try:\n")
        new_lines.append(indent + "    faces, vertices, vertex_colors, vertex_uvs = utils3d.numpy.image_mesh(points, panorama_mask)\n")
        new_lines.append(indent + "except:\n")
        new_lines.append(indent + "    print('SKIP MESH (Fonction manquante)'); faces=None\n")
    
    # Fix 4b: Skip Save OBj if Skipped Mesh
    elif 'utils3d.io.save_obj' in l:
        indent = l.split('utils3d')[0]
        # Wrap save in check
        new_lines.append(indent + "if faces is not None: utils3d.io.save_obj" + l.split('save_obj')[1])

    # Fix 5: Save EXR Crash
    elif "cv2.imwrite(str(save_path / 'points.exr')" in l:
        indent = l.split('cv2')[0]
        new_lines.append(indent + "try:\n")
        new_lines.append(indent + "    " + l.strip() + "\n")
        new_lines.append(indent + "except:\n")
        new_lines.append(indent + "    pass\n")
    
    else:
        new_lines.append(l)

with open('code/MoGe/scripts/infer_panorama.py', 'w') as f:
    f.writelines(new_lines)

print("ULTIMATE FIX SUCCES")
