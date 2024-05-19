from django.urls import path
from .views import RequisitionListCreateAPIView, RequisitionRetrieveUpdateDestroyAPIView, RequisitionItemCreateAPIView, RequisitionItemDeleteAPIView

urlpatterns = [
    path('', RequisitionListCreateAPIView.as_view()),
    path('<int:pk>', RequisitionRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:requisition_id>/items', RequisitionItemCreateAPIView.as_view()),
    path('<int:requisition_id>/items/<int:pk>', RequisitionItemDeleteAPIView.as_view()),
]