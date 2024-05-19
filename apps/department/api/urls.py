from django.urls import path
from .views import DepartmentListCreateAPIView, DepartmentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', DepartmentListCreateAPIView.as_view()),
    path('<int:pk>', DepartmentRetrieveUpdateDestroyAPIView.as_view())
]

