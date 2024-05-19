from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework import status
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Call the default exception handler first to get the standard error response
    response = exception_handler(exc, context)
   
    # Check if the exception is a validation error
    if isinstance(exc, ValidationError) and response is not None:
        # Customize the error response format
        response_data = {
            'status': status.HTTP_422_UNPROCESSABLE_ENTITY,
            'message': 'Failed',
            'errors': response.data
        }
        response.data = response_data

    elif isinstance(exc, AuthenticationFailed):
        response_data = {
            'status': status.HTTP_401_UNAUTHORIZED,
            'message': 'Authentication failed',
            'errors':  ''
        }
        response = Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

    elif isinstance(exc, NotAuthenticated):
        response_data = {
            'status': status.HTTP_401_UNAUTHORIZED,
            'message': 'Unauthorized',
            'errors':  ''
        }
        response = Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

    elif isinstance(exc, PermissionDenied):
        response_data = {
            'status': status.HTTP_403_FORBIDDEN,
            'message': 'Permission Denied',
            'errors': 'You do not have permission to perform this action.'
        }
        response = Response(response_data, status=status.HTTP_403_FORBIDDEN)

    elif response is not None and response.status_code == 404:
        response_data = {
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'Not Found',
            'errors': 'Resource not found.'
        }
        response = Response(response_data, status=status.HTTP_404_NOT_FOUND)

    return response
