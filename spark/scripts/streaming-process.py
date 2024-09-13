import time
from dotenv import load_dotenv
from pyspark.sql.types import IntegerType
import os
from pyspark.sql.functions import from_json, col, to_timestamp

from config import ss_config, json_schema_to_spark, create_config, k_config, load_schema_from_json



load_dotenv()

# Paths de los archivos de configuración
consumer_config_path = os.getenv('CONSUMER_CONFIG_PATH')
schema_config_path = os.getenv('SCHEMA_PATH')
spark_config_path = os.getenv('SPARK_CONFIG_PATH')

# App name
app_name = os.getenv('APP_NAME')

# Configuraciones
consumer_config = create_config(consumer_config_path)
sesion_congif = create_config(spark_config_path)
# Cargar el esquema desde el archivo JSON
schema_json = load_schema_from_json(schema_config_path)

# Convertir el esquema JSON a un esquema de PySpark
schema_config = json_schema_to_spark(schema_json)

# Crear una sesión de Spark con el classpath del driver de PostgreSQL
spark = ss_config(spark_config_path, app_name)

# Configurar el DataFrame de streaming en Spark para leer datos en tiempo real desde Kafka
kafka_stream_df = k_config(consumer_config_path, spark)

# Convertir los datos de Kafka a formato legible
# Validación básica de la estructura JSON
processed_df = kafka_stream_df.select(
    col("key").cast("string"),
    col("value").cast("string")
).filter(col("value").isNotNull())

# Aplicar el esquema y manejar errores en el JSON
try:
    processed_df = processed_df.withColumn("value", from_json(col("value"), schema_config))
except Exception as e:
    # Manejo de excepción si ocurre un error en la aplicación del esquema
    print(f"Error aplicando el esquema JSON: {e}")
    # Opcional: Redirigir los datos erróneos a un tema especial de Kafka o almacenamiento alternativo


# Aplicar el esquema a los datos procesados
processed_df = processed_df.withColumn("value", from_json(col("value"), schema_config))

# Función para procesar cada micro-batch
def process_batch(df, batch_id):
    df_transformed = df.select(
        col("value.results.gender").getItem(0).alias("gender"),
        col("value.results.name.title").getItem(0).alias("name_title"),
        col("value.results.name.first").getItem(0).alias("name_first"),
        col("value.results.name.last").getItem(0).alias("name_last"),
        col("value.results.location.street.number").getItem(0).cast(IntegerType()).alias("street_number"),
        col("value.results.location.street.name").getItem(0).alias("street_name"),
        col("value.results.location.city").getItem(0).alias("city"),
        col("value.results.location.state").getItem(0).alias("state"),
        col("value.results.location.country").getItem(0).alias("country"),
        col("value.results.location.postcode").getItem(0).alias("postcode"),
        col("value.results.email").getItem(0).alias("email"),
        col("value.results.login.uuid").getItem(0).alias("uuid"),
        to_timestamp(col("value.results.dob.date").getItem(0), "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'").alias("dob_date"),
        col("value.results.dob.age").getItem(0).cast(IntegerType()).alias("age"),
        col("value.results.phone").getItem(0).alias("phone"),
        col("value.results.cell").getItem(0).alias("cell"),
        col("value.results.picture.large").getItem(0).alias("picture_large")
    )

    # Implementación de lógica de reintento
    max_retries = 3
    retry_delay = 5  # Segundos
    retries = 0
    success = False

    while retries < max_retries and not success:
        try:
            # Escribir los datos en la db
            df_transformed.write.jdbc(
                url=os.getenv('POSTGRES_URL'),
                table="users",
                mode="append",
                properties={
                    "user": os.getenv('POSTGRES_USER'),
                    "password": os.getenv('POSTGRES_PASSWORD'),
                    "driver": "org.postgresql.Driver",
                    "batchsize": "500"
                }
            )
            success = True
        except Exception as e:
            retries += 1
            print(f"Error al escribir en PostgreSQL, intento {retries}/{max_retries}: {e}")
            time.sleep(retry_delay)

    if not success:
        print(f"Fallo al escribir en PostgreSQL después de {max_retries} intentos. Redirigiendo los datos a almacenamiento alternativo.")
        # Opcional: Guardar el batch en almacenamiento alternativo (HDFS, S3, etc.)

# Configurar el streaming query con un intervalo de disparo ajustado
query = processed_df.writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .option("checkpointLocation", "/opt/spark/checkpoints") \
    .trigger(processingTime='10 seconds') \
    .start()

# Esperar a que la consulta termine
query.awaitTermination()