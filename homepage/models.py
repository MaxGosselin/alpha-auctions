from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator 


class User(AbstractUser):
    name = models.CharField(max_length=20, default="")
    member_level = models.CharField(max_length=20, default="")
    team = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)], default=98)
    