import os


def try_parse_int(value: str):
    try:
        return int(value)
    except Exception:
        return None


def try_parse(type, value: str):
    try:
        return type(value)
    except Exception:
        return None


# Configuration for the Store API
STORE_API_HOST = os.environ.get("STORE_API_HOST") or "localhost"
STORE_API_PORT = try_parse_int(os.environ.get("STORE_API_PORT")) or 8000
STORE_API_BASE_URL = f"http://{STORE_API_HOST}:{STORE_API_PORT}"
# Configure for Redis
REDIS_HOST = os.environ.get("REDIS_HOST") or "localhost"
REDIS_PORT = try_parse_int(os.environ.get("REDIS_PORT")) or 6379
# Configure for hub logic
BATCH_SIZE = try_parse_int(os.environ.get("BATCH_SIZE")) or 5
# MQTT
MQTT_BROKER_HOST = os.environ.get("MQTT_BROKER_HOST") or "localhost"
MQTT_BROKER_PORT = try_parse_int(os.environ.get("MQTT_BROKER_PORT")) or 1883
MQTT_TOPIC = os.environ.get("MQTT_TOPIC") or "agent_data_topic"

POSTGRES_HOST = os.environ.get("POSTGRES_HOST") or "localhost"
POSTGRES_PORT = try_parse(int, os.environ.get("POSTGRES_PORT")) or 5432
POSTGRES_USER = os.environ.get("POSTGRES_USER") or "user"
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASS") or "pass"
POSTGRES_DB = os.environ.get("POSTGRES_DB") or "test_db"
