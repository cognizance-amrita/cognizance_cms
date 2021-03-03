import discord
from discord.ext import commands
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime
from .models import Member
    
client = commands.Bot(command_prefix='jillu ')

guild = client.get_guild('790264911254388776')

time = datetime.now().strftime("%H:%M:%S")

if str(time) == '15:22:00':
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


def add_role(discord_handle, role):
    #member = guild.get_member_named(name=discord_handle)
    member = discord.utils.get(guild.members, name=discord_handle)
    the_role = discord.utils.get(guild.roles,name=role)
    #member.add_roles(discord.Role('790265904894050344'))
    member.add_roles(the_role)