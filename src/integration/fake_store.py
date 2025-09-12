from typing import Dict, List, Optional
from requests import Session
from loguru import logger
from src.configurations import Configurations
from src.constants import APPLICATION_JSON

configurations = Configurations()


class FakeStore:

    def __init__(self):
        self.url = configurations.FAKE_STORE_URL
        self.session = Session()
        self.headers = {
            'Content-Type': APPLICATION_JSON
        }
    
    def get_products(self) -> Optional[List[Dict]]:
        try:
            response_data = None
            with self.session as client:
                response = client.get(f"{self.url}/products", headers=self.headers)
                response.raise_for_status()
                response_data = response.json()
            return response_data
        except Exception as e:
            logger.exception(f"Error fetching products: {e}")
            return None

    def get_product_by_api_id(self, product_api_id) -> Optional[Dict]:
        try:
            response_data = None
            with self.session as client:
                response = client.get(f"{self.url}/products/{product_api_id}", headers=self.headers)
                response.raise_for_status()
                response_data = response.json()
            return response_data
        except Exception as e:
            logger.exception(f"Error fetching product by API ID {product_api_id}: {e}")
            return None