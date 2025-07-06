from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone
import re

class CustomUser(AbstractUser):
    # Campos adicionais
    is_store_admin = models.BooleanField(default=False)
    creation_date = models.DateTimeField(default=timezone.now)

    # Campos padrão do AbstractUser já incluem:
    # - id
    # - username
    # - password
    # - email
    # - is_active
    # - is_staff
    # - groups

    def is_in_group(self, group_name):
        return self.groups.filter(name=group_name).exists()

    def __str__(self):
        return self.username

class Architect(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Nome", max_length=100)
    cpf_cnpj = models.CharField(
        "CPF/CNPJ",
        max_length=14,
        unique=True,
        validators=[
            MinLengthValidator(11),
            MaxLengthValidator(14),
        ]
    )
    registration_number = models.CharField("Número de Registro", max_length=20)
    created_at = models.DateTimeField("Data de Criação", default=timezone.now)
    is_active = models.BooleanField("Ativo", default=True)

    def save(self, *args, **kwargs):
        # Remove pontuação antes de salvar
        self.cpf_cnpj = re.sub(r'\D', '', self.cpf_cnpj)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Nome", max_length=100)
    cnpj = models.CharField(
        "CNPJ",
        max_length=14,
        unique=True,
        validators=[
            MinLengthValidator(14),
            MaxLengthValidator(14)
        ]
    )
    address = models.CharField("Endereço", max_length=200)
    created_at = models.DateTimeField("Data de Criação", default=timezone.now)
    is_active = models.BooleanField("Ativa", default=True)

    def save(self, *args, **kwargs):
        # Remove pontuações do CNPJ antes de salvar
        self.cnpj = re.sub(r'\D', '', self.cnpj)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class UserStore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Data de Associação", default=timezone.now)

    class Meta:
        unique_together = ('user', 'store')  # Garante que não haja duplicatas

    def __str__(self):
        return f"{self.user.username} - {self.store.name}"

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    architect = models.ForeignKey(Architect, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    value = models.DecimalField("Valor", max_digits=10, decimal_places=2)
    date = models.DateField("Data da Venda")
    cpf_cnpj = models.CharField(
        "CPF/CNPJ do Cliente",
        max_length=14,
        validators=[
            MinLengthValidator(11),
            MaxLengthValidator(14)
        ]
    )
    nota_fiscal = models.CharField("Nota Fiscal", max_length=12, validators=[MinLengthValidator(1)])
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField("Data de Criação", default=timezone.now)

    def save(self, *args, **kwargs):
        # Remove pontuações do CPF/CNPJ antes de salvar
        self.cpf_cnpj = re.sub(r'\D', '', self.cpf_cnpj)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venda #{self.id}"
