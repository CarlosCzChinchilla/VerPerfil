from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cargar_archivo/', views.cargar_archivo, name='cargar_archivo'),
    path('consultar_datos/', views.consultar_datos, name='consultar_datos'),
    path('resumen_por_fecha/', views.resumen_por_fecha, name='resumen_por_fecha'),
    path('resumen_por_rango/', views.resumen_por_rango, name='resumen_por_rango'),
    path('prueba_mensaje/', views.prueba_mensaje, name='prueba_mensaje'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('resetear/', views.resetear, name='resetear'),
]