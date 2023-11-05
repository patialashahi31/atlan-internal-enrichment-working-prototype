from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    api_version=(0, 11, 5),
)

while True:
    metadata_update = {"entity_id": 1, "new_value": "Updated Value"}
    producer.send("metadata_updates", value=metadata_update)
    print(f"Produced Metadata Update: {metadata_update}")
    time.sleep(5)
