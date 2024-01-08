#  ==================================================================================================
#  File Name: admin.py
#  Description: File serves the purpose of configuring and customizing the Django admin interface.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

from django.contrib import admin
from backend_app.models import Organization_data
from .models import *

admin.site.site_title = 'XDR Master'
admin.site.site_header = 'XDR Master Admin'
admin.site.index_title = 'Master Dashboard'

# Register your models here.
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Organization_data._meta.fields]

admin.site.register(Organization_data, OrganizationAdmin)

class PlansAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Plans_data._meta.fields]
admin.site.register(Plans_data, PlansAdmin)

class BillingsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Billings_data._meta.fields]
admin.site.register(Billings_data, BillingsAdmin)

class CountryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Country_data._meta.fields]
admin.site.register(Country_data, CountryAdmin)

class TimeZoneAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Time_Zone_data._meta.fields]
admin.site.register(Time_Zone_data, TimeZoneAdmin)

class AgentAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Agent_data._meta.fields]
admin.site.register(Agent_data, AgentAdmin)

class RoleAbilityAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Role_ability._meta.fields]
admin.site.register(Role_ability, RoleAbilityAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Client_data._meta.fields]
admin.site.register(Client_data, ClientAdmin)

class emailConfigAdmin(admin.ModelAdmin):
    list_display = [f.name for f in email_config_data._meta.fields]
admin.site.register(email_config_data, emailConfigAdmin)

class ApplicationsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Applications._meta.fields]
admin.site.register(Applications, ApplicationsAdmin)

class ApiExportAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Api_export._meta.fields]
admin.site.register(Api_export, ApiExportAdmin)

class InitConfigAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Init_Configs._meta.fields]
admin.site.register(Init_Configs, InitConfigAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in User._meta.fields if f.name != 'password']
admin.site.register(User, UserAdmin)

class ApiLogsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ApiLogs._meta.fields]
    list_per_page = 10
    list_filter = ['type']
    search_fields = ['req_method','type','table_name', 'id']
admin.site.register(ApiLogs, ApiLogsAdmin)