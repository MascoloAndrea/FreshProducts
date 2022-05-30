from django.db import DJANGO_VERSION_PICKLE_KEY, models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
'''
Author.objects.filter(name__contains='Terry')
data = Students.objects.all()
#django.contrib.auth.get_user_model()
'''

class Licenze(models.Model):
    Code = models.CharField(max_length=100, primary_key=True)
    Data_sottoscrizione = models.DateField('Data_sottoscrizione')
    Data_scadenza = models.DateField('Data_scadenza')
    Prezzo = models.IntegerField()

class Punto_vendita(models.Model):
    Shop_code = models.AutoField(primary_key=True) # auto increment con id
    Nome = models.CharField(max_length=200)
    Indirizzo = models.CharField(max_length=200)
    Civico = models.CharField(max_length=200)
    Citta = models.CharField(max_length=200)
    Cap = models.IntegerField()
    Code = models.ForeignKey(Licenze, on_delete=models.CASCADE)
    #Username = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.DO_NOTHING,
        null=True, 
        blank=True,
    )
    
'''
class Credenziali(models.Model):
    Username = models.CharField(primary_key=True, max_length=200)
    Password = models.CharField(max_length=200)
    Shop_code = models.ForeignKey(Punto_vendita, on_delete=models.CASCADE)
'''
class Prodotto(models.Model):
    Barcode = models.CharField(max_length=100, primary_key=True)
    Nome = models.CharField(max_length=200)
    Marca = models.CharField(max_length=200)

class Magazzino(models.Model):
    class Meta:
        unique_together = (('Barcode', 'Shop_code'),)
    Barcode = models.ForeignKey(Prodotto, on_delete=models.CASCADE) # primary key
    Shop_code = models.ForeignKey(Punto_vendita, on_delete=models.CASCADE) # primary key
    Quantita = models.IntegerField()
    Reparto = models.CharField(max_length=200)
    Prezzo = models.FloatField()
    Scadenza = models.DateField(null=True, blank=True)

'''
models.AutoField()
models.IntegerField()
models.BooleanField()
'''