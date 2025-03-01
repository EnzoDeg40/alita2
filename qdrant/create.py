from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

# Connexion à Qdrant (assure-toi que Qdrant tourne sur localhost:6333)
client = QdrantClient(host="localhost", port=6333)

# Définir les paramètres de la collection
collection_name = "ma_collection"
vector_size = 512  # Adapte cette valeur à la dimension de tes embeddings (ex: 512 pour CLIP base)
distance = Distance.COSINE  # Distance utilisée pour la similarité (Cosine, Euclidean, etc.)

# Créer (ou recréer) la collection
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=vector_size, distance=distance)
)

print(f"La collection '{collection_name}' a été créée avec des vecteurs de dimension {vector_size} et la distance {distance}.")
