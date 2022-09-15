from clickhouse_driver import Client

client = Client(host='localhost')

client.execute('DROP DATABASE IF EXISTS movies_statistics ON CLUSTER company_cluster')

client.execute('CREATE DATABASE IF NOT EXISTS movies_statistics ON CLUSTER company_cluster')

new_table_views = 'CREATE TABLE movies_statistics.view_stat ON CLUSTER company_cluster (' \
                  'movie_id FixedString(36), ' \
                  'user_id FixedString(36), ' \
                  'eventTime DateTime,' \
                  'view_run_time Int64) ' \
                  'Engine=MergeTree() ' \
                  'ORDER BY movie_id'
try:
    client.execute(new_table_views)
except:
    pass

new_table_likes = 'CREATE TABLE movies_statistics.likes ON CLUSTER company_cluster (' \
                  'movie_id FixedString(36), ' \
                  'user_id FixedString(36)) ' \
                  'Engine=MergeTree() ' \
                  'ORDER BY movie_id'
try:
    client.execute(new_table_likes)
except:
    pass

new_table_comments = 'CREATE TABLE movies_statistics.comments ON CLUSTER company_cluster (' \
                     'movie_id FixedString(36), ' \
                     'user_id FixedString(36), ' \
                     'event_time DateTime, ' \
                     'title Text, ' \
                     'body Text, ' \
                     'score int) ' \
                     'Engine=MergeTree() ' \
                     'ORDER BY movie_id'

client.execute(new_table_comments)
