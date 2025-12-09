import subprocess
import base64
import re

# Configuration
SSH_KEY = r"C:\Users\Administrateur\.ssh\id_ed25519"
SSH_USER_HOST = "0bcl5xhuw2l141-64410d8a@ssh.runpod.io"
REMOTE_DIR = "/workspace/matrix3d"

def get_remote_file_content(filename):
    print(f"Fetching {filename}...")
    # Use -t to force PTY to avoid "Client doesn't support PTY" error.
    # We wrap the output in delimiters to find it amidst the banner/motd.
    cmd = f"echo '<<<START>>>'; base64 -w 0 {REMOTE_DIR}/{filename}; echo '<<<END>>>'"
    full_cmd = f'ssh -t -i "{SSH_KEY}" -o StrictHostKeyChecking=no {SSH_USER_HOST} "{cmd}"'
    
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    
    # helper regex to find content between <<<START>>> and <<<END>>>
    # output might contain \r\n so we use DOTALL
    match = re.search(r"<<<START>>>(.*?)<<<END>>>", result.stdout, re.DOTALL)
    
    if not match:
        print(f"Error fetching {filename}: Could not find delimiters in output.")
        # print(f"Raw output (truncated): {result.stdout[:200]}...")
        return None
        
    try:
        clean_b64 = match.group(1).strip().replace('\r', '').replace('\n', '')
        decoded_bytes = base64.b64decode(clean_b64)
        return decoded_bytes.decode('utf-8', errors='replace')
    except Exception as e:
        print(f"Failed to decode {filename}: {e}")
        return None

def main():
    print("--- MONITORING LOGS V2 ---")
    
    # Check Install Log
    install_log = get_remote_file_content("install_log.txt")
    if install_log:
        print("\n=== INSTALL LOG (LAST 20 LINES) ===")
        print(install_log[-1000:] if len(install_log) > 1000 else install_log)
    else:
        print("\n!!! Could not read install_log.txt")

    # Check Clean Pipeline Log
    pipeline_log = get_remote_file_content("clean_pipeline_log.txt")
    if pipeline_log:
        print("\n=== CLEAN PIPELINE LOG (LAST 20 LINES) ===")
        lines = pipeline_log.splitlines()
        for line in lines[-20:]:
            print(line)
    else:
        print("\n!!! Could not read clean_pipeline_log.txt")

if __name__ == "__main__":
    main()
