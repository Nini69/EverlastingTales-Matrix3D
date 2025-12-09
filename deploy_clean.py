import subprocess
import base64
import time
import os

# Configuration
SSH_KEY = r"C:\Users\Administrateur\.ssh\id_ed25519"
SSH_USER_HOST = "0bcl5xhuw2l141-64410d8a@ssh.runpod.io"
REMOTE_DIR = "/workspace/matrix3d"
LOCAL_FILE = r"C:\Users\Administrateur\Documents\EverlastingTales\Matrix\install_clean.sh"

def run_ssh(command, use_tty=False):
    # -T disables pseudo-terminal allocation (good for piping/scripts)
    # -t forces it (good for top/interactive)
    flags = "-t" if use_tty else "-T"
    full_cmd = f'ssh {flags} -i "{SSH_KEY}" -o StrictHostKeyChecking=no {SSH_USER_HOST} "{command}"'
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return result

def main():
    print("--- DECOUPAGE ET ENVOI DE 'install_clean.sh' ---")
    
    # 1. Read and Encode
    print(f"Reading {LOCAL_FILE}...")
    with open(LOCAL_FILE, 'rb') as f:
        content = f.read()
    b64_content = base64.b64encode(content).decode('utf-8')
    
    # 2. Split
    CHUNK_SIZE = 1000
    chunks = [b64_content[i:i+CHUNK_SIZE] for i in range(0, len(b64_content), CHUNK_SIZE)]
    
    # 3. Clean Remote Temp
    print("Cleaning remote temp files...")
    run_ssh(f"rm -f {REMOTE_DIR}/blob_clean.b64 {REMOTE_DIR}/install_clean.sh")

    # 4. Send Chunks
    print("Sending chunks...")
    for i, chunk in enumerate(chunks):
        print(f"Sending chunk {i+1}/{len(chunks)}...")
        run_ssh(f"echo -n '{chunk}' >> {REMOTE_DIR}/blob_clean.b64")

    # 5. Decode
    print("Decoding...")
    run_ssh(f"base64 -d {REMOTE_DIR}/blob_clean.b64 > {REMOTE_DIR}/install_clean.sh")
    run_ssh(f"chmod +x {REMOTE_DIR}/install_clean.sh")
    
    # 6. Execute Install Script
    print("EXECUTING CLEAN INSTALL (Git Reset + Dependencies)...")
    # Using -t here to see output if possible, or redirect to log
    run_ssh(f"cd {REMOTE_DIR} && ./install_clean.sh > install_log.txt 2>&1")
    
    # Check Install Log
    print("Checking install logs...")
    res = run_ssh(f"cat {REMOTE_DIR}/install_log.txt")
    print("INSTALL LOG OUTPUT:\n", res.stdout)
    
    # 7. Run OFFICIAL Pipeline (No patching)
    print("LAUNCHING OFFICIAL PIPELINE (ModelScope)...")
    pipeline_cmd = (
        f"cd {REMOTE_DIR} && "
        "python code/MoGe/scripts/infer_panorama.py --input output/throne_demo/pano_img.jpg --output output/throne_demo --maps && "
        "MASTER_ADDR=127.0.0.1 MASTER_PORT=5678 RANK=0 WORLD_SIZE=1 python code/panoramic_image_to_video.py --inout_dir output/throne_demo && "
        "python code/panoramic_video_to_3DScene.py --inout_dir output/throne_demo"
    )
    
    # Run and log to clean_pipeline_log.txt
    run_ssh(f"{pipeline_cmd} > clean_pipeline_log.txt 2>&1")
    
    print("Pipeline launched in background (redirected to log).")
    print("To monitor: ssh ... 'tail -f /workspace/matrix3d/clean_pipeline_log.txt'")

if __name__ == "__main__":
    main()
