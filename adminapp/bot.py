import discord
from discord.ext import commands
    
client = commands.Bot(command_prefix='jillu ')

guild = client.get_guild('790264911254388776')


def add_role(discord_handle, role):
    #member = guild.get_member_named(name=discord_handle)
    member = discord.utils.get(client.get_all_members(), id=discord_handle)
    the_role = discord.utils.get(member.guild.roles,name=role)
    #member.add_roles(discord.Role('790265904894050344'))
    member.add_roles(the_role)