from typing import Optional
import uuid
import pytz
from loguru import logger
from email_validator import validate_email, EmailNotValidError

from src.configurations import Configurations

config_app = Configurations()

def timezone_br() -> pytz.timezone:
    return pytz.timezone(config_app.TIMEZONE)

def get_uuid() -> uuid.UUID:
    return uuid.uuid4()

def mask_email(email: str) -> str:
        split_email = str(email).split("@")
        first_part = split_email[0]
        domain_part = split_email[1]
        masked_first_part = first_part[0] + ('*' * len(first_part[1:])) 
        split_domain_part = domain_part.split(".")
        masked_domain_part = ('*' * len(split_domain_part[0])) + "." + split_domain_part[1]
        return masked_first_part + "@" + masked_domain_part

def validate_email(email: str) -> Optional[str]:
    email_normalized = None
    try:
        email_info = validate_email(email)
        email_normalized = email_info.normalized
        logger.info("Valid email address")
    except EmailNotValidError as e:
        logger.exception("Invalid email address: {e}")
    finally:
        return email_normalized