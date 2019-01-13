from django.contrib import admin
from .models import *

# Give the admin option to add and edit all database entries.
admin.register(Jed, JedilniList, JediNarocila, Restavracija, TipRestavracije, Naslov, Posta, Uporabnik,
               AdminUporabnik, Narocilo, Mize)(admin.ModelAdmin)
