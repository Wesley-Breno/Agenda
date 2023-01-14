from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .form import ContatoForm
from .models import Contato


def login(request):
    usuario_logado = str(auth.get_user(request))
    if usuario_logado != 'AnonymousUser':
        messages.add_message(request, messages.ERROR, f'Voce ja esta logado como: {usuario_logado}')
        return redirect('home')

    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    if not usuario or not senha:
        messages.add_message(request, messages.ERROR, 'Preencha os campos ques estão vazios.')
        return render(request, 'accounts/login.html')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.add_message(request, messages.ERROR, 'Nome de usuario ou senha invalidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Você fez login com sucesso.')
        return redirect('home')


@login_required(redirect_field_name='login')
def logout(request):
    auth.logout(request)
    return redirect('home')


def cadastro(request):
    usuario_logado = str(auth.get_user(request))
    if usuario_logado != 'AnonymousUser':
        messages.add_message(request, messages.ERROR, f'Voce ja esta logado como: {usuario_logado}')
        messages.add_message(request, messages.ERROR, f'Saia da sua conta antes de criar outra.')
        return redirect('home')

    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not usuario or not email or not senha or not senha2:
        messages.add_message(request, messages.ERROR, 'Preencha os campos ques estão vazios.')
        return render(request, 'accounts/cadastro.html')

    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'Confirme sua senha corretamente.')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 8:
        messages.add_message(request, messages.ERROR, 'Senha muito fraca! Coloque no minimo 8 caracteres contendo numeros e letras maiusculas e minusculas.')
        return render(request, 'accounts/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'O email que voce informou é invalido.')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.ERROR, 'Ja existe um usuario com esse nome.')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, 'Ja existe um cadastro com esse endereço de email.')
        return render(request, 'accounts/cadastro.html')

    messages.add_message(request, messages.SUCCESS, 'Usuario cadastrado com sucesso! Faça login e acesse sua agenda.')
    user = User.objects.create_user(username=usuario, email=email, password=senha)
    user.save()

    return redirect('login')


def adicionar_contato(request):
    usuario_logado = str(auth.get_user(request))
    if usuario_logado == 'AnonymousUser':
        messages.add_message(request, messages.ERROR, f'Voce não pode adicionar um contato sem estar logado na sua conta.')
        return redirect('sobre')

    data = {}

    if request.method != 'POST':
        form = ContatoForm()
        data['form'] = form
        return render(request, 'accounts/formulario.html', data)

    form = ContatoForm(request.POST, request.FILES)

    if form.is_valid():
        contato = form.save(commit=False)
        contato.user = request.user
        contato.save()
        messages.add_message(request, messages.SUCCESS, f'Contato salvo com sucesso.')
        return redirect('home')

    else:
        form = ContatoForm(request.POST)
        data['form'] = form
        messages.add_message(request, messages.ERROR, f'Alguns dos dados informados estão invalidos!')
        return render(request, 'accounts/formulario.html', data)


def atualizar_contato(request, pk):
    usuario_logado = str(auth.get_user(request))
    if usuario_logado == 'AnonymousUser':
        messages.add_message(request, messages.ERROR,
                             f'Voce não pode atualizar um contato sem estar logado na sua conta.')
        return redirect('sobre')

    data = {}
    try:
        contato = Contato.objects.filter(user=request.user).get(pk=pk)
    except:
        return redirect('home')

    if request.method != 'POST':
        form = ContatoForm(request.POST or None, request.FILES or None, instance=contato)
        data['form'] = form
        data['atualizar'] = True
        return render(request, 'accounts/formulario.html', data)

    form = ContatoForm(request.POST or None, request.FILES or None, instance=contato)

    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, f'Contato atualizado com sucesso.')
        return redirect('home')

    form = ContatoForm(request.POST or None, request.FILES or None, instance=contato)
    data['form'] = form
    data['atualizar'] = True
    messages.add_message(request, messages.ERROR, f'Alguns dos dados informados estão invalidos!')
    return render(request, 'accounts/formulario.html', data)


def deletar_contato(request, pk):
    usuario_logado = str(auth.get_user(request))
    if usuario_logado == 'AnonymousUser':
        messages.add_message(request, messages.ERROR,
                             f'Voce não pode apagar um contato sem estar logado na sua conta.')
        return redirect('sobre')

    try:
        contato = Contato.objects.filter(user=request.user).get(pk=pk)
    except:
        return redirect('home')

    contato.delete()
    messages.add_message(request, messages.SUCCESS, f'Contato deletado com sucesso.')
    return redirect('home')


def busca(request):
    usuario_logado = str(auth.get_user(request))
    if usuario_logado == 'AnonymousUser':
        messages.add_message(request, messages.ERROR,
                             f'Voce não pode fazer uma pesquisa sem estar logado na sua conta.')
        return redirect('sobre')

    data = {}

    data['todos_contatos'] = Contato.objects.all().filter(user=request.user)
    if len(data['todos_contatos']) > 0:
        busca = request.GET.get('busca')

        data['busca'] = busca
        data['tem_usuario'] = False

        data['contatos'] = Contato.objects.order_by('nome').filter(
            nome__icontains=busca,
            user=request.user
        )

        if len(data['contatos']) > 0:
            data['tem_usuario'] = True

        return render(request, 'accounts/busca.html', data)

    else:
        return redirect('home')
