from fastapi import APIRouter
from src.controller.customer import CustomerController
from src.schema.customer import PostCustomerPayload
from src.schema.customer import GetCustomerResponse
from src.schema.customer import PutCustomerPayload

router = APIRouter(prefix="/customers")

#TODO: improve swagger documentation
@router.post(
    "",
    status_code=201,
    summary="Create a new customer",
    responses={201: {"description": "Customer created successfully"}}
)
def create_customer(payload: PostCustomerPayload):
    controller = CustomerController()
    response_data = controller.create_customer(payload)
    return response_data

@router.get(
    "/{customer_id}",
    status_code=200,
    summary="Get customer by ID",
    responses={200: {"description": "Customer details", "model": GetCustomerResponse}}
)
def get_customer(customer_id: str):
    controller = CustomerController()
    response_data = controller.get_customer(customer_id)
    return response_data

@router.put(
    "/{customer_id}",
    status_code=200,
    summary="Update customer details",
    responses={200: {"description": "Customer updated successfully"}}
)
def update_customer(customer_id: str, customer_data: PutCustomerPayload):
    controller = CustomerController()
    response_data = controller.update_customer(customer_id, customer_data)
    return response_data

@router.delete(
    "/{customer_id}",
    status_code=200,
    summary="Delete a customer",
    responses={200: {"description": "Customer deleted successfully"}}
)
def delete_customer(customer_id: str):
    controller = CustomerController()
    response_data = controller.delete_customer(customer_id)
    return response_data