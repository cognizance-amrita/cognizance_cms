from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/',views.dashboard),
    path('members/',views.members, name='members'),
    path('announcements/', views.announcements, name='announcements'),
    path('add-members/',views.add_members, name='add-members'),
    path('add-meeting/',views.add_meeting, name='add-meetings'),
    path('meetings/', views.meetings, name='meetings'),
    path('edit-profile/',views.edit_profile, name='edit-profile'),
    path('groups/',views.groups, name='groups'),
    path('submissions/<int:task_id>/',views.task_submissions, name='submissions'),
    path('add-group/',views.add_group,name='add-group'),
    path('reviewing/<str:application_id>/', views.reviewing, name='reviewing'),
    path('delete/<int:mid>/', views.delete),
    path('applications/', views.applications, name='applications'),
    path('tasks/',views.tasks, name='tasks'),
    path('status-updates/<str:sdate>/',views.status_updates, name='status-updates'),
]
