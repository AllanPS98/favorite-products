class InvalidEmailError(Exception):
    """Exception raised for invalid email addresses."""
    pass

class DuplicateEmailError(Exception):
    """Exception raised when trying to create a customer with an email that already exists."""
    pass

class SetFavoriteCustomerNotFoundError(Exception):
    """Exception raised when a customer is not found in set favorite method."""
    pass

class SetFavoriteProductNotFoundError(Exception):
    """Exception raised when a product is not found in set favorite method."""
    pass

class RemoveFavoriteNotFoundError(Exception):
    """Exception raised when a favorite is not found in remove favorite method."""
    pass

class DuplicateFavoriteProductError(Exception):
    """Exception raised when trying to add a duplicate favorite product for a customer."""
    pass