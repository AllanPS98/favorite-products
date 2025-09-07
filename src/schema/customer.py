from pydantic import BaseModel


class PostCustomerPayload(BaseModel):
    name: str
    email: str

class GetCustomerResponse(BaseModel):
    customer_id: str
    name: str
    email: str

class PutCustomerPayload(BaseModel):
    name: str
    email: str