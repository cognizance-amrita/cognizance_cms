from discord import Webhook, RequestsWebhookAdapter
import requests

class Announcer:

    cMention = ''
    cMessage = ''

    def __init__(self, mention, message):
        self.cMention = mention
        self.cMessage = message

    def announce(self):
        webhook = Webhook.from_url('https://discordapp.com/api/webhooks/790274622880612393/cflyX0RGsh5kqkz5x2LRqe6cJZpSt7dH6RY5-PvQKSrOP5720qTkoEbIJY9DPkT_Y69T'
        , adapter= RequestsWebhookAdapter()
        )
        msg = 'This is an announcement for => ' + self.cMention + '\n' + self.cMessage
        webhook.send(msg)
