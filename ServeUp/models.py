# This is an auto-generated Django model module.
from django.db import models

# TODO: * Make sure each ForeignKey has `on_delete` set to the desired behavior.


class Jed(models.Model):
    id_jed = models.IntegerField(primary_key=True)
    id_jedilni_list = models.ForeignKey('JedilniList', models.DO_NOTHING, db_column='id_jedilni_list')
    id_restavracija = models.ForeignKey('Restavracija', models.DO_NOTHING, db_column='id_restavracija', blank=True, null=True)
    ime_jedi = models.CharField(max_length=256)
    cena = models.FloatField()
    opis = models.CharField(max_length=256)

    class Meta:
        db_table = 'jed'


class JediNarocila(models.Model):
    id_jed = models.ForeignKey(Jed, models.DO_NOTHING, db_column='id_jed', primary_key=True)
    id_narocila = models.ForeignKey('Narocilo', models.DO_NOTHING, db_column='id_narocila')

    class Meta:
        db_table = 'jedi_narocila'
        unique_together = (('id_jed', 'id_narocila'), ('id_jed', 'id_narocila'),)


class JedilniList(models.Model):
    id_jedilni_list = models.IntegerField(primary_key=True)
    vrsta = models.CharField(max_length=256)

    class Meta:
        db_table = 'jedilni_list'


class Narocilo(models.Model):
    id_narocila = models.IntegerField(primary_key=True)
    id_restavracija = models.ForeignKey('Restavracija', models.DO_NOTHING, db_column='id_restavracija')
    id_uporabnik = models.ForeignKey('Uporabnik', models.DO_NOTHING, db_column='id_uporabnik')
    cas_prevzema = models.TimeField()

    class Meta:
        db_table = 'narocilo'


class Naslov(models.Model):
    id_naslov = models.IntegerField(primary_key=True)
    postna_stevilka = models.ForeignKey('Posta', models.DO_NOTHING, db_column='postna_stevilka')
    ulica = models.CharField(max_length=256)
    hisna_stevilka = models.IntegerField()

    class Meta:
        db_table = 'naslov'


class Posta(models.Model):
    postna_stevilka = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    kraj = models.CharField(max_length=256)

    class Meta:
        db_table = 'posta'


class Restavracija(models.Model):
    id_restavracija = models.IntegerField(primary_key=True)
    id_naslov = models.ForeignKey(Naslov, models.DO_NOTHING, db_column='id_naslov')
    id_tip_restavracije = models.ForeignKey('TipRestavracije', models.DO_NOTHING, db_column='id_tip_restavracije')
    ime_restavracije = models.CharField(max_length=256)
    ocena = models.FloatField()

    class Meta:
        db_table = 'restavracija'


class Sestavine(models.Model):
    id_sestavine = models.IntegerField(primary_key=True)
    ime_sestavine = models.CharField(max_length=256)

    class Meta:
        db_table = 'sestavine'


class TipRestavracije(models.Model):
    id_tip_restavracije = models.IntegerField(primary_key=True)
    tip = models.CharField(max_length=256)

    class Meta:
        db_table = 'tip_restavracije'


class Uporabnik(models.Model):
    id_uporabnik = models.IntegerField(primary_key=True)
    id_vloga = models.ForeignKey('Vloga', models.DO_NOTHING, db_column='id_vloga')
    e_mail = models.CharField(db_column='E-mail', max_length=256)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    geslo = models.CharField(max_length=256)

    class Meta:
        db_table = 'uporabnik'


class Upravlja(models.Model):
    id_restavracija = models.ForeignKey(Restavracija, models.DO_NOTHING, db_column='id_restavracija', primary_key=True)
    id_uporabnik = models.ForeignKey(Uporabnik, models.DO_NOTHING, db_column='id_uporabnik')

    class Meta:
        db_table = 'upravlja'
        unique_together = (('id_restavracija', 'id_uporabnik'), ('id_restavracija', 'id_uporabnik'),)


class Vloga(models.Model):
    id_vloga = models.IntegerField(primary_key=True)
    ime_vloga = models.CharField(max_length=256)

    class Meta:
        db_table = 'vloga'


class Vsebuje(models.Model):
    id_jed = models.ForeignKey(Jed, models.DO_NOTHING, db_column='id_jed', primary_key=True)
    id_sestavine = models.ForeignKey(Sestavine, models.DO_NOTHING, db_column='id_sestavine')

    class Meta:
        db_table = 'vsebuje'
        unique_together = (('id_jed', 'id_sestavine'), ('id_jed', 'id_sestavine'),)
