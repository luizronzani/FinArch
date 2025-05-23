from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

class CustomUser(AbstractUser):
    is_architect = models.BooleanField(default=False)
    is_store_admin = models.BooleanField(default=False)
    allowed_stores = models.ManyToManyField('Store', blank=True)
    def is_in_group(self, group_name):
        return self.groups.filter(name=group_name).exists()

class Architect(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, validators=[MinLengthValidator(11)])
    registration_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='managed_stores')

    def __str__(self):
        return self.name

class Sale(models.Model):
    architect = models.ForeignKey(Architect, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    cpf = models.CharField(max_length=14, validators=[MinLengthValidator(11)])
    nota_fiscal = models.CharField(max_length=12, validators=[MinLengthValidator(1)])
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale {self.nota_fiscal} for {self.architect.name}"