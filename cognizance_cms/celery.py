from __future__ import absolute_import, unicode_literals  
import os  
from celery import Celery  
from celery.schedules import crontab  
  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cognizance_cms.settings')  
# celery settings for the demo_project  
app = Celery('cognizance_cms')  
app.config_from_object('django.conf:settings', namespace='CELERY')  
# here is the beat schedule dictionary defined  
app.conf.beat_schedule = {  
    'print-every-day': {  
        'task': 'adminapp.tasks.periodic_mailer',  
        'schedule': crontab(hour=14, minute=59)  
    },  
}  
app.conf.timezone = 'IST'  
app.autodiscover_tasks()  