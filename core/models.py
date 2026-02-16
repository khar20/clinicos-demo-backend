from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.conf import settings


class AuditableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="id_created_at",
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="id_updated_at",
        related_name="%(class)s_updated",
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="id_deleted_at",
        related_name="%(class)s_deleted",
    )

    is_deleted = models.BooleanField(default=False, db_column="deleted")

    class Meta:
        abstract = True


class Empresa(AuditableModel):
    id = models.AutoField(primary_key=True, db_column="idempresa")
    razon_social = models.CharField(max_length=150)
    nombre_comercial = models.CharField(max_length=150, blank=True, null=True)
    num_documento = models.CharField(max_length=20, db_column="num_document")
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = "empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nombre_comercial or self.razon_social


class TipoPersona(AuditableModel):
    id = models.AutoField(primary_key=True, db_column="idtipo_persona")
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "tipo_persona"

    def __str__(self):
        return self.nombre


class Persona(AuditableModel):
    id = models.AutoField(primary_key=True, db_column="idpersona")
    tipo_persona = models.ForeignKey(
        TipoPersona, on_delete=models.PROTECT, db_column="idtipo_persona"
    )
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = "persona"

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"


class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("El username es obligatorio")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin, AuditableModel):
    id = models.AutoField(primary_key=True, db_column="idusuario")
    empresa = models.ForeignKey(
        Empresa, on_delete=models.SET_NULL, null=True, blank=True, db_column="idempresa"
    )
    persona = models.ForeignKey(
        Persona, on_delete=models.SET_NULL, null=True, blank=True, db_column="idpersona"
    )

    username = models.CharField(max_length=50, unique=True)
    rol = models.CharField(max_length=50, blank=True, null=True)
    estado = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True, db_column="ultimo_login")

    objects = UsuarioManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "usuario"

    def __str__(self):
        return self.username


class Paciente(AuditableModel):
    id = models.AutoField(primary_key=True, db_column="idpaciente")
    persona = models.OneToOneField(
        Persona, on_delete=models.CASCADE, db_column="idpersona"
    )
    historia_clinica = models.CharField(max_length=50, blank=True, null=True)
    grupo_sanguineo = models.CharField(max_length=5, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "paciente"

    def __str__(self):
        return f"Paciente: {self.persona}"


class Servicio(AuditableModel):
    id = models.AutoField(primary_key=True, db_column="idservicio")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    duracion_minutos = models.IntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = "servicio"

    def __str__(self):
        return self.nombre


class CitaMedica(AuditableModel):
    ESTADO_CHOICES = [
        ("PROGRAMADA", "Programada"),
        ("CONFIRMADA", "Confirmada"),
        ("CANCELADA", "Cancelada"),
        ("ATENDIDA", "Atendida"),
    ]

    id = models.AutoField(primary_key=True, db_column="idcitamedica")
    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, db_column="idpaciente", related_name="citas"
    )
    servicio = models.ForeignKey(
        Servicio, on_delete=models.PROTECT, db_column="idservicio"
    )

    fecha = models.DateField()
    hora = models.TimeField()

    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="PROGRAMADA"
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "citamedica"

    def __str__(self):
        return f"Cita {self.id} - {self.fecha}"
