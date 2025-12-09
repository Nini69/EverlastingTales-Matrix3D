import os

target_file = 'code/panoramic_image_to_video.py'

print(f"Patching {target_file} to use Hugging Face...")
with open(target_file, 'r') as f:
    content = f.read()

# Remplacement des imports et fonctions
if 'modelscope' in content:
    # Remplacer l'import specifique
    new_content = content.replace('from modelscope.hub.snapshot_download import snapshot_download', 'from huggingface_hub import snapshot_download')
    # Remplacer l'import general si present
    new_content = new_content.replace('from modelscope import snapshot_download', 'from huggingface_hub import snapshot_download')
    # Remplacer les appels explicites modelscope.snapshot_download
    new_content = new_content.replace('modelscope.snapshot_download', 'snapshot_download')
    
    with open(target_file, 'w') as f:
        f.write(new_content)
    print("SUCCESS: Bascule sur Hugging Face effectuee !")
else:
    print("WARNING: 'modelscope' introuvable. Fichier deja patche ?")
