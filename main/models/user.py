from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Member(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    deadline_from = models.DateTimeField()
    deadline_to = models.DateTimeField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
            if self.pk is None:  # New user
                self.set_password(self.password)  # Hash password
            super().save(*args, **kwargs)