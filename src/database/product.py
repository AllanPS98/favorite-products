from typing import Dict, List, Tuple
from sqlalchemy.orm import Session

from src.model.favorite import Favorite
from src.model.product import Product


class ProductDatabase:
    def __init__(self, database_session: Session):
        self.database_session = database_session
    
    def insert(self, product_data):
        with self.database_session as session:
            self.database_session.add(product_data)
            self.database_session.commit()
    
    def insert_all(self, products_data: List[Dict]):
        with self.database_session as session:
            session.bulk_insert_mappings(Product, products_data)
            session.commit()

    def get_all_products(self, page: int = 1, size: int = 10) -> Tuple[List[Product], int]:
        offset = (page - 1) * size
        with self.database_session as session:
            total = session.query(Product).count()
            products = session.query(Product).offset(offset).limit(size).all()
            return products, total

    def get_product(self, product_id: str):
        with self.database_session as session:
            product = session.query(Product).filter(Product.product_id == product_id).first()
            return product

    def get_products_by_customer(self, customer_id: str):
        with self.database_session as session:
            products = (
                session.query(Product)
                .join(Favorite, Favorite.product_id == Product.product_id)
                .filter(Favorite.customer_id == customer_id)
                .all()
            )
            return products

    def get_product_by_api_id(self, product_api_id: int):
        with self.database_session as session:
            product = session.query(Product).filter(Product.product_api_id == product_api_id).first()
            return product
    
    def update(self, product_id: str, update_data: dict):
        with self.database_session as session:
            session.query(Product).filter(Product.product_id == product_id).update(update_data)
            session.commit()
    
    def update_all(self, products_data: List[Dict]):
        with self.database_session as session:
            session.bulk_update_mappings(Product, products_data)
            session.commit()