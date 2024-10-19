plugins {
    kotlin("jvm") version "2.0.20"
}

group = "com.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

kotlin {
    jvmToolchain(17)
}

val kafkaVersion = "3.8.0"

dependencies {
    implementation("org.apache.kafka:kafka-clients:$kafkaVersion")
}