from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Empresa, Persona, Paciente, Servicio, CitaMedica


@admin.register(Usuario)
class CustomUsuarioAdmin(UserAdmin):
    list_display = ("username", "email", "rol", "empresa", "is_active", "is_staff")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Información Adicional",
            {"fields": ("empresa", "persona", "rol", "is_deleted")},
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Información Adicional", {"fields": ("email", "empresa", "persona", "rol")}),
    )


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("razon_social", "get_documento", "telefono", "is_active")
    search_fields = ("razon_social", "num_documento")

    def get_documento(self, obj):
        return obj.num_documento

    get_documento.short_description = "RUC/Documento"


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ("apellidos", "nombres", "documento", "is_active")
    search_fields = ("apellidos", "nombres", "documento")


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("get_nombre_completo", "historia_clinica", "grupo_sanguineo")
    search_fields = ("persona__apellidos", "persona__nombres", "historia_clinica")

    def get_nombre_completo(self, obj):
        return obj.persona

    get_nombre_completo.short_description = "Paciente"


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "duracion_minutos", "is_active")


@admin.register(CitaMedica)
class CitaMedicaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "hora", "paciente", "servicio", "estado")
    list_filter = ("estado", "fecha")
    search_fields = ("paciente__persona__apellidos", "paciente__persona__nombres")
