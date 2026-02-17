from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class AuditableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_%(class)s_set",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_%(class)s_set",
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="deleted_%(class)s_set",
    )

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Empresa(AuditableModel):
    razon_social = models.CharField(max_length=150)
    nombre_comercial = models.CharField(max_length=150, blank=True, null=True)
    num_documento = models.CharField(max_length=20, unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    logo = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "empresas"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.razon_social


class Persona(AuditableModel):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "personas"
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        indexes = [
            models.Index(fields=["apellidos", "nombres"]),
            models.Index(fields=["documento"]),
        ]

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"


class Usuario(AbstractUser):
    empresa = models.ForeignKey(
        Empresa, on_delete=models.SET_NULL, null=True, blank=True
    )
    persona = models.ForeignKey(
        Persona, on_delete=models.SET_NULL, null=True, blank=True
    )
    rol = models.CharField(max_length=50, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "usuarios"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username


class Paciente(AuditableModel):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    historia_clinica = models.CharField(max_length=50, unique=True)
    grupo_sanguineo = models.CharField(max_length=5, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "pacientes"
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"HC: {self.historia_clinica} - {self.persona}"


class Servicio(AuditableModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    duracion_minutos = models.IntegerField(default=30)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "servicios"
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre


class CitaMedica(AuditableModel):
    ESTADO_CHOICES = [
        ("PROGRAMADA", "Programada"),
        ("CONFIRMADA", "Confirmada"),
        ("CANCELADA", "Cancelada"),
        ("REALIZADA", "Realizada"),
    ]

    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, related_name="citas"
    )
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="PROGRAMADA"
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "citas_medicas"
        verbose_name = "Cita Médica"
        verbose_name_plural = "Citas Médicas"
        indexes = [
            models.Index(fields=["fecha", "hora"]),
            models.Index(fields=["estado"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["fecha", "hora", "servicio"],
                name="unique_cita_servicio_datetime",
            )
        ]

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.paciente}"
