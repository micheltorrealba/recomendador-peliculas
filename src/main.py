from fastapi import FastAPI
import pandas as pd
import os
from dotenv import load_dotenv
from src.recommender import recomendar_peliculas


# Cargar variables de entorno
load_dotenv("config/.env")

# Obtener la ruta del dataset desde las variables de entorno
dataset_path = os.getenv("DATASET_PATH", "src/data/dataset_final_sin_peliculas_excesivamente_largas.csv")


# Cargar el dataset
df = pd.read_csv(dataset_path, parse_dates=["release_date"])

# Iniciar FastAPI
app = FastAPI()

# Primer Endpoint: Cantidad de filmaciones en un mes

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    meses_dict = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    
    mes_num = meses_dict.get(mes.lower())
    if mes_num:
        cantidad = df[df["release_date"].dt.month == mes_num].shape[0]
        return {"mensaje": f"{cantidad} películas fueron estrenadas en {mes.capitalize()}"}
    else:
        return {"error": "Mes inválido. Usa un mes en español."}

# Segundo Endpoint: Cantidad de filmaciones en un día

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dias_dict = {
        "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
        "viernes": 4, "sábado": 5, "domingo": 6
    }

    dia_num = dias_dict.get(dia.lower())
    if dia_num is not None:
        cantidad = df[df["release_date"].dt.dayofweek == dia_num].shape[0]
        return {"mensaje": f"{cantidad} películas fueron estrenadas un {dia.capitalize()}"}
    else:
        return {"error": "Día inválido. Usa un día en español."}

# Tercer Endpoint: Obtener score de una película

@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    film = df[df["title"].str.lower() == titulo.lower()]
    if not film.empty:
        return {
            "titulo": titulo,
            "año": int(film["release_year"].values[0]),
            "score": float(film["popularity"].values[0])
        }
    else:
        return {"error": "Película no encontrada."}

# Cuarto Endpoint: Obtener votos de una película

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    film = df[df["title"].str.lower() == titulo.lower()]
    if not film.empty:
        votos = int(film["vote_count"].values[0])  # ✅ Usamos vote_count
        if votos >= 2000:
            return {
                "titulo": titulo,
                "año": int(film["release_year"].values[0]),
                "cantidad_votos": votos,
                "promedio_votos": float(film["vote_average"].values[0])  # Esto sí es vote_average
            }
        else:
            return {"mensaje": "La película no tiene suficientes votos (mínimo 2000)."}
    else:
        return {"error": "Película no encontrada."}

# Quinto Endpoint: Información sobre un actor

@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    actor_films = df[df["actores"].str.contains(nombre_actor, na=False, case=False)]
    if not actor_films.empty:
        total_retorno = actor_films["return"].sum()
        cantidad_peliculas = actor_films.shape[0]
        promedio_retorno = total_retorno / cantidad_peliculas
        return {
            "actor": nombre_actor,
            "cantidad_peliculas": cantidad_peliculas,
            "retorno_total": total_retorno,
            "retorno_promedio": promedio_retorno
        }
    else:
        return {"error": "Actor no encontrado."}

# Sexto Endpoint: Información sobre un director

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    director_films = df[df["director"].str.contains(nombre_director, na=False, case=False)]
    if not director_films.empty:
        total_retorno = director_films["return"].sum()
        peliculas = director_films[["title", "release_date", "return", "budget", "revenue"]].to_dict(orient="records")
        return {
            "director": nombre_director,
            "total_retorno": total_retorno,
            "peliculas": peliculas
        }
    else:
        return {"error": "Director no encontrado."}

#Mensaje de bienvenida
@app.get("/")
def read_root():
    return {"mensaje": "API de consulta de películas"}

# Endpoint de recomendación con respuesta mejorada
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    return {"mensaje": recomendar_peliculas(titulo)}

# Agregar ejecución de FastAPI con Uvicorn 🔥
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
