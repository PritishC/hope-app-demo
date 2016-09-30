from rest_framework import permissions


class IsAnonCreate(permissions.BasePermission):
    """
    Obtained from http://stackoverflow.com/a/34162842/2842216.
    """
    def has_permission(self, request, view): 
        if view.action in ['list', 'destroy']:
            return request.user.is_authenticated() and request.user.is_superuser
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return request.user.is_authenticated() and (obj == request.user or request.user.is_staff)
        elif view.action in ['update', 'partial_update']:
            return request.user.is_authenticated() and (obj == request.user or request.user.is_staff)
        elif view.action == 'destroy':
            return request.user.is_authenticated() and request.user.is_staff

        return False
