from django.urls import path
from .views import WastageListCreateAPIView, WastageRetrieveUpdateDestroyAPIView, WastageItemCreateAPIView, WastageItemDeleteAPIView

urlpatterns = [
    path('', WastageListCreateAPIView.as_view()),
    path('<int:pk>', WastageRetrieveUpdateDestroyAPIView.as_view()),
]