import os
import pandas as pd
import requests
import time
import sqlite3
import logging 
from dotenv import load_dotenv
from tqdm import tqdm
from typing import List, Dict, Optional 

# --- Configuración del Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Carga de Variables de Entorno ---
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# --- Constantes del Proyecto ---
JSON_FILE = 'Cell_Phones_and_Accessories_5.json'
DB_NAME = 'sentiments.db'
TABLE_NAME = 'reviews'
API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
ROWS_TO_PROCESS = 500 # <-- MUESTRA 

def query_sentiment(text: str) -> Optional[List[Dict]]:
    """Envía un texto a la API de Hugging Face y devuelve el análisis de sentimiento."""
    payload = {"inputs": text[:512]} 
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error en la llamada a la API: {e}")
        return None

def load_df_to_sqlite(df: pd.DataFrame, db_name: str, table_name: str) -> bool:
    """Carga el DataFrame en una base de datos SQLite."""
    if df.empty:
        logging.warning("El DataFrame está vacío, no se cargarán datos.")
        return False
    try:
        conn = sqlite3.connect(db_name)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        logging.info(f"¡Datos cargados con éxito en la tabla '{table_name}' de la base de datos '{db_name}'!")
        return True
    except sqlite3.Error as e:
        logging.error(f"Ocurrió un error al cargar los datos a SQLite: {e}")
        return False

def main():
    """Función principal que orquesta el pipeline de ETL."""
    logging.info("Iniciando pipeline de análisis de sentimiento...")
    
    # 1. EXTRACCIÓN
    try:
        logging.info(f"Cargando el dataset {JSON_FILE}...")
        df = pd.read_json(JSON_FILE, lines=True)
        logging.info(f"Dataset cargado con {df.shape[0]} filas y {df.shape[1]} columnas.")
    except FileNotFoundError:
        logging.error(f"No se encontró el archivo '{JSON_FILE}'. Abortando.")
        return

    # 2. TRANSFORMACIÓN Y ENRIQUECIMIENTO
    if 'reviewText' not in df.columns:
        logging.error("La columna 'reviewText' no se encontró en el dataset. Abortando.")
        return
        
    df_clean = df.dropna(subset=['reviewText'])
    df_sample = df_clean.head(ROWS_TO_PROCESS).copy()
    logging.info(f"Procesando una muestra de {df_sample.shape[0]} reseñas...")
    
    sentiments = []
    scores = []
    
    for review in tqdm(df_sample['reviewText'], desc="Analizando sentimientos"):
        result = query_sentiment(review)
        
        if result and isinstance(result, list) and result[0]:
            best_sentiment = max(result[0], key=lambda x: x['score'])
            sentiments.append(best_sentiment.get('label'))
            scores.append(best_sentiment.get('score'))
        else:
            sentiments.append(None)
            scores.append(None)
        
        time.sleep(1)

    df_sample['sentiment'] = sentiments
    df_sample['score'] = scores
    
    logging.info("Muestra de datos enriquecidos:")
    logging.info("\n" + df_sample[['reviewerName', 'reviewText', 'sentiment', 'score']].head().to_string())

    # 3. CARGA
    if 'helpful' in df_sample.columns:
        df_sample['helpful'] = df_sample['helpful'].astype(str)
    
    load_df_to_sqlite(df_sample, DB_NAME, TABLE_NAME)
    logging.info("Pipeline finalizado.")

# --- Punto de Entrada del Script ---
if __name__ == "__main__":
    main()