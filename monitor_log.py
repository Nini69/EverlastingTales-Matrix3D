import subprocess
import base64

# Configuration
SSH_KEY = r"C:\Users\Administrateur\.ssh\id_ed25519"
SSH_USER_HOST = "9pq7fh47rmyapy-64410d74@ssh.runpod.io"
REMOTE_DIR = "/workspace/matrix3d"

def get_remote_file_content(filename):
    print(f"Fetching {filename}...")
    # Use -T to avoid PTY. Ensure 'base64' command exists (standard on linux)
    cmd = f"base64 -w 0 {REMOTE_DIR}/{filename}"
    full_cmd = f'ssh -T -i "{SSH_KEY}" -o StrictHostKeyChecking=no {SSH_USER_HOST} "{cmd}"'
    
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error fetching {filename}: {result.stderr}")
        return None
        
    try:
        # PTY errors might still be in stdout/stderr mix depending on client, 
        # but -T should keep stdout clean for the piped command.
        # However, sometimes banners appear. base64 shouldn't have spaces usually.
        # We strip whitespace.
        clean_b64 = result.stdout.strip()
        # Decode
        decoded_bytes = base64.b64decode(clean_b64)
        return decoded_bytes.decode('utf-8', errors='replace')
    except Exception as e:
        print(f"Failed to decode {filename}: {e}")
        print(f"Raw output start: {result.stdout[:100]}...")
        return None

def main():
    print("--- MONITORING LOGS ---")
    
    # Check Patch Log
    patch_log = get_remote_file_content("patch_log.txt")
    if patch_log:
        print("\n=== PATCH LOG ===")
        print(patch_log)
    else:
        print("\n!!! Could not read patch_log.txt")

    # Check Pipeline Log
    finish_log = get_remote_file_content("finish_log.txt")
    if finish_log:
        print("\n=== FINISH LOG (LAST 20 LINES) ===")
        lines = finish_log.splitlines()
        for line in lines[-20:]:
            print(line)
            
        if "Traceback" in finish_log:
            print("\nALERT: Exception detected in logs!")
    else:
        print("\n!!! Could not read finish_log.txt")

if __name__ == "__main__":
    main()
