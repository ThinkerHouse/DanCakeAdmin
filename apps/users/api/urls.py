from django.urls import path
# from .views import CreateUser
from .views import UserListCreateApiView, UsersRetrieveUpdateAPIView

urlpatterns = [
    path('', UserListCreateApiView.as_view()),
    path('<int:pk>/', UsersRetrieveUpdateAPIView.as_view()),
    
]
