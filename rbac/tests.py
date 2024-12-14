from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status
from .models import Role, Permission, AuditLog
import json

class RBACTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123'
        )
        self.regular_user = User.objects.create_user(
            username='user',
            password='user123'
        )
        
        # Create roles
        self.admin_role = Role.objects.create(name='ADMIN')
        self.user_role = Role.objects.create(name='USER')
        
        # Create permissions
        self.create_user_permission = Permission.objects.create(
            name='Create User',
            resource='USERS',
            action='CREATE'
        )
        self.assign_role_permission = Permission.objects.create(
            name='Assign Role',
            resource='ROLES',
            action='ASSIGN'
        )
        self.read_audit_permission = Permission.objects.create(
            name='Read Audit',
            resource='AUDIT',
            action='READ'
        )
        
        # Assign permissions to roles
        self.admin_role.permissions.add(
            self.create_user_permission,
            self.assign_role_permission,
            self.read_audit_permission
        )
        
        # Assign roles to users
        self.admin_user.roles.add(self.admin_role)
        self.regular_user.roles.add(self.user_role)
        
        # Setup API client
        self.client = APIClient()

    def test_create_user(self):
        # Login as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Test creating a new user
        response = self.client.post(reverse('user-list'), {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'newuser@example.com',
            'role': 'USER'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_create_user_unauthorized(self):
        # Login as regular user
        self.client.force_authenticate(user=self.regular_user)
        
        # Attempt to create a new user
        response = self.client.post(reverse('user-list'), {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'newuser@example.com'
        })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assign_role(self):
        # Login as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Create a new user
        new_user = User.objects.create_user(
            username='roletest',
            password='test123'
        )
        
        # Test assigning role
        response = self.client.post(
            reverse('assign-role-to-user', kwargs={
                'user_id': new_user.id,
                'role_id': self.user_role.id
            })
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertTrue(new_user.roles.filter(id=self.user_role.id).exists())

    def test_validate_access(self):
        # Login as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Test access validation
        response = self.client.get(
            reverse('validate-access', kwargs={
                'resource': 'USERS',
                'action': 'CREATE'
            })
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_get_audit_logs(self):
        # Login as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Create some audit logs
        AuditLog.objects.create(
            user=self.admin_user,
            action='CREATE',
            resource='USERS',
            outcome=True
        )
        
        # Test retrieving audit logs
        response = self.client.get(reverse('get-audit-logs'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertTrue(len(response.data['data']) > 0)

    def test_get_role_permissions(self):
        # Login as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Test getting role permissions
        response = self.client.get(
            reverse('get-role-permissions', kwargs={'role_id': self.admin_role.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 3)  # Admin should have 3 permissions