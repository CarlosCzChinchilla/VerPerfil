# my_django_app/views.py
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistroForm, RestablecerContraForm, NuevaContrasenaForm
from django.http import JsonResponse
import requests
from django.http import HttpResponse
import json

def home(request):
    return render(request, 'login.html')

def login(request):
    return render(request, 'login.html')

def principal(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        return render(request, 'PantallaInicial.html', {'user_id': user_id})
    else:
        return redirect('login')

from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                'id': form.cleaned_data['id'],
                'password': form.cleaned_data['password']
            }
            try:
                response = requests.post('http://localhost:5000/login', json=data)
                response.raise_for_status()  # Verifica que no hubo errores en la respuesta
                
                if response.status_code == 200:
                    # Redirige al usuario a la página principal
                    response = redirect('principal')
                    response.set_cookie('user_id', data['id']) 
                    return response
                else:
                    # Maneja los errores de la API
                    respuesta = response.json()
                    return render(request, 'login.html', {'form': form, 'error_message': respuesta.get('error', 'Login failed')})
            except requests.exceptions.RequestException:
                # Maneja errores de conexión con la API
                return render(request, 'login.html', {'form': form, 'error_message': 'Error en la conexión con el servidor'})
            except ValueError:
                # Maneja errores de respuesta JSON
                return render(request, 'login.html', {'form': form, 'error_message': 'Error en la respuesta del servidor'})
        else:
            # Maneja datos de formulario inválidos
            return render(request, 'login.html', {'form': form, 'error_message': 'Datos del formulario inválidos'})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(f"Datos enviados al servidor: {data}")  # Verifica qué datos estás enviando
            response = requests.post('http://localhost:5000/registro', json=data)
            if response.status_code == 201:
                return redirect('login')  # Redirige a otra página en caso de éxito
            else:
                print(response.status_code)
                print(response.json())  # Verifica qué error está devolviendo el servidor
                return JsonResponse({'message': 'Registration failed'}, status=400)
    else:
        form = RegistroForm()
    return render(request, 'RegistroUsuario.html', {'form': form})

def ir_registro(request):
    return render(request, 'RegistroUsuario.html')

def ir_verificacion(request):
    return render(request, 'RestablecerContra.html')

def verificar(request):
    if request.method == 'POST':
        form = RestablecerContraForm(request.POST)
        if form.is_valid():
            data = {
                'email': form.cleaned_data['email'],
                'registration': form.cleaned_data['registration']
            }
            print(f"Datos enviados al servidor: {data}")  # Verifica qué datos estás enviando
            try:
                response = requests.post('http://localhost:5000/verificar', json=data)
                response.raise_for_status()
                
                if response.status_code == 200:
                    # Almacenar el ID verificado en la sesión
                    request.session['verified_id'] = form.cleaned_data['registration']
                    return redirect('nueva_contrasena')
                else:
                    return JsonResponse({'message': 'Datos incorrectos'}, status=400)
            except requests.exceptions.RequestException:
                return JsonResponse({'error': 'Error en la conexión con el servidor'}, status=500)
        else:
            return JsonResponse({'error': 'Datos del formulario inválidos'}, status=400)
    else:
        form = RestablecerContraForm()
    return render(request, 'RestablecerContra.html', {'form': form})

def nueva_contrasena(request):
    if request.method == 'POST':  # Django usa POST en formularios, aunque sea PUT para la API
        form = NuevaContrasenaForm(request.POST)
        if form.is_valid():
            data = {
                'email': form.cleaned_data['email'],
                'id': form.cleaned_data['registroAcademico'],
                'nueva_contrasena': form.cleaned_data['contrasena']
            }
            try:
                # Cambiar a método PUT
                response = requests.put('http://localhost:5000/restablecer', json=data)
                
                if response.status_code == 200:
                    return redirect('login')  # Redirigir al login si es exitoso
                else:
                    return JsonResponse({'message': 'Error al restablecer la contraseña'}, status=response.status_code)
            except requests.exceptions.RequestException:
                return JsonResponse({'error': 'Error en la conexión con el servidor'}, status=500)
        else:
            return JsonResponse({'error': 'Datos del formulario inválidos'}, status=400)
    else:
        form = NuevaContrasenaForm()  # En caso de GET, se envía el formulario vacío
    return render(request, 'NuevaContraseña.html', {'form': form})


# BUSCAR USUARIOS POR MEDIO DE ID--------------------------------------------------------------------------------------------------------------------
from django.shortcuts import render
from .forms import BuscarUsuarioForm
    
# formulario para id de usuario
from django.shortcuts import render
from django.http import JsonResponse
from .forms import BuscarUsuarioForm
import requests


def buscar_usuario(request):
    if request.method == 'GET':  # Cambiado a GET
        form = BuscarUsuarioForm(request.GET)  # Cambiado a request.GET
        if form.is_valid():
            user_id = form.cleaned_data['id']  # Obtener el ID del formulario
            data = {
                'id': user_id
            }
            try:
                response = requests.get('http://localhost:5000/buscar_usuario', params=data)
                response.raise_for_status()
                
                if response.status_code == 200:
                    usuario = response.json()
                    return render(request, 'VerPerfil.html', {'usuario': usuario})
                else:
                    return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
            except requests.exceptions.RequestException:
                return JsonResponse({'error': 'Error en la conexión con el servidor'}, status=500)
        else:
            return JsonResponse({'error': 'Datos del formulario inválidos'}, status=400)
    else:
        form = BuscarUsuarioForm()
    return render(request, 'VerPerfil.html', {'form': form})