from discord import Webhook, RequestsWebhookAdapter
import requests
import discord
from discord.ext import commands
    
client = commands.Bot(command_prefix='jillu ')

class Bot:

    webhook = Webhook.from_url('https://discord.com/api/webhooks/818330362509918238/EQjeQmYltevJAjho3jKFVUzwQvUZVbzIENDNcMbBRcu7VO4kdZYQkRXN3s-EI3zNDKuN'
        , adapter= RequestsWebhookAdapter()
        )
    
    def add_role(self, username, role):
        msg = f'jillu admit <@!{username}> {role}'
        self.webhook.send(msg)


client.run('Nzg0NzU3MzM1MzIyOTE4OTEz.X8t8OA.21ySTuR_j6Sfe8f11kyPZCaj0rs')