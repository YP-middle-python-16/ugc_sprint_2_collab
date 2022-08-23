from clickhouse_driver import Client

client = Client(host='localhost')
client.execute('CREATE DATABASE IF NOT EXISTS movies_statistics ON CLUSTER company_cluster')

new_table_sql = 'CREATE TABLE movies_statistics.view_stat ON CLUSTER company_cluster (' \
                'movie_id FixedString(36), ' \
                'user_id FixedString(36), ' \
                'eventTime DateTime,' \
                'view_run_time Int64) ' \
                'Engine=MergeTree() ' \
                'ORDER BY movie_id'

client.execute(new_table_sql)
