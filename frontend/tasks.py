#  ===================================================================================================================================================================================
#  File Name: tasks.py
#  Description: Typically used to define Celery tasks. To define asynchronous tasks that need to be executed asynchronously, outside the normal request-response flow.

#  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================================================================================================

#from time import sleep
from __future__ import absolute_import, unicode_literals
import json
from urllib import response
from django.core.serializers import serialize
from .serializers import *
from .serializers import Attack_dataSerializer,Attack_Top_VictimSerializer,Attack_IPs_Serializer,data_Fastest_Attackers,data_Geolocation,Attack_Victim_tcpSerializer,Attack_Victim_udpSerializer,Attack_cardSerializer,Attack_TypesSerializer
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json
from django.http import JsonResponse
from datetime import timedelta, timezone
from calendar import c, month, week
from django.utils import timezone
from datetime import date, timedelta
import datetime
import json
from django.http import JsonResponse
from django.db.models.functions import TruncWeek, TruncMonth, TruncDate, ExtractWeek, TruncHour, TruncSecond, Cast
#import all the views.py file
from django.db.models import Count
#from __future__ import absolute_import, unicode_literals
import celery
from django.core import serializers
#data = serializers.serialize("json", SomeModel.objects.all())

#from .backend import ProgressRecorder
from time import sleep
from celery import shared_task
from django.http import JsonResponse
#from .task import test_func, testst_func

#from time import sleep
from .models import Attack_data
from .serializers import Attack_dataSerializer

#from celery.decorators import task
@shared_task(bind=True)
def test_func(self, duration):
    return "task is working with celery"   

# To show 100 records by database

@shared_task(bind=True)
def testst_func(self):
    if 'attack' in cache:
        data = cache.get('attack')
        print("DATA FROM CACHE")
        return data
    else:        
        results= Attack_data.objects.all()[:100]
        serialize = Attack_dataSerializer(results,many=True)
        cache.set('attack',serialize.data,timeout=60*30)
        print("DATA FROM DB")
    return serialize.data

# Top attacks by baby kumari latter on Priya with Redis on 2/3/2022
@shared_task(bind=True)
def test_first_count(self):
        if 'top_attackc' in cache:
            finalresult = cache.get('top_attackc')
            return finalresult
        else:
            time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
            results = Attack_data.objects.values('attack_threat_class').exclude(attack_threat_class__isnull=True).exclude(attack_threat_class__exact="Miscellaneous").exclude(attack_threat_class__exact="tls").exclude(attack_threat_class__exact="mqtt").exclude(attack_threat_class__exact="rfb").exclude(attack_threat_class__exact="smb").exclude(attack_threat_class__exact="rdp").exclude(attack_threat_class__exact="dcerpc").exclude(attack_threat_class__exact="tftp").exclude(attack_threat_class__exact="ftp").exclude(attack_threat_class__exact="anomaly").exclude(attack_threat_class__exact="smtp").exclude(attack_threat_class__exact="snmp").exclude(attack_threat_class__exact="Potential Corporate Privacy Violation").exclude(attack_threat_class__exact="http").exclude(attack_threat_class__exact="fileinfo").exclude(attack_threat_class__exact="ssh").exclude(attack_threat_class__exact="dns").annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('-count')
            finalresult = {}
            finalresult = {"count":[], "attack_threat_class": []}
            for i in results:
                finalresult['count'].append(i.get('count'))
                finalresult['attack_threat_class'].append(i.get('attack_threat_class'))
            for i,n in enumerate(finalresult['attack_threat_class']):
                if n == ('alert'):
                    finalresult['attack_threat_class'][i] = 'Alert'
                elif n == ('Generic Protocol Command Decode'):
                    finalresult['attack_threat_class'][i] = 'CnC Injection'
                elif n == ('Attempted Information Leak'):
                    finalresult['attack_threat_class'][i] = 'Data Breach'
                elif n == ('Device Retrieving External IP Address Detected'):
                    finalresult['attack_threat_class'][i] = 'CnC Communication'
                elif n == ('Potentially Bad Traffic'):
                    finalresult['attack_threat_class'][i] = 'Shell-code Execution'
                elif n == ('Misc Attack'):
                    finalresult['attack_threat_class'][i] = 'Possible Recon'
                elif n == ('Misc activity'):
                    finalresult['attack_threat_class'][i] = 'Suspicious Event'    
            cache.set('top_attackc',finalresult,timeout=60*30)
            return finalresult


#Baby Kumari Top OS attack Details
@shared_task(bind=True)
def tests_sec(self):
        if 'top_celery' in cache:
            finalresult = cache.get('top_celery')
            return finalresult
        else:    
            time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
            results = Attack_data.objects.values('attack_threat_class').exclude(attack_threat_class__isnull=True).exclude(attack_threat_class__exact="Miscellaneous").exclude(attack_threat_class__exact="tls").exclude(attack_threat_class__exact="alert").exclude(attack_threat_class__exact="Misc activity").exclude(attack_threat_class__exact="Misc Attack").exclude(attack_threat_class__exact="None").exclude(attack_threat_class__exact="mqtt").exclude(attack_threat_class__exact="rfb").exclude(attack_threat_class__exact="smb").exclude(attack_threat_class__exact="rdp").exclude(attack_threat_class__exact="dcerpc").exclude(attack_threat_class__exact="tftp").exclude(attack_threat_class__exact="ftp").exclude(attack_threat_class__exact="anomaly").exclude(attack_threat_class__exact="smtp").exclude(attack_threat_class__exact="snmp").exclude(attack_threat_class__exact="Potential Corporate Privacy Violation").exclude(attack_threat_class__exact="http").exclude(attack_threat_class__exact="fileinfo").exclude(attack_threat_class__exact="ssh").exclude(attack_threat_class__exact="dns").annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('-count')
            finalresult = {}
            finalresult = {"series":[], "labels": []}
            for i in results:
                finalresult['series'].append(i.get('count'))
                finalresult['labels'].append(i.get('attack_threat_class'))
           
            for i,n in enumerate(finalresult['labels']):
                if n == ('alert'):
                    finalresult['labels'][i] = 'Alert'
                elif n == ('Generic Protocol Command Decode'):
                    finalresult['labels'][i] = 'CnC Injection'
                elif n == ('Attempted Information Leak'):
                    finalresult['labels'][i] = 'Data Breach'
                elif n == ('Device Retrieving External IP Address Detected'):
                    finalresult['labels'][i] = 'CnC Communication'
                elif n == ('Potentially Bad Traffic'):
                    finalresult['labels'][i] = 'Shell-code Execution'
                elif n == ('Misc Attack'):
                    finalresult['labels'][i] = 'Possible Recon'
                elif n == ('Misc activity'):
                    finalresult['labels'][i] = 'Suspicious Event'
            cache.set('top_celery',finalresult,timeout=60*30)    
            return finalresult

# to top 7 records in attack_threat_class
#Top 7 Malware by Baby Kumari 
@shared_task(bind=True)           
def test_third(self):
        if 'class' in cache:
            finalresult = cache.get('class')
            return finalresult 
        else:
            time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
            results = Attack_data.objects.values('attack_threat_class').exclude(attack_threat_class__isnull=True).exclude(attack_threat_class__exact="Not Available").exclude(attack_threat_class__exact="Miscellaneous").annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('count')[:7]  
            finalresult={}
            finalresult = {"series":[], "labels": []}
            for i in results:
                finalresult['series'].append(i.get('count'))
                finalresult['labels'].append(i.get('attack_threat_class'))      
            cache.set('class',finalresult,timeout=60*30)
            return finalresult 


#Top attack country json response by priya duggal with redis cache 2/3/2022
@shared_task(bind=True)           
def test_four(self):   
        if 'attack_country' in cache:
            finalresult=cache.get('attack_country')
            return finalresult
        else:
            time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
            results = Attack_data.objects.values('attacker_country').exclude(attacker_country__isnull=True).exclude(attacker_country__exact="Not Available").exclude(attacker_country__exact="Internal Communication").exclude(attacker_country__exact="Miscellaneous").annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('-count')[:7]
            finalresult = {}
            finalresult = {"series":[], "labels": []}
            for i in results:
                finalresult['series'].append(i.get('count'))
                finalresult['labels'].append(i.get('attacker_country'))
           
            cache.set('attack_country',finalresult,timeout=60*30)
            return finalresult 

#Top Attack IPs view file by priya duggal
@shared_task(bind=True)            
def test_five(self):
    if 'attackports' in cache:
        finalresult=cache.get('attackports')
        return finalresult
    else:
        time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
        results = Attack_data.objects.values('attacker_ip').annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('-count')[:10]
        finalresult = {}
        finalresult = {"series":[], "labels": []}
        for i in results:
            finalresult['series'].append(i.get('count'))
            finalresult['labels'].append(i.get('attacker_ip'))
                
        cache.set('attackports',finalresult,timeout=60*30)
        return finalresult

#Top Attack City Data view file by priya duggal
@shared_task(bind=True)            
def test_six(self):
    if 'attackcity' in cache:
        finalresult=cache.get('attackcity')
        return finalresult
    else:
        time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
        results = Attack_data.objects.values('attacker_city').exclude(attacker_city__isnull=True).exclude(attacker_city__exact="Not Available").exclude(attacker_city__exact="Miscellaneous").annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('-count')[:7]
        finalresult = {}
        finalresult = {"series":[], "labels": []}
        for i in results:
            finalresult['series'].append(i.get('count'))
            finalresult['labels'].append(i.get('attacker_city'))
                
        cache.set('attackcity',finalresult,timeout=60*30)
        return finalresult 

#Baby Kumari Attack OS  json file view
@shared_task(bind=True)
def test_sev(self):
        if 'test_cel' in cache:
            finalresult=cache.get('test_cel')
            return finalresult
        else:    
            time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
            results = Attack_data.objects.values('attack_os').annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('attack_os')
            finalresult = {}
            finalresult = {"count":[], "attack_threat_class": []}
            for i in results:
                finalresult['count'].append(i.get('count'))
                finalresult['attack_threat_class'].append(i.get('attack_threat_class'))
        cache.set('test_cel',finalresult,timeout=60*30)    
        return finalresult 

# Target OS Details by Priya Diggal
@shared_task(bind=True)
def test_eight(self):
        if 'test_os' in cache:
            finalresult=cache.get('test_os')
            return finalresult
        else:
            time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
            results = Attack_data.objects.values('target_os').exclude(target_os__isnull=True).exclude(target_os__exact="Not Available").exclude(target_os__exact="Miscellaneous").annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('-count')[:7]
            finalresult = {}
            finalresult = {"series":[], "labels": []}
            for i in results:
                finalresult['series'].append(i.get('count'))
                finalresult['labels'].append(i.get('target_os'))
        # print(finalresult)
        cache.set('test_os',finalresult,timeout=60*30)  
        return finalresult

#To count top 100 row
@shared_task(bind=True)
def test_nine(self):
        if 'attackhd' in cache:
            data=cache.get('attackhd')
            return data
        else:    
            #time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
            results= Attack_data.objects.all()[:100]
        serialize = Attack_dataSerializer(results,many=True)
        cache.set('attackhd',data,timeout=60*30)
        return serialize.data  

# Data Source Json responce  details by Priya Duggal with cache
@shared_task(bind=True)
def test_ten(self):    
    if 'data_source' in cache:
        finalresult = cache.get('data_source')
        return finalresult
    else:
        time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
        results = Attack_data.objects.values('detection_mechanism').exclude(detection_mechanism__isnull=True).exclude(detection_mechanism__exact="Not Available").exclude(detection_mechanism__exact="Miscellaneous").annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('-count')[:7]
        finalresult = {}
        finalresult = {"series":[], "labels": []}
        for i in results:
            finalresult['series'].append(i.get('count'))
            finalresult['labels'].append(i.get('detection_mechanism'))
        cache.set('data_source',finalresult,timeout=60*30)
        return finalresult   

# 1 month attack Graph Chart by Baby Kumari
@shared_task(bind=True)
def test_ele(self):
        if 'attacktimestamp' in cache:
            finalresult=cache.get('attacktimestamp')
            return finalresult
        else:
            results = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).order_by('day')
            for i in results:
                print("??", i.get('c'))
            finalresult={}
            finalresult = {"categories":[], "series": []}
            co = 0
            for i in results:
                co = co + 1
                day = "Day " + str(co)
                finalresult['categories'].append(i.get('day'))
                finalresult['series'].append(i.get('c'))
            cache.set('attacktimestamp',finalresult,timeout=60*30)
            return finalresult
#To count 
@shared_task(bind=True)
def test_twelve(self):
        if 'miscellaneouscache' in cache:
            finalresult = cache.get('miscellaneouscache')
            return finalresult
        else:
            mis_results = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).exclude(attack_threat_class__exact="alert").exclude(attack_threat_class__exact="None").exclude(attack_threat_class__exact="Generic Protocol Command Decode").exclude(attack_threat_class__exact="Attempted Information Leak").exclude(attack_threat_class__exact="Device Retrieving External IP Address Detected").exclude(attack_threat_class__exact="Potentially Bad Traffic").exclude(attack_threat_class__exact="Misc Attack").exclude(attack_threat_class__exact="Misc activity").order_by('day')
            finalresult={}
            finalresult = {"labels":[], "Miscellaneous": [], "attackevent": []}
            for i in mis_results:
                finalresult['labels'].append(i.get('day'))
                finalresult['Miscellaneous'].append(i.get('c'))
            #finalresult['labels'].remove(finalresult['labels'][-1]) #Removing the last element from categories list
            #finalresult['Miscellaneous'].remove(finalresult['Miscellaneous'][-1]) #Removing the last element from categories list
            results = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).exclude(attack_threat_class__isnull=True).exclude(attack_threat_class__exact="tls").exclude(attack_threat_class__exact="None").exclude(attack_threat_class__exact="mqtt").exclude(attack_threat_class__exact="rfb").exclude(attack_threat_class__exact="smb").exclude(attack_threat_class__exact="rdp").exclude(attack_threat_class__exact="dcerpc").exclude(attack_threat_class__exact="tftp").exclude(attack_threat_class__exact="ftp").exclude(attack_threat_class__exact="anomaly").exclude(attack_threat_class__exact="smtp").exclude(attack_threat_class__exact="snmp").exclude(attack_threat_class__exact="Potential Corporate Privacy Violation").exclude(attack_threat_class__exact="http").exclude(attack_threat_class__exact="fileinfo").exclude(attack_threat_class__exact="ssh").exclude(attack_threat_class__exact="dns").order_by('day')
            #finalresult={}
            #finalresult = {"labels":[], "attackevent": []}
            for i in results:
                #finalresult['labels'].append(i.get('day'))
                finalresult["attackevent"].append(i.get('c'))
            #finalresult['attackevent'].remove(finalresult['attackevent'][-1])
            cache.set('miscellaneouscache',finalresult,timeout=60*30)
            return finalresult 

# TCP Port Details by Priya Duggal on 28.01.2022
@shared_task(bind=True)
def test_thir(self):
    if 'tcp' in cache:
        finalresult = cache.get('tcp')
        return finalresult
    else:
        results = Attack_data.objects.values('tcp_port').exclude(tcp_port__isnull=True).exclude(tcp_port__exact="Not Available").exclude(tcp_port__exact="unknown").annotate(count=Count('id')).order_by('-count')[:10]
        finalresult = {}
        finalresult = {"series":[], "labels": []}
        for i in results:
            finalresult['series'].append(i.get('count'))
            finalresult['labels'].append(i.get('tcp_port'))
            for i,n in enumerate(finalresult['labels']):
                if n == ('22.0'):
                    finalresult['labels'][i] = 'ssh'
                elif n == ('80.0'):
                    finalresult['labels'][i] = 'http'
                elif n == ('8007.0'):
                    finalresult['labels'][i] = 'Proxmox Backup Server'
                elif n == ('445.0'):
                    finalresult['labels'][i] = 'smb'
            cache.set('tcp',finalresult,timeout=60*30)
            return finalresult  

#UDP Port Details by Priya Duggal on 28.01.2022
@shared_task(bind=True)
def test_fourteen(self):
    if 'udp' in cache:
        finalresult = cache.get('udp')
        return finalresult
    else:
        results = Attack_data.objects.values('udp_port').exclude(udp_port__isnull=True).exclude(udp_port__exact="Not Available").exclude(udp_port__exact="unknown").annotate(count=Count('id')).order_by('-count')[:10]
        finalresult = {}
        finalresult = {"series":[], "labels": []}
        for i in results:
            finalresult['series'].append(i.get('count'))
            finalresult['labels'].append(i.get('udp_port'))
            for i,n in enumerate(finalresult['labels']):
                if n == ('4789.0'):
                    finalresult['labels'][i] = 'VXLAN'
                else:
                    break        
            cache.set('udp',finalresult,timeout=60*30)
            return finalresult  

#ICMP Port Details by Priya Duggal on 28.01.2022
@shared_task(bind=True)
def test_fifteen(self):
        if 'icmp' in cache:
            finalresult = cache.get('icmp')
            return finalresult
        else:
            results = Attack_data.objects.values('icmp_port').exclude(icmp_port__isnull=True).exclude(icmp_port__exact="Not Available").exclude(icmp_port__exact="unknown").annotate(count=Count('id')).order_by('-count')[:10]
            finalresult = {}
            finalresult = {"series":[], "labels": []}
            for i in results:
                finalresult['series'].append(i.get('count'))
                finalresult['labels'].append(i.get('icmp_port'))
            for i,n in enumerate(finalresult['labels']):
                if n == ('4789.0'):
                    finalresult['labels'][i] = 'VXLAN'
                else:
                    break
            cache.set('icmp',finalresult,timeout=60*30)
            return finalresult                                                                                                        

# Attacker Mac Addres groupby count by Priya Duggal on 28.01.21
@shared_task(bind=True)
def test_sixteen(self):
        if 'mac' in cache:
            finalresult = cache.get('mac')
            return finalresult
        else:
            time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
            results = Attack_data.objects.values('attacker_mac').exclude(attacker_mac__isnull=True).exclude(attacker_mac__exact="Not Available").exclude(attacker_mac="ff:ff:ff:ff:ff:ff").annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('-count')
            finalresult = {}
            finalresult = {"series":[], "labels": []}
            for i in results:
                finalresult['series'].append(i.get('count'))
                finalresult['labels'].append(i.get('attacker_mac'))
                cache.set('mac',finalresult,timeout=60*30)
            return finalresult


# MAP View
# top 7 lat, lon, attack_city in json format--- 
# view by Priya Duggal on 28 Feb 2022
@shared_task(bind=True)
def test_seventeen(self):
        if 'locationcache' in cache:
            finalresult = cache.get('locationcache')
            return finalresult
        else:
            threshold_time = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
            results = Attack_data.objects.values('attacker_lat', 'attacker_lon', 'attacker_city').exclude(attacker_lat__isnull=True).exclude(attacker_lat__exact="Not Available").exclude(attacker_lat__exact="Internal Communication").exclude(attacker_lon__exact="Internal Communication").exclude(attacker_city__exact="Internal Communication").filter(attack_timestamp__gte=threshold_time).annotate(count=Count('id')).order_by('-count')[:50]
            finalresult = []
            for i in results:
            # Creating a list of positions and appending to dictionary
                positions = [float(i.get('attacker_lat')),float(i.get('attacker_lon'))]
                finalresult.append({'position' : positions, 'content' : i.get('attacker_city')})
           
            cache.set('locationcache',finalresult,timeout=60*30)
            return finalresult

# Card 1: Top Victim IP addresses.
# Description: IPs that require immediate attention
@shared_task(bind=True)
def test_eighteen(self):
        if 'attack_vic' in cache:
            victims = cache.get('attack_vic')
            return victims
        else:    
            results = Attack_data.objects.values('target_ip','target_mac_address').exclude(target_ip__isnull=True).exclude(target_ip="Not Available").exclude(target_mac_address="ff:ff:ff:ff:ff:ff").annotate(no_of_times_attacked=Count('target_ip')).order_by('-no_of_times_attacked')[:20]
            serialize = Attack_Top_VictimSerializer(results,many=True)
            cache.set('attack_vic',serialize.data,timeout=60*30)
        return serialize.data 

#Card 2: Top Attacking IPs
#Description: IPs that must be blocked for a high number of attacks
@shared_task(bind=True)
def test_nineteen(self):
        if 'attack' in cache:
            ips = cache.get('attack')
            return ips
        else:    
            results = Attack_data.objects.values('attacker_ip','attacker_mac').exclude(attacker_ip__isnull=True).exclude(attacker_ip="Not Available").annotate(no_of_times_attacked=Count('attacker_ip')).order_by('-no_of_times_attacked')[:20]
            serialize = Attack_IPs_Serializer(results,many=True)
            cache.set('attack',serialize.data,timeout=60*30)
        return serialize.data 

# Card 3: Fastest Attackers with using redis
# Description: Potential DDoS attackers 
# datetime_filter = datetime(2009, 8, 22) 
# MyObject.objects.filter(datetime_attr__startswith=datetime_filter.date())
@shared_task(bind=True)
def test_twenty(self):
        if 'attackfas' in cache:
            fast = cache.get('attackfas')
            return fast
        else:    
            results = Attack_data.objects.values('attacker_ip','attacker_mac','attack_timestamp').exclude(attacker_ip__isnull=True).exclude(attacker_ip="Not Available").annotate(no_of_times_attacked=Count('attacker_ip')).order_by('-no_of_times_attacked')[:20]
            serialize = data_Fastest_Attackers(results,many=True)
            cache.set('attackfas',serialize.data,timeout=60*30)
        return serialize.data                      
           
# Card 4: Geolocation
# Description: This card shows where your latest attacks are coming from. You can download completedata from the reports section.
@shared_task(bind=True)
def test_twentyfir(self):
        if 'attack_geo' in cache:
            geo = cache.get('attack_geo')
            return geo
        else:
            results = Attack_data.objects.values('attacker_ip','attacker_mac','attacker_asn','attack_timestamp','attacker_city').exclude(attacker_mac__isnull=True).exclude(attacker_mac="ff:ff:ff:ff:ff:ff").order_by('-attack_timestamp')[:20]
            #import pdb; pdb.set_trace()
            serialize = data_Geolocation(results,many=True) 
            cache.set('attack_geo',serialize.data,timeout=60*30)            
        return serialize.data  

# Card 5: Victim tcp services attacked
# Description: These are the services being attacked in your network along with victim machines.
@shared_task(bind=True)
def test_twentysec(self):
        if 'attack' in cache:
            tcp = cache.get('attack')
            return tcp
        else:    
            results = Attack_data.objects.values('target_ip','target_mac_address','tcp_port').exclude(tcp_port__isnull=True).exclude(tcp_port__exact="unknown").annotate(no_of_times_attacked=Count('target_ip')).order_by('-no_of_times_attacked')[:20]
            serialize = Attack_Victim_tcpSerializer(results,many=True)
            cache.set('attack',serialize.data,timeout=60*30)
        return serialize.data 

# Card 6: Victim udp services attacked
# Description: These are the services being attacked in your network along with victim machines. 
@shared_task(bind=True)
def test_twentythir(self):
        if 'attack_udp' in cache:
            udp = cache.get('attack_udp')
            return udp
        else:
            results = Attack_data.objects.values('target_ip','target_mac_address','udp_port').exclude(udp_port__isnull=True).exclude(udp_port__exact="Not Available").exclude(udp_port__exact="unknown").annotate(no_of_times_attacked=Count('target_ip')).order_by('-no_of_times_attacked')[:20]
            serialize = Attack_Victim_udpSerializer(results,many=True)
            cache.set('attack_udp',serialize.data,timeout=60*30)
        return serialize.data 

# Card 7: Top Attack Types (Victims)
# Description: This is where your machines are being attacked from. Many Lateral Movement implies that you have an active threat actor in your network.  
@shared_task(bind=True)
def test_twentyfour(self):
        if 'attack_types' in cache:
            attack = cache.get('attack_types')
            return attack
        else:    
            results = Attack_data.objects.values('target_ip','target_mac_address','type_of_threat').exclude(target_ip__isnull=True).exclude(target_ip__exact="Not Available").exclude(target_ip__exact="unknown").annotate(no_of_times_attacked=Count('target_ip')).order_by('-no_of_times_attacked')[:20]
            serialize = Attack_cardSerializer(results,many=True)
            cache.set('attack_types',serialize.data,timeout=60*30)
        return serialize.data 

# Card 8: Top Attack Types (Attackers)
# Description: This is where your attackers come from. Many Lateral Movement implies that you have anactive threat actor in your network. 
@shared_task(bind=True)
def test_twentyfive(self):
        if 'tops_attacker' in cache:
            top = cache.get('tops_attacker')
            return top
        else:    
            results = Attack_data.objects.values('attacker_ip','attacker_mac','type_of_threat').exclude(attacker_ip__isnull=True).exclude(attacker_ip__exact="Not Available").exclude(attacker_ip__exact="unknown").annotate(no_of_times_attacked=Count('attacker_ip')).order_by('-no_of_times_attacked')[:20]
            #import pdb; pdb.set_trace()
            serialize =Attack_TypesSerializer(results,many=True)
            cache.set('tops_attacker',serialize.data,timeout=60*30) 
        return serialize.data

#updated some quries 02-05-2022
# Card 1: Dashboard Card-3.
# Description: IPs that require immediate attention
@shared_task(bind=True)
def Ips_attention(self):
        if 'detail' in cache:
            victims = cache.get('detail')
            return victims
        else:    
            results = Attack_data.objects.values('attack_timestamp','target_ip','target_mac_address','attacker_ip','attacker_mac','type_of_threat').exclude(target_ip__isnull=True).exclude(target_ip="Not Available").exclude(target_mac_address="ff:ff:ff:ff:ff:ff").annotate(no_of_times_attacked=Count('target_ip')).order_by('-no_of_times_attacked')[:20]
            #import pdb; pdb.set_trace()
            serialize =  updated_threat(results,many=True)
            cache.set('detail',serialize.data,timeout=60*30)
        return serialize.data

# Card 2: Dashboard Card-4.
# Description: Signature Information
@shared_task(bind=True)
def signatureinformation(self): 
        if 'sign' in cache:
            victims = cache.get('sign')
            return victims
        else:    
            results = Attack_data.objects.values('attack_timestamp','attacker_ip','attacker_mac','attack_threat_class','attack_threat_type','attack_threat_severity').exclude(attack_threat_class__exact="None").exclude(attack_threat_type__exact="None").exclude(attack_threat_severity__exact="Not Available").exclude(attack_threat_class__exact="Generic Protocol Command Decode").exclude(attack_threat_class__exact="Misc activity").filter(detection_mechanism = 'IDS').exclude(attack_threat_severity__exact = 1).annotate(no_of_times_attacked=Count('attacker_ip')).order_by('-no_of_times_attacked')[:20]
            serialize = signature_threat(results,many=True)
            cache.set('sign',serialize.data,timeout=60*30)
        return serialize.data 

# Card 3: Dashboard Card-5.
# Description: Port wise Information
@shared_task(bind=True)
def portdetails(self):
        if 'port_vic' in cache:
            port_up = cache.get('port_vic')
            return port_up
        else:    
            results = Attack_data.objects.values('attack_timestamp','attacker_ip','attacker_mac','target_ip','target_mac_address','attack_threat_class','tcp_port','udp_port').exclude(udp_port__exact = "Not Available").exclude(tcp_port__exact = "Not Available").exclude(target_ip__isnull=True).exclude(target_ip="Not Available").exclude(target_mac_address="ff:ff:ff:ff:ff:ff").exclude(attack_threat_class="Generic Protocol Command Decode").exclude(attack_threat_class="Misc activity").annotate(no_of_times_attacked=Count('attacker_ip')).order_by('-no_of_times_attacked')[:20]
            serialize = Port_DetailSerializer(results,many=True)
            cache.set('port_vic',serialize.data,timeout=60*30)
        return serialize.data 

# Threat Detection Types with IDS(Dashboard in chart)update
# Types of detection techniques being applied for detection of malicious actors in your network
@shared_task(bind=True)
def ids_detection(self):
            if 'data_ids' in cache:
                finalresult = cache.get('data_ids')
                return finalresult
            else:
                time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
                results = Attack_data.objects.values('type_of_threat').filter(detection_mechanism= 'IDS').exclude(detection_mechanism__isnull=True).exclude(detection_mechanism__exact="Not Available").annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('-count')
                finalresult = {}
                finalresult = {"series":[], "labels": []}
                for i in results:
                    finalresult['series'].append(i.get('count'))
                    finalresult['labels'].append(i.get('type_of_threat'))
                cache.set('data_ids',finalresult,timeout=60*30)
                return finalresult 

# Threat Detection Types with ML(Dashboard in chart)update
# Types of detection techniques being applied for detection of malicious actors in your network
@shared_task(bind=True)
def ml_detection(self):    
            if 'data_ml' in cache:
                finalresult = cache.get('data_ml')
                return finalresult
            else:
                time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
                results = Attack_data.objects.values('type_of_threat').filter(detection_mechanism= 'SML').exclude(detection_mechanism__isnull=True).exclude(detection_mechanism__exact="Not Available").annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('-count')
                finalresult = {}
                finalresult = {"series":[], "labels": []}
                for i in results:
                    finalresult['series'].append(i.get('count'))
                    finalresult['labels'].append(i.get('type_of_threat'))
                cache.set('data_ml',finalresult,timeout=60*30)
                return finalresult


# Threat Detection Types with DL(Dashboard in chart)update
# Types of detection techniques being applied for detection of malicious actors in your network
@shared_task(bind=True)
def dl_detection(self):    
            if 'data_dl' in cache:
                finalresult = cache.get('data_dl')
                return finalresult
            else:
                time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
                results = Attack_data.objects.values('type_of_threat').filter(detection_mechanism= 'SDL').exclude(detection_mechanism__isnull=True).exclude(detection_mechanism__exact="Not Available").annotate(count=Count('id')).filter(attack_timestamp__gt=time_threshold).order_by('-count')
                finalresult = {}
                finalresult = {"series":[], "labels": []}
                for i in results:
                    finalresult['series'].append(i.get('count'))
                    finalresult['labels'].append(i.get('type_of_threat'))
                cache.set('data_dl',finalresult,timeout=60*30)
                return finalresult

# create table with Attacker Details
@shared_task(bind=True)
def Attacker_detail(request):
        if 'q_attack' in cache:
            new = cache.get('q_attack')
            return new
        else:
            results = Attack_data.objects.values('attack_timestamp','attacker_ip','attacker_mac','attacker_asn','attacker_isp', 'attacker_city', 'attack_os').exclude(attack_os__exact="Not Available").annotate(no_of_times_attacked=Count('attacker_ip')).order_by('-no_of_times_attacked')[:15]
            serialize = Attacker_Serializer(results,many=True)
            cache.set('q_attack',serialize.data,timeout=60*30)
        return serialize.data

#To create ids services traffic
@shared_task(bind=True)
def ids_service_traffics(request):
    if 'idstraffic' in cache:
        finalresult = cache.get('idstraffic')
        return finalresult
    else:
        external_machine = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).filter(detection_mechanism = 'IDS').filter(type_of_threat = 'External Attack').order_by('day')
        finalresult={}
        finalresult = {"labels":[], "external_Attack_Count": [],"internal_Compromised_Machine_Count": [],"lateral_Movement_Count": []}
        for i in external_machine:
            finalresult['labels'].append(i.get('day'))
            finalresult['external_Attack_Count'].append(i.get('c'))
        internal_machine = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).filter(detection_mechanism = 'IDS').filter(type_of_threat = 'Internal Compromised Machine').order_by('day')
        for i in internal_machine:
            finalresult['internal_Compromised_Machine_Count'].append(i.get('c'))
        lateral_movement = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).filter(detection_mechanism = 'IDS').filter(type_of_threat = 'Lateral Movement').order_by('day')
        for i in lateral_movement:
            finalresult['lateral_Movement_Count'].append(i.get('c'))          
        cache.set('idstraffic',finalresult,timeout=60*1)    
        return finalresult  
# SDL Service (Threat)
@shared_task(bind=True)
def sdl_service_traffics(self):
    if 'sdltraffic' in cache:
        finalresult = cache.get('sdltraffic')
        return finalresult
    else:
        external_machine = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).filter(detection_mechanism = 'SDL').filter(type_of_threat = 'External Attack').order_by('day')
        finalresult={}
        finalresult = {"labels":[], "external_attack_count": [],"internal_compromised_machine_count": [],"lateral_movement_count": []}
        for i in external_machine:
            finalresult['labels'].append(i.get('day'))
            finalresult['external_attack_count'].append(i.get('c'))
        internal_machine = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).filter(detection_mechanism = 'SDL').filter(type_of_threat = 'Internal Compromised Machine').order_by('day')
        for i in internal_machine:
            finalresult['internal_compromised_machine_count'].append(i.get('c'))
        lateral_movement = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).filter(detection_mechanism = 'SDL').filter(type_of_threat = 'Lateral Movement').order_by('day')
        for i in lateral_movement:
            finalresult['lateral_movement_count'].append(i.get('c'))          
        cache.set('sdltraffic',finalresult,timeout=60*30)    
        return finalresult

# SML Service (Threat)
@shared_task(bind=True)
def sml_service_traffics(self):
    if 'smltraffic' in cache:
        finalresult = cache.get('smltraffic')
        return finalresult
    else:
        external_machine = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).filter(detection_mechanism = 'SML').filter(type_of_threat = 'External Attack').order_by('day')
        finalresult={}
        finalresult = {"labels":[], "external_attack_count": [],"internal_compromised_machine_count": [],"lateral_movement_count": []}
        for i in external_machine:
            finalresult['labels'].append(i.get('day'))
            finalresult['external_attack_count'].append(i.get('c'))
        internal_machine = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).filter(detection_mechanism = 'SML').filter(type_of_threat = 'Internal Compromised Machine').order_by('day')
        for i in internal_machine:
            finalresult['internal_compromised_machine_count'].append(i.get('c'))
        lateral_movement = Attack_data.objects.annotate(day=TruncDate('attack_timestamp')).values('day').annotate(c=Count('id')).filter(detection_mechanism = 'SML').filter(type_of_threat = 'Lateral Movement').order_by('day')
        for i in lateral_movement:
            finalresult['lateral_movement_count'].append(i.get('c'))          
        cache.set('smltraffic',finalresult,timeout=60*30)    
        return finalresult

                                                                 