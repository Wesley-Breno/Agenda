from django.db import models
from django.contrib.auth import get_user_model


class Categoria(models.Model):
    nome = models.CharField(max_length=120)

    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=120)
    sobrenome = models.CharField(max_length=120, blank=True, null=True)
    telefone = models.CharField(max_length=17)
    sobre = models.CharField(max_length=400, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    foto = models.ImageField(null=True, blank=True, upload_to='fotos/%Y/%m/')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
