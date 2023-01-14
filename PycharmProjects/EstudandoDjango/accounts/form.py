from django.forms import ModelForm
from .models import Contato


class ContatoForm(ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'sobrenome', 'telefone', 'sobre', 'categoria', 'foto']
