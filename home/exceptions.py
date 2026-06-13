from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler to handle multipart form parse errors gracefully.
    """
    # Check if it's a multipart parsing error
    if 'Invalid boundary in multipart' in str(exc):
        return Response(
            {
                'detail': 'Invalid Content-Type header. When uploading files, ensure the Content-Type header includes a proper boundary parameter. Example: Content-Type: multipart/form-data; boundary=----...'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Use default exception handler for other errors
    response = exception_handler(exc, context)
    return response
