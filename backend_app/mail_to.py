#  ==================================================================================================
#  File Name: mail_to.py
#  Description: This file contains code to send mail to single client or multiple clients at once. 
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

# This file contains functions to send mail to user
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings

# used when new user is added
def send_email_from_app(sendTo,subject,content_data,htmlTplPath):
    html_template_render = get_template(htmlTplPath).render(content_data)
    
    sendTo = list(sendTo.split(" "))
    email_msg = EmailMessage(subject = subject, body = html_template_render, from_email = settings.EMAIL_HOST_USER, to = sendTo, reply_to=[settings.EMAIL_HOST_USER])   
    email_msg.content_subtype = 'html'
    return email_msg.send(fail_silently=False)

def send_email_from_app_multiple(sendTo,subject,content_data,htmlTplPath):
    html_template_render = get_template(htmlTplPath).render(content_data)

    email_msg = EmailMessage(subject = subject, body = html_template_render, from_email = settings.EMAIL_HOST_USER, to = sendTo, reply_to=[settings.EMAIL_HOST_USER])   
    email_msg.content_subtype = 'html'
    return email_msg.send(fail_silently=False)


def send_multiple_mail(sendTo, subject, content_data, htmlTplPath):
    try:
        if not sendTo or not subject or not content_data or not htmlTplPath:
            return {"status": "error", "msg": "Missing required input parameters in the mail notification section"}

        # Render the HTML template
        html_template_render = get_template(htmlTplPath).render(content_data)

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = ', '.join(sendTo)
        msg['Subject'] = subject

        # Attach the HTML content to the email
        msg.attach(MIMEText(html_template_render, 'html'))

        # Connect to the SMTP server and send the email
        smtp_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        smtp_server.starttls()
        smtp_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp_server.sendmail(settings.EMAIL_HOST_USER, sendTo, msg.as_string())
        smtp_server.quit()

        return {"status": "ok", "msg": "Email sent successfully"}
    except Exception as e:
        return {"status": "error", "msg": f"An error occurred while sending mail: {str(e)}"}