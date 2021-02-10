from huey.contrib.djhuey import periodic_task
from huey import crontab
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime
from datetime import datetime
from datetime import date 

@periodic_task(crontab(minute='*/2'))
def send_status_updates():
    template = render_to_string('adminapp/status-update-template.html')
    subject = f'Cognizance Status Update [{date.today()}]'
    plain_msg = strip_tags(template)
    mail.send_mail(
        subject,
        plain_msg,
        settings.EMAIL_HOST_USER,
        settings.EMAIL_GROUP,
        html_message=template,
        )
    print('Sent periodic status update')