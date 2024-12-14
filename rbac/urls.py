from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'permissions', views.PermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('assign-role/<int:user_id>/<int:role_id>/', views.assign_role_to_user),
    path('assign-permission/<int:role_id>/<int:permission_id>/', views.assign_permission_to_role),
    path('role-permissions/<int:role_id>/', views.get_role_permissions),
    path('validate-access/<str:resource>/<str:action>/', views.validate_access),
    path('audit-logs/', views.get_audit_logs),
]
