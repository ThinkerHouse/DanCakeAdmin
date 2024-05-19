from django.urls import path
from .views import ReceivedOrderListCreateAPIView, ReceivedOrderRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', ReceivedOrderListCreateAPIView.as_view()),
    path('<int:pk>', ReceivedOrderRetrieveUpdateDestroyAPIView.as_view())
]