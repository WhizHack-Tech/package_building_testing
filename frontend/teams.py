#  ==================================================================================================
#  File Name: teams.py
#  Description: File to create a web hook for Teams application.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

import requests

webhook_url = "https://whizhacktech.webhook.office.com/webhookb2/d3722f5d-f9e8-4c35-9255-de03bfc7b16e@841fbdba-c11c-4b74-afee-4bb3712866d7/IncomingWebhook/7a559a26e5384ada80499b516d9f7ce7/2870e706-0f76-4f19-b919-a5cfc3222481"

webhook_url2 = "https://whizhacktech.webhook.office.com/webhookb2/d3722f5d-f9e8-4c35-9255-de03bfc7b16e@841fbdba-c11c-4b74-afee-4bb3712866d7/IncomingWebhook/46f5a24461264dbb8c50213ed24a7a94/2870e706-0f76-4f19-b919-a5cfc3222481"

payload = {
    "text": "Notification Details check"
}

response = requests.post(
    webhook_url2,
    json=payload
)

if response.status_code == 200:
    print("Notification sent successfully!")
else:
    print("Error sending notification:", response.text)
