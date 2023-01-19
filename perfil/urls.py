from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.logout, name='logout'),
    path('adicionarcontato/', views.adicionar, name='adicionar'),
    path('apagar/<int:pk>', views.apagar, name='apagar'),
    path('atualizar/<int:pk>', views.atualizar, name='atualizar'),
    path('busca/', views.busca, name='busca')
]
