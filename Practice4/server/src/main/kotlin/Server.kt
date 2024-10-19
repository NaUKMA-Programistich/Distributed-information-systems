import io.grpc.ServerBuilder
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import org.apache.kafka.clients.producer.KafkaProducer
import org.apache.kafka.clients.producer.ProducerConfig
import org.apache.kafka.clients.producer.ProducerRecord
import org.apache.kafka.common.serialization.StringSerializer
import java.util.*

class Server(private val port: Int) {
    private val messageQueue = MessageQueue()

    private val server = ServerBuilder.forPort(port)
        .addService(Service(messageQueue))
        .build()

    fun start() {
        server.start()
        println("Server started, listening on $port")
        Runtime.getRuntime().addShutdownHook(Thread {
            println("Shutting down gRPC server")
            this@Server.stop()
            println("Server shut down")
        })
    }

    private fun stop() {
        server.shutdown()
        messageQueue.close()
    }

    fun blockUntilShutdown() {
        server.awaitTermination()
        messageQueue.close()
    }
}

private class MessageQueue {
    private val kafkaProps = Properties().apply {
        put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092")
        put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer::class.java.name)
        put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer::class.java.name)
    }

    private val producer = KafkaProducer<String, String>(kafkaProps)

    fun send(message: String) {
        val id = UUID.randomUUID().toString()
        val record = ProducerRecord("simple-proto", id, message)
        producer.send(record) { metadata, exception ->
            if (exception != null) {
                println("Failed to send message: $exception")
            } else {
                println("Message sent: $metadata")
            }
        }
    }

    fun close () {
        producer.close()
    }
}


private class Service(private val messageQueue: MessageQueue) : GreeterGrpcKt.GreeterCoroutineImplBase() {
    override suspend fun sayHello(request: Simple.HelloRequest): Simple.HelloReply {
        messageQueue.send("Hello ${request.name}")
        return helloReply {
            message = "Hello ${request.name}"
        }
    }

    override fun sayHelloAgain(request: Simple.HelloRequest): Flow<Simple.HelloReply> {
        messageQueue.send("Hello Again ${request.name}")
        return flow {
            repeat(10) {
                emit(helloReply {
                    message = "Hello again ${request.name}"
                })
                kotlinx.coroutines.delay(1000)
            }
        }
    }
}

fun main() {
    val server = Server(50051)
    server.start()
    server.blockUntilShutdown()
}