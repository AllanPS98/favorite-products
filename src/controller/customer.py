from typing import Dict
from fastapi import Response
from loguru import logger
from http import HTTPStatus

from src.common.functions import get_uuid, check_email
from src.database.database import Database
from src.model.customer import Customer
from src.schema.customer import CreateCustomerErrorResponse, CreateCustomerInvalidEmailResponse, CreateCustomerSuccessResponse, DeleteCustomerErrorResponse, DeleteCustomerNotFoundResponse, DeleteCustomerSuccessResponse, GetCustomerErrorResponse, GetCustomerNotFoundResponse, PostCustomerPayload, UpdateCustomerErrorResponse, UpdateCustomerNotFoundResponse, UpdateCustomerSuccessResponse
from src.schema.customer import GetCustomerResponse
from src.schema.customer import PutCustomerPayload
from src.schema.exceptions import InvalidEmailError
from src.constants import APPLICATION_JSON


class CustomerController:
    
    def __init__(self):
        pass

    @property
    def __database(self) -> Database:
        return Database()
    
    @staticmethod
    def __validate_email(email: str) -> str | InvalidEmailError:
        normalized_email = check_email(email)
        if not normalized_email:
            raise InvalidEmailError("Invalid email")
        return normalized_email
    
    def __insert_customer(self, customer_data: PostCustomerPayload, normalized_email: str) -> CreateCustomerSuccessResponse:
        customer_model = Customer(
            customer_id= get_uuid(),
            name=customer_data.name,
            email=normalized_email
        )
        self.__database.customers.insert(customer_model)
        success = CreateCustomerSuccessResponse(customer_id=str(customer_model.customer_id))
        logger.info(success.message)
        return success
    
    def create_customer(self, customer_data: PostCustomerPayload) -> Response:
        try:
            normalized_email = self.__validate_email(customer_data.email)
            success = self.__insert_customer(customer_data, normalized_email)
            response = Response(content=success.model_dump_json(), media_type=APPLICATION_JSON, status_code=HTTPStatus.CREATED)
        except InvalidEmailError as invalid_email_error:
            error = CreateCustomerInvalidEmailResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.BAD_REQUEST)
            logger.exception(f"Email validation failed: {invalid_email_error}")
        except Exception as e:
            error = CreateCustomerErrorResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.exception(f"Failed to create customer: {e}")
        finally:
            return response

    def get_customer(self, customer_id: str) -> Response:
        try:
            error = GetCustomerNotFoundResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.NOT_FOUND)
            customer = self.__database.customers.get_by_id(customer_id)
            if customer:
                result = GetCustomerResponse(**customer.get())
                response = Response(content=result.model_dump_json(), media_type=APPLICATION_JSON, status_code=HTTPStatus.OK)
                logger.info("Customer retrieved successfully")
        except Exception as e:
            error = GetCustomerErrorResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.exception(f"Failed to retrieve customer: {e}")
        finally:
            return response

    def update_customer(self, customer_id: str, customer_data: PutCustomerPayload) -> Response:
        try:
            error = UpdateCustomerNotFoundResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.NOT_FOUND)
            existing_customer = self.__database.customers.get_by_id(customer_id)
            if existing_customer:
                self.__database.customers.update(customer_id, customer_data.model_dump(exclude_unset=True))
                success = UpdateCustomerSuccessResponse().model_dump_json()
                response = Response(content=success, media_type=APPLICATION_JSON, status_code=HTTPStatus.OK)
                logger.info("Customer updated successfully")
        except Exception as e:
            error = UpdateCustomerErrorResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.exception(f"Failed to update customer: {e}")
        finally:
            return response

    def delete_customer(self, customer_id: str) -> Response:
        try:
            error = DeleteCustomerNotFoundResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.NOT_FOUND)
            existing_customer = self.__database.customers.get_by_id(customer_id)
            if existing_customer:
                self.__database.customers.delete(customer_id)
                success = DeleteCustomerSuccessResponse().model_dump_json()
                response = Response(content=success, media_type=APPLICATION_JSON, status_code=HTTPStatus.OK)
                logger.info("Customer deleted successfully")
        except Exception as e:
            error = DeleteCustomerErrorResponse().model_dump_json()
            response = Response(content=error, media_type=APPLICATION_JSON, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
            logger.exception(f"Failed to delete customer: {e}")
        finally:    
            return response