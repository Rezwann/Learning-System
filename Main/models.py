from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_information = models.TextField('User Information', max_length=300,default='', blank=True)    
    class Meta:
        db_table = 'auth_user'