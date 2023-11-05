from kafka import KafkaConsumer
from cassandra.cluster import Cluster
import psycopg2
import json
from psycopg2 import sql
from datetime import datetime

# Set up a Kafka consumer
consumer = KafkaConsumer(
    "metadata_updates",
    bootstrap_servers="kafka:9092",
    group_id="metadata_consumer_group",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    api_version=(0, 11, 5),
)

# Set up a Cassandra connection
cassandra_cluster = Cluster(["cassandra"])
cassandra_session = cassandra_cluster.connect()

# Create a keyspace and table in Cassandra
cassandra_session.execute(
    "CREATE KEYSPACE IF NOT EXISTS metadata WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1}"
)
cassandra_session.execute(
    "CREATE TABLE IF NOT EXISTS metadata.metadata_updates (entity_id int PRIMARY KEY, new_value text)"
)

# Set up a Postgres connection
postgres_connection = psycopg2.connect(
    user="metadata_user",
    password="metadata_password",
    host="postgres",
    database="metadata",
)
cursor = postgres_connection.cursor()

# Create a table in Postgres
cursor.execute(
    "CREATE TABLE IF NOT EXISTS metadata_updates (entity_id serial PRIMARY KEY, new_value text)"
)
postgres_connection.commit()

# Consume and store metadata updates
for message in consumer:
    metadata_update = message.value
    entity_id = metadata_update["entity_id"]
    new_value = metadata_update["new_value"]

    # Store in Cassandra
    cassandra_session.execute(
        "INSERT INTO metadata.metadata_updates (entity_id, new_value) VALUES (%s, %s)",
        (entity_id, new_value),
    )
    cursor.execute(
        sql.SQL("SELECT entity_id FROM metadata_updates WHERE entity_id = %s"),
        [entity_id],
    )

    existing_record = cursor.fetchone()

    if existing_record:
        # Update the existing record
        cursor.execute(
            sql.SQL("UPDATE metadata_updates SET new_value = %s WHERE entity_id = %s"),
            [new_value, entity_id],
        )
    else:
        # Insert a new record
        cursor.execute(
            sql.SQL(
                "INSERT INTO metadata_updates (entity_id, new_value) VALUES (%s, %s)"
            ),
            [entity_id, new_value],
        )

    postgres_connection.commit()

    print(
        f"Received and stored Metadata Update: Entity ID {entity_id}, New Value {new_value}"
    )

# Close connections
cassandra_session.shutdown()
cassandra_cluster.shutdown()
postgres_cursor.close()
postgres_connection.close()
