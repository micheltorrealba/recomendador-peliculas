# Sistema de Recomendación de Películas 🎬

## 🎯 Descripción General

Bienvenidos a mi primer proyecto individual de MLOps, donde he usado las herramientas adquiridas en el curso del Bootcamp de Data Science de Henry. El obtivo principal de este proyecto de machine learning es crear un sistema de recomendación de películas basado en el análisis de similitud del coseno. Se desarrolló utilizando FastAPI para exponer los endpoints, Pandas para la manipulación de datos y Scikit-Learn para la implementación del modelo de recomendación.

## 🚀 Endpoints de la API

La API cuenta con los siguientes endpoints:

| Método   | Endpoint   | Descripción   |
|----------|------------|---------------|
| GET      | /cantidad_filmaciones_mes/{mes}   | Cantidad de películas estrenadas en un mes específico.                        |
| GET      | /cantidad_filmaciones_dia/{dia}   | Cantidad de películas estrenadas en un día específico.                        |
| GET      | /score_titulo/{titulo}            | Devuelve el score de popularidad de una película.                             |
| GET      | /votos_titulo/{titulo}            | Devuelve la cantidad de votos y el promedio de puntuación de una película.    |
| GET      | /get_actor/{nombre_actor}         | Información sobre un actor y su impacto en taquilla.                          |
| GET      | /get_director/{nombre_director}   | Información sobre un director y sus películas.                                |
| GET      | /recomendacion/{titulo}           | Devuelve una lista de 5 películas similares a la consultada.                  |

## ✍️ Autor

Michel Torrealba - Proyecto Final Henry Data Science Bootcamp 2025.


