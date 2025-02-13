import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ----------------------------------------------------------------------
# 1. Charger les données et le modèle
# ----------------------------------------------------------------------
# Charger le modèle de transformation de phrases
model = SentenceTransformer('all-MiniLM-L6-v2')

# Charger l'index FAISS
index = faiss.read_index('index.faiss')

# Charger les documents associés aux vecteurs
documents = np.load('documents.npy', allow_pickle=True)

# ----------------------------------------------------------------------
# 2. Effectuer une recherche par similarité
# ----------------------------------------------------------------------
while True:
    # Demander à l'utilisateur de saisir une requête
    query = input("Entrez votre requête (ou tapez 'exit' pour quitter) : ")
    
    if query.lower() == 'exit':
        break

    # Convertir la requête en vecteur via le même modèle
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')

    # Nombre de résultats à récupérer
    k = 5

    # Rechercher dans l'index : retourne distances et indices des vecteurs les plus proches
    distances, indices = index.search(query_embedding, k)

    # Afficher les résultats
    print(f"\nRésultats pour la requête : '{query}'\n")
    for rank, idx in enumerate(indices[0]):
        print(f"Résultat {rank+1}:")
        print(f"Texte: {documents[idx]}")
        print(f"Distance: {distances[0][rank]:.4f}\n")

