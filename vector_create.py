# Importation des bibliothèques nécessaires
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# ----------------------------------------------------------------------
# 1. Préparer un jeu de données textuel
# ----------------------------------------------------------------------

# Lire les documents à partir d'un fichier
with open('list.txt', 'r', encoding='utf-8') as file:
    documents = file.readlines()
documents = [doc.strip() for doc in documents]

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
# 4. Sauvegarder 
# ----------------------------------------------------------------------
# Sauvegarder l'index sur disque
faiss.write_index(index, "index.faiss")
print("Index sauvegardé avec succès !")

# Sauvegarder les documents associés aux vecteurs
np.save("documents.npy", documents)
print("Documents sauvegardés avec succès !")
