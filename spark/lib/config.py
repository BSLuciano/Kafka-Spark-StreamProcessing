import json
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StringType, IntegerType, DoubleType, FloatType, LongType, BooleanType, StructType, StructField, ArrayType
)

def load_config(path):
    """
    Carga una configuración desde un archivo JSON.
    Devuelve un diccionario con la configuración si el archivo es válido.
    Maneja errores de archivo no encontrado y errores de decodificación JSON.
    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo {path} no se encuentra.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo {path} no se puede decodificar como JSON.")
        return None

def create_config(path):
    """
    Crea y devuelve una configuración cargada desde un archivo JSON usando la función load_config.
    """
    config = load_config(path)
    return config

def ss_config(path, name):
    """
    Configura y crea una sesión de Spark.
    Carga la configuración de Spark desde un archivo JSON y establece las configuraciones en la sesión de Spark.
    """
    spark_config = create_config(path)

    # Crear una sesión de Spark
    spark_builder = SparkSession.builder \
        .appName(name)

    # Establecer cada clave-valor en la configuración de Spark
    for key, value in spark_config.items():
        spark_builder = spark_builder.config(key, value)

    # Retorna la sesión de Spark creada
    return spark_builder.getOrCreate()

def k_config(path, spark_session):
    """
    Configura un DataFrame de streaming desde Kafka.
    Carga la configuración del consumidor Kafka desde un archivo JSON y aplica las configuraciones al stream.
    """
    consumer_config = create_config(path)

    # Crear el DataFrame de lectura de Kafka
    df_stream = spark_session.readStream \
        .format("kafka")

    # Aplicar las opciones de configuración al DataFrame
    for key, value in consumer_config.items():
        df_stream = df_stream.option(key, value)
    
    # Cargar el stream configurado
    return df_stream.load()

def load_schema_from_json(schema_path):
    """
    Carga un esquema desde un archivo JSON y lo devuelve como un diccionario.
    """
    with open(schema_path, 'r') as file:
        schema_json = json.load(file)
    return schema_json

def json_struct_to_struct(json_schema_dict):
    """
    Convierte un esquema JSON de tipo 'struct' a un esquema de PySpark StructType.
    Procesa cada campo del esquema JSON y lo convierte al tipo correspondiente en PySpark.
    """
    struct_fields = [
        StructField(
            field['name'],
            json_type_to_spark(field['type']),
            field.get('nullable', True)
        )
        for field in json_schema_dict['fields']
    ]
    return StructType(struct_fields)

def json_type_to_spark(json_type):
    """
    Convierte un tipo de dato JSON a su tipo equivalente en PySpark.
    Soporta tipos primitivos (string, integer, long, etc.) y estructuras más complejas como arrays y structs.
    """
    if isinstance(json_type, str):
        if json_type == 'string':
            return StringType()
        elif json_type == 'integer':
            return IntegerType()
        elif json_type == 'long':
            return LongType()
        elif json_type == 'float':
            return FloatType()
        elif json_type == 'double':
            return DoubleType()
        elif json_type == 'boolean':
            return BooleanType()
        else:
            raise ValueError(f"Tipo de dato JSON no soportado: {json_type}")
    elif isinstance(json_type, dict):
        if json_type['type'] == 'array':
            return ArrayType(json_type_to_spark(json_type['elementType']))
        elif json_type['type'] == 'struct':
            return json_struct_to_struct(json_type)
        else:
            raise ValueError(f"Tipo de dato JSON no soportado: {json_type}")
    else:
        raise ValueError(f"Tipo de dato JSON no soportado: {json_type}")

def struct_fields_to_spark(fields):
    """
    Convierte una lista de campos definidos en JSON a campos de PySpark StructType.
    Crea una lista de StructFields basada en los tipos de los campos del esquema JSON.
    """
    struct_fields = []
    for field in fields:
        field_type = json_type_to_spark(field['type'])
        struct_fields.append(StructField(field['name'], field_type, field.get('nullable', True)))
    return StructType(struct_fields)

def json_schema_to_spark(json_schema_dict):
    """
    Convierte un esquema JSON completo a un esquema de PySpark StructType.
    Procesa los campos del esquema JSON y los transforma al formato de PySpark.
    """
    return struct_fields_to_spark(json_schema_dict['fields'])