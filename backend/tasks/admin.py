from django.contrib import admin
from .models import Workspace,Membership,Task,Comment
admin.site.register([Workspace,Membership,Task,Comment])
