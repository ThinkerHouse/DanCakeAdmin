from django.db import models
from apps.roles.models import Roles
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from config.util.constants.constants import ACTIVE_STATUS_CHOICES, USER_TYPE_CHOICES


class User(AbstractUser):        

    class Meta:
        db_table = 'users'

    email = models.EmailField(max_length=255, unique=True)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='users/', null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='administrator')
    is_active = models.IntegerField(choices=ACTIVE_STATUS_CHOICES, default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
