import logging
import requests
from app.entities.processed_agent_data import ProcessedAgentData
from config import STORE_API_BASE_URL
from app.interfaces.hub_gateway import HubGateway


class HubHttpAdapter(HubGateway):
    """
    HTTP-based implementation of the HubGateway interface.
    """

    def __init__(self):
        self.api_base_url = STORE_API_BASE_URL

    def save_data(self, processed_data: ProcessedAgentData) -> bool:
        """
        Sends the processed agent data to the store API over HTTP.
        """
        try:
            response = requests.post(
                f"{self.api_base_url}/save_data", json=processed_data.model_dump_json()
            )
            if response.status_code == 200:
                logging.info("Data saved successfully to the store via HTTP.")
                return True
            else:
                logging.error(
                    f"Failed to save data. Status Code: {response.status_code}"
                )
                return False
        except Exception as e:
            logging.error(f"Error while saving data via HTTP: {e}")
            return False
