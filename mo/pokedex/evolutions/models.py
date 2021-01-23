"""
Modelos para el módulo de evoluciones.
"""

from django.db import models
from mo.pokedex.core.models import Model
from mo.pokedex.pokemon.models import Pokemon


class Evolution(Model):
    """
    Evolución de un pokémon.
    """

    # Nivel de esta evolución en la cadena de evoluciones.
    level = models.IntegerField(editable=False)

    # Identificador del grupo de la cadena de evoluciones.
    chain_id = models.UUIDField(editable=False)

    # Pokémon
    pokemon = models.ForeignKey(
        Pokemon,
        editable=False,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'pokedex_evolutions'
