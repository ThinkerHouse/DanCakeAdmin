import datetime
from django.db import models
from apps.users.models import User
from apps.product.models import Product
from apps.material.models import Material
from config.util.constants.constants import ACTIVE_STATUS_CHOICES

class Recipe(models.Model):
    class Meta:
        db_table = 'recipes'

    name = models.CharField(max_length=255, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="recipe_product")
    status = models.IntegerField(choices=ACTIVE_STATUS_CHOICES, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_created_by')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_approved_by', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_updated_by', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    
    
class RecipeItem(models.Model):
    class Meta:
        db_table = 'recipe_items'
        
    recipe = models.ForeignKey(Recipe, related_name="recipe_items", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, related_name='recipe_material_info', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.IntegerField(choices=ACTIVE_STATUS_CHOICES, default=0)

    
