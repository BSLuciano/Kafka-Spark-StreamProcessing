# Configuración del Consumidor

```json
{
    "kafka.bootstrap.servers": "kafka-broker-1:9095,kafka-broker-2:9096,kafka-broker-3:9097",
    "subscribe": "random-user",
    "startingOffsets": "latest",
    "maxOffsetsPerTrigger": 5000,
    "fetch.max.bytes": 104857600,
    "fetch.min.bytes": 1048576,
    "session.timeout.ms": 30000,
    "heartbeat.interval.ms": 10000
  }
```

## Explicación de los parámetros

 **kafka.bootstrap.servers**: "kafka-broker-1:9095,kafka-broker-2:9096,kafka-broker-3:9097"

   *Descripción*: Lista de servidores Kafka (brokers) a los que el consumidor se conectará inicialmente para descubrir el clúster de Kafka.
   *Función*: Se proporciona una lista de múltiples brokers para asegurar la conexión al clúster incluso si alguno de los brokers no está disponible. Esto mejora la resiliencia del consumidor.

 **subscribe**: "random-user"

   - *Descripción*: Especifica el topic al que el consumidor se suscribirá para recibir mensajes.
   - *Función*: Indica al consumidor de Kafka que lea mensajes del topic random-user.

 **startingOffsets**: "earliest"

   - *Descripción*: Determina desde qué posición (offset) comenzar a consumir mensajes. "earliest" significa que comenzará a consumir desde los mensajes que se publiquen antes de que el consumidor se haya unido al topic.
   - *Función*: Es útil en escenarios donde se busca no omitir o perder datos, ya que siempre se comenzará a consumir desde el último offset procesado (se debe realizar *checkpointing* para poder llevar el control de los offsets).

 **maxOffsetsPerTrigger**: 5000

   - *Descripción*: Establece el número máximo de offsets (mensajes) que se procesarán en cada activación del consumidor.
   - *Función*: Controla la cantidad de datos que se procesan por ciclo de activación, lo cual es crucial para manejar cargas de trabajo y evitar el procesamiento excesivo en un solo ciclo.

 **fetch.max.bytes**: 104857600 (100 MB)

   - *Descripción*: Tamaño máximo de datos que el consumidor puede recuperar en una sola solicitud de recuperación (fetch).
   - *Función*: Permite que el consumidor recupere un volumen significativo de datos en cada solicitud, mejorando la eficiencia cuando se espera procesar grandes cantidades de datos.

 **fetch.min.bytes**: 1048576 (1 MB)

   - *Descripción*: El tamaño mínimo de datos que el consumidor intentará recuperar en una solicitud de recuperación. Si no hay suficientes datos, esperará hasta que los haya o hasta que se alcance el tiempo de espera.
   - *Función*: Asegura que el consumidor solo reciba datos cuando hay suficiente para procesar, lo que puede reducir la sobrecarga de solicitudes pequeñas y mejorar la eficiencia.

 **session.timeout.ms**: 30000 (30 segundos)

   - *Descripción*: Tiempo máximo que el consumidor puede estar sin enviar un latido (heartbeat) al coordinador del grupo de consumidores antes de que se considere fallido.
   - *Función*: Permite al consumidor tener un margen razonable de tiempo para fallos temporales en la red o tiempos de procesamiento, antes de ser considerado fallido y re-equilibrado por el coordinador.

 **heartbeat.interval.ms**: 10000 (10 segundos)

   - *Descripción*: Intervalo de tiempo entre cada latido (heartbeat) que el consumidor envía al coordinador del grupo de consumidores para indicar que está activo.
   - *Función*: Mantiene la conexión activa y ayuda al coordinador a monitorear la salud del consumidor. Un intervalo más corto permite una detección más rápida de fallos, mientras que un intervalo más largo reduce la sobrecarga de red.

 **key.deserializer**:

   - *Descripción*: Especifica la clase que se utiliza para deserializar las claves de los mensajes. En este caso, se aplica una clase proporcionada por Kafka que convierte las claves de los mensajes desde bytes a cadenas de texto ('String').
   - *Función*: Cuando los mensajes son producidos y almacenados en Kafka, las claves son convertidas a bytes usando un serializador. El consumidor necesita deserializar estos bytes oara oider procesar las claves como cadenas de texto.
   
 **value.deserializer**:

   - *Descripción*: Especifica la clase que se utiliza para deserializar los valores de los mensajes. Similar al deserializador de claves, convierte los valores de los mensajes desde bytes a cadenas de texto ('String').
   - *Función*: Al igual que con las claves, los valores de los mensajes son convertidos a bytes por el productor. El consumidor necesita deserializar estos bytes para interpretar los valores como cadenas de texto. Esto permite que el consumidor procese el contenido de los mensajes en su forma legible y útil..