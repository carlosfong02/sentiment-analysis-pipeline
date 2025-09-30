# Pipeline de Análisis de Sentimiento con IA y Hugging Face

## Descripción del Proyecto
Este proyecto implementa un pipeline ETL que extrae reseñas de productos de un dataset de Amazon. Utiliza Python y Pandas para procesar los datos y los enriquece con análisis de sentimiento llamando a un modelo de Procesamiento de Lenguaje Natural (NLP) a través de la API de Hugging Face. Finalmente, los datos enriquecidos se cargan en una base de datos SQLite para su posterior análisis con SQL.

## Fuente de Datos
El dataset utilizado en este proyecto ("Amazon Customer Reviews") se puede descargar desde Kaggle.

**Enlace:** (https://www.kaggle.com/datasets/abdallahwagih/amazon-reviews)

*Nota: Para ejecutar el proyecto, descarga el archivo `Cell_Phones_and_Accessories_5.json` y colócalo en la carpeta raíz del proyecto.*

## Flujo del Proyecto
`[Archivo JSON]` -> `[Python/Pandas (ETL)]` -> `[API de Hugging Face (Enriquecimiento)]` -> `[Base de Datos SQLite]` -> `[Análisis con SQL]`

## Tecnologías Utilizadas
* Python
* Pandas
* SQLite
* Hugging Face (Inference API)
* Requests, TQDM, python-dotenv

## Uso
1.  Clonar el repositorio.
2.  Instalar las dependencias: `pip install -r requirements.txt`.
3.  Crear un archivo `.env` y añadir el token de acceso de Hugging Face (`HF_TOKEN="tu-token"`).
4.  Ejecutar el script principal para iniciar el pipeline: `python sentiment_pipeline.py`.
5.  Explorar la base de datos `sentiments.db` resultante con un cliente SQL.

## Ejemplos de Análisis
A continuación se muestran ejemplos de las consultas realizadas sobre los datos enriquecidos para obtener insights:

**Consulta para ver el desglose general de sentimientos:**
```sql
SELECT
    sentiment,
    COUNT(*) AS total_reviews,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reviews), 2) AS percentage
FROM
    reviews
GROUP BY
    sentiment
ORDER BY
    total_reviews DESC;
```