import logging
import paho.mqtt.client as mqtt
from app.entities.processed_agent_data import ProcessedAgentData
from redis import Redis
from app.interfaces.agent_gateway import AgentGateway
from config import (
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_TOPIC,
    REDIS_HOST,
    REDIS_PORT,
    BATCH_SIZE,
    STORE_API_BASE_URL,
)
from typing import List

from app.adapters.store_api_adapter import StoreApiAdapter
from app.interfaces.hub_gateway import HubGateway


class AgentMQTTAdapter:
    """
    An adapter that communicates with an MQTT broker and handles agent data.
    """

    def __init__(
        self, broker_host: str, broker_port: int, topic: str, hub_gateway: HubGateway
    ):
        """
        Initializes the AgentMQTTAdapter with MQTT configuration and a HubGateway instance.

        Parameters:
        broker_host (str): The MQTT broker host.
        broker_port (int): The MQTT broker port.
        topic (str): The topic to listen to.
        hub_gateway (HubGateway): The gateway adapter to save data.
        """
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic
        self.hub_gateway = hub_gateway

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """
        Handles the connection to the MQTT broker.
        """
        if rc == 0:
            logging.info("Connected to MQTT broker")
            client.subscribe(self.topic)
        else:
            logging.error(f"Failed to connect to MQTT broker with code: {rc}")

    def on_message(self, client, userdata, msg):
        """
        Handles incoming MQTT messages and forwards them to the HubGateway.
        """
        try:
            payload: str = msg.payload.decode("utf-8")
            processed_agent_data = ProcessedAgentData.model_validate_json(
                payload, strict=True
            )

            # Save the processed agent data via the HubGateway (MQTT-based)
            if not self.hub_gateway.save_data(processed_agent_data):
                logging.error("Failed to save processed data to hub.")
        except Exception as e:
            logging.error(f"Error processing MQTT message: {e}")

    def connect(self):
        """
        Connects to the MQTT broker.
        """
        logging.info(
            f"Connecting to MQTT broker at {self.broker_host}:{self.broker_port}"
        )
        self.client.connect(self.broker_host, self.broker_port)

    def start(self):
        """
        Starts listening to MQTT messages.
        """
        logging.info("Starting the MQTT listener for agent messages...")
        self.client.loop_start()

    def stop(self):
        """
        Stops the MQTT loop and disconnects.
        """
        logging.info("Stopping the MQTT client loop...")
        self.client.loop_stop()
        self.client.disconnect()
