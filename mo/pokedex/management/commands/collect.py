"""
Obtiene información acerca de la cadena de evolución de un pokémon dado un identificador de
cadena. Registra información para todos los pokémon incluidos en la cadena de evolución.
"""

import re
import uuid

import requests
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from mo.pokedex.evolutions.models import Evolution
from mo.pokedex.pokemon.models import Pokemon


class Command(BaseCommand):
    """
    Obtiene información acerca de la cadena de evolución de un pokémon dado un identificador de
    cadena. Registra información para todos los pokémon incluidos en la cadena de evolución.
    """

    help = """
    Obtiene información acerca de la cadena de evolución de un pokémon dado un identificador de
    cadena. Registra información para todos los pokémon incluidos en la cadena de evolución.
    """

    # Mapa de nombres equivalentes entre la base de datos y la respuesta del servicio para
    # las habilidades del pokémon.
    stats_map = {
        'hp': 'hidden_power',
        'attack': 'attack',
        'defense': 'defense',
        'special-attack': 'special_attack',
        'special-defense': 'special_defense',
        'speed': 'speed'
    }

    # URL del servicio de información de la cadena de evolución.
    EVOLUTION_CHAIN_URL = 'https://pokeapi.co/api/v2/evolution-chain/{id}/'

    # URL del servicio de información del pokémon.
    POKEMON_DATA_URL = 'https://pokeapi.co/api/v2/pokemon/{id}/'

    def add_arguments(self, parser):
        parser.add_argument(
            'id',
            type=int,
            help='Identificador de la cadena de evolución'
        )

    def handle(self, *args, **options):
        ec_id = options.get('id')
        self._fetch_evolution_chain(ec_id)

    def _fetch_evolution_chain(self, ec_id):
        """
        Obtiene la cadena de evolución con el id proporcionado.
        """

        self.stderr.write('Obtiendo cadena de evolución...')
        url = self.EVOLUTION_CHAIN_URL.format(id=ec_id)
        response = requests.get(url)

        if response.status_code != 200:
            self.stderr.write(
                f'No se encuentra cadena de evolución con el identificador {ec_id}.'
            )

            return

        data = response.json()
        ring = data['chain']
        self._iterate_chain(ring)

    def _iterate_chain(self, ring, level=1):
        """
        Itera y almacena la cadena de evolución.
        """

        instance = self._fetch_pokemon_data(ring)

        if not instance:
            return ()

        if not ring['evolves_to']:
            chain_id = uuid.uuid4()

            evolution = {
                'level': level,
                'chain_id': chain_id,
                'pokemon': instance
            }

            Evolution.objects.create(**evolution)

            return (chain_id,)

        chain_ids = ()

        for next_ring in ring['evolves_to']:
            chain_ids += self._iterate_chain(next_ring, level + 1)

        for chain_id in chain_ids:
            evolution = {
                'level': level,
                'chain_id': chain_id,
                'pokemon': instance
            }

            Evolution.objects.create(**evolution)

        return chain_ids

    def _fetch_pokemon_data(self, ring):
        """
        Obtiene la información del pokémon a partir de un eslabón de la cadena de evolución.
        """

        instance = None

        name = ring['species']['name']
        self.stderr.write(f'Obtiendo información para {name}...')
        url = ring['species']['url']
        sep_url = re.split(r'(.*/)(\d+)(/)', url)
        sep_url = [sep for sep in sep_url if sep]
        pokemon_id = sep_url[1]
        response = requests.get(self.POKEMON_DATA_URL.format(id=pokemon_id))

        if response.status_code != 200:
            self.stderr.write(
                f'No se pudo obtener información para {name} con identificador {pokemon_id}.'
            )

            return instance

        data = response.json()

        pokemon_data = {
            'external_id': pokemon_id,
            'name': name,
            'height': data['height'],
            'weight': data['weight']
        }

        for stat in data['stats']:
            attr = self.stats_map.get(stat['stat']['name'])

            if not attr:
                continue

            pokemon_data[attr] = stat['base_stat']

        try:
            instance = Pokemon.objects.create(**pokemon_data)
        except IntegrityError:
            self.stderr.write(f'Ya existe información para {name}.')

        return instance
