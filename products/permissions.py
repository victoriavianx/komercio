from rest_framework import permissions

class IsSellerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_seller

class IsSellerUser(permissions.BasePermission):
     def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_seller:
            return obj.seller == request.user