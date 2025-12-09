import subprocess
import time

# Configuration
SSH_KEY = r"C:\Users\Administrateur\.ssh\id_ed25519"
SSH_USER_HOST = "0bcl5xhuw2l141-64410d8a@ssh.runpod.io"
REMOTE_DIR = "/workspace/matrix3d"

def run_ssh(cmd):
    # FORCE -t for PTY allocation
    full_cmd = f'ssh -t -i "{SSH_KEY}" -o StrictHostKeyChecking=no {SSH_USER_HOST} "{cmd}"'
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=120)
        print("STDOUT:", result.stdout)
    except subprocess.TimeoutExpired:
        print("TIMEOUT")

print("--- CHECKING REMOTE STATUS V2 ---")
# List files with sizes
run_ssh(f"ls -la {REMOTE_DIR}")
run_ssh(f"tail -n 20 {REMOTE_DIR}/clean_pipeline_log.txt")
