from django.urls import path
from .views import WorkspaceListCreateView,MemberListCreateView,WorkspaceTaskListCreateView,TaskDetailView,TaskCommentListCreateView
urlpatterns=[
 path("workspaces/",WorkspaceListCreateView.as_view()),
 path("workspaces/<int:pk>/members/",MemberListCreateView.as_view()),
 path("workspaces/<int:pk>/tasks/",WorkspaceTaskListCreateView.as_view()),
 path("tasks/<int:pk>/",TaskDetailView.as_view()),
 path("tasks/<int:pk>/comments/",TaskCommentListCreateView.as_view()),
]
