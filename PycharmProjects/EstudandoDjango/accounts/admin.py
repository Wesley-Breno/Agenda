from django.contrib import admin
from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'categoria', 'user')


admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)
