#  ==================================================================================================
#  File Name: mail_to.py
#  Description: This file contains code to send mail to single client or multiple clients at once. 
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings

def send_email_from_app(sendTo,subject,content_data,htmlTplPath):
    html_template_render = get_template(htmlTplPath).render(content_data)
    
    sendTo = list(sendTo.split(" "))
    email_msg = EmailMessage(subject = subject, body = html_template_render, from_email = settings.EMAIL_HOST_USER, to = sendTo, reply_to=[settings.EMAIL_HOST_USER])   
    email_msg.content_subtype = 'html'
    return email_msg.send(fail_silently=False)

def send_email_from_app_multiple(sendTo,subject,content_data,htmlTplPath):
    
    try:
        if not sendTo or not subject or not content_data or not htmlTplPath:
            return {"status": "error", "msg": "Missing required input parameters in the mail notification section"}
            
        html_template_render = get_template(htmlTplPath).render(content_data)

        email_msg = EmailMessage(subject = subject, body = html_template_render, from_email = settings.EMAIL_HOST_USER, to = sendTo, reply_to=[settings.EMAIL_HOST_USER])   
        email_msg.content_subtype = 'html'
        return {"status": "ok", "msg": email_msg.send(fail_silently=False)}
    except Exception as e:
        return {"status": "error", "msg": f"An error occurred while sending mail: {str(e)}"}
        