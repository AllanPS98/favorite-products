import uvicorn
from src.configurations import Configurations

configurations = Configurations()

def run():
    uvicorn.run("app:app", host=configurations.APP_HOST, port=configurations.APP_PORT, limit_concurrency=4)

if __name__ == "__main__":
    run()