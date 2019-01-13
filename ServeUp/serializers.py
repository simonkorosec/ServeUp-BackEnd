from rest_framework import serializers
from ServeUp.models import *

"""
Convert received data from JSON to Django model and the other way around
"""


class TipRestavracijeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipRestavracije
        fields = '__all__'


class NarociloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Narocilo
        fields = '__all__'


class JediNarocilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = JediNarocila
        fields = '__all__'


class RestavracijaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restavracija
        fields = '__all__'


class PostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posta
        fields = ('postna_stevilka', 'kraj')


class UporabnikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uporabnik
        fields = '__all__'


class NaslovSerializer(serializers.ModelSerializer):
    class Meta:
        model = Naslov
        fields = '__all__'


class AdminUporabnikSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUporabnik
        fields = ('id', 'email', 'password')
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


class RestavracijaPodatkiSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestavracijaPodatki
        fields = '__all__'


class NarociloPodatkiSerializer(serializers.ModelSerializer):
    class Meta:
        model = JediNarocilaPodatki
        fields = '__all__'


class JedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jed
        fields = '__all__'


class JediNarocilaPodatkiSerializer(serializers.ModelSerializer):
    class Meta:
        model = JediNarocilaPodatki
        fields = '__all__'


class JedilniListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JedilniList
        fields = '__all__'


class MizeSerializer(serializers.ModelSerializer):
    id_restavracija = serializers.PrimaryKeyRelatedField(
        queryset=Restavracija.objects.all(), write_only=True)

    class Meta:
        model = Mize
        fields = '__all__'
