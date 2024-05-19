from rest_framework import status
from config.util.response_handler.custom_response_handler import custom_response_handler


class CustomListCreateMixin:
    """
    Custom mixin to handle list and create operations with custom response.
    """

    def custom_list_response(self, queryset, serializer_class, message=None):
        # def custom_list_response(self, queryset, serializer_class, details_serializer_class=None, message=None):
        queryset = self.filter_queryset(queryset)

        page = None
        if self.request.query_params.get('page') is not None:
            # Paginate the queryset
            page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = serializer_class(page, many=True)
            return custom_response_handler(
                data=serializer.data,
                paginator=self.paginator,
                status=status.HTTP_200_OK,
                message=message or f"{
                    serializer_class.Meta.model.__name__} list retrieved successfully"
            )

        serializer = serializer_class(queryset, many=True)
        return custom_response_handler(
            data=serializer.data,
            status=status.HTTP_200_OK,
            message=message or f"{
                serializer_class.Meta.model.__name__} list retrieved successfully"
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return custom_response_handler(serializer.data, status=status.HTTP_201_CREATED, message=f"{serializer.Meta.model.__name__} created successfully")


class CustomRetrieveUpdateDestroyMixin:
    """
    Custom mixin to handle retrieve and update operations with custom response.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response_handler(serializer.data, status=status.HTTP_200_OK,  message=f"{serializer.Meta.model.__name__} retrive successfully")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return custom_response_handler(serializer.data, status=status.HTTP_200_OK, message=f"{serializer.Meta.model.__name__} updated successfully")

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.delete()
        return custom_response_handler({}, status=status.HTTP_204_NO_CONTENT, message=f"{serializer.Meta.model.__name__} deleted successfully")

