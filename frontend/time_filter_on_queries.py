#  ==================================================================================================================================================================================================================================================
#  File Name: time_filter_on_queries.py
#  Description: This file contains code to return epoch_time for time filter values (used in all charts of Client Dashboard) like 'last_5_minutes' to epoch_time. Also contains function to return epoch_time for websocket notification queries.

#  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ==================================================================================================================================================================================================================================================

import pytz, dateutil.parser
from datetime import datetime, timedelta, timezone

# function to return start time, end time in epoch format
def calculate_start_end_time(condition):
    utc_now = datetime.now().utcnow()
    
    if condition == 'last_5_minutes':
        _past_time = utc_now - timedelta(minutes=5)
    elif condition == 'last_15_minutes':
        _past_time = utc_now - timedelta(minutes=15)
    elif condition == 'last_30_minutes':
        _past_time = utc_now - timedelta(minutes=30)
    elif condition == 'last_1_hour':
        _past_time = utc_now - timedelta(hours=1)
    elif condition == 'last_6_hours':
        _past_time = utc_now - timedelta(hours=6)
    elif condition == 'last_12_hours':
        _past_time = utc_now - timedelta(hours=12)
    elif condition == 'last_24_hours':
        _past_time = utc_now - timedelta(hours=24)
    elif condition == 'last_7_days':
        _past_time = utc_now - timedelta(days=7)
    # elif condition == 'last_30_days':
    #     _past_time = utc_now - timedelta(days=30)
    # elif condition == 'last_90_days':
    #     _past_time = utc_now - timedelta(days=90)
    elif condition == 'last_1_year':
        _past_time = utc_now - timedelta(days=365)
    else:
        return None, None
    
    # converting utc time to epoch time
    past_time_utc = dateutil.parser.parse(str(_past_time))
    start_time_epoch = int(round(past_time_utc.replace(tzinfo=timezone.utc).timestamp() * 1000))
    
    current_time_utc = dateutil.parser.parse(str(utc_now))
    end_time_epoch = int(round(current_time_utc.replace(tzinfo=timezone.utc).timestamp() * 1000))
    
    return start_time_epoch, end_time_epoch

# To get epoch_time on basis of condition #FOR STATIC REPORT ONLY
def calculate_start_end_time_static_report(condition):
    utc_now = datetime.now().utcnow()
    
    if condition == 'last_5_minutes':
        _past_time = utc_now - timedelta(minutes=5)
    elif condition == 'last_15_minutes':
        _past_time = utc_now - timedelta(minutes=15)
    elif condition == 'last_30_minutes':
        _past_time = utc_now - timedelta(minutes=30)
    elif condition == 'last_1_hour':
        _past_time = utc_now - timedelta(hours=1)
    elif condition == 'last_6_hours':
        _past_time = utc_now - timedelta(hours=6)
    elif condition == 'last_12_hours':
        _past_time = utc_now - timedelta(hours=12)
    elif condition == 'last_24_hours':
        _past_time = utc_now - timedelta(hours=24)
    elif condition == 'last_7_days':
        _past_time = utc_now - timedelta(days=7)
    elif condition == 'last_15_days':
        _past_time = utc_now - timedelta(days=15)
    elif condition == 'last_30_days':
        _past_time = utc_now - timedelta(days=30)
    # elif condition == 'last_90_days':
    #     _past_time = utc_now - timedelta(days=90)
    elif condition == 'last_1_year':
        _past_time = utc_now - timedelta(days=365)
    else:
        return None, None
    
    # converting utc time to epoch time
    past_time_utc = dateutil.parser.parse(str(_past_time))
    start_time_epoch = int(round(past_time_utc.replace(tzinfo=timezone.utc).timestamp() * 1000))
    
    current_time_utc = dateutil.parser.parse(str(utc_now))
    end_time_epoch = int(round(current_time_utc.replace(tzinfo=timezone.utc).timestamp() * 1000))
    
    return start_time_epoch, end_time_epoch

# function to return start time, end time in epoch format---only for websocket notification queries
def ws_notification_start_end_epoch_time(time_interval_val):
    utc_now = datetime.now().utcnow()
    
    if time_interval_val == 1:
        _past_time = utc_now - timedelta(minutes=1)
        _reset_interval_set = utc_now + timedelta(minutes=1)
    elif time_interval_val == 2:
        _past_time = utc_now - timedelta(minutes=2)
        _reset_interval_set = utc_now + timedelta(minutes=2)
    elif time_interval_val == 3:
        _past_time = utc_now - timedelta(minutes=3)
        _reset_interval_set = utc_now + timedelta(minutes=3)
    elif time_interval_val == 5:
        _past_time = utc_now - timedelta(minutes=5)
        _reset_interval_set = utc_now + timedelta(minutes=5)
    elif time_interval_val == 15:
        _past_time = utc_now - timedelta(minutes=15)
        _reset_interval_set = utc_now + timedelta(minutes=15)
    elif time_interval_val == 30:
        _past_time = utc_now - timedelta(minutes=30)
        _reset_interval_set = utc_now + timedelta(minutes=30)
    elif time_interval_val == 60:
        _past_time = utc_now - timedelta(hours=1)
        _reset_interval_set = utc_now + timedelta(hours=1)
    elif time_interval_val == 360:
        _past_time = utc_now - timedelta(hours=6)
        _reset_interval_set = utc_now + timedelta(hours=6)
    elif time_interval_val == 720:
        _past_time = utc_now - timedelta(hours=12)
        _reset_interval_set = utc_now + timedelta(hours=12)
    elif time_interval_val == 1440:
        _past_time = utc_now - timedelta(hours=24)
        _reset_interval_set = utc_now + timedelta(hours=24)
    else:
        _past_time = utc_now - timedelta(minutes=1)
        _reset_interval_set = utc_now + timedelta(minutes=1)
    
    # converting utc time to epoch time
    past_time_utc = dateutil.parser.parse(str(_past_time))
    past_time_epoch = int(round(past_time_utc.replace(tzinfo=timezone.utc).timestamp() * 1000))
    
    current_time_utc = dateutil.parser.parse(str(utc_now))
    current_time_epoch = int(round(current_time_utc.replace(tzinfo=timezone.utc).timestamp() * 1000))

    reset_time_utc = dateutil.parser.parse(str(_reset_interval_set))
    future_time_epoch = int(round(reset_time_utc.replace(tzinfo=timezone.utc).timestamp() * 1000))
    
    return past_time_epoch, current_time_epoch, future_time_epoch


# Used for recport_config this function for static code
def report_config_calculate_start_end_time(condition):
    utc_now = datetime.now().utcnow()
    if condition == 'last_7_days':
        _past_time = utc_now - timedelta(days=7)
    else:
        return None, None
    
    # converting utc time to epoch time
    past_time_utc = dateutil.parser.parse(str(_past_time))
    start_time_epoch = int(round(past_time_utc.replace(tzinfo=timezone.utc).timestamp() * 1000))
    
    current_time_utc = dateutil.parser.parse(str(utc_now))
    end_time_epoch = int(round(current_time_utc.replace(tzinfo=timezone.utc).timestamp() * 1000))
    
    return start_time_epoch, end_time_epoch