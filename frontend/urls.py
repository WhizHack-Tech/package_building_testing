#  ================================================================================================
#  File Name: urls.py
#  Description: frontend app's url file to map URL patterns to each view.

#  ---------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ================================================================================================

from django.urls import path

# for testing dashboard views
from . import dashboard_queries, views
from .account_manage_view import *
from .attack_events_queries import *
from .dashboard_queries import *
from .fake_db import *
from .health_check.common_query_all_agents import *
from .hids.hids_alert_mitre_attack_page import *
from .hids.hids_alert_query import *
from .hids.hids_event_mitre_attack_page import *
from .hids.hids_event_query import *

#
from .hids.hids_incident_mitre_attack_page import *
from .hids.hids_incident_query import *
from .live_network_map import live_network_map
from .nids.nids_alert import *
from .nids.nids_attack_events_page import *
from .nids.nids_dashboard_page import *
from .nids.nids_event import *
from .nids.nids_incident import *
from .soar_query.soar_ip_query import *
from .trace.trace_alert import *
from .trace.trace_event import *
from .trace.trace_glog import *
from .trace.trace_incident import *
from .views import *
from .wo_agent_id_hids_queries import *

urlpatterns = [
    path("client-registration", UserRegistrationView.as_view()),
    path("client-login", UserLoginView.as_view()),
    path(
        "generate-new-password", ChangeCleintPasswordView.as_view()
    ),  # called on first password change
    path("date-filter", DashboardPage.as_view()),
    path("charts-attack-events", ChartsAttackEvents.as_view()),
    path("account-maf", AccountSettingMFA.as_view()),
    path("mfa-verity-otp", MFA_veriryOtp.as_view()),
    path(
        "forgot-pass", ForgotPassword.as_view()
    ),  # mail sent to user with 6 digit code-pass changed
    path("resend-otp", Resend_otp.as_view()),
    path("charts-intelligence", ChartsIntelligence.as_view()),
    path(
        "user-register", UserRegistateView
    ),  # called when user created through XDR- Mail is sent to user
    path("sub-clients", SubClientView.as_view()),
    # user log per user wise
    path("user-api-logs", Show_ApiLogs),
    path("countries", views.Display_Country_data),
    path("account-manage-detail", AccountManageView.as_view()),
    path("account-information-update", UpdateInformation),
    path("account-genral-update", Update_Genral_Information),
    # Report Section
    path("incident-response-report", Incident_Response_report),
    path("executive-report", Executive_report),
    path("client-logs", Displayall_api_logs),
    path("get-trace-sensor-names", GetTraceSensorNames),
    # 3rd Party API Section(not used this api)
    path("xdr-api", Xdr_api.as_view()),  # not using this api (previous api)
    path("create-api-keys", Third_party_api),  # not using this api (previous api)
    path(
        "status-api-keys", Third_party_status_api
    ),  # not using this api (previous api)
    path("show-api-keys", Show_ApiKeys),  # not using this api (previous api)
    path("update-email-config", Email_Config_Update),
    path("display-config", Display_Config),
    path("update-dashboard-config", Dashboard_Config_Update),
    path("update-notification-config", Notification_Config_Update),
    path("activate-deativate", ActivateDeactivate),
    path("api", MlDlDetectionPage.as_view()),
    path("active-init-config", UpdateUserNotificationStatus.as_view()),
    # (r'^showtrees', views.RenderTrees, name='render')
    # FAKE DATA START #
    path("graph", graph),
    path("service", service),
    path("ip_count", ip_count),
    path("wazuh_data", wazuh_data),
    path("wazuh2_data", wazuh2_data),
    # path('logs_ativity', logs_ativity),
    # FAKE DATA END #
    # network map #
    path("dynamic-network-map", dynamic_network_map),
    # network map END #
    path("application-details", views.ApplicationListOrg),
    path("app-shop", views.ApplicationDisplay),  # for application Shop page
    path("app-shop/<int:pk>/", views.ApplicationDetailOrg),
    path("email-display/", EmailClientListOrg),
    path(
        "innovative-search-get-indices-name", InnovativeSearchIndicesNameView.as_view()
    ),
    path("innovative-search-api", InnovativeSearchApi),
    path("disable-user-account", DisableUserAccount.as_view()),
    path(
        "wazuh-integration", ApiSetData.as_view()
    ),  # whenever use this url, replace wazuh with something else #currently not being used
    path("dashboard-lang-update", dashboard_lang_update),
    path("dashboard-lang", dashboar_lang),
    path("display-page-permissions", DisplayPagePermissionsView.as_view()),
    path("date-check", Check_Api.as_view()),
    path("live-map-view", live_network_map),
    # NIDS-Dashboard Page urls
    path("nids-dashboard-int-attack", nids_dashboard_int_attack_card),
    path("nids-dashboard-int-table", nids_dashboard_int_attack_table),
    path("nids-dashboard-outgoing-botnet", nids_dashboard_outgoing_botnet_card),
    path("nids-dashboard-outgoing-botnet-table", nids_dashboard_outgoing_botnet_table),
    path("nids-dashboard-ext", nids_dashboard_ext_count),
    path("nids-dashboard-ext-table", nids_dashboard_ext_count_table),
    path("nids-dashboard-overall-attack-pie", nids_dashboard_overall_attack_pie),
    path("nids-dashboard-overall-attack-table", nids_dashboard_overall_attack_table),
    path("nids-dashboard-threat-logs", nids_dashboard_threat_logs),
    path("nids-dashboard-detected-threat-card", nids_dashboard_detected_threat_type),
    path(
        "nids-dashboard-detected-threat-table",
        nids_dashboard_detected_threat_type_table,
    ),
    path("nids-dashboard-int-ext-attack", nids_dashboard_int_ext_attack_count),
    path("nids-dashboard-int-ext-attack-table", nids_dashboard_int_ext_attack_table),
    # NIDS-Attack Events Page urls
    path("nids-attck-event-service-name", nids_attck_event_service_name),
    path("nids-attck-event-service-name-table", nids_attck_event_service_name_table),
    path("nids-attck-event-source-country", nids_attck_event_source_country),
    path(
        "nids-attck-event-source-country-table", nids_attck_event_source_country_table
    ),
    path("nids-attck-event-geo", nids_attck_event_geolocation),
    path("nids-attck-event-geo-table", nids_attck_event_geolocation_table),
    path("nids-attck-event-city", nids_attck_event_top_city),
    path("nids-attck-event-city-table", nids_attck_event_city_table),
    path("nids-attck-event-asn", nids_attck_event_top_asn),
    path("nids-attck-event-asn-table", nids_attck_event_asn_table),
    path("nids-attck-event-line", nids_attck_event_ip_line_chart),
    path("nids-attck-event-line-table", nids_attck_event_ip_line_table),
    path("nids-attck-event-port", nids_attck_event_port),
    path("nids-attck-event-port-table", nids_attck_event_port_table),
    path("nids-attck-event-mac", nids_attck_event_mac_addr),
    path("nids-attck-event-mac-table", nids_attck_event_mac_table),
    path("nids-attck-event-frequency", nids_attck_event_frequency),
    path("nids-attck-event-freq-table", nids_attck_event_freq_table),
    path("modified-line-chart-testing", modified_line_chart),  # only for testing
    path("modified-ext-count", modified_ext_count_card),
    # NIDS-Alert Page urls
    path(
        "critical-threats-count-nids-alert", nids_alert_critical_threats
    ),  # taken from dashboard page
    path(
        "nids-dashboard-critical-threats-table", nids_alert_critical_threats_table
    ),  # taken from dashboard page
    path("internal-attack-card-nids-alert", nids_alert_int_compr),
    path("internal-attack-table-nids-alert", nids_alert_int_compr_table),
    path("nids-alert-lateral-mov", nids_alert_lateral_mov),
    path("nids-alert-lateral-mov-table", nids_alert_lateral_mov_table),
    path("nids-alert-ext", nids_alert_ext),
    path("nids-alert-ext-table", nids_alert_ext_table),
    path("nids-alert-freq-targetted-host", nids_alert_freq_targetted_host),
    path("attack-frequency-card-nids-alert", nids_alert_attack_frequency),
    path("nids-alert-attack-freq-table", nids_alert_attack_freq_table),
    path("nids-alert-attacker-ip-line-chart", nids_alert_line_chart),
    path("nids-alert-attacker-ip-line-table", nids_alert_line_table),
    path("nids-alert-service-name-bar-chart", nids_alert_service_name_bar_chart),
    path("nids-alert-service-name-bar-table", nids_alert_service_name_bar_table),
    path("nids-alert-attacker-port-bar-chart", nids_alert_attacker_port_pie_chart),
    path("nids-alert-attacker-port-bar-table", nids_alert_attacker_port_pie_table),
    path("nids-alert-ids-class-bar-chart", nids_alert_ids_class_bar_chart),
    path("nids-alert-ids-class-bar-table", nids_alert_ids_class_bar_table),
    path("nids-alert-malware-type-bar-chart", nids_alert_malware_type_pie_chart),
    path("nids-alert-malware-type-table", nids_alert_malware_type_pie_table),
    path("nids-alert-mitre-tactics-bar-chart", nids_alert_mitre_tactics_bar_chart),
    path("nids-alert-mitre-tactics-table", nids_alert_mitre_tactics_bar_table),
    path("nids-alert-mitre-techniq-bar-chart", nids_alert_mitre_techniq_bar_chart),
    path("nids-alert-mitre-techniq-table", nids_alert_mitre_techniq_bar_table),
    path("nids-alert-detected-threat-card", nids_alert_detected_threat_type),
    path("nids-alert-detected-threat-table", nids_alert_detected_threat_type_table),
    path("nids-alert-geo", nids_alert_geolocation),
    path("nids-alert-geo-table", nids_alert_geolocation_table),
    path("nids-alert-country-bar-chart", nids_alert_country_bar_chart),
    path("nids-alert-country-table", nids_alert_country_bar_table),
    path("nids-alert-asn-bar-chart", nids_alert_asn_bar_chart),
    path("nids-alert-asn-table", nids_alert_asn_bar_table),
    path("nids-alert-city-pie-chart", nids_alert_city_pie_chart),
    path("nids-alert-city-table", nids_alert_city_pie_table),
    path("nids-alert-target-ip-pie", nids_alert_target_ip_pie_chart),
    path("nids-alert-target-ip-table", nids_alert_target_ip_table),
    path("nids-alert-target-mac-pie", nids_alert_target_mac_pie_chart),
    path("nids-alert-target-mac-table", nids_alert_target_mac_table),
    path("nids-alert-target-port-pie", nids_alert_target_port_pie_chart),
    path("nids-alert-target-port-table", nids_alert_target_port_table),
    path("nids-alert-freq-attacker", nids_alert_freq_attacker),
    path("nids-alert-attacked-service", nids_alert_attacked_service_details),
    path("threat-type-count-nids-alert", nids_alert_threat_type_ser_label),
    # NIDS Alert ML DL page urls
    path("nids-alert-ml-detected-threat", nids_alert_ml_detected_threat),
    path("nids-alert-ml-detected-threat-table", nids_alert_ml_detected_threat_table),
    path("nids-alert-ml-map", nids_alert_ml_map),
    path("nids-alert-ml-map-table", nids_alert_ml_map_table),
    path("nids-alert-ml-cntry-bar", nids_alert_ml_cntry_bar),
    path("nids-alert-ml-cntry-table", nids_alert_ml_cntry_bar_table),
    path("nids-alert-ml-asn-bar", nids_alert_ml_asn_bar),
    path("nids-alert-ml-asn-table", nids_alert_ml_asn_table),
    path("nids-alert-ml-city-pie", nids_alert_ml_city_pie),
    path("nids-alert-ml-city-table", nids_alert_ml_city_table),
    path("nids-alert-ml-target-ip-pie", nids_alert_ml_target_ip_pie),
    path("nids-alert-ml-target-ip-table", nids_alert_ml_target_ip_table),
    path("nids-alert-ml-target-mac-pie", nids_alert_ml_target_mac_pie_chart),
    path("nids-alert-ml-target-mac-table", nids_alert_ml_target_mac_table),
    path("nids-alert-ml-trgt-port-pie", nids_alert_ml_target_port_pie),
    path("nids-alert-ml-trgt-port-table", nids_alert_ml_target_port_table),
    path("nids-alert-ml-freq-trgted-host", nids_alert_ml_freq_trgted_host),
    path("nids-alert-ml-freq-attacker", nids_alert_ml_freq_attacker),
    path("nids-alert-ml-attacked-service", nids_alert_ml_attacked_service_details),
    # NIDS Event Page urls
    # path('nids-event-critical-threats', nids_event_critical_threats),
    # path('nids-event-critical-threats-table', nids_event_critical_threats_table),
    # path('nids-event-lateral-mov', nids_event_lateral_mov),
    # path('nids-event-lateral-mov-table', nids_event_lateral_mov_table),
    # path('nids-event-int-compr', nids_event_int_compr),
    # path('nids-event-int-compr-table', nids_event_int_compr_table),
    # path('nids-event-ext', nids_event_ext),
    # path('nids-event-ext-table', nids_event_ext_table),
    path("nids-event-attack-freq", nids_event_attack_frequency),
    path("nids-event-attack-freq-table", nids_event_attack_freq_table),
    path("nids-event-attacker-ip-line-chart", nids_event_line_chart),
    path("nids-event-attacker-ip-line-table", nids_event_line_table),
    path("nids-event-service-name-bar-chart", nids_event_service_name_bar_chart),
    path("nids-event-service-name-bar-table", nids_event_service_name_bar_table),
    path("nids-event-attacker-port-pie-chart", nids_event_attacker_port_pie_chart),
    path("nids-event-attacker-port-table", nids_event_attacker_port_pie_table),
    # path('nids-event-ids-class-bar-chart', nids_event_ids_class_bar_chart),
    # path('nids-event-ids-class-bar-table', nids_event_ids_class_bar_table),
    # path('nids-event-malware-type-bar-chart', nids_event_malware_type_bar_chart),
    # path('nids-event-malware-type-table', nids_event_malware_type_bar_table),
    # path('nids-event-mitre-tactics-bar-chart', nids_event_mitre_tactics_bar_chart),
    # path('nids-event-mitre-tactics-table', nids_event_mitre_tactics_bar_table),
    # path('nids-event-mitre-techniq-bar-chart', nids_event_mitre_techniq_bar_chart),
    # path('nids-event-mitre-techniq-table', nids_event_mitre_techniq_bar_table),
    path("ids-detected-threat-card-nids-event", nids_event_detected_threat_type),
    path("ids-detected-threat-table-nids-event", nids_event_detected_threat_type_table),
    path("nids-event-geo", nids_event_geolocation),
    path("nids-event-geo-table", nids_event_geolocation_table),
    path("nids-event-country-bar-chart", nids_event_country_bar_chart),
    path("nids-event-country-table", nids_event_country_bar_table),
    path("nids-event-city-pie-chart", nids_event_city_pie_chart),
    path("nids-event-city-table", nids_event_city_pie_table),
    path("nids-event-asn-bar-chart", nids_event_asn_bar_chart),
    path("nids-event-asn-table", nids_event_asn_bar_table),
    path("nids-event-target-ip-pie", nids_event_target_ip_pie_chart),
    path("nids-event-target-ip-table", nids_event_target_ip_table),
    path("nids-event-target-mac-pie", nids_event_target_mac_pie_chart),
    path("nids-event-target-mac-table", nids_event_target_mac_table),
    path("nids-event-target-port-pie", nids_event_target_port_pie_chart),
    path("nids-event-target-port-table", nids_event_target_port_table),
    path("nids-event-freq-targetted-host", nids_event_freq_targetted_host),
    path("nids-event-freq-attacker", nids_event_freq_attacker),
    path("nids-event-attacked-service", nids_event_attacked_service_details),
    # NIDS Event ML DL page urls
    path("detected-threat-nids-event-ml", nids_event_ml_detected_threat),
    path("detected-threat-table-nids-event-ml", nids_event_ml_detected_threat_table),
    path("geoloc-nids-event-ml", nids_event_ml_map),
    path("geoloc-table-nids-event-ml", nids_event_ml_map_table),
    path("cntry-bar-nids-event-ml", nids_event_ml_cntry_bar),
    path("cntry-table-nids-event-ml", nids_event_ml_cntry_bar_table),
    path("asn-bar-nids-event-ml", nids_event_ml_asn_bar),
    path("asn-table-nids-event-ml", nids_event_ml_asn_table),
    path("city-pie-nids-event-ml", nids_event_ml_city_pie),
    path("city-table-nids-event-ml", nids_event_ml_city_table),
    path("target-ip-pie-nids-event-ml", nids_event_ml_target_ip_pie),
    path("target-ip-table-nids-event-ml", nids_event_ml_target_ip_table),
    path("target-mac-pie-nids-event-ml", nids_event_ml_target_mac_pie_chart),
    path("target-mac-table-nids-event-ml", nids_event_ml_target_mac_table),
    path("trgt-port-pie-nids-event-ml", nids_event_ml_target_port_pie),
    path("trgt-port-table-nids-event-ml", nids_event_ml_target_port_table),
    path("freq-trgted-host-nids-event-ml", nids_event_ml_freq_trgted_host),
    path("freq-attacker-nids-event-ml", nids_event_ml_freq_attacker),
    path("attacked-service-nids-event-ml", nids_event_ml_attacked_service_details),
    # NIDS-Incident Page urls
    path("nids-incident-critical-threats", nids_incident_critical_threats),
    path("nids-incident-critical-threats-table", nids_incident_critical_threats_table),
    path("nids-incident-int-compr", nids_incident_int_compr),
    path("nids-incident-int-compr-table", nids_incident_int_compr_table),
    path("nids-incident-lateral-mov", nids_incident_lateral_mov),
    path("nids-incident-lateral-mov-table", nids_incident_lateral_mov_table),
    path("nids-incident-ext", nids_incident_ext),
    path("nids-incident-ext-table", nids_incident_ext_table),
    path("nids-incident-attack-freq", nids_incident_attack_frequency),
    path("nids-incident-attack-freq-table", nids_incident_attack_freq_table),
    path("nids-incident-attacker-ip-line-chart", nids_incident_line_chart),
    path("nids-incident-attacker-ip-line-table", nids_incident_line_table),
    path("nids-incident-service-name-bar-chart", nids_incident_service_name_bar_chart),
    path("nids-incident-service-name-bar-table", nids_incident_service_name_bar_table),
    path(
        "nids-incident-attacker-port-bar-chart", nids_incident_attacker_port_bar_chart
    ),
    path(
        "nids-incident-attacker-port-bar-table", nids_incident_attacker_port_bar_table
    ),
    path("nids-incident-ids-class-bar-chart", nids_incident_ids_class_bar_chart),
    path("nids-incident-ids-class-bar-table", nids_incident_ids_class_bar_table),
    path("nids-incident-malware-type-bar-chart", nids_incident_malware_type_pie_chart),
    path("nids-incident-malware-type-table", nids_incident_malware_type_pie_table),
    path("nids-incident-detected-threat-card", nids_incident_detected_threat_type),
    path(
        "nids-incident-detected-threat-table", nids_incident_detected_threat_type_table
    ),
    path("nids-incident-geo", nids_incident_geolocation),
    path("nids-incident-geo-table", nids_incident_geolocation_table),
    path("nids-incident-country-bar-chart", nids_incident_country_bar_chart),
    path("nids-incident-country-table", nids_incident_country_bar_table),
    path("nids-incident-city-pie-chart", nids_incident_city_pie_chart),
    path("nids-incident-city-table", nids_incident_city_pie_table),
    path("nids-incident-asn-bar-chart", nids_incident_asn_bar_chart),
    path("nids-incident-asn-table", nids_incident_asn_bar_table),
    path("nids-incident-target-ip-pie", nids_incident_target_ip_pie_chart),
    path("nids-incident-target-ip-table", nids_incident_target_ip_table),
    path("nids-incident-target-mac-pie", nids_incident_target_mac_pie_chart),
    path("nids-incident-target-mac-table", nids_incident_target_mac_table),
    path("nids-incident-target-port-pie", nids_incident_target_port_pie_chart),
    path("nids-incident-target-port-table", nids_incident_target_port_table),
    path("nids-incident-freq-targetted-host", nids_incident_freq_targetted_host),
    path("nids-incident-freq-attacker", nids_incident_freq_attacker),
    path("nids-incident-attacked-service", nids_incident_attacked_service_details),
    path("nids-incident-threat-type", nids_incident_threat_type_ser_label),
    path(
        "mitre-tactics-pie-chart-nids-incident", nids_incident_mitre_tactics_pie_chart
    ),
    path("mitre-tactics-table-nids-incident", nids_incident_mitre_tactics_pie_table),
    path("mitre-techniq-nids-incident", nids_incident_mitre_techniq_pie_chart),
    path("mitre-techniq-table-nids-incident", nids_incident_mitre_techniq_pie_table),
    # NIDS Incident ML DL page urls
    path("nids-incident-ml-detected-threat", nids_incident_ml_detected_threat),
    path(
        "nids-incident-ml-detected-threat-table", nids_incident_ml_detected_threat_table
    ),
    path("nids-incident-ml-map", nids_incident_ml_map),
    path("nids-incident-ml-map-table", nids_incident_ml_map_table),
    path("nids-incident-ml-cntry-bar", nids_incident_ml_cntry_bar),
    path("nids-incident-ml-cntry-table", nids_incident_ml_cntry_bar_table),
    path("nids-incident-ml-asn-bar", nids_incident_ml_asn_bar),
    path("nids-incident-ml-asn-table", nids_incident_ml_asn_table),
    path("nids-incident-ml-city-pie", nids_incident_ml_city_pie),
    path("nids-incident-ml-city-table", nids_incident_ml_city_table),
    path("nids-incident-ml-target-ip-pie", nids_incident_ml_target_ip_pie),
    path("nids-incident-ml-target-ip-table", nids_incident_ml_target_ip_table),
    path("nids-incident-ml-target-mac-pie", nids_incident_ml_target_mac_pie_chart),
    path("nids-incident-ml-target-mac-table", nids_incident_ml_target_mac_table),
    path("nids-incident-ml-trgt-port-pie", nids_incident_ml_target_port_pie),
    path("nids-incident-ml-trgt-port-table", nids_incident_ml_target_port_table),
    path("nids-incident-ml-freq-trgted-host", nids_incident_ml_freq_trgted_host),
    path("nids-incident-ml-freq-attacker", nids_incident_ml_freq_attacker),
    path(
        "nids-incident-ml-attacked-service", nids_incident_ml_attacked_service_details
    ),
    # To add classes types(blacklisted models api)
    path("add-blacklisted-details", add_classes_blacklist),
    path("get-blacklisted-details", display_blacklisted_details),
    # hids_Query urls(indice name = xdr-hids-alert-jay-jasi9552-*)
    path(
        "hids-alert-security-event-page", HidsAlertSecurityEventPage.as_view()
    ),  # hids urls(agent_details column name = hids_alert_agent)
    
    # -------HIDS Alert queries for Security Event Page (HIDS ALERTS)---------
    path(
        "hids-alert-security-event-page-top-alert",
        hids_alert_security_page_top_five_alert,
    ),
    path(
        "hids-alert-security-event-page-top-alert-table",
        hids_alert_security_page_top_five_alert_table,
    ),
    path(
        "hids-alert-security-event-page-top-rule-groups",
        hids_alert_security_page_top_five_rule_groups,
    ),
    path(
        "hids-alert-security-event-page-top-rule-groups-table",
        hids_alert_security_page_top_five_rule_groups_table,
    ),
    path(
        "hids-alert-security-event-page-top-rule-pci-dss",
        hids_alert_security_page_top_five_rule_pci_dss,
    ),
    path(
        "hids-alert-security-event-page-top-rule-pci-dss-table",
        hids_alert_security_page_top_five_rule_pci_dss_table,
    ),
    path("hids-alert-security-grp-evolution",hids_alert_security_page_alert_groups_evolution,),  # HidsAlertSecurityEventPage
    path("hids-alert-security-grp-evolution-table",hids_alert_security_page_alert_groups_evolution_table,),  # HidsAlertSecurityEventPage
    path("hids-alert-security-log-table", hids_alert_security_logs_table),  # HidsAlertSecurityEventPage

    # -------HIDS Alert queries for Mitre Attack Page  (HIDS ALERTS)---------
    path("hids-alert-mitre-attack-event-page-rule-level-by-attack-id",hids_alert_mitre_attack_page_rule_level_by_attack_id,),
    path("hids-alert-mitre-attack-event-page-rule-level-by-attack-id-table",hids_alert_mitre_attack_page_rule_level_by_attack_id_table,),
    path("hids-alert-mitre-attack-event-page-rule-mitre-technique",hids_alert_mitre_attack_page_rule_mitre_technique,),
    path("hids-alert-mitre-attack-event-page-rule-mitre-technique-table",hids_alert_mitre_attack_page_rule_mitre_technique_table,),
    path("hids-alert-mitre-evolution-time",hids_alert_mitre_alert_evolution_over_time), # HidsAlertMitreAttackPage
    path("hids-alert-mitre-evolution-time-table",hids_alert_mitre_alert_evolution_over_time_table), # HidsAlertMitreAttackPage
    path("hids-alert-mitre-attack-tactic",hids_alert_mitre_attack_by_tactic), # HidsAlertMitreAttackPage
    path("hids-alert-mitre-attack-tactic-table",hids_alert_mitre_attack_by_tactic_table), # HidsAlertMitreAttackPage

    # ----------------------------------------------------------------------
    path("show-unique-agent-id", UniquedataAgentId),
    # hids_Query urls(indice name = xdr-hids-incident-jay-jasi9552-*)
    path("hids-incident-agent-id-details", hids_incident_uniquedata_agentid),
    path(
        "hids-incident-security-event-page", HidsIncidentSecurityEventPage.as_view()
    ),  # hids urls(agent_details column name = hids_incident_agent)
    # -------HIDS Incident queries for Security Event Page (HIDS INCIDENTS)---------
    path(
        "hids-incident-security-event-page-top-alert",
        hids_incident_security_page_top_five_alert,
    ),
    path(
        "hids-incident-security-event-page-top-alert-table",
        hids_incident_security_page_top_five_alert_table,
    ),
    path(
        "hids-incident-security-event-page-top-rule-groups",
        hids_incident_security_page_top_five_rule_groups,
    ),
    path(
        "hids-incident-security-event-page-top-rule-groups-table",
        hids_incident_security_page_top_five_rule_groups_table,
    ),
    path(
        "hids-incident-security-event-page-top-rule-pci-dss",
        hids_incident_security_page_top_five_rule_pci_dss,
    ),
    path(
        "hids-incident-security-event-page-top-rule-pci-dss-table",
        hids_incident_security_page_top_five_rule_pci_dss_table,
    ),
    path("hids-incident-security-grp-evolution",hids_incident_security_page_alert_groups_evolution,),  # HidsIncidentSecurityEventPage
    path("hids-incident-security-grp-evolution-table",hids_incident_security_page_alert_groups_evolution_table,),  # HidsIncidentSecurityEventPage
    path("hids-incident-security-log-table", hids_incident_security_logs_table),  # HidsIncidentSecurityEventPage

    # -------HIDS Incident queries for Mitre Attack Page (HIDS INCIDENTS)---------
    path(
        "hids-incident-mitre-attack-event-page-rule-level-by-attack-id",
        hids_incident_mitre_attack_page_rule_level_by_attack_id,
    ),
    path(
        "hids-incident-mitre-attack-event-page-rule-level-by-attack-id-table",
        hids_incident_mitre_attack_page_rule_level_by_attack_id_table,
    ),
    path(
        "hids-incident-mitre-attack-event-page-rule-mitre-technique",
        hids_incident_mitre_attack_page_rule_mitre_technique,
    ),
    path(
        "hids-incident-mitre-attack-event-page-rule-mitre-technique-table",
        hids_incident_mitre_attack_page_rule_mitre_technique_table,
    ),
    path("hids-incident-mitre-evolution-time",hids_incident_mitre_alert_evolution_over_time), # HidsIncidentMitreAttackPage
    path("hids-incident-mitre-evolution-time-table",hids_incident_mitre_alert_evolution_over_time_table), # HidsIncidentMitreAttackPage
    path("hids-incident-mitre-attack-tactic",hids_incident_mitre_attack_by_tactic), # HidsIncidentMitreAttackPage
    path("hids-incident-mitre-attack-tactic-table",hids_incident_mitre_attack_by_tactic_table), # HidsIncidentMitreAttackPage

    # ----------------------------------------------------------------------
    # hids_Query urls(indice name = xdr-hids-event-jay-jasi9552-*)
    path("hids-event-agent-id-details", hids_event_uniquedata_agentid),
    path(
        "hids-event-security-event-page", HidsEventSecurityEventPage.as_view()
    ),  # hids urls(agent_details column name = hids_event_agent)
    # -------HIDS Event queries for Security Event Page Charts (HIDS EVENTS)---------
    path("hids-event-security-event-page-top-alert",hids_event_security_page_top_five_alert,),
    path(
        "hids-event-security-event-page-top-alert-table",
        hids_event_security_page_top_five_alert_table,
    ),
    path(
        "hids-event-security-event-page-top-rule-groups",
        hids_event_security_page_top_five_rule_groups,
    ),
    path(
        "hids-event-security-event-page-top-rule-groups-table",
        hids_event_security_page_top_five_rule_groups_table,
    ),
    path(
        "hids-event-security-event-page-top-rule-pci-dss",
        hids_event_security_page_top_five_rule_pci_dss,
    ),
    path(
        "hids-event-security-event-page-top-rule-pci-dss-table",
        hids_event_security_page_top_five_rule_pci_dss_table,
    ),
    path("hids-event-security-grp-evolution",hids_event_security_page_alert_groups_evolution,),  # HidsEventSecurityEventPage
    path("hids-event-security-grp-evolution-table",hids_event_security_page_alert_groups_evolution_table,),  # HidsEventSecurityEventPage
    path("hids-event-security-log-table", hids_event_security_logs_table),  # HidsEventSecurityEventPage
    
    # -------HIDS Event queries for Mitre Attack Page (HIDS EVENTS)---------
    path(
        "hids-event-mitre-attack-event-page-rule-level-by-attack-id",
        hids_event_mitre_attack_page_rule_level_by_attack_id,
    ),
    path(
        "hids-event-mitre-attack-event-page-rule-level-by-attack-id-table",
        hids_event_mitre_attack_page_rule_level_by_attack_id_table,
    ),
    path(
        "hids-event-mitre-attack-event-page-rule-mitre-technique",
        hids_event_mitre_attack_page_rule_mitre_technique,
    ),
    path(
        "hids-event-mitre-attack-event-page-rule-mitre-technique-table",
        hids_event_mitre_attack_page_rule_mitre_technique_table,
    ),
    path("hids-event-mitre-evolution-time",hids_event_mitre_alert_evolution_over_time), # HidsEventMitreAttackPage
    path("hids-event-mitre-evolution-time-table",hids_event_mitre_alert_evolution_over_time_table), # HidsEventMitreAttackPage
    path("hids-event-mitre-attack-tactic",hids_event_mitre_attack_by_tactic), # HidsEventMitreAttackPage
    path("hids-event-mitre-attack-tactic-table",hids_event_mitre_attack_by_tactic_table), # HidsEventMitreAttackPage

    # ----------------------------------------------------------------------
    # hids queries with grouping of column on basis of agent_id
    path("hids-alert-mitre-tactic-pie-chart-old", hids_alert_rule_mitre_pie_chart),
    path("hids-alert-mitre-tactic-table", hids_alert_mitre_tactic_card_table),
    path("hids-alert-mitre-techniq-pie-chart-old", hids_alert_mitre_techniq_pie_chart),
    path("hids-alert-mitre-techniq-table", hids_alert_mitre_techniq_table),
    path("hids-alert-rule-pci-dss-pie-old", hids_alert_rule_pci_dss_pie_chart),
    # ------------- testing alert hids queries with grouping of column on basis of agent_id -------
    path("hids-alert-rule-pci-dss-pie", hids_alert_rule_pci_dss_pie_chart_testing),
    path("hids-alert-mitre-tactic-pie-chart", hids_alert_rule_mitre_pie_chart_testing),
    path("hids-alert-mitre-techniq-pie-chart", hids_alert_mitre_techniq_pie_chart_testing),
    # ---------------------------------------------------------------------------------------------
    path("hids-alert-rule-pci-dss-table", hids_alert_rule_pci_dss_table),
    path("hids-alert-potential-ransomware", hids_alert_potential_ransomware),
    path("hids-alert-ransomware-table", hids_alert_potential_ransomware_table),
    path("hids-alert-anomaly-label", hids_alert_anomaly_label),
    path("hids-alert-anomaly-table", hids_alert_anomaly_table),
    path("hids-event-tactic-pie-old", hids_event_tactic_pie_chart),
    path("hids-event-tactic-table", hids_event_tactic_table),
    path("hids-event-techniq-pie-old", hids_event_techniq_pie_chart),
    path("hids-event-techniq-table", hids_event_techniq_table),
    path("hids-event-rule-pci-dss-pie-old", hids_event_pci_dss_pie_chart),
    # ---------- testing event hids queries with grouping of column on basis of agent_id ---
    path("hids-event-techniq-pie", hids_event_techniq_pie_chart_testing),
    path("hids-event-tactic-pie", hids_event_tactic_pie_chart_testing),
    path("hids-event-rule-pci-dss-pie", hids_event_pci_dss_pie_chart_testing),
    # --------------------------------------------------------------------------------------
    path("hids-event-rule-pci-dss-table", hids_event_pci_dss_table),
    path("hids-event-potential-ransomware", hids_event_potential_ransomware),
    path("hids-event-ransomware-table", hids_event_potential_ransomware_table),
    path("hids-event-anomaly-label", hids_event_anomaly_label),
    path("hids-event-anomaly-table", hids_event_anomaly_table),
    path("incident-hids-tactic-pie-old", hids_incident_tactic_pie_chart),
    path("incident-hids-tactic-table", hids_incident_tactic_table),
    path("incident-hids-techniq-pie-old", hids_incident_techniq_pie_chart),
    path("incident-hids-techniq-table", hids_incident_techniq_table),
    path("incident-hids-rule-pci-dss-pie-old", hids_incident_pci_dss_pie_chart),
    # ---------- testing incident hids queries with grouping of column on basis of agent_id ---
    path("incident-hids-rule-pci-dss-pie", hids_incident_pci_dss_pie_chart_testing),
    path("incident-hids-tactic-pie", hids_incident_tactic_pie_chart_testing),
    path("incident-hids-techniq-pie", hids_incident_techniq_pie_chart_testing),
    # --------------------------------------------------------------------------------------
    path("incident-hids-rule-pci-dss-table", hids_incident_pci_dss_table),
    path("incident-hids-potential-ransomware", hids_incident_potential_ransomware),
    path("incident-hids-ransomware-table", hids_incident_potential_ransomware_table),
    path("incident-hids-anomaly-label", hids_incident_anomaly_label),
    path("incident-hids-anomaly-table", hids_incident_anomaly_table),
    # dynamic report section #To get all indices name behalf of page-permission evn true or false in agent details
    path("get-indices-name", IndicesNameView.as_view()),
    path("get-indice-details", FilterIndiceData.as_view()),  # to get data indice basis
    path(
        "dynamic-report-filter", DynamicReportFilter.as_view()
    ),  # apply filter conditions dynamically in dynamic report
   
    path("encrypt-attacker-port-bar-chart", attacker_port_pie_chart_encrypt),
    path("encrypt-attacker-port-bar-table", attacker_port_pie_table_encrypt),
    # Trace Alert Page urls
    path("trace-alert-critical-threats", trace_alert_critical_threats),
    path("trace-alert-critical-threats-table", trace_alert_critical_threats_table),
    path("trace-alert-internal-attack", trace_alert_int_compr),
    path("trace-alert-int-attack-table", trace_alert_int_compr_table),
    path("trace-alert-lateral-mov", trace_alert_lateral_mov),
    path("trace-alert-lateral-mov-table", trace_alert_lateral_mov_table),
    path("trace-alert-ext", trace_alert_ext),
    path("trace-alert-ext-table", trace_alert_ext_table),
    path("trace-alert-geo-location", trace_alert_geolocation),
    path("trace-alert-geo-table", trace_alert_geolocation_table),
    path("trace-alert-threat-type", trace_alert_threat_type_count),
    path("trace-alert-attacker-port", trace_alert_attacker_port_pie_chart),
    path("trace-alert-attker-port-table", trace_alert_attacker_port_pie_table),
    path("trace-alert-attker-ip-line", trace_alert_attacker_ip_line_chart),
    path("trace-alert-attker-ip-table", trace_alert_line_table),
    path("trace-alert-attck-cntry", trace_alert_country_bar_chart),
    path("trace-alert-cntry-table", trace_alert_country_bar_table),
    path("trace-alert-attck-city", trace_alert_city_pie_chart),
    path("trace-alert-city-table", trace_alert_city_pie_table),
    path("trace-alert-attker-asn", trace_alert_asn_bar_chart),
    path("trace-alert-asn-table", trace_alert_asn_bar_table),
    path("trace-alert-target-ip", trace_alert_trget_ip_pie_chart),
    path("trget-ip-table-trace-alert", trace_alert_trget_ip_table),
    path("freq-attacker-trace-alert", trace_alert_freq_attacker),
    path("attacked-service-trace-alert", trace_alert_attacked_service_details),
    path("trace-alert-brut-username", trace_alert_brut_username),
    path("trace-alert-brut-passwrd", trace_alert_brut_password),
    path("trace-alert-target-port", trace_alert_trget_port_pie_chart),
    path("trget-port-table-trace-alert", trace_alert_trget_port_table),
    # Trace EVENT Page urls
    path("critical-threats-trace-event", critical_threats_trace_event),
    path("critical-threats-table-trace-event", critical_threats_table_trace_event),
    path("internal-attack-trace-event", int_compr_trace_event),
    path("int-attack-table-trace-event", int_compr_table_trace_event),
    path("lateral-mov-trace-event", lateral_mov_trace_event),
    path("lateral-mov-table-trace-event", lateral_mov_table_trace_event),
    path("ext-trace-event", ext_trace_event),
    path("ext-table-trace-event", ext_table_trace_event),
    path("geo-location-trace-event", geolocation_trace_event),
    path("geo-table-trace-event", geolocation_table_trace_event),
    path("threat-type-trace-event", threat_type_count_trace_event),
    path("attacker-port-trace-event", attacker_port_pie_chart_trace_event),
    path("attker-port-table-trace-event", attacker_port_pie_table_trace_event),
    path("attker-ip-line-trace-event", attacker_ip_line_chart_trace_event),
    path("attker-ip-table-trace-event", line_table_trace_event),
    path("attck-cntry-trace-event", country_bar_chart_trace_event),
    path("cntry-table-trace-event", country_bar_table_trace_event),
    path("attck-city-trace-event", city_pie_chart_trace_event),
    path("city-table-trace-event", city_pie_table_trace_event),
    path("attker-asn-trace-event", asn_bar_chart_trace_event),
    path("asn-table-trace-event", asn_bar_table_trace_event),
    path("target-ip-trace-event", trget_ip_pie_chart_trace_event),
    path("trget-ip-table-trace-event", trget_ip_table_trace_event),
    path("freq-attacker-trace-event", freq_attacker_trace_event),
    path("attacked-service-trace-event", attacked_service_details_trace_event),
    path("brut-username-trace-event", brut_username_trace_event),
    path("brut-passwrd-trace-event", brut_password_trace_event),
    path("target-port-trace-event", trget_port_pie_chart_trace_event),
    path("trget-port-table-trace-event", trget_port_table_trace_event),
    # Trace Incident Page urls
    path("incident-critical-threats-trace", trace_incident_critical_threats),
    path(
        "incident-critical-threats-table-trace", trace_incident_critical_threats_table
    ),
    path("incident-internal-attack-trace", trace_incident_int_compr),
    path("incident-int-attack-table-trace", trace_incident_int_compr_table),
    path("incident-lateral-mov-trace", trace_incident_lateral_mov),
    path("incident-lateral-mov-table-trace", trace_incident_lateral_mov_table),
    path("incident-ext-trace", trace_incident_ext),
    path("incident-ext-table-trace", trace_incident_ext_table),
    path("incident-geo-location-trace", trace_incident_geolocation),
    path("incident-geo-table-trace", trace_incident_geolocation_table),
    path("incident-threat-type-trace", trace_incident_threat_type_count),
    path("incident-attacker-port-trace", trace_incident_attacker_port_pie_chart),
    path("incident-attker-port-table-trace", trace_incident_attacker_port_pie_table),
    path("incident-attker-ip-line-trace", trace_incident_attacker_ip_line_chart),
    path("incident-attker-ip-table-trace", trace_incident_line_table),
    path("incident-attck-cntry-trace", trace_incident_country_bar_chart),
    path("incident-cntry-table-trace", trace_incident_country_bar_table),
    path("incident-attck-city-trace", trace_incident_city_pie_chart),
    path("incident-city-table-trace", trace_incident_city_pie_table),
    path("incident-attker-asn-trace", trace_incident_asn_bar_chart),
    path("incident-asn-table-trace", trace_incident_asn_bar_table),
    path("incident-target-ip-trace", trace_incident_trget_ip_pie_chart),
    path("incident-trget-ip-table-trace", trace_incident_trget_ip_table),
    path("incident-freq-attacker-trace", trace_incident_freq_attacker),
    path("incident-attacked-service-trace", trace_incident_attacked_service_details),
    path("incident-brut-username-trace", trace_incident_brut_username),
    path("incident-brut-passwrd-trace", trace_incident_brut_password),
    path("incident-target-port-trace", trace_incident_trget_port_pie_chart),
    path("incident-trget-port-table-trace", trace_incident_trget_port_table),
    # Trace Global Threat Feed Page
    path("glog-trace-malware-details", trace_glog_malware_details_pie_chart),
    path("glog-trace-malware-table", trace_glog_malware_details_pie_table),
    path("glog-trace-intel-source", trace_glog_intel_source_pie_chart),
    path("glog-trace-intel-source-table", trace_glog_intel_source_pie_table),
    path("glog-trace-threat-type-pie", trace_glog_threat_type_pie_chart),
    path("glog-trace-threat-type-table", trace_glog_threat_type_pie_table),
    path("glog-trace-logs-table", trace_glog_logs_table),
    # Health Check section
    path("hc-status-all-products", health_check_status_all_products),
    path("hc-dynamic-latest-info", health_check_dynamic_latest_cpu_ram_disk),
    path("hc-feeds-table", health_check_logs_only_table),
    path("hc-level-line-chart", health_check_level_line_chart),
    path("hc-level-line-table", health_check_level_line_chart_table),
    # Soar section
    path("soar-blocked-ips-table", soar_blocked_ips_table),
    path("user-soar-urls-details", soar_urls_details),
    # Report Config api
    path(
        "report-config-display-log-indice", Report_Config_Display_Log_Indice.as_view()
    ),
    path("report-config-fileds-name", report_config_indice_fields_records),
    path("save-scheduler-format", save_date_time),
    path("display-save-scheduler-format", display_save_date_time),

    # Updted Key Management api modules (Third party api) 13-12-2023
    path("third-party-api-get-logindice", Testing_Display_Log_Indice.as_view()),
    path("updated-third-party-api-create-api-key", updated_third_party_api_create_api_key),
    path("display-third-party-api-key", updated_display_third_party_api),
    path("get-third-party-api", Testing_Updated_Xdr_api.as_view()), #third party get api behalf of key filter (headers)
    # applied encryption on one card of nids-alert #for testing
]
