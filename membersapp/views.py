from django.shortcuts import render
from .decorators import allowed_users, unAuthenticated_user
from adminapp.models import Task, Member
from django.contrib.auth.models import User

# Create your views here.

@allowed_users(allowed_roles=['member'])
def dashboard(request):
    return render(request, 'membersapp/member-dashboard.html')

def member_tasks(request):

    return render(request, 'membersapp/member-tasks.html')