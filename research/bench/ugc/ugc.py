from dataclasses import dataclass


@dataclass
class UGCSettings:
    MESSAGES_BATCH_SIZE = 1000000
    BATCHES = 10

    USER_COUNT = 10
    MOVIE_COUNT = 10
    MOVIE_MAX_LEN = 18

    OBJECTS_MAX_LIM = 1000

    storages = []




ucg_config = UGCSettings()


