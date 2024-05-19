from django.urls import path
from .views import PurchaseOrderListCreateAPIView, PurchaseOrderRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', PurchaseOrderListCreateAPIView.as_view()),
    path('<int:pk>', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view())
]