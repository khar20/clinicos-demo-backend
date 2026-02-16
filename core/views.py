from rest_framework import viewsets, permissions
from .models import (
    Empresa,
    TipoPersona,
    Persona,
    Usuario,
    Paciente,
    Servicio,
    CitaMedica,
)
from .serializers import (
    EmpresaSerializer,
    TipoPersonaSerializer,
    PersonaSerializer,
    UsuarioSerializer,
    PacienteSerializer,
    ServicioSerializer,
    CitaMedicaSerializer,
)


class BaseAuditViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class EmpresaViewSet(BaseAuditViewSet):
    queryset = Empresa.objects.filter(is_deleted=False)
    serializer_class = EmpresaSerializer


class TipoPersonaViewSet(BaseAuditViewSet):
    queryset = TipoPersona.objects.filter(is_deleted=False)
    serializer_class = TipoPersonaSerializer


class PersonaViewSet(BaseAuditViewSet):
    queryset = Persona.objects.filter(is_deleted=False)
    serializer_class = PersonaSerializer


class UsuarioViewSet(BaseAuditViewSet):
    queryset = Usuario.objects.filter(is_deleted=False)
    serializer_class = UsuarioSerializer

    # admin users can see all
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Usuario.objects.filter(is_deleted=False)
        return Usuario.objects.filter(id=user.id, is_deleted=False)


class PacienteViewSet(BaseAuditViewSet):
    queryset = Paciente.objects.filter(is_deleted=False)
    serializer_class = PacienteSerializer


class ServicioViewSet(BaseAuditViewSet):
    queryset = Servicio.objects.filter(is_deleted=False)
    serializer_class = ServicioSerializer


class CitaMedicaViewSet(BaseAuditViewSet):
    queryset = CitaMedica.objects.filter(is_deleted=False)
    serializer_class = CitaMedicaSerializer

    # filter 'citas' by 'fecha'
    def get_queryset(self):
        queryset = super().get_queryset()
        fecha = self.request.query_params.get("fecha")
        if fecha:
            queryset = queryset.filter(fecha=fecha)
        return queryset
