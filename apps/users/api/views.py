from rest_framework import generics
from apps.users.models import User
from .serializers import UserSerializer, UserDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.permissions.GroupPermission import GroupPermission
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser


class UserListCreateApiView(BasicQueryParamsFilterMixin, CustomListCreateMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['view_user', 'add_user']
    parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailsSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        return self.custom_list_response(
            queryset=self.get_queryset(),
            serializer_class=self.get_serializer_class(),
            message="User list retrieved successfully"
        )

    def create(self, request, *args, **kwargs):
        return CustomListCreateMixin.create(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset, username='username', email='email', user_type='user_type', is_active='status')


class UsersRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView, CustomRetrieveUpdateDestroyMixin):
    """
    API view for retrieving, updating, and deleting a user.
    """
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['view_user', 'add_user']
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailsSerializer
        return UserSerializer

    def retrieve(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.update(self, request, *args, **kwargs)
