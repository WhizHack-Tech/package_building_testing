#  =============================================================================================================================================
#  File Name: grouping_epoch_time.py
#  Description: To group time_filters by a specific time value, used internally as helper functions for charts on Client Dashboard.

#  ---------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  =============================================================================================================================================

# this file contains functions which "accepts" start_epoch_time, end_epoch_time and group epoch time in intervals on basis of different conditions
# only used for Attacker IP Line chart in nids attack events----"returns" intervals of (start_epoch, end_epoch) in a list

# conditions available
# today
# last_5_minutes-----minutes
# last_15_minutes------grp by minutes
# last_30_minutes------grp by 5 min
# last_1_hour----------grp by 5 min
# last_24_hours--------grp by 3 hours
# last_7_days----------grp by 12 hrs
# last_30_days---------grp by 3 days
# last_90_days---------grp by 7 days
# last_1_year----------grp by month


import time
from datetime import datetime

# formatting epoch time to ("%Y-%m-%d %H:%M") format #start
def format_epoch_time(epoch_time):
    formatted_time = datetime.fromtimestamp(epoch_time // 1000).strftime("%Y-%m-%d %H:%M")
    return formatted_time
#end


#1 grp by minutes
def group_time_by_minute(start_time, end_time):
    
    # Calculate the total number of minutes
    total_minutes = (end_time - start_time) // (60 * 1000)

    # Initialize the result list
    result = []

    # Generate start and end times for each minute
    for i in range(total_minutes):
        minute_start = start_time + (i * 60 * 1000)
        minute_end = minute_start + (60 * 1000)
        result.append((minute_start, minute_end))

    return result

#2 grp by 5 minutes
def group_time_by_5_minutes(start_time, end_time):
    
    # Calculate the total number of 5-minute intervals
    total_intervals = (end_time - start_time) // (5 * 60 * 1000)

    # Initialize the result list
    result = []

    # Generate start and end times for each 5-minute interval
    for i in range(total_intervals):
        interval_start = start_time + (i * 5 * 60 * 1000)
        interval_end = interval_start + (5 * 60 * 1000)
        result.append((interval_start, interval_end))
        
    return result

#3 grp by 30 minutes
def group_time_by_30_minutes(start_time, end_time):
    
    # Calculate the total number of 30-minute intervals
    total_intervals = (end_time - start_time) // (30 * 60 * 1000)

    # Initialize the result list
    result = []

    # Generate start and end times for each 30-minute interval
    for i in range(total_intervals):
        interval_start = start_time + (i * 30 * 60 * 1000)
        interval_end = interval_start + (30 * 60 * 1000)
        result.append((interval_start, interval_end))
        
    return result

#4 group by hour
def group_time_by_hour(start_time, end_time):
    
    # Calculate the total number of hour intervals
    total_intervals = (end_time - start_time) // (60 * 60 * 1000)

    # Initialize the result list
    result = []

    # Generate start and end times for each hour interval
    for i in range(total_intervals):
        interval_start = start_time + (i * 60 * 60 * 1000)
        interval_end = interval_start + (60 * 60 * 1000)
        result.append((interval_start, interval_end))
        
    return result

#5 group by 3 hours
def group_time_by_3_hours(start_time, end_time):
    
    # Calculate the total number of 3-hour intervals
    total_intervals = (end_time - start_time) // (3 * 60 * 60 * 1000)

    # Initialize the result list
    result = []

    # Generate start and end times for each 3-hour interval
    for i in range(total_intervals):
        interval_start = start_time + (i * 3 * 60 * 60 * 1000)
        interval_end = interval_start + (3 * 60 * 60 * 1000)
        result.append((interval_start, interval_end))
        
    return result

#6 grp by 12 hrs
def group_time_by_12_hours(start_time, end_time):
    
    # Calculate the total number of 12-hour intervals
    total_intervals = 7    
    interval_duration = (end_time - start_time) // total_intervals

    # Initialize the result list
    result = []

    # Generate start and end times for each 12-hour interval
    for i in range(total_intervals):
        interval_start = start_time + (i * interval_duration)
        interval_end = interval_start + interval_duration
        result.append((interval_start, interval_end))
    
    return result

#7 group by 3 days
def group_time_by_3_day(start_time, end_time):

    # Calculate the total number of 3-day intervals
    total_intervals = (end_time - start_time) // (3 * 24 * 60 * 60 * 1000)

    # Initialize the result list
    result = []

    # Generate start and end times for each 3-day interval
    for i in range(total_intervals):
        interval_start = start_time + (i * 3 * 24 * 60 * 60 * 1000)
        interval_end = interval_start + (3 * 24 * 60 * 60 * 1000)
        result.append((interval_start, interval_end))
    
    return result


#8 group by 7 days
def group_time_by_7_days(start_time, end_time):
    
    # Calculate the total number of 7-day intervals
    total_intervals = (end_time - start_time) // (7 * 24 * 60 * 60 * 1000)

    # Calculate the remaining days after all complete 7-day intervals
    remaining_days = (end_time - start_time) % (7 * 24 * 60 * 60 * 1000)

    # Initialize the result list
    result = []

    # Generate start and end times for each 7-day interval
    for i in range(total_intervals):
        interval_start = start_time + (i * 7 * 24 * 60 * 60 * 1000)
        interval_end = interval_start + (7 * 24 * 60 * 60 * 1000)
        result.append((interval_start, interval_end))
    
    # Add the interval for the remaining days
    if remaining_days > 0:
        interval_start = end_time - remaining_days
        result.append((interval_start, end_time))

    return result

#9 group by month
def group_time_by_month(start_time, end_time):
    
    # Convert the start and end timestamps to struct_time format
    start_struct = time.gmtime(start_time // 1000)
    end_struct = time.gmtime(end_time // 1000)

    # Extract the year and month from the start and end timestamps
    start_year, start_month = start_struct.tm_year, start_struct.tm_mon
    end_year, end_month = end_struct.tm_year, end_struct.tm_mon

    # Calculate the total number of months
    total_months = (end_year - start_year) * 12 + (end_month - start_month) + 1

    # Initialize the result list
    result = []

    # Generate start and end times for each month
    for i in range(total_months):
        month_start = time.mktime((start_year, start_month + i, 1, 0, 0, 0, 0, 0, 0))
        month_end = time.mktime((start_year if start_month + i <= 12 else start_year + 1, (start_month + i) % 12 + 1, 1, 0, 0, 0, 0, 0, 0))
        result.append((int(month_start * 1000), int(month_end * 1000)))
    
    return result

# below function accepts time filter value and returns list containg epoch time grouping
def getEpochIntervalGroupList(condition, past_time, current_time):
    
    if condition == "last_5_minutes":
        epoch_interval_group_list = group_time_by_minute(past_time, current_time)
    elif condition == "last_15_minutes":
        epoch_interval_group_list = group_time_by_minute(past_time, current_time)
    elif condition == "last_30_minutes":
        epoch_interval_group_list = group_time_by_5_minutes(past_time, current_time)
    elif condition == "last_1_hour":
        epoch_interval_group_list = group_time_by_5_minutes(past_time, current_time)
    elif condition == "last_6_hours":
        epoch_interval_group_list = group_time_by_30_minutes(past_time, current_time)
    elif condition == "last_12_hours":
        epoch_interval_group_list = group_time_by_hour(past_time, current_time)
    elif condition == "last_24_hours":
        epoch_interval_group_list = group_time_by_3_hours(past_time, current_time)
    elif condition == "last_7_days":
        epoch_interval_group_list = group_time_by_12_hours(past_time, current_time)
    # elif condition == "last_30_days":
    #     epoch_interval_group_list = group_time_by_3_day(past_time, current_time)
    # elif condition == "last_90_days":
    #     epoch_interval_group_list = group_time_by_7_days(past_time, current_time)
    elif condition == "last_1_year":
        epoch_interval_group_list = group_time_by_month(past_time, current_time)
    else:
        epoch_interval_group_list = None
        
    return epoch_interval_group_list

