from .....cores.implement.egress import Core
from typing import Any, Iterable, NoReturn, Union

from confluent_kafka.admin import AdminClient, NewTopic, KafkaException, KafkaError
from confluent_kafka import Producer

from logging import Logger
from attrs import define, field

@define(kw_only=True)
class KafkaEgressCore(Core):
    # Core Configs
    input: Union[Iterable, Any] = field(default=None)
    heartbeat: int = field(default=1)
    forgiving: bool = field(default=False)
    backpressure: int = field(default=0)
    on_error: callable = field(default=None)
    logger:Logger = field(default=None)
    
    # Record Configs
    topic_name: str = field(init=True)
    message_key: str = field(default=None)
    message_headers: dict = field(default=None)

    # Kafka Server Configs 
    bootstrap_servers:str = field(default=None)
    client_id:str = field(default='')
    
    # Kafka Topic Configs
    partitions:int = field(default=1)
    replication:int = field(default=1)
    retention_ms: int = field(default=None)
    max_message_bytes: int = field(default=None)
    ensure_topic: bool = True
    overwrite_topic: bool = False
    
    __ensured = False
    
    def __call__(self, input:Union[Iterable, Any]) -> Any:
        self.input = input
        return self
    
    def ensure_kafka_topic(self):
        
        if self.__ensured:
            return
        
        self.__ensured = True
        
        # Ensure Topic
        new_topic = NewTopic(
            self.topic_name, 
            self.partitions, 
            self.replication, 
            config = {
                'retention.ms' : self.retention_ms,
                'max.message.bytes' : self.max_message_bytes,
            }
        )
        # Create the topic
        self.admin_client.create_topics([new_topic])
    
    def constructor(self) -> NoReturn:
        kafka_config = {
            "bootstrap.servers": self.bootstrap_servers,
            "client.id": self.client_id
        }
        self.admin_client = AdminClient(kafka_config)
        
        try:
            if self.overwrite_topic:
                self.delete_topic(self.topic_name)
                self.logger.debug(f"Cleared Topic: {self.topic_name}")
                self.ensure_kafka_topic()
            
            if self.ensure_topic:
                self.ensure_kafka_topic()
        
        except KafkaException as e:
            self.logger.error(f"Kafka exception occurred: {e}")
        
        self.producer = Producer({ 
            "bootstrap.servers": self.bootstrap_servers, 
            "client.id": self.client_id, 
            "queue.buffering.max.messages": 50_000_000, 
            "queue.buffering.max.kbytes": 1048576, 
            'queue.buffering.max.ms': 1000, 
            'acks': 'all', 
            'retries': 5,
            'linger.ms': 5
        })
        self.total_loaded = 0
        self.total_length = 0
    
    def delete_topic(self, topic_name: str) -> None:
        fs = self.admin_client.delete_topics([topic_name])
        for topic, f in fs.items():
            try:
                f.result()  # Block until the topic is deleted
                self.logger.debug(f"Topic {topic_name} deletion completed.")
            except KafkaException as e:
                self.logger.error(f"Failed to delete topic {topic_name}: {e}")
    
    def ensure_kafka_topic(self) -> None:
        new_topic = NewTopic(
            self.topic_name, 
            self.partitions, 
            self.replication, 
            config = {
                'retention.ms' : self.retention_ms,
                'max.message.bytes' : self.max_message_bytes,
            }
        )
        fs = self.admin_client.create_topics([new_topic])
        for topic, f in fs.items():
            try:
                f.result()  # Block until the topic is created
                self.logger.debug(f"Topic {self.topic_name} creation completed.")
            except KafkaException as e:
                if e.args[0].code() != KafkaError.TOPIC_ALREADY_EXISTS:
                    self.logger.error(f"Failed to create topic {self.topic_name}: {e}")
                else:
                    self.logger.debug(f"Topic {self.topic_name} already exists.")
        
    def destructor(self, exc_type, exc_value, traceback) -> NoReturn:
        if self.logger:
            self.logger.info(f"Produced {self.total_loaded} messages ({self.total_length} bytes) into topic: '{self.topic_name}'.")
        
        self.producer.flush()
            
    def pulse(self) -> NoReturn:
        self.producer.flush()
    
    def callback(self, record: Any, exception: Exception) -> NoReturn:
        if exception != None:
            if self.on_error != None:
                self.on_error(record, exception)
        else:
            if hasattr(record, '__len__'):
                self.total_length += len(record)
            
            self.total_loaded += 1
        
    def consume(self, record: Any) -> NoReturn:
        self.producer.produce(
            self.topic_name, 
            key = self.message_key,
            value=record)
        
