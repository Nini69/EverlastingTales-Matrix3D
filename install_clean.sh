#!/bin/bash
echo "--- CLEANING WORKSPACE ---"
cd /workspace/matrix3d
# Reset code to official state
git checkout .
git clean -fd

# Remove potential garbage files
rm -f final_patch.py force_fix.py patch_log.txt finish_log.txt blob.b64

echo "--- INSTALLING DEPENDENCIES ---"
# Install critical missing packages identified in previous runs
pip install rembg trimesh "imageio[ffmpeg]" scikit-image opencv-python-headless onnxruntime utils3d

echo "--- READY FOR OFFICIAL LAUNCH ---"
echo "You can now run the pipeline."
