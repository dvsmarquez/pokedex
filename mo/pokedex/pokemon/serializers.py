"""
Serializadores del módulo de Pokémon.
"""

from rest_framework import serializers
from mo.pokedex.pokemon.models import Pokemon
from mo.pokedex.evolutions.models import Evolution


class PokemonSerializer(serializers.ModelSerializer):
    """
    Serializador de un Pokémon.
    """

    evolutions = serializers.SerializerMethodField()

    class Meta:
        model = Pokemon

        fields = (
            'id',
            'external_id',
            'name',
            'height',
            'weight',
            'hidden_power',
            'attack',
            'defense',
            'special_attack',
            'special_defense',
            'speed',
            'evolutions',
        )

    def get_evolutions(self, obj):
        """
        Obtiene las evoluciones para este pokémon.
        """

        chains = obj.evolution_set.all()
        evolutions = []

        for chain in chains:
            related_evolutions = Evolution.objects.filter(
                chain_id=chain.chain_id
            )

            related_evolutions = related_evolutions.exclude(pokemon=obj)
            related_evolutions = related_evolutions.order_by('level')

            for related_evolution in related_evolutions:
                level_up = related_evolution.level > chain.level
                evolution_type = 'evolution' if level_up else 'preevolution'

                evolution = {
                    'id': chain.chain_id,
                    'type': evolution_type,
                    'name': related_evolution.pokemon.name,
                    'level': related_evolution.level
                }

                evolutions.append(evolution)

        return evolutions
