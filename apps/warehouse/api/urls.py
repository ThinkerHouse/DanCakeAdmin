from django.urls import path
from .views import WarehouseListCreateAPIView, WarehouseRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', WarehouseListCreateAPIView.as_view()),
    path('<int:pk>', WarehouseRetrieveUpdateDestroyAPIView.as_view())
]

