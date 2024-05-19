"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include('apps.authentication.api.urls')),
    path('api/role-permission/', include('apps.roles.api.urls')),
    # path('api/permissions/', include('apps.permissions.api.urls')),
    path('api/users/', include('apps.users.api.urls')),
    path('api/units/', include('apps.unit.api.urls')),
    path('api/material-type/', include('apps.material_type.api.urls')),
    path('api/materials/', include('apps.material.api.urls')),
    path('api/departments/', include('apps.department.api.urls')),
    path('api/check-lists/', include('apps.check_list.api.urls')),
    path('api/warehouses/', include('apps.warehouse.api.urls')),
    path('api/products/', include('apps.product.api.urls')),
    path('api/production-plants/', include('apps.production_plant.api.urls')),
    path('api/purchase-orders/', include('apps.purchase_order.api.urls')),
    path('api/productions/', include('apps.production.api.urls')),
    path('api/requisitions/', include('apps.requisition.api.urls')),
    path('api/received_orders/', include('apps.received_order.api.urls')),
    path('api/recipies/', include('apps.recipe.api.urls')),
    path('api/return/', include('apps.returns.api.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
