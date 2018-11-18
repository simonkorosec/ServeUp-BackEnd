from rest_framework import serializers
from ServeUp.models import Restavracija, Posta

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
        fields = ('ime_restavracije', 'ocena')


class PostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posta
        fields = ('postna_stevilka', 'kraj')
