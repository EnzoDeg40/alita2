from qdrant_client import QdrantClient
import json

# Charger les points depuis le fichier JSON
with open("points.json", "r") as f:
    points = json.load(f)

# Connexion au serveur Qdrant
client = QdrantClient(host="localhost", port=6333)

# Insertion des points dans la collection "ma_collection"
client.upsert(collection_name="ma_collection", points=points)

print("Les images ont été chargées avec succès dans Qdrant.")
