import tensorflow as tf
import kafka
import json

# Load model
model = tf.keras.models.load_model("content_recommendation_model.h5")

# Kafka configuration
kafka_brokers = "localhost:9092"
kafka_topic = "recommendations"

producer = kafka.KafkaProducer(bootstrap_servers=kafka_brokers)

def recommend(content_features):
    prediction = model.predict(content_features)
    return prediction

# Kafka consumer
consumer = kafka.KafkaConsumer('user_behavior', bootstrap_servers=kafka_brokers)

for message in consumer:
    content_features = json.loads(message.value)
    recommendations = recommend(content_features)
    producer.send(kafka_topic, value=json.dumps(recommendations).encode('utf-8'))
