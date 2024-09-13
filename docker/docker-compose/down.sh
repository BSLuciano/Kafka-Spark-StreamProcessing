#!/bin/bash

# Eliminar los contenedores con Docker Compose
docker-compose -f docker-compose-airflow.yaml -f docker-compose-kafka.yaml -f docker-compose-spark.yaml down -v