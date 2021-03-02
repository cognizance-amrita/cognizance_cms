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

if str(time) == '17:31:00':
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

'''
@client.event
async def on_ready():
    print('Look who\'s here..')

@client.command(aliases=['hey','hi','hii'])
async def hello(ctx):
    await ctx.send('Hey dude')
'''

def add_role(discord_handle, role):
    guildd = discord.Guild()
    member = guildd.get_member_named(name=discord_handle)
    the_role = discord.utils.get(guild.roles,name=role)
    member.add_roles(discord.Role('790265904894050344'))

'''
@client.command()
@commands.has_permissions(manage_messages=True)
async def wipe(ctx, amt=1):
    await ctx.channel.purge(limit=amt)
    await ctx.send('Wiped out ' + str(amt) + ' messages')
    await ctx.channel.purge(limit=1)

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.event
async def on_message(message):
    ctx = await client.get_context(message)
    await client.invoke(ctx)

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return 

@commands.command()
async def trythis(ctx):
    ctx.send('Does this work ?')

client.run('Nzg0NzU3MzM1MzIyOTE4OTEz.X8t8OA.ZVF5GzEfMfcBKXtDCBSbrISFAHQ')

'''