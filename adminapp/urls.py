from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard/',views.dashboard),
    path('members/',views.members, name='members'),
    path('announcements/', views.announcements, name='announcements'),
    path('add-members/',views.add_members, name='add-members'),
    path('groups/',views.groups, name='groups'),
    path('submissions/<int:task_id>/',views.task_submissions, name='submissions'),
    path('add-group/',views.add_group,name='add-group'),
    path('reviewing/<str:application_id>/', views.reviewing, name='reviewing'),
    path('delete/<int:mid>/', views.delete),
  #  path('submit-review/<str:application_id>/', views.submit_review, name='submit-review'),
    path('applications/', views.applications, name='applications'),
    path('tasks/',views.tasks, name='tasks'),
    path('status-updates/',views.status_updates, name='status-updates'),
    path('status-updates/<str:date>',views.view_status, name='view-status'),
]
