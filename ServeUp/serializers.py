from rest_framework import serializers
from ServeUp.models import *

"""
Convert received data from JSON to Django model and the other way around
"""


class RestavracijaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restavracija
        fields = ('ime_restavracije', 'ocena')


class PostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posta
        fields = ('postna_stevilka', 'kraj')


class UporabnikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uporabnik
        fields = ('email', 'password')
        write_only_fields = ['password']

    def create(self, validated_data):
        """
        Override the default method so we can use the .set_password() and not save the password as clear text
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Override the default method so we can use the .set_password() and not save the password as clear text
        """
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
