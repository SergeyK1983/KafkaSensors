from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Модель пользователей """

    def __str__(self):
        return f"{self.id}-{self.username}"

