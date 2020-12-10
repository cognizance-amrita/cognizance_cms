from discord import Webhook, RequestsWebhookAdapter
import requests

class Announcer:

    cMention = ''
    cMessage = ''

    def __init__(self, mention, message):
        self.cMention = mention
        self.cMessage = message

    def announce(self):
        webhook = Webhook.from_url('https://discordapp.com/api/webhooks/784819553779712082/2cMicOmikSrR8Yua5TAFE9rUWjw_KoKdkcs4UJZ7bJ39LSviYuwGO9mL5xVC-ngLuZV0'
        , adapter= RequestsWebhookAdapter()
        )
        msg = 'This is an announcement for => ' + self.cMention + '\n' + self.cMessage
        webhook.send(msg)
