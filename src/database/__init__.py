from src.model.configurations import get_session

def get_database_session():
    with get_session() as session:
        return session