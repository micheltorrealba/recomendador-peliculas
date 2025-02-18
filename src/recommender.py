import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv("config/.env")

# Definir la ruta del dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "../data/dataset_final_sin_peliculas_excesivamente_largas.csv")

# Cargar el dataset
df = pd.read_csv(dataset_path)

# Ponderamos los atributos según la importancia requerida
df["features"] = (df["genres"].fillna('') * 3) + " " + \
                 (df["actores"].fillna('') * 2) + " " + \
                 (df["director"].fillna('') * 2)

# Vectorización con TF-IDF
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["features"])

# Calcular la similitud del coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Crear un índice de películas
indices = pd.Series(df.index, index=df["title"]).drop_duplicates()

# **Función de recomendación con ponderación ajustada**
def recomendacion(titulo: str):
    if titulo not in indices:
        return {"error": "Película no encontrada."}

    idx = indices[titulo]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Tomamos las 5 películas más similares

    movie_indices = [i[0] for i in sim_scores]
    recommended_movies = df["title"].iloc[movie_indices].tolist()

    # Respuesta en una sola línea, separada por comas
    return {
        "mensaje": f"Te recomendamos las siguientes películas similares a {titulo}: " + ", ".join(recommended_movies)
    }
