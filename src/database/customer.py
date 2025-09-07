from typing import Dict, Optional
from sqlalchemy.orm import Session
from src.model.customer import Customer


class CustomerDatabase:

    def __init__(self, database_session: Session):
        self.database_session = database_session
    
    def insert(self, customer_model: Customer):
        with self.database_session.begin():
            self.database_session.add(customer_model)
            self.database_session.commit()
    
    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        with self.database_session.begin():
            customer = self.database_session.query(Customer).filter(Customer.customer_id == customer_id).first()
            return customer
    
    def update(self, customer_id: str, customer_data: Dict):
        with self.database_session.begin():
            self.database_session.query(Customer).filter(Customer.customer_id == customer_id).update(customer_data)
            self.database_session.commit()
    
    def delete(self, customer_id: str):
        with self.database_session.begin():
            self.database_session.query(Customer).filter(Customer.customer_id == customer_id).delete()
            self.database_session.commit()