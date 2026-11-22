from rest_framework.permissions import BasePermission
from .models import Membership
def membership_for(user,workspace):
    return Membership.objects.filter(user=user,workspace=workspace).first()
class IsWorkspaceMember(BasePermission):
    def has_object_permission(self,request,view,obj):
        workspace=getattr(obj,"workspace",obj)
        return membership_for(request.user,workspace) is not None
class IsWorkspaceAdmin(BasePermission):
    def has_permission(self,request,view): return request.user and request.user.is_authenticated
    def has_object_permission(self,request,view,obj):
        m=membership_for(request.user,obj)
        return bool(m and m.role in (Membership.OWNER,Membership.ADMIN))
