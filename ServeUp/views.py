from rest_framework.decorators import action
from rest_framework import viewsets
from ServeUp.models import Restavracija
from ServeUp.serializers import RestavracijaSerializer

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
