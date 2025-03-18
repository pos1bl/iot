import json
import logging
from typing import List
import pydantic_core
import requests
from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_api_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        logging.info(f"Saving {processed_agent_data_batch} to {self.api_base_url}")
        url = f"{self.api_base_url}/processed_agent_data/"  # Adjust the endpoint accordingly
        data = [
            agent_data.model_dump(mode="json")
            for agent_data in processed_agent_data_batch
        ]
        for item in data:
            response = requests.post(url, json=item)
            if response.status_code != 200:
                raise Exception(
                    f"Failed to save data: {response.status_code}, {response.text}"
                )

        return response.json()
