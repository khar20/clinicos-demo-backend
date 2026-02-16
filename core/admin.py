from django.contrib import admin
from .models import (
    Empresa,
    TipoPersona,
    Persona,
    Usuario,
    Paciente,
    Servicio,
    CitaMedica,
)


# Custom User Admin
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("username", "rol", "empresa", "estado")
    search_fields = ("username",)


class CitaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "hora", "paciente", "servicio", "estado")
    list_filter = ("estado", "fecha")


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Empresa)
admin.site.register(TipoPersona)
admin.site.register(Persona)
admin.site.register(Paciente)
admin.site.register(Servicio)
admin.site.register(CitaMedica, CitaAdmin)
