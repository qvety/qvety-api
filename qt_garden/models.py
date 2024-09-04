from django.db import models

from common.db_models import CreatedUpdatedDateModel
from qt_search.models import Specie
from qt_space.models import Space
from qt_user.models import User


class GardenParameters(models.Model):
    class StateChoices(models.TextChoices):
        BAD = 'bad', 'Bad'
        NORMAL = 'normal', 'Normal'
        GOOD = 'good', 'Good'

    class ExposureChoices(models.TextChoices):
        EXPOSED = 'exposed', 'Exposed'
        SHELTERED = 'sheltered', 'Sheltered'
        EXPOSED_OR_SHELTERED = 'exposed_or_sheltered', 'Exposed or Sheltered'

    last_water = models.DateTimeField(blank=True, null=True)
    last_fertilizer = models.DateTimeField(blank=True, null=True)
    last_repot = models.DateTimeField(blank=True, null=True)
    last_prun = models.DateTimeField(blank=True, null=True)

    height = models.IntegerField(blank=True, null=True)
    pot_diameter = models.IntegerField(blank=True, null=True)
    pot_height = models.IntegerField(blank=True, null=True)

    current_state = models.CharField(max_length=8, choices=StateChoices.choices, null=True, blank=True)
    exposure = models.CharField(max_length=32, choices=ExposureChoices.choices, null=True, blank=True)


class Garden(CreatedUpdatedDateModel):
    room = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='room_plants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_plants')
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='specie_plants')

    parameters = models.OneToOneField(
        GardenParameters,
        on_delete=models.CASCADE,
        related_name='parameters',
        blank=True,
        null=True,
    )

    custom_name = models.CharField(max_length=255, blank=True, null=True)
    # Need custom photo
    description = models.CharField(max_length=1024, blank=True, null=True)
