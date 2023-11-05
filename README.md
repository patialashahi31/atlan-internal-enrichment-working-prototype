# (OUTBOUND, INTERNAL) : There are internal enrichment automation requirements towards metadata into Atlan, such that any change in the Atlan entity triggers similar changes to entities connected downstream in lineage from that entity.

We will be simulating this scenario

### producer.py will generate the metadata update which is subscribed by Kafka consumer in consumer.py. 
### We will record the updates in Cassandra DB and it will be migrated to other datastores/ entities here postgres is used. 


## Local Setup

```bash

make up

```
<img width="1021" alt="Screenshot 2023-11-05 at 9 40 47 PM" src="https://github.com/patialashahi31/atlan-internal-enrichment-working-prototype/assets/40652331/ee4ed79d-00f7-475a-b1bf-ef7a377bff81">

