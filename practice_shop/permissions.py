from rest_framework import permissions

class IsAjaxRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        
        if request.method == 'GET':
            return False
            
        return is_ajax