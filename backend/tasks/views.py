from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Workspace,Membership,Task,Comment
from .serializers import RegisterSerializer,WorkspaceSerializer,MembershipSerializer,TaskSerializer,CommentSerializer
from .permissions import membership_for
User=get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all(); serializer_class=RegisterSerializer; permission_classes=[AllowAny]
class WorkspaceListCreateView(generics.ListCreateAPIView):
    serializer_class=WorkspaceSerializer
    def get_queryset(self): return Workspace.objects.filter(memberships__user=self.request.user).distinct()
    def perform_create(self,serializer):
        workspace=serializer.save(created_by=self.request.user)
        Membership.objects.create(workspace=workspace,user=self.request.user,role=Membership.OWNER)
class MemberListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def get_workspace(self,pk):
        workspace=get_object_or_404(Workspace,pk=pk)
        if not membership_for(self.request.user,workspace): raise PermissionDenied("Workspace membership required.")
        return workspace
    def get(self,request,pk):
        workspace=self.get_workspace(pk)
        return Response(MembershipSerializer(workspace.memberships.select_related("user"),many=True).data)
    def post(self,request,pk):
        workspace=self.get_workspace(pk); m=membership_for(request.user,workspace)
        if m.role not in (Membership.OWNER,Membership.ADMIN): raise PermissionDenied("Only owners/admins can add members.")
        username=request.data.get("username"); role=request.data.get("role",Membership.MEMBER)
        if role not in (Membership.ADMIN,Membership.MEMBER): return Response({"detail":"Role must be ADMIN or MEMBER."},status=400)
        user=get_object_or_404(User,username=username)
        membership,created=Membership.objects.get_or_create(workspace=workspace,user=user,defaults={"role":role})
        if not created: return Response({"detail":"User is already a member."},status=400)
        return Response(MembershipSerializer(membership).data,status=201)
class WorkspaceTaskListCreateView(generics.ListCreateAPIView):
    serializer_class=TaskSerializer
    def get_workspace(self):
        workspace=get_object_or_404(Workspace,pk=self.kwargs["pk"])
        if not membership_for(self.request.user,workspace): raise PermissionDenied("Workspace membership required.")
        return workspace
    def get_queryset(self):
        ws=self.get_workspace(); qs=Task.objects.filter(workspace=ws).select_related("assignee","created_by")
        status_filter=self.request.query_params.get("status")
        priority=self.request.query_params.get("priority")
        if status_filter: qs=qs.filter(status=status_filter)
        if priority: qs=qs.filter(priority=priority)
        return qs
    def get_serializer_context(self):
        context=super().get_serializer_context(); context["workspace"]=self.get_workspace(); return context
    def perform_create(self,serializer): serializer.save(workspace=self.get_workspace(),created_by=self.request.user)
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=TaskSerializer
    def get_queryset(self): return Task.objects.filter(workspace__memberships__user=self.request.user).select_related("workspace","assignee")
    def perform_update(self,serializer):
        task=self.get_object(); m=membership_for(self.request.user,task.workspace)
        if m.role not in (Membership.OWNER,Membership.ADMIN) and task.assignee_id!=self.request.user.id:
            raise PermissionDenied("Members can update only tasks assigned to them.")
        serializer.save()
    def perform_destroy(self,instance):
        m=membership_for(self.request.user,instance.workspace)
        if m.role not in (Membership.OWNER,Membership.ADMIN): raise PermissionDenied("Only owners/admins can delete tasks.")
        instance.delete()
class TaskCommentListCreateView(generics.ListCreateAPIView):
    serializer_class=CommentSerializer
    def get_task(self):
        task=get_object_or_404(Task,pk=self.kwargs["pk"])
        if not membership_for(self.request.user,task.workspace): raise PermissionDenied("Workspace membership required.")
        return task
    def get_queryset(self): return Comment.objects.filter(task=self.get_task()).select_related("author")
    def perform_create(self,serializer): serializer.save(task=self.get_task(),author=self.request.user)
