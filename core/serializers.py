from rest_framework import serializers
from .models import Empresa, Persona, Usuario, Paciente, Servicio, CitaMedica


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = "__all__"


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = "__all__"


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "password",
            "email",
            "empresa",
            "persona",
            "rol",
            "is_active",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PacienteSerializer(serializers.ModelSerializer):
    persona_details = PersonaSerializer(source="persona", read_only=True)

    class Meta:
        model = Paciente
        fields = "__all__"


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = "__all__"


class CitaMedicaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.CharField(
        source="paciente.persona.nombres", read_only=True
    )
    servicio_nombre = serializers.CharField(source="servicio.nombre", read_only=True)

    class Meta:
        model = CitaMedica
        fields = "__all__"
