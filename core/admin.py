from django.contrib import admin
from .models import MedicosEspecialidad,Cita,Soporte,RegistroMedico,Paciente

# Register your models here.

class CitasAdmin(admin.ModelAdmin):
    list_display=["nombre","correo","telefono","fecha_cita","especialidadMedico","descripcion"]
    list_editable=["fecha_cita"]
    search_fields=["nombre",]
    list_filter=["nombre","especialidadMedico"]
    list_per_page=[5]


class RegistroMedicoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'cita', 'especialidad', 'fecha_registro')
    search_fields = ('paciente', 'especialidad__especialidad', 'cita__nombre')
    list_filter = ('fecha_registro', 'especialidad')

admin.site.register(MedicosEspecialidad)
admin.site.register(Cita)
admin.site.register(Soporte)
admin.site.register(RegistroMedico)
