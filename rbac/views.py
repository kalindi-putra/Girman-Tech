from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny
from django.utils import timezone
from datetime import timedelta
from .models import Role, Permission, AuditLog
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, AuditLogSerializer
from .decorators import validate_permission
from django.contrib.auth.models import User

'''class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @validate_permission('USERS', 'CREATE')
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'User created successfully',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)'''


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # If no users exist, allow anyone to create the first user
        print(self.action)
        if self.action == 'create' and User.objects.count() == 0:
            return [AllowAny()]
        return [IsAuthenticated()]  # Otherwise, require authentication

    @validate_permission('USERS', 'CREATE')
    def create(self, request):
        # Handle user creation
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'message': 'User created successfully',
                'data': UserSerializer(user).data
            })
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@validate_permission('ROLES', 'ASSIGN')
def assign_role_to_user(request, user_id, role_id):
    try:
        user = User.objects.get(id=user_id)
        role = Role.objects.get(id=role_id)
        user.roles.add(role)
        return Response({
            'success': True,
            'message': f'Role {role.name} assigned to user {user.username}'
        })
    except (User.DoesNotExist, Role.DoesNotExist) as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@validate_permission('PERMISSIONS', 'ASSIGN')
def assign_permission_to_role(request, role_id, permission_id):
    try:
        role = Role.objects.get(id=role_id)
        permission = Permission.objects.get(id=permission_id)
        role.permissions.add(permission)
        return Response({
            'success': True,
            'message': f'Permission {permission.name} assigned to role {role.name}'
        })
    except (Role.DoesNotExist, Permission.DoesNotExist) as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_role_permissions(request, role_id):
    try:
        role = Role.objects.get(id=role_id)
        permissions = role.permissions.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response({
            'success': True,
            'message': 'Permissions retrieved successfully',
            'data': serializer.data
        })
    except Role.DoesNotExist as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_access(request, resource, action):
    user = request.user
    has_permission = False
    
    for role in user.roles.all():
        if role.permissions.filter(resource=resource, action=action).exists():
            has_permission = True
            break

    AuditLog.objects.create(
        user=user,
        action=action,
        resource=resource,
        outcome=has_permission
    )

    return Response({
        'success': has_permission,
        'message': 'Access granted' if has_permission else 'Access denied'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@validate_permission('AUDIT', 'READ')
def get_audit_logs(request):
    hours = int(request.GET.get('hours', 24))
    time_threshold = timezone.now() - timedelta(hours=hours)
    logs = AuditLog.objects.filter(timestamp__gte=time_threshold)
    serializer = AuditLogSerializer(logs, many=True)
    return Response({
        'success': True,
        'message': 'Audit logs retrieved successfully',
        'data': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_roles(request, user_id=None):
    try:
        user = request.user if user_id is None else User.objects.get(id=user_id)
        roles = user.roles.all()
        return Response({
            'success': True,
            'message': 'User roles retrieved successfully',
            'data': RoleSerializer(roles, many=True).data
        })
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
