import logging
import paho.mqtt.client as mqtt
from app.entities.processed_agent_data import ProcessedAgentData
from config import MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_TOPIC
from app.interfaces.hub_gateway import HubGateway


class HubMqttAdapter(HubGateway):
    """
    MQTT-based implementation of the HubGateway interface.
    """

    def __init__(self, broker: str, port: int, topic: str):
        """
        Initializes the HubMqttAdapter with MQTT broker details.

        Parameters:
        broker (str): The MQTT broker hostname.
        port (int): The port number to connect to the MQTT broker.
        topic (str): The topic to subscribe to or publish to.
        """
        self.broker = broker
        self.port = port
        self.topic = topic

        self.client = mqtt.Client()

        # Set up MQTT event handlers
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        logging.info(f"Connecting to MQTT broker {self.broker}:{self.port}")
        self.client.connect(self.broker, self.port)

    def on_connect(self, client, userdata, flags, rc):
        """
        Handle connection to MQTT broker.
        """
        if rc == 0:
            logging.info("Connected to MQTT broker")
            client.subscribe(self.topic)
        else:
            logging.error(f"Failed to connect to MQTT broker with code: {rc}")

    def on_publish(self, client, userdata, mid):
        """
        Handle successful message publish.
        """
        logging.info(f"Message {mid} successfully published to the broker.")

    def save_data(self, processed_data: ProcessedAgentData) -> bool:
        """
        Publishes the processed agent data to the store via MQTT.
        """
        try:
            payload = processed_data.model_dump_json()
            result = self.client.publish(self.topic, payload)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.info("Data successfully published to MQTT broker.")
                return True
            else:
                logging.error(
                    f"Failed to publish data to MQTT broker. Return code: {result.rc}"
                )
                return False
        except Exception as e:
            logging.error(f"Error while publishing data via MQTT: {e}")
            return False

    def start(self):
        """
        Starts the MQTT loop to listen for messages.
        """
        logging.info("Starting MQTT client loop...")
        self.client.loop_start()

    def stop(self):
        """
        Stops the MQTT loop and disconnects from the broker.
        """
        logging.info("Stopping MQTT client loop...")
        self.client.loop_stop()
        self.client.disconnect()
