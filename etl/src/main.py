import time
from contextlib import closing

from config import settings
from services.clickhouse_loader import ClickHouseLoader
from services.data_transformer import DataTransformer
from services.kafka_extractor import KafkaExtractor
from utils import backoff


@backoff()
def run():
    with closing(
        ClickHouseLoader(
            host=settings.clickhouse_host,
            database=settings.clickhouse_database,
            cluster=settings.clickhouse_cluster,
            batch_size=settings.etl_batch_size,
        )
    ) as clickhouse, closing(
        KafkaExtractor(
            bootstrap_servers=settings.kafka_brokers,
            topic_list=settings.kafka_topics,
            group_id=settings.kafka_group_id,
            batch_size=settings.etl_batch_size,
        )
    ) as kafka:
        # subscribe to topic
        kafka.subscribe()
        # init database
        clickhouse.create_database()
        input_data_gen = kafka.list_messages()
        if input_data_gen:
            transformed = DataTransformer.get_aggregate_topic_data(input_data_gen)
            clickhouse.load(data=transformed)


@backoff()
def wait_for_services():
    with closing(
        ClickHouseLoader(
            host=settings.clickhouse_host,
            database=settings.clickhouse_database,
            cluster=settings.clickhouse_cluster,
            batch_size=settings.etl_batch_size,
        )
    ) as clickhouse, closing(
        KafkaExtractor(
            bootstrap_servers=settings.kafka_brokers,
            topic_list=settings.kafka_topics,
            group_id=settings.kafka_group_id,
            batch_size=settings.etl_batch_size,
        )
    ) as kafka:
        # clickhouse
        clickhouse.client.execute("SHOW DATABASES")

        # kafka
        kafka.consumer.subscription()


if __name__ == "__main__":
    wait_for_services()
    while True:
        run()
        time.sleep(settings.etl_pause_duration)
