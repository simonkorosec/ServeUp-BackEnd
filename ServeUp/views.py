from rest_framework.decorators import action
from rest_framework import viewsets
from url_filter.integrations.drf import \
    DjangoFilterBackend  # https://github.com/miki725/django-url-filter - how to use filters
from ServeUp.models import *
from ServeUp.serializers import *

"""
All views should be created here

Implement using ViewSets, otherwise use generic views or class-based views with
APIView and Response libraries
"""


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    ViewSet provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions

    Additional actions can be added using '@action()' decorator, default response
    is GET, you can add POST using 'methods' argument
    """
    queryset = Restavracija.objects.all()
    serializer_class = RestavracijaSerializer


class PostaViewSet(viewsets.ModelViewSet):
    """
    ViewSet provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions

    Additional actions can be added using '@action()' decorator, default response
    is GET, you can add POST using 'methods' argument
    """
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['postna_stevilka', 'kraj']

    serializer_class = PostaSerializer
    queryset = Posta.objects.all()
    model = Posta


class UporabnikViewSet(viewsets.ModelViewSet):
    """
    ViewSet provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions

    Additional actions can be added using '@action()' decorator, default response
    is GET, you can add POST using 'methods' argument
    """
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id_vloga', 'e_mail']

    serializer_class = UporabnikSerializer
    queryset = Uporabnik.objects.all()
    model = Uporabnik
