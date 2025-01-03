
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission,UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups'  # Unique related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions'  # Unique related_name
    )
    objects = UserManager()



    
    
    
        

# Create your models here.