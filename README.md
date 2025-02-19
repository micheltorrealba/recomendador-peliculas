# Sistema de Recomendación de Películas 🎬

## 🎯 Descripción General

Bienvenidos a mi proyecto de Sistema de Recomendación de Películas 🎬! 
Este proyecto, desarrollado como parte del Bootcamp de Data Science de Henry, consiste en un sistema de recomendación de películas basado en Machine Learning. Para ello, utilicé Python, Pandas, Scikit-Learn y FastAPI, y se optimizó para ofrecer recomendaciones relevantes en segundos. Utilizando similitud del coseno, se analizan géneros, actores y directores para encontrar películas similares.

## 🛠️ Tecnologías Utilizadas

Tecnología | Uso en el Proyecto |
|----------|------------|
Python        | Lenguaje principal de desarrollo.|
FastAPI       | Creación de la API y exposición de los endpoints.|
Pandas        | Manipulación y limpieza de datos.|
Scikit-Learn  | Implementación de la similitud del coseno.|
Uvicorn       | Servidor ASGI para correr FastAPI.|
Render        | Despliegue de la API en la nube.|

## 📌 Fase 1: Adquisición y Exploración de los Datos

### 1️⃣ Obtención de los datasets originales en el repositorio de presentación de la asignación

- movies_dataset.csv
- credits.csv

### 2️⃣ Carga inicial y primeras inspecciones

- Se cargaron los datasets en Visual Studio Code para explorarlos con pandas.
- Se verificó la estructura de los datos con df.info(), df.head(), df.describe(), etc.
- Se detectaron problemas como valores nulos, columnas innecesarias y estructuras anidadas JSON dentro de algunas columnas.

## 📌 Fase 2: Limpieza y Transformación de Datos

### 3️⃣ Transformaciones sobre movies_dataset.csv

- Se eliminaron columnas irrelevantes para el análisis.
- Se manejaron valores nulos en columnas clave (reemplazo, eliminación o imputación).
- Se transformaron las fechas (release_date) al formato datetime.
- Se convirtió la columna de presupuesto (budget) a tipo numérico y se filtraron valores sospechosamente bajos.
- Se realizó el cálculo del retorno de inversión (return = revenue / budget).
- Columnas con estructuras JSON:
    - genres → Contenía una lista de diccionarios con los géneros de la película.
    - production_companies → Lista de compañías productoras en formato JSON.
    - production_countries → Lista de países de producción en formato JSON.
    - spoken_languages → Lista de idiomas hablados en la película.
- Se tuvo que convertir esta cadena en una lista real de Python con la librería ast y luego extraer solo los nombres de los géneros.

### 4️⃣ Transformaciones sobre credits.csv

- Se desanidaron y extrajeron actores y directores desde los campos JSON.
- Se extrajeron solo los nombres de los actores principales para simplificar el dataset.
- En crew, se filtraron solo los registros donde "job": "Director" para obtener el nombre del director de la película.
- Se convirtieron listas de diccionarios en listas planas de nombres.
- Se eliminaron caracteres innecesarios y se hicieron las columnas más manejables.
- Se unió este dataset con el de películas mediante la columna id.

### 5️⃣ Creación de dataset final

- Inicialmente, el dataset contenía miles de películas, lo cual hacía que el procesamiento fuera más lento.
- Para optimizar el rendimiento y obtener recomendaciones más precisas, se redujo el dataset considerando:
    - Películas con mayor popularidad y buen puntaje en vote_average.
    - Películas con un número significativo de votos en vote_count.
- Se detectaron valores nulos en los géneros, actores y directores, lo que implicaría problemas en el modelo de recomendación, así que se eliminaron.
- Se eliminaron películas con duración menor a 40 minutos, por ser consideradas cortometrajes, y películas extremadamente largas (fuera de los estándares comerciales).
- Se trabajó sólo con películas cuyo idioma original fuese inglés (en).
- Se guardó el dataset limpio y reducido como:
  - dataset_final_sin_peliculas_excesivamente_largas.csv
- El dataset final cuenta con sólo 2076 filas.

## 📌 Fase 3: Análisis Exploratorio de Datos (EDA)

### 6️⃣ Exploración de valores nulos y duplicados

- Se verificaron valores faltantes en las columnas principales.
- Se eliminaron duplicados que podrían afectar el análisis.

### 7️⃣ Análisis estadístico

- Se calcularon distribuciones de variables clave (budget, revenue, popularity, vote_average, vote_count).
- Se identificaron outliers (valores extremos en presupuesto, ingresos, etc.).
- Se exploraron correlaciones entre variables.
- Identificación de los **Top 10 géneros** más frecuentes en el dataset.

### 8️⃣ Análisis visual

- Histogramas y boxplots para visualizar distribuciones.
- Matrices de correlación para analizar relaciones entre variables.
- Nubes de palabras para analizar tendencias en los títulos de películas.

### Puedes ver el **notebook completo del EDA** en este enlace:

📎 [EDA.ipynb](https://github.com/micheltorrealba/recomendador-peliculas/blob/main/notebooks/EDA.ipynb)

⚠ **Nota:** Para ejecutar el EDA en local, asegúrate de que el dataset esté en la misma carpeta que el notebook. También puedes descargarlo desde aquí:  

📎 [Dataset para EDA](https://github.com/micheltorrealba/recomendador-peliculas/blob/main/notebooks/dataset_final_sin_peliculas_excesivamente_largas.csv)

## 📌 Fase 4: Creación de la API con FastAPI

### 9️⃣ Desarrollo de main.py

- Se creó una API REST con FastAPI para exponer los endpoints del sistema de recomendación.
- Se cargó el dataset limpio (dataset_final_sin_peliculas_excesivamente_largas.csv) dentro de la API.

### 🔟 Implementación de los endpoints

- La API cuenta con los siguientes endpoints:

| Método   | Endpoint   | Descripción   |
|----------|------------|---------------|
| GET      | /cantidad_filmaciones_mes/{mes}   | Cantidad de películas estrenadas en un mes específico.                        |
| GET      | /cantidad_filmaciones_dia/{dia}   | Cantidad de películas estrenadas en un día específico.                        |
| GET      | /score_titulo/{titulo}            | Devuelve el score de popularidad de una película.                             |
| GET      | /votos_titulo/{titulo}            | Devuelve la cantidad de votos y el promedio de puntuación de una película.    |
| GET      | /get_actor/{nombre_actor}         | Información sobre un actor y su impacto en taquilla.                          |
| GET      | /get_director/{nombre_director}   | Información sobre un director y sus películas.                                |
| GET      | /recomendacion/{titulo}           | Devuelve una lista de 5 películas similares a la consultada.                  |

## 📌 Fase 5: Desarrollo del Sistema de Recomendación

### 1️⃣1️⃣ Implementación de la Similitud del Coseno

- Se utilizó la técnica de TF-IDF Vectorizer para transformar las descripciones de las películas en vectores numéricos.
- Se aplicó similitud del coseno para encontrar películas similares.
- Se implementó una función que, dado un título de película, devuelve una lista de 5 recomendaciones.
- Para mejorar la calidad de las recomendaciones, decidí que el género de una película debía tener más influencia que los actores o el director, ya que los usuarios suelen buscar películas dentro de un mismo género.
- Para lograrlo, asigné los siguientes pesos en la construcción del perfil de cada película:

    | **Factor Analizado** | **Peso Asignado** |  
    |------------------|----------------|  
    | 🎭 **Géneros**  | 🔥🔥🔥 3x peso |  
    | 🎬 **Actores**  | 🔥🔥 2x peso |  
    | 🎥 **Director** | 🔥🔥 2x peso |

- Esto permitió mejorar la calidad de las recomendaciones, priorizando el género como la característica más importante.

## 📌 Fase 6: Organización del Repositorio en GitHub

### 1️⃣2️⃣ Estructuración de Carpetas

- Se organizó el código en carpetas dentro del repositorio:

        ├── config/    → Configuraciones y variables de entorno (.env)
        ├── data/      → Datasets procesados
        ├── notebooks/ → Exploraciones y análisis en Notebooks
        ├── src/       → Código fuente de la API (FastAPI)
        ├── README.md  → Documentación del proyecto
        ├── requirements.txt → Dependencias

### 1️⃣3️⃣ Uso de Variables de Entorno

- Se configuró un archivo .env en config/ para evitar credenciales hardcodeadas en el código.

## 📌 Fase 7: Despliegue de la API en Render

### 1️⃣4️⃣ Implementación en la Nube

- Se creó un servicio en Render para alojar la API.
- Se configuró para ejecutar Uvicorn con el siguiente comando:
        
        uvicorn src.main:app --host 0.0.0.0 --port 10000

- Se configuró el servicio para que instale las dependencias desde requirements.txt.
- Se cargó la base de datos en la carpeta /data/.
- Durante el despliegue, se resolvieron errores relacionados con la importación de variables de entorno (dotenv) y rutas de archivos.
- Se probó la API en la URL pública:
        🔗 https://recomendador-peliculas-kew3.onrender.com


## 🚀 Instalación y Ejecución

Si quieres probar la API en tu máquina local, sigue estos pasos:

1️⃣ Clona este repositorio:

        git clone https://github.com/micheltorrealba/recomendador-peliculas.git
        cd recomendador-peliculas

2️⃣ Crea un entorno virtual e instala dependencias:

        python -m venv venv
        source venv/bin/activate  # En Windows usa: venv\Scripts\activate
        pip install -r requirements.txt

3️⃣ Ejecuta la API:

        uvicorn src.main:app --reload

4️⃣ Accede a la documentación interactiva en:
👉 http://127.0.0.1:8000/docs

## 🎯 Cómo Probar la API

### Prueba en Navegador con Swagger UI

La forma más sencilla de probar los endpoints es usando Swagger UI, que FastAPI genera automáticamente.

🔗 Accede a la documentación interactiva aquí:
👉 https://recomendador-peliculas-kew3.onrender.com/docs

Abre el enlace en tu navegador.
Verás una lista con todos los endpoints disponibles.
Haz clic en el endpoint que quieras probar, ingresa los parámetros y presiona el botón "Execute" para ver la respuesta en tiempo real.

### Ejemplo: Probar el recomendador en Swagger UI

1️⃣ Ir a 👉 Swagger UI https://recomendador-peliculas-kew3.onrender.com/docs

2️⃣ Seleccionar /recomendacion/{titulo}

3️⃣ Ingresar el nombre de una película, por ejemplo: "Minions"

4️⃣ Presionar "Try it out" → "Execute"

5️⃣ La API generará una respuesta en formato JSON con las recomendaciones más relevantes, por ejemplo:

        {
          "mensaje": "Te recomendamos las siguientes películas similares a Minions: Penguins of Madagascar, Bee Movie, Million Dollar Arm, ParaNorman, Despicable Me 2"
        }

### 🛠 Otros Endpoints para Probar

Si quieres probar más funciones de la API, aquí tienes algunos ejemplos con sus respectivas URL:

| Función  | URL para probar en navegador, Postman o cURL   |
|----------|------------------------------------------------|
| Películas estrenadas en un mes                 | https://recomendador-peliculas-kew3.onrender.com/cantidad_filmaciones_mes/julio |
| Películas estrenadas en un día                 | https://recomendador-peliculas-kew3.onrender.com/cantidad_filmaciones_dia/viernes |
| Score de popularidad de una película           | https://recomendador-peliculas-kew3.onrender.com/score_titulo/Interstellar |
| Votos y promedio de puntuación de una película | https://recomendador-peliculas-kew3.onrender.com/votos_titulo/Interstellar |
| Información sobre un actor                     | https://recomendador-peliculas-kew3.onrender.com/get_actor/Leonardo%20DiCaprio |
| Información sobre un director                  | https://recomendador-peliculas-kew3.onrender.com/get_director/Christopher%20Nolan |


## ✍️ Autor

Michel Torrealba - Proyecto Individual de Machine Learning - 2025.
