# Generated by Django 5.0.1 on 2024-05-02 21:44

import bitfield.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qt_search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distributionspecie',
            name='statuses',
            field=bitfield.models.BitField([('native', 'Native'), ('introduced', 'Introduced'), ('doubtful', 'Doubtful'), ('absent', 'Absent'), ('extinct', 'Extinct')], default=None, help_text='BitFlag. DistributionSpecie.', null=True),
        ),
        migrations.AlterField(
            model_name='growthtip',
            name='tip_type',
            field=models.CharField(choices=[('propagation', 'Propagation'), ('suggested_panting_places', 'Suggested Planting Places'), ('pruning', 'Pruning')], max_length=64),
        ),
        migrations.AlterField(
            model_name='image',
            name='part',
            field=models.CharField(choices=[('bark', 'Bark'), ('fruit', 'Fruit'), ('flower', 'Flower'), ('habit', 'Habit'), ('leaf', 'Leaf'), ('other', 'Other'), ('root', 'Root'), ('stem', 'Stem'), ('seed', 'Seed'), ('tuber', 'Tuber'), ('foliage', 'Foliage')], help_text='Which part of the plant is this photo?', max_length=64),
        ),
        migrations.AlterField(
            model_name='partcolor',
            name='plant_part',
            field=models.CharField(choices=[('bark', 'Bark'), ('fruit', 'Fruit'), ('flower', 'Flower'), ('habit', 'Habit'), ('leaf', 'Leaf'), ('other', 'Other'), ('root', 'Root'), ('stem', 'Stem'), ('seed', 'Seed'), ('tuber', 'Tuber'), ('foliage', 'Foliage')], max_length=64),
        ),
        migrations.AlterField(
            model_name='partcolor',
            name='season',
            field=models.CharField(choices=[('spring', 'Spring'), ('summer', 'Summer'), ('autumn', 'Autumn'), ('winter', 'Winter')], max_length=64),
        ),
        migrations.AlterField(
            model_name='pathogen',
            name='pathogen_type',
            field=models.CharField(choices=[('disease', 'Disease'), ('pest', 'Pest')], max_length=64),
        ),
        migrations.AlterField(
            model_name='regularevent',
            name='frequency_unit',
            field=models.CharField(choices=[('minute', 'Minute'), ('hour', 'Hour'), ('day', 'Day'), ('week', 'Week'), ('fortnight', 'Fortnight'), ('month', 'Month'), ('year', 'Year'), ('century', 'Century')], max_length=64),
        ),
        migrations.AlterField(
            model_name='specie',
            name='duration',
            field=models.CharField(choices=[('annual', 'Annual'), ('biennial', 'Biennial'), ('perennial', 'Perennial')], help_text='BitFlag. How long does the plant live in time.', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='edible_part',
            field=bitfield.models.BitField([('bark', 'Bark'), ('fruit', 'Fruit'), ('flower', 'Flower'), ('habit', 'Habit'), ('leaf', 'Leaf'), ('other', 'Other'), ('root', 'Root'), ('stem', 'Stem'), ('seed', 'Seed'), ('tuber', 'Tuber'), ('foliage', 'Foliage')], db_index=True, default=None, help_text='BitFlag. The plant edible part(s), if any.', null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='exposure',
            field=models.CharField(choices=[('exposed', 'Exposed'), ('sheltered', 'Sheltered'), ('exposed_or_sheltered', 'Exposed or Sheltered'), ('sheltered_or_exposed', 'Sheltered or Exposed')], db_index=True, help_text='Sun-loving or not plant. The amount of light that the plant receives.', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='foliage',
            field=bitfield.models.BitField([('deciduous', 'Deciduous'), ('evergreen', 'Evergreen'), ('semi_evergreen', 'Semi evergreen')], db_index=True, default=None, help_text='BitFlag. Features regarding seasonal changes in foliage.', null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='fragrance',
            field=bitfield.models.BitField([('bark', 'Bark'), ('fruit', 'Fruit'), ('flower', 'Flower'), ('habit', 'Habit'), ('leaf', 'Leaf'), ('other', 'Other'), ('root', 'Root'), ('stem', 'Stem'), ('seed', 'Seed'), ('tuber', 'Tuber'), ('foliage', 'Foliage')], db_index=True, default=None, help_text='Which part of the plant emits fragrance.', null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='habit',
            field=bitfield.models.BitField([('tufted', 'Tufted'), ('trailing', 'Trailing'), ('pendulous_weeping', 'Pendulous weeping'), ('clump_forming', 'Clump forming'), ('columnar_upright', 'Columnar upright'), ('submerged', 'Submerged'), ('suckering', 'Suckering'), ('floating', 'Floating'), ('mat_forming', 'Matforming'), ('bushy', 'Bushy'), ('climbing', 'Climbing')], db_index=True, default=None, help_text='BitFlag. The general shape and morphology of the plant, its growth method and organization of structures.', null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='harvest',
            field=bitfield.models.BitField([('winter', 'Winter'), ('spring', 'Spring'), ('mid_autumn', 'Mid autumn'), ('mid_summer', 'Mid summer'), ('summer', 'Summer'), ('autumn', 'Autumn'), ('late_autumn', 'Late autumn'), ('all_year_around', 'All year around'), ('mid_spring', 'Mid spring'), ('mid_winter', 'Mid winter'), ('late_summer', 'Late summer'), ('early_autumn', 'Early autumn'), ('late_winter', 'Late winter'), ('early_summer', 'Early summer'), ('late_spring', 'Late spring'), ('early_spring', 'Early spring'), ('early_winter', 'Early winter')], db_index=True, default=None, help_text='BitFlag. The time at which to harvest, if any.', null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='planting',
            field=bitfield.models.BitField([('winter', 'Winter'), ('spring', 'Spring'), ('mid_autumn', 'Mid autumn'), ('mid_summer', 'Mid summer'), ('summer', 'Summer'), ('autumn', 'Autumn'), ('late_autumn', 'Late autumn'), ('all_year_around', 'All year around'), ('mid_spring', 'Mid spring'), ('mid_winter', 'Mid winter'), ('late_summer', 'Late summer'), ('early_autumn', 'Early autumn'), ('late_winter', 'Late winter'), ('early_summer', 'Early summer'), ('late_spring', 'Late spring'), ('early_spring', 'Early spring'), ('early_winter', 'Early winter')], db_index=True, default=None, help_text='BitFlag. The time at which to plant the plant.', null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='position_side',
            field=bitfield.models.BitField([('east_facing', 'East-facing'), ('north_facing', 'North-facing'), ('west_facing', 'West-facing'), ('south_facing', 'South-facing')], db_index=True, default=None, help_text='BitFlag. The side of the world where the plant can grow well.', null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='position_sunlight',
            field=bitfield.models.BitField([('partial_shade', 'Partial shade'), ('full_sun', 'Full sun'), ('full_shade', 'Full shade')], db_index=True, default=None, help_text='BitFlag. The level of sunlight on the plant.', null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='soil_moisture',
            field=bitfield.models.BitField([('moist_well_drained', 'Moist but well-drained'), ('poorly_drained', 'Poorly-drained'), ('well_drained', 'Well-drained')], db_index=True, default=None, help_text='BitFlag. Ground humidity level.', null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='soil_ph',
            field=bitfield.models.BitField([('acid', 'Acid'), ('neutral', 'Neutral'), ('alkaline', 'Alkaline')], db_index=True, default=None, help_text='BitFlag. The acidity of the soil required for the plant.', null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='soil_type',
            field=bitfield.models.BitField([('clay', 'Clay'), ('sand', 'Sand'), ('chalk', 'Chalk'), ('loam', 'Loam')], db_index=True, default=None, help_text='BitFlag. The type of soil in which the plant can grow.', null=True),
        ),
        migrations.AlterField(
            model_name='specie',
            name='toxicity',
            field=bitfield.models.BitField([('toxic_to_cats', 'Toxic to Cats'), ('slightly_toxic_to_humans', 'Slightly Toxic to Humans'), ('moderate_toxic_to_humans', 'Moderate Toxic to Humans'), ('highly_toxic_to_humans', 'Highly Toxic to Humans'), ('toxic_to_dogs', 'Toxic to Dogs')], db_index=True, default=None, help_text='BitFlag. The level of toxicity of the plant to humans and animals.', null=True),
        ),
    ]
