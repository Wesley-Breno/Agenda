from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Categoria(models.Model):
    nome = models.CharField(max_length=120)

    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=120)
    sobrenome = models.CharField(max_length=120, null=True, blank=True)
    numero = models.CharField(max_length=16)
    sobre = models.CharField(max_length=400, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    foto = models.ImageField(null=True, blank=True, upload_to='fotos/%Y/%m')
    data_criacao = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
