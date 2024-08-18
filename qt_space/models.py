import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from qt_user.models import User


class Space(models.Model):
    DEFAULT_TEMPERATURE = 23
    DEFAULT_HUMIDITY = 45

    class HemispheresChoices(models.TextChoices):
        NORTH = "north", "North"
        SOUTH = "south", "South"

    class CardinalDirectionChoices(models.TextChoices):
        NORTH = "north", "North"
        SOUTH = "south", "South"
        EAST = "east", "East"
        West = "west", "West"

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')

    hemisphere = models.CharField(max_length=8, choices=HemispheresChoices.choices, null=True, blank=True)
    temperature = models.SmallIntegerField(
        default=DEFAULT_TEMPERATURE,
        validators=[MaxValueValidator(100), MinValueValidator(-273)],
    )
    humidity = models.PositiveSmallIntegerField(
        default=DEFAULT_HUMIDITY,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
    )
    window_side = models.CharField(max_length=8, choices=CardinalDirectionChoices.choices, null=True, blank=True)
