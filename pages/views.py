from django.shortcuts import render,redirect
from django.http import HttpResponse
from pages.models import displayUserNames
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .decorators import unAuthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from adminapp.models import Member, Blog
from .models import Application
from adminapp.models import Achievement

# Create your views here.
def error_404_view(request,exception):
    return render(request,'404.html')

def error_500_view(request):
    return render(request,'pages/500.html')

def home(request):
    return render(request, 'pages/index.html')

def blogs(request):
    blogs = Blog.objects.all()
    count = Blog.objects.count
    if count == 0:
        return render(request, 'pages/blogs.html', {'blogs':blogs, 'empty': 0})
    else:
        return render(request, 'pages/blogs.html', {'blogs':blogs})

def blog_view(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    return render(request, 'pages/blog-view.html', {'blog':blog})

def apply(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        department = request.POST.get('department')
        domain = request.POST.get('domain')
        ques1 = request.POST.get('ques1')
        writeup = request.POST.get('writeup')
        ac_year = request.POST.get('ac_year')
        status = 'Under review'
        experience = request.POST.get('experience')
        tasksrepo = request.POST.get('taskrepo')
        password = request.POST.get('password')
        discord_handle = request.POST.get('discord_handle')
        github_username = request.POST.get('github_username')
        phone = request.POST.get('phone')
        ap = Application(
            fullname=fullname,
            email=email,
            department=department,
            domain=domain,
            ques1=ques1,
            writeup=writeup,
            ac_year=ac_year,
            status=status,
            experience=experience,
            tasksrepo=tasksrepo,
            discord_handle=discord_handle,
            github_username=github_username,
            phone=phone,
            password=password
        )
        ap.save()
        return redirect(home)
        
    return render(request, 'pages/apply.html')

#Method to display user details using dynamic URL

def applications(request):
    return render(request, 'pages/applications.html')

def member(request, member_name):
    
    member = Member.objects.get(username=member_name)

    return render(request,'pages/member.html',{'user':member})

@unAuthenticated_user
def loginApp(request):
    if request.method == 'POST':
        username  = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            mem = Member.objects.get(username=username)
            if str(mem.role) == 'Administrator':
                return(redirect('adminapp'))
            else:
                return(redirect('membersapp'))
        else:
            messages.info(request, 'Wrong credentials')
            return render(request, 'pages/login.html')

    return render(request, 'pages/login.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrator'])
def admin_members(request):
    displaynames = User.objects.all()
    counts = User.objects.count
    roles = []
    user = User()
    role = request.user.groups.all()[0].name
    return render(request, 'adminapp/admin-members.html',{'displayUserNames': displaynames, 'counts':counts, 'role':role})

def achievements(request):
    achievements = Achievement.objects.all()
    return render(request, 'pages/achievements.html',{'achievements':achievements})

def logoutApp(request):
    logout(request)
    return redirect(loginApp)

def contact_us(request):
    return render(request, 'pages/contact-us.html')

def gallery(request):
    return render(request, 'pages/gallery.html')
