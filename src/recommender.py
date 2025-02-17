import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el dataset
df = pd.read_csv("src/data/dataset_final_sin_peliculas_excesivamente_largas.csv")

# Preparar los datos
# Asegurar que las columnas clave sean strings y estén en minúsculas sin espacios adicionales
for col in ["genres", "actores", "director", "companias_produccion"]:
    df[col] = df[col].astype(str).str.lower().str.replace(" ", "")

# Ajustar la combinación de características con pesos
df["combined_features"] = (df["genres"] + " " + df["genres"] + " " + df["genres"] + " " + 
                           df["actores"] + " " + df["actores"] + " " + 
                           df["director"] + " " + df["director"] + " " + 
                           df["companias_produccion"] + " " + df["companias_produccion"])

# Vectorización con TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["combined_features"])

# Calcular la matriz de similitud del coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Función de recomendación mejorada
def recomendar_peliculas(titulo):
    # Verificar si la película existe
    if titulo.lower() not in df["title"].str.lower().values:
        return "Error: Película no encontrada en el dataset"

    # Obtener índice de la película
    idx = df[df["title"].str.lower() == titulo.lower()].index[0]

    # Obtener lista de similitud
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenar por mayor similitud y tomar las 5 más cercanas (sin contar la misma película)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]

    # Obtener los títulos recomendados
    recomendadas = df.iloc[[i[0] for i in sim_scores]]["title"].tolist()

    # Formato de la respuesta
    respuesta = f"Te recomendamos las siguientes películas similares a {titulo}:\n"
    respuesta += "\n".join(recomendadas)

    return respuesta

