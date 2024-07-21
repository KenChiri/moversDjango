from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Add a unique related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups')
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Add a unique related_name
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions')
    )

    is_superuser = models.BooleanField(
        default = False,
        help_text = 'Designates wether this users should have all permissions without explicitly assigning them',
        verbose_name = 'superuser status'
    )

    def __str__(self):
        return self.username
