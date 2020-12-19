from django.urls import path 
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('tasks/', views.member_tasks, name='tasks')
    
]
