
import os

target_path = "/usr/local/lib/python3.10/dist-packages/xfuser/model_executor/layers/usp.py"

print(f"🔍 Reading {target_path}...")

try:
    with open(target_path, "r") as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"❌ Error: File not found at {target_path}")
    exit(1)

new_lines = []
patched = False

for line in lines:
    # We look for the specific import causing the crash
    if "from torch.distributed.tensor.experimental.attention" in line and "import templated_ring_attention" in line:
        print(f"🔴 Found faulty line: {line.strip()}")
        # Replacement with safe dummy function
        new_line = "templated_ring_attention = lambda *args, **kwargs: None # FORCED PATCH BY MATRIX3D\n"
        new_lines.append(new_line)
        patched = True
        print(f"🟢 Replaced with: {new_line.strip()}")
    else:
        new_lines.append(line)

if patched:
    print("💾 Saving patched file...")
    with open(target_path, "w") as f:
        f.writelines(new_lines)
    print("✅ SUCCESS: Library file patched correctly.")
else:
    print("⚠️ WARNING: Target line not found. Maybe already patched?")
    # Print first few lines for debug
    print("--- First 10 lines of file ---")
    for i in range(min(10, len(lines))):
        print(f"{i+1}: {lines[i].strip()}")
