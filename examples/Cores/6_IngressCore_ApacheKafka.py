from confluent_kafka import Consumer, KafkaException, KafkaError
import json

# Configure the Consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'new-group-sdas23as23dsdasdaasdfssaddsa2',             # Consumer group id
    'auto.offset.reset': 'earliest',    # Start from the earliest message
    'enable.auto.commit': True         # Disable automatic offset committing
})

# Subscribe to a topic
consumer.subscribe(['target-data-topic'])

try:
    print(f"---------------------------------------------------------------")
    print(f"| Timestamp \t| Partition, Offset \t| 'Key', \t'Value'")
    print(f"---------------------------------------------------------------")
    while True:
        # Poll for messages
        msg = consumer.poll(0.3)  # Timeout in seconds

        if msg is None:
            continue
        
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print(f"Reached end of partition {msg.partition()} at offset {msg.offset()}")
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            # Successful message
            tstamp = msg.timestamp()[1]
            msg_val = msg.value().decode('utf-8')
            msg_key = msg.key().decode('utf-8')
            offset = msg.offset()
            partition = msg.partition()
            print(f"| {tstamp} \t| {partition}, {offset}\t\t\t| '{msg_key}', '{msg_val}'")



except KeyboardInterrupt:
    pass
finally:
    # Close the consumer
    consumer.close()