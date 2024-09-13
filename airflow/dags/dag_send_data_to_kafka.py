from airflow.decorators import dag, task
import pendulum
from datetime import timedelta

@dag(
    dag_id="send_data_to_kafka",
    start_date=pendulum.datetime(2024, 8, 16, tz='UTC'),
    schedule_interval=timedelta(seconds=25),
    catchup=False,
    default_args={'owner': 'LBS', 'retries': 3, 'retry_delay': pendulum.duration(seconds=12)},
    tags=["Producer", "Kafka", "Random User API"],
    description='Consultar API a intervalos regulares y enviar datos a kafka'
)
def TaskFlow():

    @task
    def producer():
        from airflow.models import Variable
        from kafka import KafkaProducer
        import json
        import requests

        # Obtener parámetros de configuración del productor
        config_json = Variable.get('kafka_producer_config')
        config_dict = json.loads(config_json)
        topic = Variable.get('kafka_topic')

        # Crear el productor de Kafka con la configuración
        kafka_producer = KafkaProducer(
            client_id=config_dict.get('client_id'),
            bootstrap_servers=config_dict.get('bootstrap_servers'),
            key_serializer=lambda k: k.encode('utf-8') if k is not None else None,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks=config_dict.get('acks'),
            retries=config_dict.get('retries'),
            linger_ms=config_dict.get('linger_ms'),
            batch_size=config_dict.get('batch_size'),
            compression_type=config_dict.get('compression_type'),
            max_in_flight_requests_per_connection=config_dict.get('max_in_flight_requests_per_connection'),
            request_timeout_ms=config_dict.get('request_timeout_ms'),
            buffer_memory=config_dict.get('buffer_memory'),
            max_block_ms=config_dict.get('max_block_ms')
        )

        for i in range(10):
            # Consultar la API de Random User Generator
            response = requests.get("https://randomuser.me/api/")
            data = response.json()

            # Enviar mensaje al topic de kafka
            kafka_producer.send(topic, key=None, value=data)
        
        kafka_producer.flush()  # Asegura que todos los mensajes sean enviados
        kafka_producer.close()  # Cierra el productor después de enviar los mensajes

        return {
            'response': 200,
            'body': 'Mensajes enviados al topic.'
        }
    
    producer()

TaskFlow()