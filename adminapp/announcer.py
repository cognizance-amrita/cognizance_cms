from discord import Webhook, RequestsWebhookAdapter
import requests

class Announcer:

    cMention = ''
    cMessage = ''
    webhook = Webhook.from_url('https://discordapp.com/api/webhooks/790274622880612393/cflyX0RGsh5kqkz5x2LRqe6cJZpSt7dH6RY5-PvQKSrOP5720qTkoEbIJY9DPkT_Y69T'
        , adapter= RequestsWebhookAdapter()
        )

    def __init__(self, mention=None, message=None):
        self.cMention = mention
        self.cMessage = message

    def announce(self):
        msg = 'This is an announcement for => ' + self.cMention + '\n' + self.cMessage
        self.webhook.send(msg)

    def notify_acceptance(self, username):
        msg = f'{username} is accepted into the club.'
        self.webhook.send(msg)
    
    def add_role(self, username):
        msg = f'jillu admit <@{username}>'
        self.webhook.send(msg)


