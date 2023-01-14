from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('adicionarcontato/', views.adicionar_contato, name='adicionar_contato'),
    path('atualizarcontato/<int:pk>', views.atualizar_contato, name='atualizar_contato'),
    path('deletarcontato/<int:pk>', views.deletar_contato, name='deletar_contato'),
    path('busca/', views.busca, name='busca')
]
