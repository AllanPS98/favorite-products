from typing import Dict, Optional
from sqlalchemy.orm import Session
from src.model.customer import Customer
from src.configurations import Configurations

configurations = Configurations()

class CustomerDatabase:

    def __init__(self, database_session: Session):
        self.database_session = database_session
    
    def insert(self, customer_model: Customer):
        with self.database_session as session:
            session.add(customer_model)
            session.commit()
    
    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        with self.database_session as session:
            customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
            return customer
    
    def get_by_email(self, email: str) -> Optional[Customer]:
        with self.database_session as session:
            customer = session.query(Customer).filter(Customer.email == email).first()
            return customer
    
    def update(self, customer_id: str, customer_data: Dict):
        with self.database_session as session:
            session.query(Customer).filter(Customer.customer_id == customer_id).update(customer_data)
            session.commit()
    
    def delete(self, customer_id: str):
        with self.database_session as session:
            session.query(Customer).filter(Customer.customer_id == customer_id).delete()
            session.commit()
    
    def delete_all_customers(self):
        if configurations.MODE:
            with self.database_session as session:
                session.query(Customer).delete()
                session.commit()