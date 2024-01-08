#  ================================================================================================
#  File Name: urls.py
#  Description: backend_app's url file to map URL patterns to each view.

#  ------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ================================================================================================

from django.urls import path
from .fake_db import *
from .import views
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include, re_path
from .account_manage_view import *

urlpatterns = [
    # path('', views.index),
    path('master-registration', UserRegistrationView.as_view()),
    path('master-login', UserLoginView.as_view()),
    path('master-profile', UserProfileView.as_view()),
    path('create/',Create_data,name='Create_data'), #Add New Organization
    path('administration/account-settings/', index),
    path('settings/billing', index),
    path('settings/plans', index),
    path('administration/roles', index),
    path('administration/user/view/', index),
    path('administration/user/view/<str:pk>/', index),
    path('administration/user/list', index),
    path('delete/<str:pk>/',Delete_data,name='Delete_data'),
    path('show/',show,name='show_data'),
    path('0status/', Displayall_org_with_0status),
    path('1status/', Displayall_org_with_1status),
    path('update/<str:pk>/', updateOrg.as_view()),
    path('bothstatus/', Displayall_org_with_bothstatus),
    path('bothstatus/<str:pk>/', Displayall_org_with_bothstatus2),
    path('products/', getProducts),
    path('products/<str:pk>/', getProduct),
    path('users/', UserListOrg.as_view()),
    path('users/<str:organization_id>/', UserDetailOrg.as_view()),
    path('planbilling/', Billings_Plans_data),#no need to integrate with frontend
    path('addplan/', Add_Plans_data_status_updated),
    path('addbilling/', Add_Billings_data_status_updated),
    path('showplan/', Show_Plan_Data),#no need to integrate with frontend
    path('billinglist/', BillingListOrg), #views list all of billings
    path('billinglist/<int:pk>/', BillingDetailOrg), #views list id of billings
    path('planlist/', PlanListOrg), #views list all of plan
    path('planlist/<int:pk>/', PlanDetailOrg), #views list id of plan
    #re_path(r'.*', views.index),
    #re_path(r'images/backend_master/static/images.*', views.index),
    path('countrydata/', Display_Country_data),
    path('timezonedata/', Display_TimeZone_data),
    path('billinglisttimes/', BillingListOrgTimes.as_view()), #views list all of billings with date and time based on india
    path('billinglisttimes/<int:pk>/', BillingDetailOrgTimes.as_view()), #views list id of billings with date and time based on india
    path('planlisttimes/', PlanListOrgTimes.as_view()), #views list all of plan
    path('planlisttimes/<int:pk>/', PlanDetailOrgTimes.as_view()), #views list id of plan
    path('agentintodb', store_agent_into_db), #agent data add(updated)
    path('usertodb', store_user_in_db), #user data add
    path('emailconfigtodb', store_email_config_indb), #email config data add
    path('displayemailconfig', display_email_config), #display email config data
    path('displayuser/', list_users),
    path('displayuser/<str:pk>/', Retrieve_users.as_view()),
    path('client-logs', Displayall_Client_Logs),
    path('master-logs', Displayall_Master_Logs),
    path('user-api-logs', Show_ApiLogs),
    path('allagent/', get_all_agent_details, name='all-agent-details'),
    # Other URL patterns for your API views
    path('addapplication',Add_Applications),
    path('application-views/', ApplicationListOrg),
    path('application-views/<int:pk>/', ApplicationDetailOrg),
  #fake data urls 
    path('support_tarcker', support),
    path('agents', count),
    path('sales', service),
    path('nsrc', nsrccount),
    path('sessions', sessions_by_os),
    path('customers', customers_count),
    path('earnings', earnings_count),	
    path('save-data-opensearch', ApiSetData.as_view()),
    path('disable-org',DisableOrgAccount.as_view()),
    path('disable-user', DisableUserAccount.as_view()),
    path('show-user-org-count', OrgUserNumber),
    path('add-app-details', AddAppDetails),
    path('change-application-status', ApplicationStatus.as_view()),
    path('show-page-permissions', PagePermissionsView.as_view()), #not used
    path('org-location-json', display_location_org_nested_json),
    #get all location data within an organization #similar to bothstatus url
    path('location-data-org', display_all_location_in_org),
    path('add-location-get-org', add_location_get_org_name),#get org-names when location is added

#---------------------- Update some api currently working (previous api) in XDR Master----------------------------------
    # To add location
    path('add-location-step-one', add_location_step_one), # basic details add this url only store details in location models
    path('add-location-step-three', add_location_step_three), # updated code step-3 agent-details, init config and and db credentials add this url
    path('add-location-step-two', add_location_step_two), # updated code step-2 updated plan create,page pagepermission only add this url

     # To get location
    path('show-location-org/<str:pk>/<int:pk2>', pkey_display_location),
    path('show-location-org/', display_location),

    # To get email_config with config_type and location_id with update
    path('add-email-config-update', email_config_update),
    path('add-dashboard-config-update', dashboard_config_update),
    path('add-notification-config-update', notification_config_update),  

    path('get-notification', display_notification_config),
    path('get-dashboard', display_dashboard_config),
    path('get-email', display_email_config),


    path('all-config', all_display_config),#working with frontend
    path('get-all-pagepermission', display_all_pagepermission), # working
    path('update-pagepermission', update_pagepermission),

    # To get all agents with ture and false condition
    path('get-agent', display_all_agent),
    path('ture-false-agent-details', is_active_true_false_all_agent), # active and deactive agent details
   
    # update opensearch connection details on basis of location_id, plan_id
    path('update-opensearch-connection-details', update_opensearch_connection_details),
    path('email-display', EmailClientListOrg),

    # To add license-management details:- Trace,Nids and Hids
    path('add-trace-license-management', add_trace_license_management),
    path('add-nids-license-management', add_nids_license_management),
    path('add-hids-license-management', add_hids_license_management),
    path('add-soar-sensor-details',add_soar_license_management),

    # To Get api license-managemt details
    path('display-trace-license-management',display_trace_license_management),
    path('display-nids-license-management',display_nids_license_management),
    path('display-hids-license-management',display_hids_license_management),
    path('display-soar-sensor-details',display_soar_license_management),

    # client email IDs, admin email IDs for Health check sensor alert notifications
    path('display-hc-sensor-alert-email',display_hc_sensor_alert_email_config),
    path('add-hc-sensor-alert-email',add_hc_sensor_alert_email_config),

    # updated_plan section
    # add plan
    path('add-plan-step-one',add_plan_step_one),
    path('add-plan-step-two',add_plan_step_two),
    path('add-trace-license-plan-step-three',add_trace_license_plan_step_three),
    path('add-nids-license-plan-step-three',add_nids_license_plan_step_three),
    path('add-hids-license-plan-step-three',add_hids_license_plan_step_three),
    path('add-soar-license-plan-step-three',add_soar_license_plan_step_three),
    # display plan
    path('display-updated-plan/', display_all_updated_plan),
    path('display-updated-plan/<int:pk>/', display_id_wise_updated_plan),
    # update plan
    path('upgrade-plan', upgrade_plan),
    # get plans not active on any location
    path('get-inactive-plans/', get_all_plans_not_active_on_any_location),
    path('get-inactive-plans/<int:pk>/', get_single_plan_not_active_on_any_location),


    # Plan2 (section - plan2 (upgrade)) updated api individuals 
    path('plan2-update-details', plan2_update_details),
    path('pruduct-update-details-plan2', pruduct_update_details_plan2),
    path('trace-license-update-details-plan2', trace_license_management_update_details_plan2),
    path('nids-license-update-details-plan2', nids_license_management_update_details_plan2),
    path('hids-license-update-details-plan2', hids_license_management_update_details_plan2),
    path('soar-license-update-details-plan2', soar_license_management_update_details_plan2),


    # Get(get api) and Decrease(post api) count multiple license models
    path('multiple-decrease-license-count', DecreaseLicenseCount.as_view(), name='decrease-license-count'), # multiple license management models  decrease count behalf of sensor key from active count
    path('display-multiple-decrease-license-count', GetMultipleLicenseData.as_view(), name='display-multiple-decrease-license-count'), # multiple license management models  decrease count behalf of sensor key from active count
    
    # get plan_id with env product true and logs indices name
    path('get-all-license-management-details',get_license_management_details_with_logs_indices_env),# working get all details  api plan and sensor_id only

    # to verify-- unverified users 
    path('verify-unverified-user/<str:user_id>', verify_unverified_user), #already existing user verify
    path('reset-user-password', reset_user_password), #already existing user password reset


]

urlpatterns = format_suffix_patterns(urlpatterns)