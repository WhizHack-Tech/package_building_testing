#  ==================================================================================================
#  File Name: slack.py
#  Description: File to create a web hook for slack application.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

import requests
import json 

web_hook_url = "https://hooks.slack.com/services/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"

# web_hook_url2 = "https://whizhacktech.webhook.office.com/webhookb2/d3722f5d-f9e8-4c35-9255-de03bfc7b16e@841fbdba-c11c-4b74-afee-4bb3712866d7/IncomingWebhook/7a559a26e5384ada80499b516d9f7ce7/2870e706-0f76-4f19-b919-a5cfc3222481"

slack_msg = {
    "text": "It's an alert ",
    "username": "Zerohack Alerts Check",
    "graph_url": "https://xdr.zerohack.in/static/media/logo3.f52483f1.png",
    "as_user": False}

requests.post(web_hook_url, data=json.dumps(slack_msg))
