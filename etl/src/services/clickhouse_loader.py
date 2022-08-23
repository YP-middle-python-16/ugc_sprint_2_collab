from clickhouse_driver import Client

from config import settings


class ClickHouseLoader:
    def __init__(self,
                 host: str,
                 database: str,
                 batch_size: int = 500,
                 cluster: str = 'company_cluster'):
        self._host = host
        self._database = database
        self._batch_size = batch_size
        self._cluster = cluster
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = Client(host=self._host)

        return self._client

    def load(self, data: dict):
        """
        Метод загружает данные в таблицу
        :param data: словарь данных
        """
        # create table if not exists
        self.create_tables()
        for table_name, data_list in data.items():
            # load data
            self.client.execute(
                f'INSERT INTO {self._database}.{table_name} VALUES',
                data_list,
            )

    def create_database(self):
        """
        Создаем БД, если она отсутствует
        """
        self.client.execute(f'CREATE DATABASE IF NOT EXISTS {self._database} ON CLUSTER {self._cluster}')

    def create_tables(self):
        """
        Создаем таблицы, если она отсутствует, новые таблицы добавляем сюда же
        """
        self.client.execute(f'CREATE TABLE IF NOT EXISTS {self._database}.{settings.clickhouse_film_view_table} '
                            f'ON CLUSTER {self._cluster} '
                            '(user_id String, movie_id String, event_time DateTime, view_second Int32) '
                            'Engine=MergeTree() ORDER BY user_id')

    def close(self):
        self.client.disconnect()
        self._client = None
