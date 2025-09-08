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

class CreateCustomerSuccessResponse(BaseModel):
    message: str = "Customer created successfully"
    customer_id: str = "uuid"

class CreateCustomerErrorResponse(BaseModel):
    error: str = "Failed to create customer"

class CreateCustomerInvalidEmailResponse(BaseModel):
    error: str = "Invalid email"

class GetCustomerNotFoundResponse(BaseModel):
    error: str = "Customer not found"

class GetCustomerErrorResponse(BaseModel):
    error: str = "Failed to retrieve customer"

class UpdateCustomerSuccessResponse(BaseModel):
    message: str = "Customer updated successfully"

class UpdateCustomerNotFoundResponse(BaseModel):
    error: str = "Customer not found"

class UpdateCustomerErrorResponse(BaseModel):
    error: str = "Failed to update customer"

class DeleteCustomerSuccessResponse(BaseModel):
    message: str = "Customer deleted successfully"

class DeleteCustomerNotFoundResponse(BaseModel):
    error: str = "Customer not found"

class DeleteCustomerErrorResponse(BaseModel):
    error: str = "Failed to delete customer"