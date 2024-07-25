from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class HemispheresChoices(models.TextChoices):
        NORTH = "north", "North"
        SOUTH = "south", "South"

    class GendersChoices(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    gender = models.CharField(max_length=8, choices=GendersChoices.choices, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    location = models.CharField(max_length=50, null=True, blank=True)
    hemisphere = models.CharField(max_length=8, choices=HemispheresChoices.choices, null=True, blank=True)
