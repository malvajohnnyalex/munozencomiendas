from django.contrib import admin
from .models import Encomienda, Empleado, HistorialEstado

@admin.register(Encomienda)
class EncomiendaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'remitente',
        'destinatario',
        'ruta',
        'peso',
        'precio',
        'estado',
        'fecha_envio'
    )
    list_filter = ('estado', 'ruta')
    search_fields = ('descripcion',)


admin.site.register(Empleado)
admin.site.register(HistorialEstado)