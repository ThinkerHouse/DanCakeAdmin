from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

def custom_response_handler(data, status=None, message=None, paginator=None):
    response_data = {
        'status': status,
        'message': message,
        'data': data,
        # Add any additional fields you want in your response
    }
    if paginator is not None:
        response_data['pagination'] = {
            'count': paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'limit': paginator.limit,
            'offset': paginator.offset,
        }
    return Response(response_data, status=status)
