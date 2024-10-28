from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import UploadFileForm, TestMessageForm
import requests

def index(request):
    return render(request, 'main/index.html')

def cargar_archivo(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            response = requests.post('http://127.0.0.1:5000/procesar-mensajes', files={'archivo': archivo})
            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return HttpResponse("Error al procesar el archivo", status=500)
    else:
        form = UploadFileForm()
    return render(request, 'main/cargar_archivo.html', {'form': form})

def consultar_datos(request):
    response = requests.get('http://127.0.0.1:5000/consultar-datos')
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return HttpResponse("Error al consultar los datos", status=500)

def resumen_por_fecha(request):
    fecha = request.GET.get('fecha')
    response = requests.get(f'http://127.0.0.1:5000/resumen-por-fecha?fecha={fecha}')
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return HttpResponse("Error al consultar el resumen por fecha", status=500)

def resumen_por_rango(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    response = requests.get(f'http://127.0.0.1:5000/resumen-por-rango?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}')
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return HttpResponse("Error al consultar el resumen por rango", status=500)

def prueba_mensaje(request):
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        response = requests.post('http://127.0.0.1:5000/procesar-mensajes', data={'mensaje': mensaje})
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return HttpResponse("Error al procesar el mensaje", status=500)
    return render(request, 'main/prueba_mensaje.html')

def ayuda(request):
    return render(request, 'main/ayuda.html')

def resetear(request):
    response = requests.post('http://127.0.0.1:5000/resetear')
    if response.status_code == 200:
        return JsonResponse({"message": "Base de datos reseteada"})
    else:
        return HttpResponse("Error al resetear la base de datos", status=500)