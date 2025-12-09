#!/bin/bash
# fix_runpod.sh

echo "1. Reinstalling PyTorch & Xformers..."
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu121
pip install xformers==0.0.24 --index-url https://download.pytorch.org/whl/cu121

echo "2. Installing Dependencies..."
pip install fvcore iopath omegaconf trimesh

echo "3. Creating PyTorch3D Stub..."
# Find site-packages
SP_PATH=$(python -c "import site; print(site.getsitepackages()[0])")
mkdir -p "$SP_PATH/pytorch3d/transforms"
touch "$SP_PATH/pytorch3d/__init__.py"

# Write the stub code
cat <<EOF > "$SP_PATH/pytorch3d/transforms/__init__.py"
import torch

def matrix_to_quaternion(matrix: torch.Tensor) -> torch.Tensor:
    if matrix.size(-1) != 3 or matrix.size(-2) != 3:
        raise ValueError(f"Invalid rotation matrix shape {matrix.shape}.")
    m00 = matrix[..., 0, 0]
    m11 = matrix[..., 1, 1]
    m22 = matrix[..., 2, 2]
    trace = m00 + m11 + m22
    def trace_positive_cond():
        s = torch.sqrt(trace + 1.0) * 2
        w = 0.25 * s
        x = (matrix[..., 2, 1] - matrix[..., 1, 2]) / s
        y = (matrix[..., 0, 2] - matrix[..., 2, 0]) / s
        z = (matrix[..., 1, 0] - matrix[..., 0, 1]) / s
        return torch.stack((w, x, y, z), dim=-1)
    def cond_1():
        s = torch.sqrt(1.0 + m00 - m11 - m22) * 2
        w = (matrix[..., 2, 1] - matrix[..., 1, 2]) / s
        x = 0.25 * s
        y = (matrix[..., 0, 1] + matrix[..., 1, 0]) / s
        z = (matrix[..., 0, 2] + matrix[..., 2, 0]) / s
        return torch.stack((w, x, y, z), dim=-1)
    def cond_2():
        s = torch.sqrt(1.0 + m11 - m00 - m22) * 2
        w = (matrix[..., 0, 2] - matrix[..., 2, 0]) / s
        x = (matrix[..., 0, 1] + matrix[..., 1, 0]) / s
        y = 0.25 * s
        z = (matrix[..., 1, 2] + matrix[..., 2, 1]) / s
        return torch.stack((w, x, y, z), dim=-1)
    def cond_3():
        s = torch.sqrt(1.0 + m22 - m00 - m11) * 2
        w = (matrix[..., 1, 0] - matrix[..., 0, 1]) / s
        x = (matrix[..., 0, 2] + matrix[..., 2, 0]) / s
        y = (matrix[..., 1, 2] + matrix[..., 2, 1]) / s
        z = 0.25 * s
        return torch.stack((w, x, y, z), dim=-1)
    where_trace_positive = trace > 0
    res = torch.where(where_trace_positive.unsqueeze(-1), trace_positive_cond(), 
                      torch.where((m00 > m11).unsqueeze(-1) & (m00 > m22).unsqueeze(-1), cond_1(),
                                  torch.where((m11 > m22).unsqueeze(-1), cond_2(), cond_3())))
    return res

def quaternion_to_matrix(quaternions: torch.Tensor) -> torch.Tensor:
    r, i, j, k = torch.unbind(quaternions, -1)
    two_s = 2.0 / (quaternions * quaternions).sum(-1)
    o = torch.stack(
        (
            1 - two_s * (j * j + k * k),
            two_s * (i * j - k * r),
            two_s * (i * k + j * r),
            two_s * (i * j + k * r),
            1 - two_s * (i * i + k * k),
            two_s * (j * k - i * r),
            two_s * (i * k - j * r),
            two_s * (j * k + i * r),
            1 - two_s * (i * i + j * j),
        ),
        -1,
    )
    return o.reshape(quaternions.shape[:-1] + (3, 3))
EOF

echo "Done! You can now run the scene script."
