from rest_framework import viewsets
from rest_framework.decorators import action
from url_filter.integrations.drf import \
    DjangoFilterBackend  # https://github.com/miki725/django-url-filter - how to use filters

from ServeUp.serializers import *

"""
All views should be created here

Implement using ViewSets, otherwise use generic views or class-based views with
APIView and Response libraries
"""


class RestavracijaViewSet(viewsets.ModelViewSet):
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


class AdminUporabnikViewSet(viewsets.ModelViewSet):
    serializer_class = AdminUporabnikSerializer
    queryset = Uporabnik.objects.all()
    model = Uporabnik

    @action(detail=False, methods=['post'])
    def login(self, request):
        return request.data
