from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

class Sales(models.Model):
    periode = models.CharField(blank=False, max_length=255, null=True)
    fileSales = models.FileField(null=True)

    def __str__(self):
        return self.periode

class SalesDetail(models.Model):
    salesId = models.CharField(blank=False, max_length=255, default='')
    namaProduk = models.CharField(blank=False, max_length=255)
    kode = models.IntegerField(blank=False)
    qty = models.IntegerField(blank=False)
    jumlah = models.DecimalField(blank=False, max_digits=19, decimal_places=2)
    hargaPokok = models.DecimalField(blank=False, max_digits=19, decimal_places=2)


    def __str__(self):
        return self.namaProduk
    
class Stock(models.Model):
    kode = models.IntegerField(blank=False)
    namaProduk = models.CharField(blank=False, max_length=255)
    bs = models.IntegerField(blank=False)
    total = models.IntegerField(blank=False)
    supplier = models.CharField(blank=False, max_length=255, default='')

    def __str__(self):
        return self.namaProduk
    