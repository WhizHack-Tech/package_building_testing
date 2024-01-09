#  ==================================================================================================
#  File Name: teams.py
#  Description: File to create a web hook for Teams application.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

import requests

webhook_url = 'https://whizhacktech.webhook.office.com/webhookb2/d3722f5d-f9e8-4c35-9255-de03bfc7b16e@841fbdba-c11c-4b74-afee-4bb3712866d7/IncomingWebhook/7dbb55b5e15d4d069d4af7d5366a26b2/2870e706-0f76-4f19-b919-a5cfc3222481'

payload = {
    'text': 'There is an alert in your enviroment',
    'title': 'XDR ALERTS',
    'themeColor': '0072C6'
}

response = requests.post(webhook_url, json=payload)
