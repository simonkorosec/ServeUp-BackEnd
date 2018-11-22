from rest_framework import viewsets
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


class UporabnikViewSet(viewsets.ModelViewSet):
    serializer_class = UporabnikSerializer
    queryset = Uporabnik.objects.all()
    model = Uporabnik

    # def create(self, request, *args, **kwargs):
    #     data = {}
    #
    #     # check if data is in correct format
    #     if type(request.data) is QueryDict:
    #         tmp = dict(request.data)
    #         data['email'] = tmp['email'][0]  # email and password are stored as a list
    #         data['password'] = tmp['password'][0]  # so we have wot change them
    #     elif type(request.data) is dict:
    #         data = request.data
    #
    #     serializer = UporabnikSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)
