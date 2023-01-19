from django.shortcuts import render, redirect
from django.contrib import auth
from perfil.models import Contato


def home(request):
    try:
        usuario_logado = str(auth.get_user(request))
        if usuario_logado == 'AnonymousUser':
            return redirect('sobre')

        data = {}
        data['contatos'] = Contato.objects.all().filter(user=request.user)
        if len(data['contatos']) > 0:
            data['tem_contato'] = True

        return render(request, 'home/home.html', data)

    except:
        return render(request, 'home/404.html')


def sobre(request):
    return render(request, 'home/sobre.html')
