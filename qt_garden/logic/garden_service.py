from django.db import transaction
from django.db.models import QuerySet

from qt_garden.logic.exceptions import GardenItemNotFoundError
from qt_garden.models import Garden, GardenParameters
from qt_garden.schemas.garden import GardenRequestSchema
from qt_user.models import User


class GardenServie:
    def __init__(self, user: User):
        self.current_user = user

    def get(self, uid: int) -> Garden:
        qs = Garden.objects.select_related('parameters', 'room', 'specie').filter(id=uid, user=self.current_user)
        try:
            return qs.get()
        except Garden.DoesNotExist as e:
            raise GardenItemNotFoundError() from e

    @transaction.atomic
    def create(self, data: GardenRequestSchema) -> Garden:
        garden_parameters = data.parameters
        garden_data = data.model_dump(exclude={'parameters'})
        garden = Garden(
            **garden_data,
            user=self.current_user,
        )
        if garden_parameters and garden_parameters.model_dump(exclude_none=True, exclude_unset=True):
            full_data_parameters = garden_parameters.model_dump()
            garden.parameters = GardenParameters.objects.create(**full_data_parameters)
        garden.save()
        return garden

    def get_list(self) -> QuerySet[Garden]:
        return Garden.objects.select_related('specie').filter(user=self.current_user).all()

    @transaction.atomic
    def update(self, uid: int, data: GardenRequestSchema) -> Garden:
        garden = self.get(uid)

        for attr, value in data.model_dump(exclude={'parameters'}).items():
            setattr(garden, attr, value)

        if data.parameters:
            parameters_data = data.parameters.model_dump()
            if garden.parameters:
                GardenParameters.objects.filter(id=garden.parameters.id).update(**parameters_data)
            else:
                garden.parameters = GardenParameters.objects.create(**parameters_data)

            garden.save()
        return garden

    def delete(self, uid: int) -> None:
        plant = self.get(uid)
        plant.delete()
