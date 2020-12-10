from django.shortcuts import render
from .decorators import allowed_users, unAuthenticated_user

# Create your views here.

@allowed_users(allowed_roles=['member'])
def dashboard(request):
    return render(request, 'membersapp/member-dashboard.html')