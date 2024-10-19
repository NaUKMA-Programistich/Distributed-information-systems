plugins {
    kotlin("jvm") version "2.0.20"
    id("com.google.protobuf") version "0.9.4"
}

group = "com.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

kotlin {
    jvmToolchain(17)
}

sourceSets {
    main {
        proto {
            srcDir("../proto")
        }
    }
}

val grpcVersion = "1.62.2"
val grpcKotlinVersion = "1.4.1"
val protobufVersion = "4.28.2"
val coroutinesVersion = "1.8.0"
val kafkaVersion = "3.8.0"

dependencies {
    implementation("javax.annotation:javax.annotation-api:1.3.2")
    implementation("io.grpc:grpc-kotlin-stub:$grpcKotlinVersion")
    implementation("io.grpc:grpc-protobuf:$grpcVersion")
    implementation("com.google.protobuf:protobuf-kotlin:$protobufVersion")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:$coroutinesVersion")
    runtimeOnly("io.grpc:grpc-netty-shaded:$grpcVersion")
    implementation("org.apache.kafka:kafka-clients:$kafkaVersion")
}

protobuf {
    protoc {
        artifact = "com.google.protobuf:protoc:$protobufVersion"
    }

    plugins {
        create("grpc") {
            artifact = "io.grpc:protoc-gen-grpc-java:$grpcVersion"
        }
        create("grpckt") {
            artifact = "io.grpc:protoc-gen-grpc-kotlin:$grpcKotlinVersion:jdk8@jar"
        }
    }

    generateProtoTasks {
        all().forEach {
            it.plugins {
                create("grpc")
                create("grpckt")
            }
            it.builtins {
                create("kotlin")
            }
        }
    }
}