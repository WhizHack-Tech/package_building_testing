 #  ======================================================================================================================================
#  File Name: apps.py
#  Description: Essential component of django app's configuration.To provide metadata and configuration for the app itself.
#  ----------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ========================================================================================================================================

from django.apps import AppConfig


class BackendAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_app'
