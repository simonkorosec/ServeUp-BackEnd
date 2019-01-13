from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from ServeUp.Views.userManager import MyUserManager


# TODO: * Make sure each ForeignKey has `on_delete` set to the desired behavior.

class AdminUporabnik(AbstractBaseUser):
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
        db_table = 'admin_uporabnik'


class Jed(models.Model):
    id_jed = models.AutoField(primary_key=True)
    id_jedilni_list = models.ForeignKey('JedilniList', models.DO_NOTHING, db_column='id_jedilni_list')
    id_restavracija = models.ForeignKey('Restavracija', models.DO_NOTHING,
                                        db_column='id_restavracija', blank=True,
                                        null=True)
    ime_jedi = models.TextField()
    cena = models.FloatField()
    opis_jedi = models.TextField()

    class Meta:
        managed = False
        db_table = 'jed'


class JediNarocila(models.Model):
    id_jedi_narocila = models.AutoField(primary_key=True)
    id_jed = models.ForeignKey('Jed', on_delete=models.CASCADE, db_column='id_jed')
    id_narocila = models.ForeignKey('Narocilo', on_delete=models.CASCADE, db_column='id_narocila')
    kolicina = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'jedi_narocila'


class JedilniList(models.Model):
    id_jedilni_list = models.AutoField(primary_key=True)
    vrsta = models.TextField()

    class Meta:
        managed = False
        db_table = 'jedilni_list'


class Narocilo(models.Model):
    id_narocila = models.AutoField(primary_key=True)
    id_restavracija = models.ForeignKey('Restavracija', models.DO_NOTHING, db_column='id_restavracija')
    id_uporabnik = models.ForeignKey('Uporabnik', models.DO_NOTHING, db_column='id_uporabnik')
    cas_prevzema = models.DateTimeField()
    cas_narocila = models.DateTimeField()
    status = models.IntegerField()
    checked_in = models.BooleanField()
    id_miza = models.TextField(null=True)

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
    id_naslov = models.ForeignKey(Naslov, models.DO_NOTHING,
                                  db_column='id_naslov')
    id_tip_restavracije = models.ForeignKey('TipRestavracije',
                                            models.DO_NOTHING,
                                            db_column='id_tip_restavracije')
    id_admin = models.ForeignKey('AdminUporabnik', on_delete=models.SET_NULL,
                                 db_column='id_admin', blank=True, null=True)
    ime_restavracije = models.TextField()
    ocena = models.FloatField(blank=True, null=True)
    slika = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'restavracija'


class TipRestavracije(models.Model):
    id_tip_restavracije = models.AutoField(primary_key=True)
    tip = models.TextField()

    class Meta:
        managed = False
        db_table = 'tip_restavracije'


class Uporabnik(models.Model):
    id_uporabnik = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'uporabnik'


class Nudi(models.Model):
    id_restavracija = models.ForeignKey('Restavracija', models.DO_NOTHING, db_column='id_restavracija',
                                        primary_key=True)
    id_jedilni_list = models.ForeignKey('JedilniList', models.DO_NOTHING, db_column='id_jedilni_list')

    class Meta:
        managed = False
        db_table = 'nudi'
        unique_together = (('id_restavracija', 'id_jedilni_list'),)


class Mize(models.Model):
    id_restavracija = models.ForeignKey('Restavracija', on_delete=models.CASCADE, db_column='id_restavracija',
                                        primary_key=True)
    id_miza = models.TextField()

    class Meta:
        managed = False
        db_table = 'mize'
        unique_together = (('id_restavracija', 'id_miza'),)


class RestavracijaPodatki(models.Model):
    """
    View for restaurant data.
    Don't modify
    """
    id_restavracija = models.IntegerField(blank=True, primary_key=True)
    ime_restavracije = models.TextField(blank=True, null=True)
    ocena = models.FloatField(blank=True, null=True)
    tip = models.TextField(blank=True, null=True)
    ulica = models.TextField(blank=True, null=True)
    hisna_stevilka = models.IntegerField(blank=True, null=True)
    postna_stevilka = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    kraj = models.TextField(blank=True, null=True)
    slika = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'restavracija_podatki'


class JediNarocilaPodatki(models.Model):
    id_restavracija = models.IntegerField(blank=True, null=True)
    id_narocila = models.IntegerField(blank=True, primary_key=True)
    id_jed = models.IntegerField(blank=True, null=True)
    ime_jedi = models.TextField(blank=True, null=True)
    opis_jedi = models.TextField(blank=True, null=True)
    cena = models.FloatField(blank=True, null=True)
    kolicina = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    cas_narocila = models.DateTimeField()
    cas_prevzema = models.DateTimeField()
    id_uporabnik = models.IntegerField(blank=True, null=True)
    checked_in = models.BooleanField()
    id_miza = models.TextField()

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'jedi_narocila_podatki'
