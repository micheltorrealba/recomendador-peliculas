import pandas as pd
import ast

#Cargar los datasets originales
movies_path = "movies_dataset.csv"
credits_path = "credits.csv"

movies_df = pd.read_csv(movies_path, low_memory=False)
credits_df = pd.read_csv(credits_path)

#Seleccionar las columnas necesarias, incluyendo 'vote_count'
selected_columns = [
    "id", "title", "genres", "release_date", "original_language", 
    "budget", "revenue", "production_companies", "vote_average", 
    "runtime", "popularity", "vote_count"
]
movies_df = movies_df[selected_columns]

#Eliminar valores nulos en columnas clave
movies_df.dropna(subset=["id", "title", "release_date", "original_language"], inplace=True)

#Convertir 'id' a tipo entero
movies_df["id"] = movies_df["id"].astype(int)
credits_df["id"] = credits_df["id"].astype(int)

#Filtrar películas en inglés desde 1970 en adelante
movies_df = movies_df[movies_df["original_language"] == "en"]
movies_df["release_date"] = pd.to_datetime(movies_df["release_date"], errors="coerce")
movies_df.dropna(subset=["release_date"], inplace=True)
movies_df = movies_df[movies_df["release_date"].dt.year >= 1970]

#Convertir 'budget' y 'revenue' a float
movies_df["budget"] = pd.to_numeric(movies_df["budget"], errors="coerce").fillna(0).astype(float)
movies_df["revenue"] = pd.to_numeric(movies_df["revenue"], errors="coerce").fillna(0).astype(float)

#Calcular el retorno de inversión (revenue / budget)
movies_df["return"] = movies_df.apply(lambda x: x["revenue"] / x["budget"] if x["budget"] > 0 else 0, axis=1)

#Convertir 'popularity' y 'vote_count' a float
movies_df["popularity"] = pd.to_numeric(movies_df["popularity"], errors="coerce").fillna(0).astype(float)
movies_df["vote_count"] = pd.to_numeric(movies_df["vote_count"], errors="coerce").fillna(0).astype(int)

#Hacer merge con el dataset de créditos
merged_df = pd.merge(movies_df, credits_df, on="id", how="inner")

#Función para extraer nombres de géneros
def extract_genre_names(genre_list):
    try:
        if pd.notna(genre_list) and genre_list != "[]":
            genre_data = ast.literal_eval(genre_list)
            return ", ".join([genre["name"] for genre in genre_data if "name" in genre])
        return None
    except (ValueError, SyntaxError):
        return None

merged_df["genres"] = merged_df["genres"].apply(extract_genre_names)

#Función para extraer los tres primeros actores
def extract_top_actors(cast_list):
    try:
        if pd.notna(cast_list) and cast_list != "[]":
            cast_list = cast_list.replace("'", "\"")
            cast_data = ast.literal_eval(cast_list)
            return ", ".join([actor["name"] for actor in cast_data[:3] if "name" in actor])
        return None
    except (ValueError, SyntaxError):
        return None

merged_df["actores"] = merged_df["cast"].apply(extract_top_actors)

#Función para extraer el director
def extract_director(crew_list):
    try:
        if pd.notna(crew_list) and crew_list != "[]":
            crew_list = crew_list.replace("'", "\"")
            crew_data = ast.literal_eval(crew_list)
            return ", ".join([member["name"] for member in crew_data if "job" in member and member["job"] == "Director"])
        return None
    except (ValueError, SyntaxError):
        return None

merged_df["director"] = merged_df["crew"].apply(extract_director)
merged_df.drop("crew", axis=1, inplace=True)

#Función para extraer nombres de las compañías de producción
def extract_production_companies(companies):
    try:
        if pd.notna(companies) and companies != "[]":
            companies_data = ast.literal_eval(companies)
            return ", ".join([company["name"] for company in companies_data if "name" in company])
        return None
    except (ValueError, SyntaxError):
        return None

merged_df["companias_produccion"] = merged_df["production_companies"].apply(extract_production_companies)
merged_df.drop("production_companies", axis=1, inplace=True)

#Crear la columna 'release_year'
merged_df["release_year"] = merged_df["release_date"].dt.year

#Eliminar columnas innecesarias
columns_to_drop = ["video", "imdb_id", "adult", "original_title", "poster_path", "homepage", "cast"]
merged_df.drop(columns=columns_to_drop, inplace=True, errors="ignore")

#Eliminar duplicados
merged_df.drop_duplicates(inplace=True)

#Filtrar películas con runtime menor a 40 minutos
merged_df = merged_df[merged_df["runtime"] >= 40]

#Filtrar las 5000 películas más populares
merged_df = merged_df.nlargest(5000, "popularity")

#Reemplazar valores nulos en 'companias_produccion' sin FutureWarning
merged_df = merged_df.assign(companias_produccion=merged_df["companias_produccion"].fillna("Desconocido"))

#Eliminar películas sin actores o director
merged_df.dropna(subset=["actores", "director"], inplace=True)

#Guardar el dataset final limpio
dataset_final_path = "dataset_final_top_5000.csv"
merged_df.to_csv(dataset_final_path, index=False)

#Confirmación final
print(f"✅ Dataset final guardado en '{dataset_final_path}'")
print("📊 Estadísticas del dataset final:")
print(merged_df.info())

#Eliminar películas excesivamente largas (> 300 min)
df = pd.read_csv(dataset_final_path, parse_dates=["release_date"])
df = df[df["runtime"] <= 300]

#Guardar el dataset actualizado
output_path = "dataset_final_sin_peliculas_excesivamente_largas.csv"
df.to_csv(output_path, index=False)

#Mostrar información del dataset actualizado
print(f"✅ Dataset final guardado en '{output_path}'")
print("📊 Estadísticas del dataset actualizado:")
print(df.info())
