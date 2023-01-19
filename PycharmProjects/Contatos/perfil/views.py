from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from django.contrib import auth
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User
from .form import ContatoForm
from .models import Contato


def login(request):
    try:
        if str(get_user(request)) == 'AnonymousUser':
            if request.method != 'POST':
                return render(request, 'perfil/login.html')

            nome = request.POST.get('nome')
            senha = request.POST.get('senha')

            if not nome or not senha:
                messages.add_message(request, messages.ERROR, 'Informe seu nome de usuario e senha.')
                return render(request, 'perfil/login.html')

            user = auth.authenticate(request, username=nome, password=senha)

            if not user:
                messages.add_message(request, messages.ERROR, 'Usuario não encontrado. Reveja o nome de usuario e senha.')
                return render(request, 'perfil/login.html')
            else:
                auth.login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Você fez login com sucesso.')
                return redirect('home')

        else:
            return redirect('home')

    except:
        return render(request, 'home/404.html')


def cadastro(request):
    try:
        if str(get_user(request)) == 'AnonymousUser':
            if request.method != 'POST':
                return render(request, 'perfil/cadastro.html')

            nome = request.POST.get('nome')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            senha2 = request.POST.get('senha2')

            if not nome or not email or not senha or not senha2:
                messages.add_message(request, messages.ERROR, 'Adicione os campos restantes.')
                return render(request, 'perfil/cadastro.html')

            try:
                validate_email(email)
            except:
                messages.add_message(request, messages.ERROR, 'O email que você informou é invalido.')
                return render(request, 'perfil/cadastro.html')

            if User.objects.filter(email=email).exists():
                messages.add_message(request, messages.ERROR, 'Ja existe um usuario com este endereço de email.')
                return render(request, 'perfil/cadastro.html')

            if User.objects.filter(username=nome).exists():
                messages.add_message(request, messages.ERROR, 'Ja existe um usuario com este nome de usuario.')
                return render(request, 'perfil/cadastro.html')

            if senha != senha2:
                messages.add_message(request, messages.ERROR, 'Confirme a senha corretamente.')
                return render(request, 'perfil/cadastro.html')

            if len(senha) < 8:
                messages.add_message(request, messages.ERROR, 'Sua senha é muito curta. Adicione uma senha mais longa e forte.')
                return render(request, 'perfil/cadastro.html')

            if len(nome) < 3:
                messages.add_message(request, messages.ERROR, 'Nome de usuario não pode ter menos de 3 caracteres.')
                return render(request, 'perfil/cadastro.html')

            messages.add_message(request, messages.SUCCESS, 'Usuario cadastrado com sucesso.')
            user = User.objects.create_user(username=nome, email=email, password=senha)
            user.save()

            return redirect('login')

        else:
            return redirect('home')

    except:
        return render(request, 'home/404.html')


def logout(request):
    try:
        if str(get_user(request)) == 'AnonymousUser':
            return redirect('sobre')
        else:
            auth.logout(request)
            return redirect('sobre')

    except:
        return render(request, 'home/404.html')


def adicionar(request):
    try:
        if str(get_user(request)) == 'AnonymousUser':
            return redirect('sobre')

        else:
            data = {}
            form = ContatoForm(request.POST, request.FILES)

            if form.is_valid():
                contato = form.save(commit=False)
                contato.user = request.user
                contato.save()
                messages.add_message(request, messages.SUCCESS, 'Contato salvo com sucesso.')
                return redirect('home')

            data['form'] = form
            data['adicionar_atualizar'] = 'adicionar'
            return render(request, 'perfil/formulario.html', data)

    except:
        return render(request, 'home/404.html')


def apagar(request, pk):
    try:
        if str(get_user(request)) == 'AnonymousUser':
            return redirect('sobre')

        else:
            contato = Contato.objects.filter(user=request.user).get(pk=pk)
            contato.delete()
            messages.add_message(request, messages.SUCCESS, 'Contato excluido com sucesso.')
            return redirect('home')

    except:
        return render(request, 'home/404.html')


def atualizar(request, pk):
    try:
        if str(get_user(request)) == 'AnonymousUser':
            return redirect('sobre')

        else:
            data = {}
            contato = Contato.objects.filter(user=request.user).get(pk=pk)
            form = ContatoForm(request.POST or None, request.FILES or None, instance=contato)

            if form.is_valid():
                contato = form.save(commit=False)
                contato.user = request.user
                contato.save()
                messages.add_message(request, messages.SUCCESS, 'Contato atualizado com sucesso.')
                return redirect('home')

            data['form'] = form
            data['adicionar_atualizar'] = 'atualizar'
            return render(request, 'perfil/formulario.html', data)

    except:
        return render(request, 'home/404.html')


def busca(request):
    try:
        if str(get_user(request)) == 'AnonymousUser':
            return redirect('sobre')

        else:
            busca = request.GET.get('busca')

            data = {}
            data['contatos'] = Contato.objects.order_by('nome').filter(
                nome__icontains=busca,
                user=request.user
            )
            if len(data['contatos']) > 0:
                data['tem_pesquisa'] = True
            else:
                data['busca'] = busca

            return render(request, 'home/busca.html', data)

    except:
        return render(request, 'home/404.html')

