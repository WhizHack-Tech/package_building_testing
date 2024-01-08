#  ==============================================================================================================================
#  File Name: soar_ip_query.py
#  Description: It contains all the code for each chart on soar_blocked_ips under Soar tab on Client Dashboard.
#  Active URL: https://xdr-demo.zerohack.in/soar

#  ------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  =============================================================================================================================

# This file contains all the charts of "Soar" page of Soar
from rest_framework.response import Response
from ..helpers import getIndexNameByLocationId, getPlatformAndBlacklistedItemsByLocationId, getMlDlAccuracyRanges
from ..time_filter_on_queries import calculate_start_end_time
from ..grouping_epoch_time import *
from ..opensearch_config import opensearch_conn_using_db
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import defaultdict
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# To display soar blocked_ips details (table)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def soar_blocked_ips_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "err": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('soar_agent')
    sql_query = f"SELECT * FROM {indice_name}-* ORDER BY attack_epoch_time DESC limit 200;"
    api_response = opensearch_conn_using_db(sql_query, location_id, plan_id)
    if api_response.get("total") not in [0,None]:
        key_names = [item['name'] for item in api_response.get('schema')]
        
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        
        return Response({"message_type":"success", "data":final_response})
    else:
        return Response({"message_type":"d_not_f"})