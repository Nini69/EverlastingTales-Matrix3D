import subprocess
import base64
import time
import os

# Configuration
SSH_KEY = r"C:\Users\Administrateur\.ssh\id_ed25519"
SSH_USER_HOST = "9pq7fh47rmyapy-64410d74@ssh.runpod.io"
REMOTE_DIR = "/workspace/matrix3d"
LOCAL_FILE = r"C:\Users\Administrateur\Documents\EverlastingTales\Matrix\final_patch.py"

def run_ssh(command):
    full_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no {SSH_USER_HOST} "{command}"'
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR executing: {command}")
        print(f"Stderr: {result.stderr}")
    return result

def main():
    print("--- STARTING AUTOMATED DEPLOYMENT ---")
    
    # 1. Read and Encode File
    print(f"Reading {LOCAL_FILE}...")
    with open(LOCAL_FILE, 'rb') as f:
        content = f.read()
    b64_content = base64.b64encode(content).decode('utf-8')
    
    # 2. Split into chunks
    CHUNK_SIZE = 1000
    chunks = [b64_content[i:i+CHUNK_SIZE] for i in range(0, len(b64_content), CHUNK_SIZE)]
    print(f"Split into {len(chunks)} chunks.")

    # 3. Clean Remote
    print("Cleaning remote...")
    run_ssh(f"rm -f {REMOTE_DIR}/blob.b64 {REMOTE_DIR}/final_patch.py")

    # 4. Send Chunks
    print("Sending chunks...")
    for i, chunk in enumerate(chunks):
        print(f"Sending chunk {i+1}/{len(chunks)}...")
        # Use simple echo without -n if possible, but base64 needs contiguous.
        # echoing with -n is standard.
        cmd = f"echo -n '{chunk}' >> {REMOTE_DIR}/blob.b64"
        run_ssh(cmd)
        time.sleep(0.5) # Breath to avoid overwhelming connection

    # 5. Decode
    print("Decoding on remote...")
    run_ssh(f"base64 -d {REMOTE_DIR}/blob.b64 > {REMOTE_DIR}/final_patch.py")
    
    # 6. Execute Patch
    print("Executing Patch...")
    res = run_ssh(f"cd {REMOTE_DIR} && python final_patch.py")
    print("Patch Output:", res.stdout)

    # 7. Run Pipeline (Synchronous for now to verify start)
    print("Launching Pipeline...")
    pipeline_cmd = (
        f"cd {REMOTE_DIR} && "
        "python code/MoGe/scripts/infer_panorama.py --input output/throne_demo/pano_img.jpg --output output/throne_demo --maps && "
        "python patch_hf.py && "
        "MASTER_ADDR=127.0.0.1 MASTER_PORT=5678 RANK=0 WORLD_SIZE=1 python code/panoramic_image_to_video.py --inout_dir output/throne_demo && "
        "python code/panoramic_video_to_3DScene.py --inout_dir output/throne_demo"
    )
    
    # We run this in a way that we can see output.
    # If we want to detach, we'd use nohup. But user wants to see it works.
    # We will run it and print the first few lines of output then maybe detach or just let it run.
    # Actually, let's just run it. If it takes long, this script will wait.
    # But for the user, I will just start it.
    
    # Running via ssh directly
    subprocess.run(f'ssh -t -i "{SSH_KEY}" -o StrictHostKeyChecking=no {SSH_USER_HOST} "{pipeline_cmd}"', shell=True)

if __name__ == "__main__":
    main()
