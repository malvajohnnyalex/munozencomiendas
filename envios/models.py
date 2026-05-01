from django.db import models
from django.core.exceptions import ValidationError
from config.choices import EstadoEnvio, EstadoGeneral
from clientes.models import Cliente
from rutas.models import Ruta


class Encomienda(models.Model):
    remitente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='encomiendas_enviadas'
    )

    destinatario = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='encomiendas_recibidas'
    )

    ruta = models.ForeignKey(
        Ruta,
        on_delete=models.CASCADE
    )

    descripcion = models.TextField()
    peso = models.DecimalField(max_digits=8, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    estado = models.CharField(
        max_length=2,
        choices=EstadoEnvio.choices,
        default=EstadoEnvio.PENDIENTE
    )

    fecha_envio = models.DateField(auto_now_add=True)
    fecha_entrega_est = models.DateField()

    def __str__(self):
        return f'Encomienda #{self.id} - {self.estado}'

    # 🔴 VALIDACIONES
    def clean(self):
        if self.remitente == self.destinatario:
            raise ValidationError('El remitente y destinatario no pueden ser la misma persona')

        if self.fecha_entrega_est and self.fecha_envio:
            if self.fecha_entrega_est < self.fecha_envio:
                raise ValidationError('La fecha de entrega no puede ser menor que la fecha de envío')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'encomiendas'
        verbose_name = 'Encomienda'
        verbose_name_plural = 'Encomiendas'
        ordering = ['-fecha_envio']


class Empleado(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)

    estado = models.IntegerField(
        choices=EstadoGeneral.choices,
        default=EstadoGeneral.ACTIVO
    )

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.apellidos}, {self.nombres} - {self.cargo}'

    class Meta:
        db_table = 'empleados'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'


class HistorialEstado(models.Model):
    encomienda = models.ForeignKey(
        Encomienda,
        on_delete=models.CASCADE,
        related_name='historial'
    )

    estado = models.CharField(
        max_length=2,
        choices=EstadoEnvio.choices
    )

    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.encomienda.id} - {self.estado}'

    class Meta:
        db_table = 'historial_estados'
        verbose_name = 'Historial de Estado'
        verbose_name_plural = 'Historial de Estados'
        ordering = ['-fecha']