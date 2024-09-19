# my_django_app/urls.py
# my_django_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('ir_registro/', views.ir_registro, name='ir_registro'),
    path('ir_verificacion/', views.ir_verificacion, name='ir_verificacion'),
    path('verificar/', views.verificar, name='verificar'),
    path('restablecer/', views.nueva_contrasena, name='restablecer'),
    path('signin/', views.signin, name='signin'),
    path('principal/', views.principal, name='principal'),
    path('buscar_usuario/', views.buscar_usuario, name='buscar_usuario'),  # Nueva ruta PARA BUSCAR USUARIO-----------------------------
]