from src.database import get_database_session
from src.database.customer import CustomerDatabase
from src.database.favorite import FavoriteDatabase
from src.database.product import ProductDatabase


class Database:

    def __init__(self):
        self.database_session = get_database_session()
    
    @property
    def customers(self) -> CustomerDatabase:
        return CustomerDatabase(self.database_session)
    
    @property
    def favorites(self) -> FavoriteDatabase:
        return FavoriteDatabase(self.database_session)
    
    @property
    def products(self) -> ProductDatabase:
        return ProductDatabase(self.database_session)