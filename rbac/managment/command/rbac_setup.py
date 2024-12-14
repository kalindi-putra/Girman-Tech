from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rbac.models import Role, Permission

class Command(BaseCommand):
    help = 'Setup initial RBAC structure with users, roles, and permissions'

    def handle(self, *args, **kwargs):
        # Create roles
        admin_role, _ = Role.objects.get_or_create(name='admin')
        supervisor_role, _ = Role.objects.get_or_create(name='supervisor')
        staff_role, _ = Role.objects.get_or_create(name='staff')

        # Create permissions
        permissions_data = [
            # Admin permissions
            {'name': 'Create Users', 'resource': 'USERS', 'action': 'CREATE'},
            {'name': 'Manage Roles', 'resource': 'ROLES', 'action': 'MANAGE'},
            {'name': 'Manage Permissions', 'resource': 'PERMISSIONS', 'action': 'MANAGE'},
            {'name': 'View Audit Logs', 'resource': 'AUDIT', 'action': 'READ'},
            
            # Supervisor permissions
            {'name': 'Assign Roles', 'resource': 'ROLES', 'action': 'ASSIGN'},
            {'name': 'View Users', 'resource': 'USERS', 'action': 'READ'},
            
            # Staff permissions
            {'name': 'Basic Access', 'resource': 'BASIC', 'action': 'ACCESS'},
        ]

        for perm_data in permissions_data:
            perm, _ = Permission.objects.get_or_create(**perm_data)
            
            # Assign to admin role
            admin_role.permissions.add(perm)
            
            # Assign supervisor and staff permissions selectively
            if perm_data['resource'] in ['ROLES', 'USERS']:
                supervisor_role.permissions.add(perm)
            if perm_data['resource'] == 'BASIC':
                staff_role.permissions.add(perm)
                supervisor_role.permissions.add(perm)

        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'  # Change this in production
            )
            admin_user.roles.add(admin_role)
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        self.stdout.write(self.style.SUCCESS('Successfully set up RBAC structure'))
