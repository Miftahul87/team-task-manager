from django.conf import settings
from django.db import models
class Workspace(models.Model):
    name=models.CharField(max_length=120)
    description=models.TextField(blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="owned_workspaces")
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
class Membership(models.Model):
    OWNER="OWNER"; ADMIN="ADMIN"; MEMBER="MEMBER"
    ROLE_CHOICES=[(OWNER,"Owner"),(ADMIN,"Admin"),(MEMBER,"Member")]
    workspace=models.ForeignKey(Workspace,on_delete=models.CASCADE,related_name="memberships")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="workspace_memberships")
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default=MEMBER)
    joined_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["workspace","user"],name="unique_workspace_member")]
class Task(models.Model):
    TODO="TODO"; IN_PROGRESS="IN_PROGRESS"; DONE="DONE"
    STATUS_CHOICES=[(TODO,"To do"),(IN_PROGRESS,"In progress"),(DONE,"Done")]
    LOW="LOW"; MEDIUM="MEDIUM"; HIGH="HIGH"
    PRIORITY_CHOICES=[(LOW,"Low"),(MEDIUM,"Medium"),(HIGH,"High")]
    workspace=models.ForeignKey(Workspace,on_delete=models.CASCADE,related_name="tasks")
    title=models.CharField(max_length=180)
    description=models.TextField(blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default=TODO)
    priority=models.CharField(max_length=10,choices=PRIORITY_CHOICES,default=MEDIUM)
    assignee=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="assigned_tasks")
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="created_tasks")
    due_date=models.DateField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["-created_at"]
class Comment(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE,related_name="comments")
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    body=models.TextField(max_length=2000)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["created_at"]
