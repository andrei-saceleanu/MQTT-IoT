"""MQTT adaptor"""
import json
import logging
from os import getenv
from json import loads
from datetime import datetime
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


db_client = InfluxDBClient(
    url="http://tema3_db:8086",
    org=getenv("DB_ORG"),
    token=getenv("DB_TOKEN")
)
write_api = db_client.write_api(write_options=SYNCHRONOUS)
QOS = 2
LOGGING_LEVEL = logging.INFO


def set_logger(level=logging.INFO):
    """Set logger function"""
    logger = logging.getLogger()
    logger.setLevel(level)

    if len(logger.handlers) == 0:
        handler = logging.StreamHandler()
        handler.setLevel(level)

        logger.propagate = 0
        formatter = logging.Formatter(
            "%(asctime)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger

logger = set_logger()
env_var = getenv("DEBUG_DATA_FLOW")
if env_var is None or env_var != "true":
    logger.disabled = True

def _on_connect(client, args, flags, rc):
    """connect and subscribe to all topics"""
    client.subscribe("#", QOS)

def _on_message(client, args, msg):
    """handle new message"""

    logger.info("Received a message by topic %s", msg.topic)
    decoded_str = msg.payload.decode('utf-8').rstrip()
    location, station = msg.topic.split("/")

    try:
        data = loads(decoded_str)
        points = []

        timestamp = None
        if "timestamp" not in data:
            logger.info("Data timestamp is NOW")
            timestamp = datetime.now()
        else:
            logger.info("Data timestamp is %s", data["timestamp"])
            timestamp = datetime.strptime(
                data["timestamp"],
                "%Y-%m-%d %H-%M-%S%z"
            )

        for k in data:
            if isinstance(data[k], (int, float)):
                measurement = f"{location}.{station}.{k}"
                log_msg = measurement + f" {str(data[k])}"
                logger.info(log_msg)
                point = (
                    Point(measurement)
                    .tag("station", station)
                    .field("value", data[k])
                    .time(timestamp)
                )
                points.append(point)

        write_api.write(
            bucket=getenv("DB_NAME"),
            org=getenv("DB_ORG"),
            record=points
        )

    except json.decoder.JSONDecodeError as err:
        logger.error(err.msg)


def create_client():
    """create client handle"""
    client = mqtt.Client("msg_adaptor")
    client.on_connect = _on_connect
    client.on_message = _on_message

    client.connect("tema3_broker")
    client.loop_forever()

    return client


def close_client(client):
    """close client"""
    client.disconnect()
    client.loop_stop()


def main():
    """main function"""
    client = create_client()
    close_client(client)

if __name__ == "__main__":
    main()
