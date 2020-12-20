from django.urls import path 
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('tasks/', views.member_tasks, name='tasks'),
    path('submit-task/<int:task_id>/',views.submit_task,name='submit_tasks'),
    
]
