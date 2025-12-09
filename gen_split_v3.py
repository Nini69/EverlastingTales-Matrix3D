
part2 = r'''def intrinsics_from_focal_center(fx,fy,cx,cy,device='cpu',dtype=torch.float32):
    fx = torch.as_tensor(fx, device=device, dtype=dtype)
    fy = torch.as_tensor(fy, device=device, dtype=dtype)
    cx = torch.as_tensor(cx, device=device, dtype=dtype)
    cy = torch.as_tensor(cy, device=device, dtype=dtype)
    try:
        sh = torch.broadcast_shapes(fx.shape, fy.shape, cx.shape, cy.shape)
        K = torch.eye(3, device=device, dtype=dtype).expand(sh + (3, 3)).clone()
    except:
        K = torch.eye(3, device=device, dtype=dtype).clone()
    K[..., 0, 0] = fx
    K[..., 1, 1] = fy
    K[..., 0, 2] = cx
    K[..., 1, 2] = cy
    return K
def unproject_cv(uv, depth, intrinsics, extrinsics=None, **kwargs):
    if depth.dim() == uv.dim() - 1: z = depth
    else: z = depth[..., 0]
    u, v = uv[..., 0], uv[..., 1]
    if intrinsics.dim() == 2:
        fx, fy = intrinsics[0, 0], intrinsics[1, 1]
        cx, cy = intrinsics[0, 2], intrinsics[1, 2]
    else:
        fx = intrinsics[..., 0, 0]
        fy = intrinsics[..., 1, 1]
        cx = intrinsics[..., 0, 2]
        cy = intrinsics[..., 1, 2]
        # Fix for Flattened Batch (13056 vs 4)
        if z.dim() == 1 and fx.numel() > 1 and z.numel() > fx.numel():
             B = fx.numel()
             if z.numel() % B == 0:
                 N = z.numel() // B
                 if u.numel() == N:
                     fx = fx.reshape(-1).repeat_interleave(N)
                     fy = fy.reshape(-1).repeat_interleave(N)
                     cx = cx.reshape(-1).repeat_interleave(N)
                     cy = cy.reshape(-1).repeat_interleave(N)
                     u = u.reshape(-1).repeat(B)
                     v = v.reshape(-1).repeat(B)
        while fx.dim() < z.dim():
            fx = fx.unsqueeze(-1)
            fy = fy.unsqueeze(-1)
            cx = cx.unsqueeze(-1)
            cy = cy.unsqueeze(-1)
    x = (u - cx) * z / fx
    y = (v - cy) * z / fy
    return torch.stack([x, y, z], dim=-1)
'''

print(f"python3 -c \"open('/usr/local/lib/python3.10/dist-packages/utils3d/torch/__init__.py', 'a').write({repr(part2)})\"")
