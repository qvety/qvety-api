# Generated by Django 5.0.6 on 2024-08-28 21:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qt_garden', '0001_initial'),
        ('qt_search', '0003_rename_image_url_source_source_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='garden',
            name='specie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='specie_plants', to='qt_search.specie'),
            preserve_default=False,
        ),
    ]