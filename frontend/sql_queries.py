#  ==================================================================================================
#  File Name: sql_queries.py
#  Description: File contains queries for Live attack map on Client Dashboard.
# Active URL: https://xdr-demo.zerohack.in/live/map
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

from .views import opensearch_conn_using_db
from .time_filter_on_queries import calculate_start_end_time
from .helpers import getPlatformAndBlacklistedItemsByLocationId


# Live attack map queries function
def map_query(agent_index, filter_type, location_id, plan_id):

    past_time, current_time = calculate_start_end_time(filter_type)

    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")

    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

    search_query = f"SELECT DISTINCT geoip_latitude, geoip_longitude, geoip_city, client_geoip_latitude, client_geoip_longitude, client_geoip_city, ids_threat_class FROM {agent_index} WHERE type_of_threat IN ('External Attack', 'Attack on External Server') "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND geoip_latitude IS NOT NULL AND geoip_longitude IS NOT NULL AND geoip_city IS NOT NULL AND client_geoip_latitude IS NOT NULL AND client_geoip_longitude IS NOT NULL AND client_geoip_city IS NOT NULL AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time desc LIMIT 100;"

    return {"resolve_query": opensearch_conn_using_db(search_query, location_id, plan_id), "search_query": search_query}
        
