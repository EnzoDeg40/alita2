# Importation des bibliothèques nécessaires
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# ----------------------------------------------------------------------
# 1. Préparer un jeu de données textuel
# ----------------------------------------------------------------------
documents = [
    "Ceci est un exemple de texte.",
    "Un autre texte à indexer dans la base de données vectorielle.",
    "Le machine learning est passionnant.",
    "FAISS est une bibliothèque de recherche par similarité.",
    "Les bases de données vectorielles facilitent la recherche sémantique."
]

# ----------------------------------------------------------------------
# 2. Charger un modèle pour obtenir les embeddings (représentations vectorielles)
# ----------------------------------------------------------------------
# Ici, nous utilisons le modèle 'all-MiniLM-L6-v2', léger et performant pour du texte court.
model = SentenceTransformer('all-MiniLM-L6-v2')

# Transformer les textes en vecteurs
embeddings = model.encode(documents)
# Convertir en tableau NumPy de type float32 (obligatoire pour FAISS)
embeddings = np.array(embeddings).astype('float32')

# Vérifier la dimension des vecteurs
dimension = embeddings.shape[1]
print(f"Dimension des embeddings : {dimension}")

# ----------------------------------------------------------------------
# 3. Créer l'index FAISS
# ----------------------------------------------------------------------
# Nous utilisons ici un index basé sur la distance L2 (Euclidienne)
index = faiss.IndexFlatL2(dimension)

# Ajouter les embeddings à l'index
index.add(embeddings)
print(f"Nombre de vecteurs indexés : {index.ntotal}")

# ----------------------------------------------------------------------
# 4. Effectuer une recherche par similarité
# ----------------------------------------------------------------------
# Exemple de requête (texte à rechercher)
query = "Recherche de texte similaire sur les embeddings"

# Convertir la requête en vecteur via le même modèle
query_embedding = model.encode([query])
query_embedding = np.array(query_embedding).astype('float32')

# Nombre de résultats à récupérer
k = 2

# Rechercher dans l'index : retourne distances et indices des vecteurs les plus proches
distances, indices = index.search(query_embedding, k)

# Afficher les résultats
print(f"\nRésultats pour la requête : '{query}'\n")
for rank, idx in enumerate(indices[0]):
    print(f"Résultat {rank+1}:")
    print(f"Texte: {documents[idx]}")
    print(f"Distance: {distances[0][rank]:.4f}\n")
