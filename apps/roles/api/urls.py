# group_api/urls.py

from django.urls import path
from .views import RolesRetrieveUpdateAPIView, RolesListCreateAPIView, PermissionListView

urlpatterns = [
    path('roles/', RolesListCreateAPIView.as_view()),
    path('roles/<int:pk>/', RolesRetrieveUpdateAPIView.as_view()),
    path('permissions/', PermissionListView.as_view()),
]
