from typing import List, Tuple
from uuid import UUID
from sqlalchemy import Row
from sqlalchemy.orm import Session
from src.model.customer import Customer
from src.model.favorite import Favorite
from src.model.product import Product


class FavoriteDatabase:
 
    def __init__(self, database_session: Session):
        self.database_session = database_session
    
    def set_favorite(self, favorite_data):
        with self.database_session as session:
            session.add(favorite_data)
            session.commit()

    def get_favorites_by_customer(self, customer_id: str, page: int, size: int) -> Tuple[List[Row[Tuple[UUID]]], int]:
        offset = (page - 1) * size
        with self.database_session as session:
            total = session.query(Favorite.product_id).filter(Favorite.customer_id == customer_id).count()
            favorites = session.query(
                Favorite.product_id
            ).filter(
                Favorite.customer_id == customer_id
            ).offset(offset).limit(size).all()
            return favorites, total

    def remove_favorite(self, customer_id: str, product_id: str):
        with self.database_session as session:
            session.query(Favorite).filter(
                Favorite.customer_id == customer_id,
                Favorite.product_id == product_id
            ).delete()
            session.commit()