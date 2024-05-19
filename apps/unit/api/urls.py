from django.urls import path
from .views import UnitListCreateAPIView, UnitRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', UnitListCreateAPIView.as_view()),
    path('<int:pk>', UnitRetrieveUpdateDestroyAPIView.as_view())
]

