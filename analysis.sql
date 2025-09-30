-- 1. Desglose General de Sentimientos
-- Propósito: Da una visión general de la distribución de las opiniones (positivas, negativas, etc) y su porcentaje.

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


-- 2. Comparación: Sentimiento de la IA vs. Calificación del Usuario
-- Propósito: Compara la calificación original que dio el usuario (overall) con la que predijo el modelo de IA (sentiment).
SELECT
    overall AS user_star_rating,
    sentiment AS ai_sentiment_prediction,
    COUNT(*) AS number_of_reviews
FROM
    reviews
GROUP BY
    user_star_rating,
    ai_sentiment_prediction
ORDER BY
    user_star_rating DESC,
    ai_sentiment_prediction;


-- 3. Encontrar las Reseñas Negativas más Seguras
-- Propósito:  Identifica las reseñas que el modelo clasificó como "1 star" (Probablemente las quejas más claras y directas)

SELECT
    reviewText,
    sentiment,
    score
FROM
    reviews
WHERE
    sentiment = '1 star'
ORDER BY
    score DESC
LIMIT 5;

-- 4. Detectar Anomalías: Reseñas Positivas con Calificación Mínima
-- Propósito:  Busca reseñas donde el usuario dio 1 estrella, pero el texto fue clasificado como positivo por la IA, (sarcasmo)

SELECT
    reviewText,
    overall AS user_star_rating,
    sentiment AS ai_sentiment_prediction,
    score
FROM
    reviews
WHERE
    overall <= 2.0 AND sentiment IN ('4 stars', '5 stars')
ORDER BY
    score DESC;