from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv("config/.env")

# 🔹 Obtener la ruta absoluta del dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "../data/dataset_final_sin_peliculas_excesivamente_largas.csv")

# Verificación de existencia del archivo
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"El dataset no se encontró en la ruta: {dataset_path}")

# 🔹 Cargar el dataset
df = pd.read_csv(dataset_path)

# Verificación de existencia de la columna "combined_features"
if "combined_features" not in df.columns:
    raise ValueError("La columna 'combined_features' no está en el dataset. Verifica su creación en el preprocesamiento.")

# Preparar TF-IDF para el modelo de recomendación
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["combined_features"])  # ✅ Nos aseguramos de que esta columna exista
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Crear un índice de películas
indices = pd.Series(df.index, index=df["title"]).drop_duplicates()

# **Función para devolver recomendaciones en JSON**
def recomendacion(titulo: str):
    if titulo not in indices:
        return {"error": "Película no encontrada."}
    
    idx = indices[titulo]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Obtener las 5 películas más similares
    movie_indices = [i[0] for i in sim_scores]
    recommended_movies = df["title"].iloc[movie_indices].tolist()

    return {
        "mensaje": f"Te recomendamos las siguientes películas similares a {titulo}:",
        "recomendaciones": recommended_movies  # Devuelve una lista en JSON
    }
