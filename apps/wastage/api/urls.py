from django.urls import path
from .views import MaterialTypeListCreateAPIView, MaterialTypeRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', MaterialTypeListCreateAPIView.as_view()),
    path('<int:pk>', MaterialTypeRetrieveUpdateDestroyAPIView.as_view())
]

