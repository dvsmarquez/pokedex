# Generated by Django 3.1.5 on 2021-01-23 22:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.IntegerField(editable=False, unique=True)),
                ('name', models.CharField(editable=False, max_length=255, unique=True)),
                ('height', models.IntegerField(editable=False)),
                ('weight', models.IntegerField(editable=False)),
                ('hidden_power', models.IntegerField(editable=False)),
                ('attack', models.IntegerField(editable=False)),
                ('defense', models.IntegerField(editable=False)),
                ('special_attack', models.IntegerField(editable=False)),
                ('special_defense', models.IntegerField(editable=False)),
                ('speed', models.IntegerField(editable=False)),
            ],
            options={
                'db_table': 'pokedex_pokemon',
            },
        ),
        migrations.CreateModel(
            name='Evolution',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.IntegerField(editable=False)),
                ('chain_id', models.UUIDField(editable=False)),
                ('pokemon', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='pokedex.pokemon')),
            ],
            options={
                'db_table': 'pokedex_evolutions',
            },
        ),
    ]
