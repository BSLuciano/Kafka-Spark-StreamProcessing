# Configuración del Productor

```json
   {
     "client_id": "airflow_producer",
     "bootstrap_servers": "kafka-broker-1:9095,kafka-broker-2:9096,kafka-broker-3:9097",
     "key_serializer": "org.apache.kafka.common.serialization.StringSerializer",
     "value_serializer": "org.apache.kafka.common.serialization.StringSerializer",
     "acks": "all",
     "retries": 3,
     "linger_ms": 5,
     "batch_size": 16384,
     "compression_type": "gzip",
     "max_in_flight_requests_per_connection": 1,
     "request_timeout_ms": 20000,
     "buffer_memory": 5242880,
     "max_block_ms": 5000
   }
```

## Explicación de los parámetros configurados

 **client.id**: "producer"

   - *Descripción*: Un identificador único para el cliente (productor en este caso). Se usa en los logs y métricas para identificar las solicitudes que provienen de este productor.
   - *Función*: Ayuda a rastrear las operaciones y diagnosticar problemas específicos del productor.

 **bootstrap.servers**: "kafka-broker-1:9095,kafka-broker-2:9096, kafka-broker-3:9097"

   - *Descripción*: Lista de direcciones de brokers de Kafka para que el productor se conecte. Los brokers en esta lista son necesarios para que el productor descubra el clúster de Kafka.
   - *Función*: Permite al productor conectar con el clúster de Kafka. Es importante tener múltiples brokers para redundancia.

 **key.serializer**: "org.apache.kafka.common.serialization.StringSerializer"

   - *Descripción*: Serializador para las claves de los mensajes. En este caso, las claves son cadenas (String).
   - *Función*: Especifica cómo convertir las claves de los mensajes en bytes antes de enviarlas al broker. Se usa un serializador de cadena porque las claves son de tipo String.

 **value.serializer**: "org.apache.kafka.common.serialization.StringSerializer"

   - *Descripción*: Serializador para los valores de los mensajes. Similar a key.serializer, pero para los valores.
   - *Función:: Convierte los valores de los mensajes en bytes para enviarlos al broker. Se utiliza el mismo serializador que para las claves si los valores también son cadenas.

 **acks**: "all"

   - *Descripción*: Configuración de confirmación de escritura. "all" asegura que el líder del topic y todos los réplicas sincrónicas deben confirmar la recepción del mensaje antes de considerar la escritura como exitosa.
   - *Función*: Garantiza la mayor durabilidad posible, minimizando la posibilidad de pérdida de mensajes en caso de fallo del broker.

 **retries**: 3

   - *Descripción*: Número de intentos de reenvío en caso de fallo. El productor intentará enviar el mensaje hasta 3 veces si ocurre un error.
   - *Función*: Proporciona una forma de manejar fallos temporales de red o de brokers sin perder los mensajes.

 **linger.ms**: 0

   - *Descripción*: Tiempo que el productor espera antes de enviar un lote de mensajes. Un valor de 0 significa que los mensajes se envían inmediatamente.
   - *Función*: En un caso donde se necesita una baja latencia y los mensajes deben ser enviados tan pronto como se produzcan, se establece a 0.

 **compression.type**: "lz4"

   - *Descripción*: Tipo de compresión usado para los mensajes. "lz4" es un algoritmo de compresión que ofrece una buena combinación de velocidad y ratio de compresión.
   - *Función*: Ayuda a reducir el tamaño de los mensajes en tránsito y en disco, mejorando la eficiencia de la red y el almacenamiento.

 **enable.idempotence**: true

   - *Descripción*: Garantiza que cada mensaje se entregue exactamente una vez, evitando duplicados.
   - *Función*: Mejora la confiabilidad y exactitud en la entrega de mensajes, importante en sistemas de mensajería donde los duplicados pueden causar problemas.

 **max.in.flight.requests.per.connection**: 1

   - *Descripción*: Número máximo de solicitudes no confirmadas permitidas en una sola conexión. Establecerlo a 1 es común para garantizar que los mensajes se entreguen en el orden en que fueron enviados.
   - *Función*: Previene el reordenamiento de mensajes que puede ocurrir si hay más de una solicitud en vuelo y se usa enable.idempotence.

 **request.timeout.ms**: 20000

   - *Descripción*: Tiempo máximo que el productor espera una respuesta del broker antes de considerar que la solicitud ha fallado. Establecido en milisegundos.
   - *Función*: Proporciona un tiempo adecuado para esperar respuestas, balanceando entre tiempo de espera y capacidad de respuesta.

 **delivery.timeout.ms**: 30000

   - *Descripción*: Tiempo total permitido para que el mensaje sea entregado, incluyendo reintentos y confirmaciones. Esto incluye el tiempo de reintento y el tiempo de espera por la confirmación.
   - *Función*: Proporciona un tiempo máximo para asegurar que el mensaje se entregue, asegurando una alta probabilidad de éxito.

 **buffer.memory**: 5242880

   - *Descripción*: Tamaño del buffer de memoria en bytes que el productor usa para almacenar mensajes antes de enviarlos.
   - *Función*: Asegura que haya suficiente memoria para manejar la producción de mensajes antes de ser enviados, evitando bloqueos si el buffer se llena.

 **max.block.ms**: 5000

   - *Descripción*: Tiempo máximo que el productor espera para obtener espacio en el buffer si está lleno.
   - *Función*: Define cuánto tiempo el productor esperará antes de lanzar una excepción si no puede obtener espacio en el buffer, evitando bloqueos indefinidos.