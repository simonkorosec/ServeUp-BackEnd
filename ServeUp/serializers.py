from rest_framework import serializers
from ServeUp.models import Restavracija

"""
Convert received data from JSON to Django model and the other way around
"""


# Create your serializers here.
class RestavracijaSerializer(serializers.ModelSerializer):
    """
    Defines which fields get serialized/deserialized
    """
    class Meta:
        model = Restavracija
        fields = ('restaurant_name', 'rating')
