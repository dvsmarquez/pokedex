"""
Modelos para el módulo de pokémon.
"""

from django.db import models

from mo.pokedex.core.models import Model


class Pokemon(Model):
    """
    Pokémon.
    """

    # Código externo.
    external_id = models.IntegerField(editable=False, unique=True)

    # Nombre.
    name = models.CharField(editable=False, max_length=255, unique=True)

    # Altura.
    height = models.IntegerField(editable=False)

    # Peso.
    weight = models.IntegerField(editable=False)

    # Puntos de poder oculto.
    hidden_power = models.IntegerField(editable=False)

    # Puntos de ataque.
    attack = models.IntegerField(editable=False)

    # Puntos de defensa.
    defense = models.IntegerField(editable=False)

    # Puntos de ataque especial.
    special_attack = models.IntegerField(editable=False)

    # Puntos de defensa especial.
    special_defense = models.IntegerField(editable=False)

    # Puntos de velocidad.
    speed = models.IntegerField(editable=False)

    class Meta:
        db_table = 'pokedex_pokemon'
