import os

# Correction TYPO: log_splited_distance -> log_splitted_distance

print("Correction de la typo dans infer_panorama.py...")
pano_path = 'code/MoGe/scripts/infer_panorama.py'
with open(pano_path, 'r') as f: content = f.read()

# On remplace simplement la variable mal orthographiee par la bonne
if 'log_splited_distance' in content:
    content = content.replace('log_splited_distance', 'log_splitted_distance')
    with open(pano_path, 'w') as f: f.write(content)
    print("Typo corrigée avec succès.")
else:
    print("Code déjà correct ou variable introuvable.")

print("Prêt pour relancer.")
