# CRON job for sending status updates

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Member

def periodic_mailer():
    members = list(Member.objects.all().values_list('email', flat=True))
    template = render_to_string('adminapp/status-update-template.html')
    plain_msg = strip_tags(template)
    send_mail(
                subject='Status Update',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=members,
                html_message=template, 
                message=plain_msg
    )
    print('Mailed')

    