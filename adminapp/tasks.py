from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime
from datetime import datetime, timedelta
from datetime import date 
import time

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

def send_email_at(send_time):
    time.sleep(send_time.timestamp() - time.time())
    send_status_updates()
    print('email sent')

first_email_time = datetime(2021,2,10,18,0,0)
interval = timedelta(days=1)
send_time = first_email_time

while True:
    send_email_at(send_time)
    send_time = send_time + interval