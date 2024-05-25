from django.urls import path
from .views import WastageListCreateAPIView, WastageRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', WastageListCreateAPIView.as_view()),
    path('<int:pk>', WastageRetrieveUpdateDestroyAPIView.as_view())
]

