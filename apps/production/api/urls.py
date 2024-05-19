from django.urls import path
from .views import ProductionListCreateAPIView, ProductionRetrieveUpdateDestroyAPIView, ProductionItemCreateAPIView, ProductionItemDeleteAPIView

urlpatterns = [
    path('', ProductionListCreateAPIView.as_view()),
    path('<int:pk>', ProductionRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:production_id>/items', ProductionItemCreateAPIView.as_view()),
    path('<int:production_id>/items/<int:pk>', ProductionItemDeleteAPIView.as_view()),
]