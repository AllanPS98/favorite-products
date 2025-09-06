import uuid
from src.configurations import Configurations
import pytz

config_app = Configurations()

def timezone_br():
    return pytz.timezone(config_app.TIMEZONE)

def get_uuid():
    return uuid.uuid4()