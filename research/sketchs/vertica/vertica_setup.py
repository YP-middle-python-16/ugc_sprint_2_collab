import vertica_python
from config import connection_info

with vertica_python.connect(**connection_info) as connection:  # 1
    cursor = connection.cursor()  # 2
    cursor.execute("""  # 3
    CREATE TABLE views (
        id IDENTITY,
        user_id VARCHAR(36) NOT NULL,
        movie_id VARCHAR(36) NOT NULL,
        event_date DATETIME NOT NULL,
        viewed_frame INTEGER NOT NULL
    );
    """)