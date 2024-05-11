from django.db.models.signals import post_delete
from django.dispatch import receiver

from qt_search.models import RegularEvent, Specie


@receiver(post_delete, sender=Specie)
def auto_delete_one_to_one_for_specie(sender, instance, **kwargs):
    one_to_one_relations = (
        instance.height_cm,
        instance.years_to_max_height,
        instance.spread_cm,
        instance.scientific_classification
    )
    for field in one_to_one_relations:
        if field:
            field.delete()


@receiver(post_delete, sender=RegularEvent)
def auto_delete_one_to_one_for_regular_event(sender, instance, **kwargs):
    if frequency := instance.frequency:
        frequency.delete()
