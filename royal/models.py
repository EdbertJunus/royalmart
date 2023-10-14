from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

class Sales(models.Model):
    sales_name = models.CharField(blank=False, max_length=255, verbose_name="sales_name")
    sales_file = models.FileField(blank=False)

    def __str__(self):
        return self.sales_name
    