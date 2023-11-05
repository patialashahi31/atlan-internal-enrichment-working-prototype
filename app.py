from flask import Flask, render_template
from kafka import KafkaConsumer
from cassandra.cluster import Cluster
import psycopg2

app = Flask(__name__)

# Set up a Kafka consumer
consumer = KafkaConsumer(
    "metadata_updates",
    bootstrap_servers="kafka:9092",
    group_id="metadata_group",
    api_version=(0, 11, 5),
)

# ... (Kafka and Cassandra setup)


@app.route("/")
def show_metadata_updates():
    # Retrieve metadata updates from Cassandra
    cassandra_cluster = Cluster(["cassandra"])
    cassandra_session = cassandra_cluster.connect()
    cassandra_session.set_keyspace("metadata")
    cassandra_rows = cassandra_session.execute(
        "SELECT entity_id, new_value FROM metadata_updates"
    )

    # Retrieve metadata updates from Postgres
    postgres_connection = psycopg2.connect(
        user="metadata_user",
        password="metadata_password",
        host="postgres",
        database="metadata",
    )
    postgres_cursor = postgres_connection.cursor()
    postgres_cursor.execute("SELECT entity_id, new_value FROM metadata_updates")
    postgres_rows = postgres_cursor.fetchall()

    return render_template(
        "metadata_updates.html",
        cassandra_rows=cassandra_rows,
        postgres_rows=postgres_rows,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
