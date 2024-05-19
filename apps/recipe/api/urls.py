from django.urls import path
from .views import RecipeListCreateAPIView, RecipeRetrieveUpdateDestroyAPIView, RecipeItemCreateAPIView, RecipeItemDeleteAPIView

urlpatterns = [
    path('', RecipeListCreateAPIView.as_view()),
    path('<int:pk>', RecipeRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:recipe_id>/items', RecipeItemCreateAPIView.as_view()),
    path('<int:recipe_id>/items/<int:pk>', RecipeItemDeleteAPIView.as_view()),
]