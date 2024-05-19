from django.urls import path
from .views import CheckListCreateAPIView, CheckListRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', CheckListCreateAPIView.as_view()),
    path('<int:pk>', CheckListRetrieveUpdateDestroyAPIView.as_view())
]

