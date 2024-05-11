from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from django.contrib import admin
from django.db.models.fields.related_descriptors import ManyToManyDescriptor

from qt_search import models

sp_related_inlines = []
sp_related_models = (
    models.CommonName,
    models.Distribution,
    models.GrowthTip,
    models.Image,
    models.PartColor,
    models.Pathogen,
    models.RegularEvent,
    models.Source,
    models.Synonym,
    models.Tag,
)


class BaseInline(admin.TabularInline):
    extra = 1


for msp in sp_related_models:
    admin.site.register(msp)
    if isinstance(msp.specie, ManyToManyDescriptor):
        msp = msp.specie.through
    sp_related_inlines.append(
        type(f'{msp.__name__}Inline', (BaseInline,), {"model": msp})
    )


admin.site.register(models.IntervalValue)
admin.site.register(models.ScientificClassification)
admin.site.register(models.Order)
admin.site.register(models.Color)


@admin.register(models.Specie)
class SpecieAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

    readonly_fields = ('slug',)

    inlines = sp_related_inlines


@admin.register(models.DistributionSpecie)
class DistributionSpecieAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }
