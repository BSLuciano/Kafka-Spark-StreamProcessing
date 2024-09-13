# Usa la imagen base de Spark
FROM apache/spark:3.4.0

# Instala pip si no está instalado
RUN apt-get update && apt-get install -y python3-pip

# Instala python-dotenv
RUN pip install python-dotenv