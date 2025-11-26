import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    telegram_id = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.username