from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, Permission, AuditLog

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Role.ROLE_CHOICES, write_only=True, required=False)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role_name = validated_data.pop('role', None)
        password = validated_data.pop('password')
        
        # Create user
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        # Assign role if provided
        if role_name:
            role, _ = Role.objects.get_or_create(name=role_name)
            user.roles.add(role)
        
        return user

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'resource', 'action']

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'resource', 'outcome', 'timestamp']
