"""
Vistas del módulo de búsqueda.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from mo.pokedex.pokemon.models import Pokemon
from mo.pokedex.pokemon.serializers import PokemonSerializer


class SearchView(generics.ListAPIView):
    """
    Vista de búsqueda de pokémon por nombre.
    """

    queryset = Pokemon.objects.all()

    serializer_class = PokemonSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', None)

        if not name:
            return Pokemon.objects.none()

        queryset = super().get_queryset()
        queryset = queryset.filter(name=name)

        return queryset

    def list(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response_status = status.HTTP_200_OK

        if not queryset:
            name = self.request.query_params.get('name', None)

            if not name:
                response_status = status.HTTP_204_NO_CONTENT
            else:
                response_status = status.HTTP_404_NOT_FOUND

        obj = queryset.first()
        serializer = self.get_serializer(obj)

        return Response(serializer.data, status=response_status)
