from django.shortcuts import render, redirect
from django.contrib import auth
from accounts.models import Contato


def home(request):
    usuario_logado = str(auth.get_user(request))
    if usuario_logado != 'AnonymousUser':
        data = {}
        data['contatos'] = Contato.objects.all().filter(user=request.user)
        data['tem_contato'] = False

        if len(data['contatos']) > 0:
            data['tem_contato'] = True

        return render(request, 'app/home.html', data)

    return redirect('sobre')


def sobre(request):
    return render(request, 'app/sobre.html')
