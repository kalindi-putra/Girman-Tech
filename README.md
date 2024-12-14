RBAC Control System for Django
Overview

This project implements a Role-Based Access Control (RBAC) system using Django and Django REST Framework (DRF) to manage user roles, permissions, and access control for different resources. The system provides APIs for managing users, roles, and permissions, as well as logging access attempts to resources for auditing purposes.
Features

    User Management: Create and manage users with specific roles.
    Role Management: Assign roles to users and manage permissions for roles.
    Permission Management: Assign permissions to roles for accessing specific resources.
    Audit Logs: Keep track of access attempts and their outcomes for auditing purposes.
    Access Control: Validate access to resources based on the assigned roles and permissions.

Setup
Prerequisites

    Python 3.x
    Django 3.x or higher
    Django REST Framework
    PostgreSQL (or any database you prefer)
    Celery for asynchronous tasks (optional)

Installation

    Clone this repository:

git clone <repository-url>
cd <repository-directory>

Install required dependencies:

pip install -r requirements.txt

Run migrations to set up the database:

python manage.py migrate

Create a superuser to access the Django admin interface:

python manage.py createsuperuser

Start the Django development server:

    python manage.py runserver

API Endpoints
1. User Management

    Create User
    POST /users/
    Creates a new user. Only allowed for users with the USERS permission and the CREATE action.

    List Users
    GET /users/
    Lists all users. Requires authentication.

2. Role Management

    Create Role
    POST /roles/
    Creates a new role.

    List Roles
    GET /roles/
    Lists all roles.

3. Permission Management

    Create Permission
    POST /permissions/
    Creates a new permission.

    List Permissions
    GET /permissions/
    Lists all permissions.

4. Assign Roles and Permissions

    Assign Role to User
    POST /roles/{user_id}/{role_id}/assign/
    Assign a specific role to a user.

    Assign Permission to Role
    POST /permissions/{role_id}/{permission_id}/assign/
    Assign a specific permission to a role.

5. Access Control

    Validate User Access
    GET /validate-access/
    Checks if the authenticated user has permission to perform a specific action on a resource.

6. Audit Logs

    Get Audit Logs
    GET /audit-logs/
    Retrieves the audit logs for the past n hours (default 24 hours). Requires AUDIT permission and READ action.

7. User Roles

    Get User Roles
    GET /user-roles/{user_id}/
    Retrieves the roles assigned to a user. If no user ID is provided, it returns the roles of the authenticated user.

Models
1. Role

    Represents a role that can be assigned to users.
    Fields: name, permissions (Many-to-many relationship with Permission).

2. Permission

    Represents a specific permission granted to roles for accessing resources.
    Fields: name, resource, action.

3. AuditLog

    Tracks user access attempts.
    Fields: user, action, resource, outcome, timestamp.

Security and Access Control

    Permissions:
        The IsAuthenticated permission is used to ensure that only authenticated users can access the APIs.
        Custom permissions can be applied using the @validate_permission decorator to check if a user has the necessary role and permission for a specific action.

    Audit Logging:
        Every access attempt to a resource is logged in the AuditLog model for auditing purposes. This can be useful for compliance and monitoring.

Decorators

    @validate_permission: A custom decorator used to ensure that the user has the required permission to perform certain actions. It checks if the user has the required role and permission for a specific resource and action.

Testing

You can use Django's built-in testing tools to write unit tests for the application. The UserViewSet, RoleViewSet, and PermissionViewSet can be tested with DRF's APIClient.

Example test for user creation:

from rest_framework.test import APITestCase

class UserTests(APITestCase):
    def test_create_user(self):
        data = {
            'username': 'testuser',
            'password': 'password123',
            'email': 'testuser@example.com'
        }
        response = self.client.post('/users/', data)
        self.assertEqual(response.status_code, 201)

License

This project is licensed under the MIT License. See the LICENSE file for more details.
You said:
how to create requirement txt for my oroject
ChatGPT said:
ChatGPT

To create a requirements.txt file for your Django project, you can follow these steps:
1. Install the required packages

First, ensure you have all the necessary dependencies installed for your project. If you're starting from scratch or want to verify your current environment, you can install the packages using pip.

Example:

pip install django
pip install djangorestframework
pip install psycopg2  # If you're using PostgreSQL
pip install celery     # If you're using Celery
# Any other dependencies...

2. Generate requirements.txt

Once all the dependencies are installed, you can automatically generate a requirements.txt file that lists the packages and their versions by running the following command in your project directory:

pip freeze > requirements.txt

This will create a requirements.txt file with the exact versions of the installed packages. Here's an example of what it might look like:

Django==4.2.5
djangorestframework==3.14.0
psycopg2==2.9.6
celery==5.2.7
# Any other dependencies...

3. Manually edit if needed

If you'd like to specify exact versions or remove any unnecessary dependencies, you can edit the requirements.txt manually. You can also group related packages or add comments for clarity.

Example requirements.txt:

# Core Django Packages
Django==4.2.5
djangorestframework==3.14.0

# Database support
psycopg2==2.9.6

4. Using the requirements.txt file

Once you have the requirements.txt file, other developers or production environments can install the exact dependencies using the following command:

pip install -r requirements.txt

This will install all the packages listed in the file and ensure the correct versions are used.

This process will help you generate a requirements.txt file that's consistent with the dependencies used in your project.
You said:
can give that readme file details in one single page
ChatGPT said:
ChatGPT

Sure! Here's a concise, single-page version of the README file for your RBAC control project in Django:
RBAC Control System for Django
Overview

This project implements a Role-Based Access Control (RBAC) system using Django and Django REST Framework (DRF). It allows managing users, roles, permissions, and access control for different resources, along with logging access attempts for auditing purposes.
Features

    User Management: Create and manage users with specific roles.
    Role Management: Assign roles to users and manage role permissions.
    Permission Management: Assign permissions to roles for specific resources.
    Audit Logs: Track and retrieve access attempts and their outcomes.
    Access Control: Validate user access based on roles and permissions.

Setup
Prerequisites

    Python 3.x
    Django 3.x or higher
    Django REST Framework
    PostgreSQL (or preferred database)

Installation

    Clone the repository:

git clone <repository-url>
cd <repository-directory>

Install dependencies:

pip install -r requirements.txt

Run migrations:

python manage.py migrate

Create a superuser:

python manage.py createsuperuser

Start the development server:

    python manage.py runserver

API Endpoints

    POST /users/: Create a new user (requires USERS permission, CREATE action).
    GET /users/: List all users (requires authentication).
    POST /roles/: Create a new role.
    GET /roles/: List all roles.
    POST /permissions/: Create a new permission.
    GET /permissions/: List all permissions.
    POST /roles/{user_id}/{role_id}/assign/: Assign a role to a user.
    POST /permissions/{role_id}/{permission_id}/assign/: Assign a permission to a role.
    GET /validate-access/: Validate if the user has permission for a resource action.
    GET /audit-logs/: Retrieve audit logs from the past n hours (default 24).
    GET /user-roles/{user_id}/: Get roles for a user.

Models

    Role: Represents roles that can be assigned to users with specific permissions.
    Permission: Represents permissions that control access to specific resources.
    AuditLog: Logs user access attempts for auditing purposes.

Security and Access Control

    Permissions: Uses IsAuthenticated for authentication and @validate_permission to check user permissions for specific actions.
    Audit Logs: Records user actions on resources for compliance and monitoring.

Decorators

    @validate_permission: Custom decorator to ensure the user has the required permission to perform an action.

