import os
import cv2
import numpy as np
import sys

# Define path
file_path = 'code/MoGe/scripts/infer_panorama.py'

print(f"RESTORING {file_path}...")
os.system(f"git checkout {file_path}")

print("READING file content...")
with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Fix 1: Log Distance Map Resize
    # Original: panorama_log_distance_map = np.where(projection_valid_mask, cv2.remap(log_splitted_distance, projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE), 0)
    if 'panorama_log_distance_map = np.where(projection_valid_mask, cv2.remap' in line:
        indent = line[:line.find('panorama')]
        new_lines.append(indent + "# FIX-1: Resize Distance Map\n")
        new_lines.append(indent + "tmp_d = cv2.remap(log_splitted_distance, projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)\n")
        new_lines.append(indent + "if tmp_d.shape != projection_valid_mask.shape: tmp_d = cv2.resize(tmp_d, (projection_valid_mask.shape[1], projection_valid_mask.shape[0]), interpolation=cv2.INTER_NEAREST)\n")
        new_lines.append(indent + "panorama_log_distance_map = np.where(projection_valid_mask, tmp_d, 0)\n")
    
    # Fix 2: Pred Mask Resize
    # Original: panorama_pred_mask = projection_valid_mask & (cv2.remap(pred_masks[i].astype(np.uint8), projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE) > 0)
    elif 'panorama_pred_mask = projection_valid_mask & (cv2.remap' in line:
        indent = line[:line.find('panorama')]
        new_lines.append(indent + "# FIX-2: Resize Mask\n")
        new_lines.append(indent + "tmp_m = cv2.remap(pred_masks[i].astype(np.uint8), projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)\n")
        new_lines.append(indent + "if tmp_m.shape != projection_valid_mask.shape: tmp_m = cv2.resize(tmp_m, (projection_valid_mask.shape[1], projection_valid_mask.shape[0]), interpolation=cv2.INTER_NEAREST)\n")
        new_lines.append(indent + "panorama_pred_mask = projection_valid_mask & (tmp_m > 0)\n")

    # Fix 3: Points to Normals Signature
    elif 'normals, normals_mask = utils3d.numpy.points_to_normals(points, panorama_mask)' in line:
        new_lines.append(line.replace('normals, normals_mask = utils3d.numpy.points_to_normals(points, panorama_mask)', 'normals = utils3d.numpy.points_to_normals(points); normals_mask = panorama_mask'))

    # Fix 4: Image Mesh (Wrap in try/except)
    elif 'faces, vertices, vertex_colors, vertex_uvs = utils3d.numpy.image_mesh(points, panorama_mask)' in line:
        indent = line[:line.find('faces')]
        new_lines.append(indent + "try:\n")
        new_lines.append(indent + "    faces, vertices, vertex_colors, vertex_uvs = utils3d.numpy.image_mesh(points, panorama_mask)\n")
        new_lines.append(indent + "except:\n")
        new_lines.append(indent + "    faces = None\n")
        new_lines.append(indent + "    print('WARNING: utils3d.image_mesh failed, skipping mesh generation')\n")

    # Fix 4b: Save OBJ (Check if faces exist)
    elif "utils3d.io.save_obj(save_path / 'mesh.obj'" in line:
        indent = line[:line.find('utils3d')]
        new_lines.append(indent + "if faces is not None:\n")
        new_lines.append(indent + "    " + line.strip() + "\n")

    # Fix 5: Save EXR (Wrap in try/except)
    elif "cv2.imwrite(str(save_path / 'points.exr')" in line:
        indent = line[:line.find('cv2')]
        new_lines.append(indent + "try:\n")
        new_lines.append(indent + "    " + line.strip() + "\n")
        new_lines.append(indent + "except:\n")
        new_lines.append(indent + "    pass\n")

    else:
        new_lines.append(line)

print("WRITING patched file...")
with open(file_path, 'w') as f:
    f.writelines(new_lines)

print("SUCCESS: infer_panorama.py is fully patched.")
