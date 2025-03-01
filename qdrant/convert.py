from PIL import Image
import glob
import torch
from transformers import CLIPProcessor, CLIPModel

# Définir le device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Charger le modèle CLIP et son processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Récupérer tous les fichiers images du dossier (modifie le chemin et l'extension si nécessaire)
image_paths = glob.glob("/home/enzo/alita/qdrant/images/*.jpg")

points = []
for idx, image_path in enumerate(image_paths):
    # Charger l'image et la convertir en RGB
    image = Image.open(image_path).convert("RGB")
    
    # Préparer l'image pour le modèle
    inputs = processor(images=image, return_tensors="pt").to(device)
    
    # Générer l'embedding de l'image
    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
    
    # Convertir le vecteur en liste (le modèle CLIP retourne en général des vecteurs de 512 dimensions)
    vector = outputs.cpu().numpy().flatten().tolist()
    
    # Construire le point avec un id, le vecteur et un payload contenant le nom du fichier
    point = {
        "id": idx, 
        "vector": vector,
        "payload": {"source": image_path, "type": "image", "image_url": "http://127.0.0.1:5000/" + image_path.split("/")[-1]}
    }
    points.append(point)
    print(f"Image {idx+1}/{len(image_paths)} traitée.")

print(f"{len(points)} images sauvegardées dans points.json.")

# save points to file
import json
with open("points.json", "w") as f:
    json.dump(points, f)
    