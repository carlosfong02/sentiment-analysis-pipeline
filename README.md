# Pipeline de Análisis de Sentimiento con IA y Hugging Face

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![SQL](https://img.shields.io/badge/sql-%23FFD700.svg?style=for-the-badge&logo=sql&logoColor=black)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

## Descripción del Proyecto
Este proyecto implementa un pipeline ETL que extrae reseñas de productos de un dataset de Amazon. Utiliza Python para procesar los datos y los **enriquece con análisis de sentimiento**, llamando a un modelo de Procesamiento de Lenguaje Natural (NLP) a través de la API de **Hugging Face**.

Finalmente, los datos enriquecidos se cargan en una base de datos **SQLite**, listos para ser analizados con consultas SQL complejas y generar insights sobre la opinión de los clientes.

## Flujo del Proyecto
El pipeline sigue un flujo de trabajo de ETL clásico con un paso de enriquecimiento mediante IA:
`[Archivo JSON]` -> `[Python/Pandas (ETL)]` -> `[API de Hugging Face (Enriquecimiento)]` -> `[Base de Datos SQLite]` -> `[Análisis con SQL]` -> `[Insights]`

## Fuente de Datos
El dataset utilizado en este proyecto ("Amazon Customer Reviews") es demasiado grande para ser incluido en este repositorio. Puede ser descargado desde Kaggle.

**Enlace:** [Amazon Reviews](https://www.kaggle.com/datasets/abdallahwagih/amazon-reviews)

*Nota: Para ejecutar el proyecto, descarga el archivo `Cell_Phones_and_Accessories_5.json` y colócalo en la carpeta raíz del proyecto.*

## Características Clave
* **Pipeline ETL Funcional**: Script de Python que automatiza la extracción, transformación y carga de los datos.
* **Integración de IA (NLP)**: Enriquece los datos crudos con análisis de sentimiento utilizando un modelo pre-entrenado de Hugging Face.
* **Manejo de APIs Externas**: Realiza llamadas a una API REST de forma robusta, incluyendo manejo de errores.
* **Almacenamiento en Base de Datos**: Carga los datos procesados en una base de datos relacional (SQLite) para su almacenamiento persistente.
* **Análisis con SQL**: Demuestra la capacidad de consultar y extraer valor de los datos almacenados.
* **Manejo Seguro de Credenciales**: Protege las claves de la API utilizando variables de entorno (`.env`).

## Tecnologías Utilizadas
* **Lenguajes:** Python, SQL
* **Base de Datos:** SQLite
* **Librerías Python:** Pandas, Requests, SQLAlchemy, python-dotenv, TQDM
* **Plataforma de IA:** Hugging Face (Inference API)
* **Herramientas:** Git/GitHub

## Configuración e Instalación
1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DE_TU_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```
2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configurar Variables de Entorno:**
    * Crea un archivo `.env` y añade tu token de acceso de Hugging Face:
    ```
    HF_TOKEN="tu-token-secreto"
    ```

## Uso
1.  **Ejecuta el pipeline principal** para iniciar la extracción, el análisis de sentimiento y la carga a la base de datos:
    ```bash
    python sentiment_pipeline.py
    ```
2.  **Explora los resultados** abriendo el archivo `sentiments.db` con un cliente SQL (como DB Browser for SQLite) y ejecuta las consultas del siguiente apartado.

## Ejemplos de Análisis Realizado
A continuación se muestran ejemplos de las consultas realizadas sobre los datos enriquecidos.

#### 1. Desglose General de Sentimientos
**Propósito:** Entender la distribución general de las opiniones de los clientes.

**Consulta:**
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
**Resultado:**
| sentiment | total_reviews | percentage |
| :---    | :--- | :--- |
| 5 stars | 350 | 70.0 |
| 4 stars | 75 | 15.0 |
| 1 star  | 30 | 6.0 |
| 3 stars | 25 | 5.0 |
| 2 stars | 20 | 4.0 |

#### 2. Correlación entre Longitud de la Reseña y Sentimiento
**Propósito:** Investigar si los clientes descontentos tienden a escribir reseñas más largas.

**Consulta:**
```sql
SELECT
    sentiment,
    AVG(LENGTH(reviewText)) AS average_review_length
FROM
    reviews
GROUP BY
    sentiment
ORDER BY
    average_review_length DESC;
```
**Resultado:**
| sentiment | average_review_length |
| :---    | :--- |
| 1 star  | 450.5 |
| 2 stars | 380.2 |
| 3 stars | 310.8 |
| 5 stars | 250.1 |
| 4 stars | 245.7 |