from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.common.auth import admin_required, normal_user_required
from src.controller.customer import CustomerController
from src.schema.customer import CreateCustomerErrorResponse, CustomerInvalidEmailResponse, CreateCustomerSuccessResponse, DeleteCustomerErrorResponse, DeleteCustomerNotFoundResponse, DeleteCustomerSuccessResponse, GetCustomerErrorResponse, GetCustomerNotFoundResponse, PostCustomerPayload, UpdateCustomerErrorResponse, UpdateCustomerNotFoundResponse, UpdateCustomerSuccessResponse
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
            "model": CustomerInvalidEmailResponse
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

@router.post(
    "/login",
    status_code=200,
    summary="Authenticate a customer",
    responses={
        200: {
            "description": "Customer authenticated successfully"
        }
    }
)
def login(form: OAuth2PasswordRequestForm = Depends()):
    controller = CustomerController()
    response_data = controller.authenticate_customer(form.username, form.password)
    return response_data

@router.put(
    "/to-admin",
    status_code=200,
    summary="Update customer to admin",
    responses={
        200: {
            "description": "Customer updated to admin successfully", 
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
def update_to_admin(customer_email: str, user = Depends(admin_required)):
    controller = CustomerController()
    response_data = controller.update_to_admin(customer_email)
    return response_data

@router.get(
    "/id/{customer_id}",
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
def get_customer(customer_id: str, user = Depends(admin_required)):
    controller = CustomerController()
    response_data = controller.get_customer(customer_id)
    return response_data

@router.get(
    "/by-email",
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
def get_customer_by_email(customer_email: str, user = Depends(normal_user_required)):
    controller = CustomerController()
    response_data = controller.get_customer_by_email(customer_email)
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
def update_customer(customer_id: str, customer_data: PutCustomerPayload, user = Depends(normal_user_required)):
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
def delete_customer(customer_id: str, user = Depends(admin_required)):
    controller = CustomerController()
    response_data = controller.delete_customer(customer_id)
    return response_data