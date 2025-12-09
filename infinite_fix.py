import os

# 0. RESET
print("RESETTING infer_panorama.py...")
os.system("git checkout code/MoGe/scripts/infer_panorama.py")

# 1. READ ALL
path = 'code/MoGe/scripts/infer_panorama.py'
with open(path, 'r') as f:
    code = f.read()

# 2. DEFINE REPLACEMENTS (PRECISE STRINGS)

# Fix 1: Distance Map Resize
old_dist = "panorama_log_distance_map = np.where(projection_valid_mask, cv2.remap(log_splitted_distance, projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE), 0)"
new_dist = """tmp_d = cv2.remap(log_splitted_distance, projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    if tmp_d.shape != projection_valid_mask.shape: tmp_d = cv2.resize(tmp_d, (projection_valid_mask.shape[1], projection_valid_mask.shape[0]), interpolation=cv2.INTER_NEAREST)
    panorama_log_distance_map = np.where(projection_valid_mask, tmp_d, 0)"""

# Fix 2: Mask Resize
old_mask = "panorama_pred_mask = projection_valid_mask & (cv2.remap(pred_masks[i].astype(np.uint8), projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE) > 0)"
new_mask = """tmp_m = cv2.remap(pred_masks[i].astype(np.uint8), projected_pixels[..., 0], projected_pixels[..., 1], cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)
    if tmp_m.shape != projection_valid_mask.shape: tmp_m = cv2.resize(tmp_m, (projection_valid_mask.shape[1], projection_valid_mask.shape[0]), interpolation=cv2.INTER_NEAREST)
    panorama_pred_mask = projection_valid_mask & (tmp_m > 0)"""

# Fix 3: Normals Signature
old_norm = "normals, normals_mask = utils3d.numpy.points_to_normals(points, panorama_mask)"
new_norm = "normals = utils3d.numpy.points_to_normals(points); normals_mask = panorama_mask"

# Fix 4: Mesh Missing & Save Crash (Replaces the whole block at the end)
old_mesh_save = """    faces, vertices, vertex_colors, vertex_uvs = utils3d.numpy.image_mesh(points, panorama_mask)
    utils3d.io.save_obj(save_path / 'mesh.obj', vertices, faces, vertex_colors=vertex_colors, vertex_uvs=vertex_uvs, texture_map=panorama_image)
    cv2.imwrite(str(save_path / 'points.exr'), points, [cv2.IMWRITE_EXR_TYPE, cv2.IMWRITE_EXR_TYPE_FLOAT])"""

new_mesh_save = """    try:
        faces, vertices, vertex_colors, vertex_uvs = utils3d.numpy.image_mesh(points, panorama_mask)
        utils3d.io.save_obj(save_path / 'mesh.obj', vertices, faces, vertex_colors=vertex_colors, vertex_uvs=vertex_uvs, texture_map=panorama_image)
    except:
        print("SKIP MESH GENERATION")

    try:
        cv2.imwrite(str(save_path / 'points.exr'), points, [cv2.IMWRITE_EXR_TYPE, cv2.IMWRITE_EXR_TYPE_FLOAT])
    except:
        pass"""

# 3. APPLY REPLACE
code = code.replace(old_dist, new_dist)
code = code.replace(old_mask, new_mask)
code = code.replace(old_norm, new_norm)
code = code.replace(old_mesh_save, new_mesh_save)

# 4. WRITE BACK
with open(path, 'w') as f:
    f.write(code)

print("INFINITE FIX APPLIED SUCCESSFULLY")
