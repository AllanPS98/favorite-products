from fastapi import APIRouter
from src.controller.customer import CustomerController
from src.schema.customer import CreateCustomerErrorResponse, CreateCustomerInvalidEmailResponse, CreateCustomerSuccessResponse, DeleteCustomerErrorResponse, DeleteCustomerNotFoundResponse, DeleteCustomerSuccessResponse, GetCustomerErrorResponse, GetCustomerNotFoundResponse, PostCustomerPayload, UpdateCustomerErrorResponse, UpdateCustomerNotFoundResponse, UpdateCustomerSuccessResponse
from src.schema.customer import GetCustomerResponse
from src.schema.customer import PutCustomerPayload

router = APIRouter(prefix="/customers")

@router.post(
    "",
    status_code=201,
    summary="Create a new customer",
    responses={
        201: {
            "description": "Customer created successfully", 
            "model": CreateCustomerSuccessResponse
        },
        400: {
            "description": "Invalid email",
            "model": CreateCustomerInvalidEmailResponse
        },
        500: {
            "description": "Failed to create customer",
            "model": CreateCustomerErrorResponse
        }
    }
)
def create_customer(payload: PostCustomerPayload):
    controller = CustomerController()
    response_data = controller.create_customer(payload)
    return response_data

#TODO: ADICIONAR ENDPOINT PARA BUSCAR CLIENTE POR EMAIL
@router.get(
    "/{customer_id}",
    status_code=200,
    summary="Get customer by ID",
    responses={
        200: {
            "description": "Customer details",
            "model": GetCustomerResponse
        },
        404: {
            "description": "Customer not found",
            "model": GetCustomerNotFoundResponse
        },
        500: {
            "description": "Failed to retrieve customer",
            "model": GetCustomerErrorResponse
        }
    }
)
def get_customer(customer_id: str):
    controller = CustomerController()
    response_data = controller.get_customer(customer_id)
    return response_data

@router.put(
    "/{customer_id}",
    status_code=200,
    summary="Update customer details",
    responses={
        200: {
            "description": "Customer updated successfully",
            "model": UpdateCustomerSuccessResponse
        },
        404: {
            "description": "Customer not found",
            "model": UpdateCustomerNotFoundResponse
        },
        500: {
            "description": "Failed to update customer",
            "model": UpdateCustomerErrorResponse
        }
    }
)
def update_customer(customer_id: str, customer_data: PutCustomerPayload):
    controller = CustomerController()
    response_data = controller.update_customer(customer_id, customer_data)
    return response_data

@router.delete(
    "/{customer_id}",
    status_code=200,
    summary="Delete a customer",
    responses={
        200: {
            "description": "Customer deleted successfully",
            "model": DeleteCustomerSuccessResponse
        },
        404: {
            "description": "Customer not found",
            "model": DeleteCustomerNotFoundResponse
        },
        500: {
            "description": "Failed to delete customer",
            "model": DeleteCustomerErrorResponse
        }
    }
)
def delete_customer(customer_id: str):
    controller = CustomerController()
    response_data = controller.delete_customer(customer_id)
    return response_data