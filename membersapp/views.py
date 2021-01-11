from django.shortcuts import render,redirect
from .decorators import allowed_users, unAuthenticated_user
from adminapp.models import Task, Member, Submission
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

def submit_task(request, task_id):
    member = Member.objects.get(username=request.user.username)
    task = Task.objects.get(id=task_id)
    fullname = member.fullname
    if request.method == 'POST':
        submission_text = request.POST.get('submission_text')
        submission_file = request.POST.get('submission_file')
        submission = Submission.objects.create(fullname=fullname, task_id=task_id, submission_text=submission_text)
        submission.save()
        return redirect('tasks')
        
    return render(request, 'membersapp/submit-task.html',{'fullname':fullname, 'task':task})
