from django.contrib import admin

# Register your models here.
#from .models import Credenziali
from .models import Prodotto, Magazzino, Licenze, Punto_vendita

admin.site.register(Licenze)
admin.site.register(Punto_vendita)
#admin.site.register(Credenziali)
admin.site.register(Prodotto)
admin.site.register(Magazzino)