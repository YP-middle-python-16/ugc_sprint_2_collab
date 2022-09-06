import os


MESSAGES_BATCH_SIZE = 10000
BATCHES = 10

API_TOPIC = "events_topic"

API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = os.environ.get("API_PORT", "8000")

SLEEP_PAUSE = 0.5
