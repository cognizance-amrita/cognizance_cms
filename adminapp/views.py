from django.shortcuts import render,redirect
from django.http import HttpResponse
from .decorators import unAuthenticated_user, allowed_users
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from .models import Member, Task, Submission, StatusUpdate  
from pages.models import Application
from .announcer import Announcer
from django.core.mail import send_mail
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime

# Create your views here.

@allowed_users(allowed_roles=['administrator'])
def dashboard(request):
    dates = StatusUpdate.objects.order_by('date').values('date').distinct()
    s_date =  dates[len(dates)-1]['date']
    return render(request, 'adminapp/admin-dashboard.html',{'s_date':s_date})

def announcements(request):

    if request.method == 'POST':
        mention = request.POST.get('mention_field')
        message = request.POST.get('message_field')

        ann = Announcer(mention, message)
        ann.announce()

    return render(request, 'adminapp/announcements.html')

def applications(request):
    applications = Application.objects.all()
    counts = Application.objects.count

    return render(request, 'adminapp/admin-applications.html', {'applications':applications, 'count':counts})

def task_submissions(request,task_id):
    submissions = Submission.objects.all()
    count = 0
    for s in submissions:
        if s.task_id == task_id:
            count = count + 1
    return render(request, 'adminapp/task-submissions.html',{'count':count, 'submissions':submissions, 'task_id':task_id})


def reviewing(request, application_id):
    application = Application.objects.get(id=application_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        application.status = status
        cusr = Member.objects.get(username=request.user.username)
        rev_name = cusr.fullname
        application.reviewer = rev_name
        application.save()
        email = application.email
        if application.status == 'Accepted':
            template = render_to_string('adminapp/accepted-mail-template.html',{'name':application.fullname})
            subject = 'Congratulations, you\'re in! 🎉'
        if application.status == 'Rejected':
            template = render_to_string('adminapp/rejected-mail-template.html',{'name':application.fullname})
            subject = 'Better luck next time 😔'
        plain_msg = strip_tags(template)
        mail.send_mail(
            subject,
            plain_msg,
            settings.EMAIL_HOST_USER,
            [email],
            html_message=template,
        )
      #  mail.fail_silently = False
      #  mail.send()

        return redirect("applications")
    
    return render(request, 'adminapp/admin-reviewing.html', {'application':application})




@allowed_users(allowed_roles=['administrator'])
def members(request):
    roles = []
    members = Member.objects.all()
    counts = Member.objects.count
    role = request.user.groups.all()[0].name
    return render(request, 'adminapp/admin-members.html',{'displayUserNames': members, 'counts':counts, 'role':role})

def tasks(request):
    tasks = Task.objects.all()
    counts = Task.objects.count
    return render(request, 'adminapp/admin-tasks.html',{'displayTasks':tasks, 'counts':counts})

def groups(request):
    groups = Group.objects.all()
    counts = Group.objects.count
    return render(request, 'adminapp/admin-groups.html',{'displayGroups':groups, 'counts':counts})

def delete(request, member_id):
    Member.objects.filter(id=member_id).delete()
    return redirect('members')


def add_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name_field')
        gp = Group.objects.create(name=group_name)
        return redirect('groups')

    return render(request, 'adminapp/add-group.html')


@allowed_users(allowed_roles=['administrator'])
def add_members(request):

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')
        github_handle = request.POST.get('github_handle')
        discord_handle = request.POST.get('discord_handle')
        role = request.POST.get('role')
        email = request.POST.get('email')
        image = request.POST.get('profile_pic_field')

        member = Member(
        fullname = fullname,
        username = username,
        phone = phone,
        email = email,
        password = password,
        github_username = github_handle,
        discord_handle = discord_handle,
        profile_pic = image,
        role = role
        )
        member.save()
        mygrp = Group.objects.get(name=role)

        result = User.objects.create(email=email, password=password, username=username)
        mygrp.user_set.add(result)

        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()

        return redirect('members')

    return render(request, 'adminapp/add-members.html')
  
@allowed_users(allowed_roles=['administrator'])  
def status_updates(request,sdate):
    listdictdates = StatusUpdate.objects.order_by('date').values('date').distinct()
    dates=[] 
    for i in range(0,len(listdictdates)):
    	dates.append(listdictdates[i]['date'].strftime("%Y-%m-%d"))
    details = StatusUpdate.objects.all()	
    if sdate in dates:
    	sub_users=[]
    	for mem in details:
    	    if (mem.date.strftime("%Y-%m-%d")==sdate):
    	    	sub_users.append(mem)
    	print(sub_users)
    	return render(request, 'adminapp/status-updates.html',{'DATE':dates,'sdate':sdate,'sub_users':sub_users})


    
