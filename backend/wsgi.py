"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""
#  ==============================================================================================================================================================================================================================================================================================================================
#  File Name: wsgi.py (Web Server Gateway Interface file)
#  Description: Automatically generated file and included by default in Django project. This file is serves a crucial role in deploying your Django application to a production web server, forms a bridge between the web server and Django application.

#  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===============================================================================================================================================================================================================================================================================================================================
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
