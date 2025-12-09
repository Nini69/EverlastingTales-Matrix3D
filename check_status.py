import subprocess
import time

# Configuration
SSH_KEY = r"C:\Users\Administrateur\.ssh\id_ed25519"
SSH_USER_HOST = "0bcl5xhuw2l141-64410d8a@ssh.runpod.io"
REMOTE_DIR = "/workspace/matrix3d"

def run_ssh(cmd):
    full_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no {SSH_USER_HOST} "{cmd}"'
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=10)
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    except subprocess.TimeoutExpired:
        print("TIMEOUT")

print("--- CHECKING REMOTE STATUS ---")
# 1. Check if python is running
run_ssh("ps aux | grep python")

# 2. List files to see sizes (logs should grow)
run_ssh(f"ls -la {REMOTE_DIR}")

# 3. Read end of log (try simple cat)
run_ssh(f"tail -n 10 {REMOTE_DIR}/clean_pipeline_log.txt")
