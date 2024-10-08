# Generated by Django 5.0.6 on 2024-08-23 21:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('qt_space', '0004_alter_space_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GardenParameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_water', models.DateTimeField(blank=True, null=True)),
                ('last_fertilizer', models.DateTimeField(blank=True, null=True)),
                ('last_repot', models.DateTimeField(blank=True, null=True)),
                ('last_prun', models.DateTimeField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('pot_diameter', models.IntegerField(blank=True, null=True)),
                ('pot_height', models.IntegerField(blank=True, null=True)),
                ('current_state', models.CharField(blank=True, choices=[('bad', 'Bad'), ('normal', 'Normal'), ('good', 'Good')], max_length=8, null=True)),
                ('exposure', models.CharField(blank=True, choices=[('exposed', 'Exposed'), ('sheltered', 'Sheltered'), ('exposed_or_sheltered', 'Exposed or Sheltered')], max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Garden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_plants', to='qt_space.space')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_plants', to=settings.AUTH_USER_MODEL)),
                ('parameters', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='qt_garden.gardenparameters')),
            ],
        ),
    ]
