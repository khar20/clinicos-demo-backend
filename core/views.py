from rest_framework import viewsets
from .models import Empresa, Persona, Usuario, Paciente, Servicio, CitaMedica
from .serializers import (
    EmpresaSerializer,
    PersonaSerializer,
    UsuarioSerializer,
    PacienteSerializer,
    ServicioSerializer,
    CitaMedicaSerializer,
)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.filter(is_deleted=False)
    serializer_class = EmpresaSerializer


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.filter(is_deleted=False)
    serializer_class = PersonaSerializer
    filterset_fields = ["documento", "apellidos"]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.filter(is_deleted=False)
    serializer_class = UsuarioSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.filter(is_deleted=False)
    serializer_class = PacienteSerializer
    filterset_fields = ["historia_clinica"]


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.filter(is_deleted=False)
    serializer_class = ServicioSerializer


class CitaMedicaViewSet(viewsets.ModelViewSet):
    queryset = CitaMedica.objects.filter(is_deleted=False)
    serializer_class = CitaMedicaSerializer
    filterset_fields = ["fecha", "estado", "paciente"]
