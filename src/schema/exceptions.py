class InvalidEmailError(Exception):
    """Exception raised for invalid email addresses."""
    pass

class SetFavoriteCustomerNotFoundError(Exception):
    """Exception raised when a customer is not found in set favorite method."""
    pass

class SetFavoriteProductNotFoundError(Exception):
    """Exception raised when a product is not found in set favorite method."""
    pass