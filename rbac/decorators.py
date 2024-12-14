from functools import wraps
from django.http import JsonResponse
from .models import AuditLog

def validate_permission(resource, action):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            print(request)
            user = request.user

            if user.is_anonymous:

                return JsonResponse({
                    'success': False,
                    'message': 'Authentication required.'
                }, status=401)

            has_permission = False
            #has_permission = False
            
            for role in user.roles.all():
                if role.permissions.filter(resource=resource, action=action).exists():
                    has_permission = True
                    break

            # Log the access attempt
            AuditLog.objects.create(
                user=user,
                action=action,
                resource=resource,
                outcome=has_permission
            )

            if not has_permission:
                return JsonResponse({
                    'success': False,
                    'message': 'Permission denied'
                }, status=403)

            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
