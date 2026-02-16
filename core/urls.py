from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaViewSet,
    TipoPersonaViewSet,
    PersonaViewSet,
    UsuarioViewSet,
    PacienteViewSet,
    ServicioViewSet,
    CitaMedicaViewSet,
)

router = DefaultRouter()
router.register(r"empresas", EmpresaViewSet)
router.register(r"tipo-personas", TipoPersonaViewSet)
router.register(r"personas", PersonaViewSet)
router.register(r"usuarios", UsuarioViewSet)
router.register(r"pacientes", PacienteViewSet)
router.register(r"servicios", ServicioViewSet)
router.register(r"citas", CitaMedicaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
