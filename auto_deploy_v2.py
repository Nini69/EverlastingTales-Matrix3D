import subprocess
import base64
import time
import os

# Configuration
SSH_KEY = r"C:\Users\Administrateur\.ssh\id_ed25519"
SSH_USER_HOST = "9pq7fh47rmyapy-64410d74@ssh.runpod.io"
REMOTE_DIR = "/workspace/matrix3d"
LOCAL_FILE = r"C:\Users\Administrateur\Documents\EverlastingTales\Matrix\final_patch.py"

def run_ssh(command, use_tty=False):
    # -T disables pseudo-terminal allocation (good for piping/scripts)
    # -t forces it (good for top/interactive)
    flags = "-t" if use_tty else "-T"
    full_cmd = f'ssh {flags} -i "{SSH_KEY}" -o StrictHostKeyChecking=no {SSH_USER_HOST} "{command}"'
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return result

def main():
    print("--- STARTING AUTOMATED DEPLOYMENT V2 ---")
    
    # 1. Read and Encode
    print(f"Reading {LOCAL_FILE}...")
    with open(LOCAL_FILE, 'rb') as f:
        content = f.read()
    b64_content = base64.b64encode(content).decode('utf-8')
    
    # 2. Split
    CHUNK_SIZE = 1000
    chunks = [b64_content[i:i+CHUNK_SIZE] for i in range(0, len(b64_content), CHUNK_SIZE)]
    
    # 3. Clean
    print("Cleaning remote...")
    run_ssh(f"rm -f {REMOTE_DIR}/blob.b64 {REMOTE_DIR}/final_patch.py")

    # 4. Send Chunks
    print("Sending chunks...")
    for i, chunk in enumerate(chunks):
        print(f"Sending chunk {i+1}/{len(chunks)}...")
        run_ssh(f"echo -n '{chunk}' >> {REMOTE_DIR}/blob.b64")

    # 5. Decode
    print("Decoding...")
    run_ssh(f"base64 -d {REMOTE_DIR}/blob.b64 > {REMOTE_DIR}/final_patch.py")
    
    # 6. Execute Patch (Capture output to file then read it)
    print("Executing Patch...")
    run_ssh(f"cd {REMOTE_DIR} && python final_patch.py > patch_log.txt 2>&1")
    
    # Read Log
    res = run_ssh(f"cat {REMOTE_DIR}/patch_log.txt")
    print("PATCH OUTPUT:\n", res.stdout)
    
    # 7. Run Pipeline (Synchronous, capture to log)
    print("Launching Pipeline...")
    pipeline_cmd = (
        f"cd {REMOTE_DIR} && "
        "python code/MoGe/scripts/infer_panorama.py --input output/throne_demo/pano_img.jpg --output output/throne_demo --maps && "
        "python patch_hf.py && "
        "MASTER_ADDR=127.0.0.1 MASTER_PORT=5678 RANK=0 WORLD_SIZE=1 python code/panoramic_image_to_video.py --inout_dir output/throne_demo && "
        "python code/panoramic_video_to_3DScene.py --inout_dir output/throne_demo"
    )
    
    # Run and log to finish_log.txt
    run_ssh(f"{pipeline_cmd} > finish_log.txt 2>&1")
    
    # Read Finish Log
    final_res = run_ssh(f"tail -n 20 {REMOTE_DIR}/finish_log.txt")
    print("PIPELINE TAIL:\n", final_res.stdout)

if __name__ == "__main__":
    main()
