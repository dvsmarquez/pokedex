"""
Rutas para el módulo de búsqueda.
"""

from django.urls import path
from mo.pokedex.search.views import SearchView

urlpatterns = [
    path(r'', SearchView.as_view())
]
