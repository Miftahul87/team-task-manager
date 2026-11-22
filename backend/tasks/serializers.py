from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Workspace,Membership,Task,Comment
User=get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8)
    class Meta:
        model=User; fields=["id","username","email","password"]
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
class MembershipSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source="user.username",read_only=True)
    class Meta:
        model=Membership; fields=["id","user","username","role","joined_at"]
        read_only_fields=["id","joined_at"]
class WorkspaceSerializer(serializers.ModelSerializer):
    role=serializers.SerializerMethodField()
    class Meta:
        model=Workspace; fields=["id","name","description","created_by","created_at","role"]
        read_only_fields=["id","created_by","created_at","role"]
    def get_role(self,obj):
        request=self.context.get("request")
        membership=obj.memberships.filter(user=request.user).first() if request and request.user.is_authenticated else None
        return membership.role if membership else None
class TaskSerializer(serializers.ModelSerializer):
    assignee_username=serializers.CharField(source="assignee.username",read_only=True)
    created_by_username=serializers.CharField(source="created_by.username",read_only=True)
    class Meta:
        model=Task
        fields=["id","workspace","title","description","status","priority","assignee","assignee_username",
                "created_by","created_by_username","due_date","created_at","updated_at"]
        read_only_fields=["id","workspace","created_by","created_at","updated_at","assignee_username","created_by_username"]
    def validate_assignee(self,value):
        workspace=self.context.get("workspace")
        if value and workspace and not Membership.objects.filter(workspace=workspace,user=value).exists():
            raise serializers.ValidationError("Assignee must be a member of this workspace.")
        return value
class CommentSerializer(serializers.ModelSerializer):
    author_username=serializers.CharField(source="author.username",read_only=True)
    class Meta:
        model=Comment; fields=["id","author","author_username","body","created_at"]
        read_only_fields=["id","author","author_username","created_at"]
