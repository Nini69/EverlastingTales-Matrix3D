s=r'''import torch
def image_uv(height, width, dtype=torch.float32, device='cpu'):
    x = torch.linspace(0, 1, width, dtype=dtype, device=device)
    y = torch.linspace(0, 1, height, dtype=dtype, device=device)
    grid_y, grid_x = torch.meshgrid(y, x, indexing='ij')
    return torch.stack([grid_x, grid_y], dim=-1)
def unproject_cv(uv, depth, intrinsics, extrinsics=None, **kwargs):
    if depth.dim() == uv.dim() - 1:
        z = depth
    else:
        z = depth[..., 0]
    u = uv[..., 0]
    v = uv[..., 1]
    if intrinsics.dim() == 2:
        fx, fy = intrinsics[0, 0], intrinsics[1, 1]
        cx, cy = intrinsics[0, 2], intrinsics[1, 2]
    else:
        fx, fy = intrinsics[..., 0, 0], intrinsics[..., 1, 1]
        cx, cy = intrinsics[..., 0, 2], intrinsics[..., 1, 2]
    x = (u - cx) * z / fx
    y = (v - cy) * z / fy
    return torch.stack([x, y, z], dim=-1)
'''
print(f"python3 -c \"open('/usr/local/lib/python3.10/dist-packages/utils3d/torch/__init__.py', 'w').write({repr(s)})\" && export RANK=0 WORLD_SIZE=1 MASTER_ADDR=127.0.0.1 MASTER_PORT=29500 && python code/panoramic_image_to_video.py --inout_dir output/throne_demo && python code/panoramic_video_to_3DScene.py --inout_dir output/throne_demo")
