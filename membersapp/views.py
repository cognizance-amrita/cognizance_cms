from django.shortcuts import render
from .decorators import allowed_users, unAuthenticated_user
from adminapp.models import Task, Member
from django.contrib.auth.models import User

# Create your views here.

@allowed_users(allowed_roles=['member'])
def dashboard(request):
    return render(request, 'membersapp/member-dashboard.html')

def member_tasks(request):
    user = User.objects.get(username=request.user.username)
    groups =  user.groups.all()
    tasks = Task.objects.all()
    domain = ''
    for t in tasks:
        if user.groups.filter(name=t.group).exists():
            domain = t.group
    return render(request, 'membersapp/member-tasks.html', {'groups':groups, 'tasks':tasks, 'domain':domain})