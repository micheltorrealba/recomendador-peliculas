import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv("config/.env")

# Obtener la ruta del dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "../data/dataset_final_sin_peliculas_excesivamente_largas.csv")

# Cargar el dataset
df = pd.read_csv(dataset_path)

# Vectorizar los textos
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Crear índice de películas
indices = pd.Series(df.index, index=df["title"]).drop_duplicates()

# Función de recomendación (respuesta en una sola línea con comas)
def recomendacion(titulo: str):
    if titulo not in indices:
        return {"error": "Película no encontrada."}
    
    idx = indices[titulo]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:6]
    recommended_movies = ", ".join(df["title"].iloc[[i[0] for i in sim_scores]])

    return {"mensaje": f"Te recomendamos las siguientes películas similares a {titulo}: {recommended_movies}"}
