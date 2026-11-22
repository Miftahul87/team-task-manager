from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Workspace,Membership,Task
User=get_user_model()
class WorkspaceTaskAPITests(TestCase):
    def setUp(self):
        self.owner=User.objects.create_user(username="owner",password="StrongPass123!")
        self.member=User.objects.create_user(username="member",password="StrongPass123!")
        self.other=User.objects.create_user(username="outsider",password="StrongPass123!")
        self.ws=Workspace.objects.create(name="Alpha",created_by=self.owner)
        Membership.objects.create(workspace=self.ws,user=self.owner,role=Membership.OWNER)
        Membership.objects.create(workspace=self.ws,user=self.member,role=Membership.MEMBER)
        self.task=Task.objects.create(workspace=self.ws,title="Assigned task",created_by=self.owner,assignee=self.member)
    def auth(self,user):
        c=APIClient(); response=c.post("/api/auth/token/",{"username":user.username,"password":"StrongPass123!"},format="json")
        c.credentials(HTTP_AUTHORIZATION="Bearer "+response.data["access"]); return c
    def test_member_can_list_workspace_tasks(self):
        r=self.auth(self.member).get(f"/api/workspaces/{self.ws.id}/tasks/")
        self.assertEqual(r.status_code,200); self.assertEqual(len(r.data["results"]),1)
    def test_outsider_cannot_read_workspace_tasks(self):
        r=self.auth(self.other).get(f"/api/workspaces/{self.ws.id}/tasks/")
        self.assertIn(r.status_code,[403,404])
    def test_member_can_update_assigned_task(self):
        r=self.auth(self.member).patch(f"/api/tasks/{self.task.id}/",{"status":"IN_PROGRESS"},format="json")
        self.assertEqual(r.status_code,200)
    def test_member_cannot_update_unassigned_task(self):
        other_task=Task.objects.create(workspace=self.ws,title="Not assigned",created_by=self.owner)
        r=self.auth(self.member).patch(f"/api/tasks/{other_task.id}/",{"status":"DONE"},format="json")
        self.assertEqual(r.status_code,403)
    def test_member_cannot_delete_task(self):
        r=self.auth(self.member).delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(r.status_code,403)
