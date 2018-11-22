# This is an auto-generated Django model module.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from ServeUp.Views.userManager import MyUserManager


# TODO: * Make sure each ForeignKey has `on_delete` set to the desired behavior.


class Jed(models.Model):
    id_jed = models.AutoField(primary_key=True)
    id_jedilni_list = models.ForeignKey('JedilniList', on_delete=models.CASCADE, db_column='id_jedilni_list')
    id_restavracija = models.ForeignKey('Restavracija', models.DO_NOTHING, db_column='id_restavracija', blank=True,
                                        null=True)
    ime_jedi = models.TextField()
    cena = models.FloatField()
    opis = models.TextField()

    class Meta:
        managed = False
        db_table = 'jed'


class JediNarocila(models.Model):
    id_jed = models.ForeignKey(Jed, models.DO_NOTHING, db_column='id_jed', primary_key=True)
    id_narocila = models.ForeignKey('Narocilo', models.CASCADE, db_column='id_narocila')

    class Meta:
        managed = False
        db_table = 'jedi_narocila'
        unique_together = (('id_jed', 'id_narocila'), ('id_jed', 'id_narocila'),)


class JedilniList(models.Model):
    id_jedilni_list = models.AutoField(primary_key=True)
    vrsta = models.TextField()

    class Meta:
        managed = False
        db_table = 'jedilni_list'


class Narocilo(models.Model):
    id_narocila = models.IntegerField(primary_key=True)
    id_restavracija = models.ForeignKey('Restavracija', models.CASCADE, db_column='id_restavracija')
    id_uporabnik = models.ForeignKey('Uporabnik', models.CASCADE, db_column='id_uporabnik')
    cas_prevzema = models.TimeField()

    class Meta:
        managed = False
        db_table = 'narocilo'


class Naslov(models.Model):
    id_naslov = models.AutoField(primary_key=True)
    postna_stevilka = models.ForeignKey('Posta', models.DO_NOTHING, db_column='postna_stevilka')
    ulica = models.TextField()
    hisna_stevilka = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'naslov'


class Posta(models.Model):
    postna_stevilka = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    kraj = models.TextField()

    class Meta:
        managed = False
        db_table = 'posta'


class Restavracija(models.Model):
    id_restavracija = models.AutoField(primary_key=True)
    id_naslov = models.ForeignKey(Naslov, models.DO_NOTHING, db_column='id_naslov')
    id_tip_restavracije = models.ForeignKey('TipRestavracije', models.DO_NOTHING, db_column='id_tip_restavracije')
    ime_restavracije = models.TextField()
    ocena = models.FloatField()

    class Meta:
        managed = False
        db_table = 'restavracija'


class Sestavine(models.Model):
    id_sestavine = models.AutoField(primary_key=True)
    ime_sestavine = models.TextField()

    class Meta:
        managed = False
        db_table = 'sestavine'


class TipRestavracije(models.Model):
    id_tip_restavracije = models.AutoField(primary_key=True)
    tip = models.TextField()

    class Meta:
        managed = False
        db_table = 'tip_restavracije'


# class Upravlja(models.Model):
#     id_restavracija = models.ForeignKey(Restavracija, on_delete=models.CASCADE, db_column='id_restavracija',
#                                         primary_key=True)
#     id_uporabnik = models.ForeignKey(Uporabnik, on_delete=models.CASCADE, db_column='id_uporabnik')
#
#     class Meta:
#         managed = False
#         db_table = 'upravlja'
#         unique_together = (('id_restavracija', 'id_uporabnik'), ('id_restavracija', 'id_uporabnik'),)


class Vloga(models.Model):
    id_vloga = models.AutoField(primary_key=True)
    ime_vloga = models.TextField()

    class Meta:
        managed = False
        db_table = 'vloga'


class Vsebuje(models.Model):
    id_jed = models.ForeignKey(Jed, models.DO_NOTHING, db_column='id_jed', primary_key=True)
    id_sestavine = models.ForeignKey(Sestavine, models.DO_NOTHING, db_column='id_sestavine')

    class Meta:
        managed = False
        db_table = 'vsebuje'
        unique_together = (('id_jed', 'id_sestavine'), ('id_jed', 'id_sestavine'),)


class Uporabnik(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        managed = False
        db_table = 'uporabnik'

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True
