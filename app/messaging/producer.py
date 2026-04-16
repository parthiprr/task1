import pika
import json

def publish_message(message: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq") 
    )
    channel = connection.channel()

    channel.queue_declare(queue="notifications")

    channel.basic_publish(
        exchange="",
        routing_key="notifications",
        body=json.dumps(message)
    )

    connection.close()
    
    print("🔥 MESSAGE SENT TO QUEUE")