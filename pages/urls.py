from django.urls import path, include
from . import views
from adminapp.views import dashboard
from membersapp.views import dashboard as mDashboard
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home),
    path('login/', views.loginApp, name='login'),
    path('achievements/',views.achievements, name='achievements'),
    path('gallery/',views.gallery, name='gallery'),
    path('about/',views.contact_us, name='contact_us'),
    path('adminapp/', dashboard, name='adminapp'),
    path('applications/',views.applications, name='applications'),
    path('membersapp/', mDashboard, name='membersapp'),
    path('logout/', views.logoutApp, name='logout'),
    path('apply/',views.apply, name='apply'),
    path('<str:member_name>/',views.member),
       
]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

urlpatterns += static(settings.FILE_URL, document_root= settings.FILE_ROOT)
