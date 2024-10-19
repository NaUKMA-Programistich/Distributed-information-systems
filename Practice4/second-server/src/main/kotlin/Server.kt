import org.apache.kafka.clients.consumer.ConsumerConfig
import org.apache.kafka.clients.consumer.KafkaConsumer
import org.apache.kafka.common.serialization.StringDeserializer
import java.time.Duration
import java.util.Properties

fun main() {
    val kafkaProps = Properties().apply {
        put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092")
        put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer::class.java.name)
        put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer::class.java.name)
        put(ConsumerConfig.GROUP_ID_CONFIG, "simple-proto-group")
        put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest")
    }

    val consumer = KafkaConsumer<String, String>(kafkaProps)
        .apply { subscribe(listOf("simple-proto")) }

    while (true) {
        val records = consumer.poll(Duration.ofMillis(100))
        for (record in records) {
            println("Consumed message with key ${record.key()} and value ${record.value()} from partition ${record.partition()} with offset ${record.offset()}")
        }
    }
}
