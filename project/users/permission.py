from rest_framework.permissions import BasePermission


class IsSeeker(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_seeker
    

class IsRecruiters(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_employer
    


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print(user,'.............admin..........')
        return user.is_authenticated and user.is_superuser
 