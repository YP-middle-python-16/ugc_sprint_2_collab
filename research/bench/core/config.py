import os

MESSAGES_BATCH_SIZE = 1000000
BATCHES = 10

USER_COUNT = 200
MOVIE_COUNT = 400
MOVIE_MAX_LEN = 180

KAFKA_TOPIC = 'views'
KAFKA_CONNECT = ['localhost:9092']

CLICKHOUSE_CONNECT = 'localhost'

MONGODB_CONNECT = 'mongodb://root:example@localhost/'


PG_DLS_1 = {'dbname': os.environ.get('DB_NAME'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'host': os.environ.get('DB_HOST', '127.0.0.1'),
            'port': os.environ.get('DB_PORT', 5432)
            }

PG_DLS = {'dbname': os.environ.get('DB_NAME', 'movies_database'),
          'user': os.environ.get('DB_USER', 'app'),
          'password': os.environ.get('DB_PASSWORD', '123qwe'),
          'host': os.environ.get('DB_HOST', '0.0.0.0'),
          'port': os.environ.get('DB_PORT', 5432)
          }
