from django.shortcuts import render,redirect
from django.http import HttpResponse
from .decorators import unAuthenticated_user, allowed_users
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from .models import Member, Task, Submission, StatusUpdate, Meeting
from pages.models import Application
from .announcer import Announcer
from .status_update import *
from .daterange import Daterange
from django.core.mail import send_mail
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime
from datetime import datetime
from datetime import date 
from datetime import timedelta 
from .tasks import *
from .bot import Bot
from .cron import periodic_mailer

@allowed_users(allowed_roles=['administrator'])
async def dashboard(request):
    dates = StatusUpdate.objects.order_by('date').values('date').distinct()

    if len(dates) != 0:
        sdate =  dates[len(dates)-1]['date']
    else:
        time = datetime.now().strftime("%H:%M:%S")
        today = date.today()
        sdate = today - timedelta(days = 1) 
        if str(time)<'06:00:00':
            sdate =  sdate - timedelta(days = 1)
        elif(str(time)=='08:34:00'):
            periodic_mailer()
        sdate = sdate.strftime("%Y-%m-%d")
    
    return render(request, 'adminapp/admin-dashboard.html',{'sdate':sdate})

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
            mem = Member(
                fullname= application.fullname,
                username=application.fullname.replace(' ', ''),
                phone=application.phone,
                email=application.email,
                password=application.password,
                role='Member',
                discord_handle=application.discord_handle,
                github_username=application.github_username
            )
            mem.save()
            bot = Bot()
            bot.add_role(username=application.discord_handle, role='<@&790265904894050344>')

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

def meetings(request):
    meetingss = Meeting.objects.all()
    count = 0
    for m in meetingss:
        if m.status == 'Pending':
            count += 1
    return render(request, 'adminapp/admin-meetings.html', {'meetings':meetingss, 'count':count})

def delete(request, member_id):
    Member.objects.filter(id=member_id).delete()
    return redirect('members')

def edit_profile(request):

    # This gets the original data from the back-end
    cusr = Member.objects.get(username=request.user.username)
    c_username = cusr.username
    c_fullname = cusr.fullname
    c_phone = cusr.phone
    c_github_username = cusr.github_username
    c_discord_handle = cusr.discord_handle
    c_image = cusr.profile_pic  
    c_id = cusr.id

    if request.method == 'POST':
        # gets the data from the front-end
        fullname = request.POST.get('FullName')
        username = request.POST.get('UserName')
        phone = request.POST.get('Phone')
        password = request.POST.get('Password')
        github_handle = request.POST.get('GitHub')
        discord_handle = request.POST.get('Discord')
        Member.objects.filter(id=c_id).update(fullname=fullname,username=username,password=password,phone=phone,discord_handle=discord_handle,github_username=github_handle)       
        return redirect('members')
    else: 
        return render(request, 'adminapp/edit-profile.html',{'UserName': c_username, 'FullName':c_fullname, 'Phone':c_phone, 'GitHub':c_github_username, 'Discord':c_discord_handle, 'PFP':c_image})
        

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
        role = role,
        streak = 0
        )
        member.save()
        mygrp = Group.objects.get(name=role)

        result = User.objects.create(email=email, password=password, username=username)
        mygrp.user_set.add(result)

        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()

    return render(request, 'adminapp/add-members.html')
  
@allowed_users(allowed_roles=['administrator'])  
def status_updates(request,sdate):
    listdictdates = StatusUpdate.objects.order_by('date').values('date').distinct()
    dates=[] 
    for i in range(0,len(listdictdates)):
        dates.append(listdictdates[i]['date'].strftime("%Y-%m-%d"))
    members = Member.objects.all()    
    if sdate not in dates:
        mem_email_queryset = Member.objects.values('email')
        mem_email=[]
        from_date = date(int(dates[-1][:4]),int(dates[-1][5:7]),int(dates[-1][8:10]))
        to_date = date(int(sdate[:4]),int(sdate[5:7]),int(sdate[8:10]))
        date_arr = [from_date + timedelta(days=x) for x in range((to_date - from_date).days + 1)]
        date_arr = date_arr[1:]
        for i in range(0,len(mem_email_queryset)):
            mem_email.append(str(mem_email_queryset[i]['email']))
        # mem_mail = ['info@twitter.com', 'bot@notifications.heroku.com', 'bot@notifications.heroku.com']
        # data = filter_update(date(2021,1,10),mem_mail)
        data = filter_update(date_arr,mem_email)
        print(data)
        if len(data)!=0:
            lates_date = data[0][2]
        for i in range(len(data)):
            if lates_date != data[i][2]:
                details = StatusUpdate.objects.all()	
                sub_users=[]
                for mem in details:
                    if (mem.date.strftime("%Y-%m-%d")==lates_date):
                        sub_users.append(mem)
                notsub = []
                mem = Member.objects.values('username')
                mem_usr=[]
                for ik in range(0,len(mem)):
                    mem_usr.append(mem[ik]['username'])
                sub_usr=[]
                for il in range(0,len(sub_users)):
                    sub_usr.append(sub_users[il].username)
                notsub= list(set(mem_usr)-set(sub_usr))
                for st in range(len(notsub)):
                    meme = Member.objects.get(username=notsub[st])
                    meme.streak+=1
                    meme.save()
                lates_date = data[i][2]
            mem_detail = Member.objects.get(email=data[i][1])
            report = StatusUpdate(fullname = mem_detail.fullname, username= mem_detail.username, email = data[i][1], date=data[i][2], reportdatetime=data[i][0])
            # report = StatusUpdate(fullname = "Helo", username= "Hi", email = data[i][1], date=sdate, reportdatetime=data[i][0])
            mem_detail.streak = 0
            mem_detail.save()         
            report.save()        
        if len(data)!=0:        
            details = StatusUpdate.objects.all()	
            sub_users=[]
            for mem in details:
                if (mem.date.strftime("%Y-%m-%d")==data[-1][2]):
                    sub_users.append(mem)
            notsub = []
            mem = Member.objects.values('username')
            mem_usr=[]
            for i in range(0,len(mem)):
                mem_usr.append(mem[i]['username'])
            sub_usr=[]
            for i in range(0,len(sub_users)):
                sub_usr.append(sub_users[i].username)
            notsub= list(set(mem_usr)-set(sub_usr))
            for st in range(len(notsub)):
                meme = Member.objects.get(username=notsub[st])
                meme.streak+=1
                meme.save()
        listdictdates = StatusUpdate.objects.order_by('date').values('date').distinct()
        dates=[] 
        for i in range(0,len(listdictdates)):
            dates.append(listdictdates[i]['date'].strftime("%Y-%m-%d"))
    details = StatusUpdate.objects.all()	
    sub_users=[]
    for mem in details:
        if (mem.date.strftime("%Y-%m-%d")==sdate):
            sub_users.append(mem)
    today = date.today()
    yesterday = today - timedelta(days = 1) 
    time = datetime.now().strftime("%H:%M:%S")
    if str(time)<'06:00:00':
        yesterday =  yesterday - timedelta(days = 1)
    latest_date = yesterday.strftime("%Y-%m-%d")
    notsub = []
    mem = Member.objects.values('username')
    mem_usr=[]
    for i in range(0,len(mem)):
        mem_usr.append(mem[i]['username'])
    sub_usr=[]
    for i in range(0,len(sub_users)):
        sub_usr.append(sub_users[i].username)
    notsub= list(set(mem_usr)-set(sub_usr)) 
    return render(request, 'adminapp/status-updates.html',{'DATE':dates,'sdate':sdate,'sub_users':sub_users,
        'yesterday':yesterday.strftime("%Y-%m-%d"),'latest_date':latest_date,'notsubmitted':notsub,'members':members})


def add_meeting(request):
    mems = Member.objects.all()
    grps = Group.objects.all()
    organisers = []
    groups = []
    for m in mems:
        if m.role == 'Administrator':
            organisers.append(m)
    for g in grps:
        groups.append(g.name)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        room_name = request.POST.get('room-name')
        organiser = request.POST.get('organiser')
        group = request.POST.get('group')
        venue = request.POST.get('venue')

        meeting_url = 'https://meet.jit.si/cognizance/'
        meeting_url = meeting_url + group + room_name

        meeting = Meeting(
            group=group, subject=subject, organiser=organiser, venue=venue, meeting_link=meeting_url, status='Pending'
        )

        meeting.save()
        return redirect('meetings')

    return render(request, 'adminapp/add-meeting.html', {'organisers':organisers, 'groups':groups})

    
