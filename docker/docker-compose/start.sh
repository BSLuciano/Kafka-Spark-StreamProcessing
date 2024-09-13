#!/bin/bash

# Construir las imágenes personalizadas de Airflow, Postgres y Spark
docker build -t airflow-kafka -f ../dockerfile/airflow.Dockerfile .
#docker build -t postgres-external-conn -f ../dockerfile/postgres.Dockerfile .
docker build -t spark-dotenv -f ../dockerfile/spark.Dockerfile .

# Comprobar el estado de salida del comando docker build de ambas imágenes
if [ $? -eq 0 ]; then
  # Verificar si ambas imágenes fueron creadas
  if docker images | grep -q "airflow-kafka" && docker images | grep -q "spark-dotenv"; then
    echo "Imágenes airflow-kafka, postgres-external-conn y spark-dotenv construidas exitosamente."
    
    # Levantar los contenedores con Docker Compose
    docker-compose -f docker-compose-airflow.yaml -f docker-compose-kafka.yaml -f docker-compose-spark.yaml up -d
  else
    echo "Una o más imágenes no fueron encontradas. No se levantarán los contenedores."
    exit 1
  fi
else
  echo "Error en la construcción de una o más imágenes. No se levantarán los contenedores."
  exit 1
fi