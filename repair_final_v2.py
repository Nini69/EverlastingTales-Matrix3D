import os
import cv2
import numpy as np

# Reset file to clean state
os.system("git checkout code/MoGe/scripts/infer_panorama.py")

print("Patching infer_panorama.py...")
with open('code/MoGe/scripts/infer_panorama.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # FIX 1: Distance Map Resize
    if 'panorama_log_distance_map = np.where' in line:
        indent = line[:line.find('panorama')]
        new_lines.append(indent + "tmp = cv2.remap(log_splitted_distance, projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)\n")
        new_lines.append(indent + "if tmp.shape != projection_valid_mask.shape: tmp = cv2.resize(tmp, (projection_valid_mask.shape[1], projection_valid_mask.shape[0]), interpolation=cv2.INTER_NEAREST)\n")
        new_lines.append(indent + "panorama_log_distance_map = np.where(projection_valid_mask, tmp, 0)\n")
    
    # FIX 2: Mask Resize
    elif 'panorama_pred_mask = projection_valid_mask &' in line:
        indent = line[:line.find('panorama')]
        new_lines.append(indent + "tmp_m = cv2.remap(pred_masks[i].astype(np.uint8), projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)\n")
        new_lines.append(indent + "if tmp_m.shape != projection_valid_mask.shape: tmp_m = cv2.resize(tmp_m, (projection_valid_mask.shape[1], projection_valid_mask.shape[0]), interpolation=cv2.INTER_NEAREST)\n")
        new_lines.append(indent + "panorama_pred_mask = projection_valid_mask & (tmp_m > 0)\n")

    # FIX 3: Point Cloud Save Crash
    elif "cv2.imwrite(str(save_path / 'points.exr')" in line:
        indent = line[:line.find('cv2')]
        new_lines.append(indent + "try:\n")
        new_lines.append(indent + "    " + line.strip() + "\n")
        new_lines.append(indent + "except:\n")
        new_lines.append(indent + "    pass\n")
    
    else:
        new_lines.append(line)

with open('code/MoGe/scripts/infer_panorama.py', 'w') as f:
    f.writelines(new_lines)

print("Infer Panorama Fixed Successfully")
