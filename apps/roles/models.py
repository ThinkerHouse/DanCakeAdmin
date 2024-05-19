from django.db import models
from django.contrib.auth.models import Group
# Create your models here.


class Roles(Group):
    class Meta:
        db_table = 'roles'
