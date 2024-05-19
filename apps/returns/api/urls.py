from django.urls import path
from .views import ReturnsListCreateAPIView, ReturnsRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', ReturnsListCreateAPIView.as_view()),
    path('<int:pk>', ReturnsRetrieveUpdateDestroyAPIView.as_view()),
]