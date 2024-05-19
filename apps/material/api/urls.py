from django.urls import path
from .views import MaterialListCreateAPIView, MaterialRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', MaterialListCreateAPIView.as_view()),
    path('<int:pk>', MaterialRetrieveUpdateDestroyAPIView.as_view())
]

