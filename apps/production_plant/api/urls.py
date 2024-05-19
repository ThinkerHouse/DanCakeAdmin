from django.urls import path
from .views import ProductionPlantListCreateAPIView, ProductionPlantRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', ProductionPlantListCreateAPIView.as_view()),
    path('<int:pk>', ProductionPlantRetrieveUpdateDestroyAPIView.as_view())
]

