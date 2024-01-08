#  ============================================
#  File Name: fake_db.py
#  Description: To define fake_db data.
#  --------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===========================================

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

####################################################################
# FAKE DATA GRAPHS #
####################################################################
#NETWORK MAP
# @api_view(['GET'])
# def graph(request):
#     dataGraph = [["aws_network", "eu-north-1"], ["aws_network", "ap-south-1"], ["aws_network", "eu-west-3"], ["aws_network", "eu-west-2"], ["aws_network", "eu-west-1"], ["aws_network", "ap-northeast-3"], ["aws_network", "ap-northeast-2"], ["aws_network", "ap-northeast-1"], ["aws_network", "sa-east-1"], ["aws_network", "ca-central-1"], ["aws_network", "ap-southeast-1"], ["aws_network", "ap-southeast-2"], ["aws_network", "eu-central-1"], ["aws_network", "us-east-1"], ["aws_network", "us-east-2"], ["aws_network", "us-west-1"], ["aws_network", "us-west-2"], ["eu-north-1", "vpc-068a336f"], ["ap-south-1", "vpc-a4c736cf"], ["ap-south-1", "vpc-05d8e866de3b16ed4"], ["eu-west-3", "vpc-919a6bf9"], ["eu-west-2", "vpc-c591c8ad"], ["eu-west-1", "vpc-a736e4de"], ["ap-northeast-3", "vpc-49b5c620"], ["ap-northeast-2", "vpc-251ea64e"], ["ap-northeast-1", "vpc-2d7e9c4b"], ["sa-east-1", "vpc-b743abd1"], ["ca-central-1", "vpc-7338151b"], ["ap-southeast-1", "vpc-076eba7798d283a7a"], ["ap-southeast-1", "vpc-a7b745c1"], ["ap-southeast-2", "vpc-30f41256"], ["eu-central-1", "vpc-dde763b7"], ["us-east-1", "vpc-0805f0179e2e62625"], ["us-east-1", "vpc-01788980ef0ecf4a0"], ["us-east-1", "vpc-0b2d8976"], ["us-east-2", "vpc-08c860b62e0557266"], ["us-east-2", "vpc-012b5fedf8c312c06"], ["us-east-2", "vpc-0ef02c4cf77b0165a"], ["us-east-2", "vpc-0439836f"], ["us-east-2", "vpc-068eec30493749de6"], ["us-west-1", "vpc-06eb721831776b3cc"], ["us-west-1", "vpc-0eae1843ceb46fdde"], ["us-west-1", "vpc-00f12532614589308"], ["us-west-1", "vpc-f3905b95"], ["us-west-1", "vpc-0e5eaa0a70cff2299"], ["us-west-2", "vpc-363e624e"], ["vpc-068a336f", "subnet-7df74914"], ["vpc-068a336f", "subnet-41b1683a"], ["vpc-068a336f", "subnet-ee778fa3"], ["vpc-a4c736cf", "subnet-3de4a871"], ["vpc-a4c736cf", "subnet-5a667832"], ["vpc-a4c736cf", "subnet-3a7deb41"], ["vpc-05d8e866de3b16ed4", "subnet-0d1bb5462d44b48ed"], ["vpc-05d8e866de3b16ed4", "subnet-0d58260129b8d423c"], ["vpc-05d8e866de3b16ed4", "subnet-0121d1fd8f8f3a4df"], ["vpc-05d8e866de3b16ed4", "subnet-00ea14e23b246902f"], ["vpc-05d8e866de3b16ed4", "subnet-01dda75472358a76e"], ["vpc-05d8e866de3b16ed4", "subnet-01088e4037bcca301"], ["vpc-919a6bf9", "subnet-48253921"], ["vpc-919a6bf9", "subnet-62c2f519"], ["vpc-919a6bf9", "subnet-7e522a33"], ["vpc-c591c8ad", "subnet-bddb66f1"], ["vpc-c591c8ad", "subnet-bfceedd6"], ["vpc-c591c8ad", "subnet-31acc34b"], ["vpc-a736e4de", "subnet-53a7b81b"], ["vpc-a736e4de", "subnet-3e1a1558"], ["vpc-a736e4de", "subnet-d9e5ac83"], ["vpc-49b5c620", "subnet-a300edd8"], ["vpc-49b5c620", "subnet-76a6641f"], ["vpc-49b5c620", "subnet-dac86497"], ["vpc-251ea64e", "subnet-1c14ff43"], ["vpc-251ea64e", "subnet-d3736a9f"], ["vpc-251ea64e", "subnet-5007612b"], ["vpc-251ea64e", "subnet-f4dc699f"], ["vpc-2d7e9c4b", "subnet-61b91629"], ["vpc-2d7e9c4b", "subnet-e49c2acf"], ["vpc-2d7e9c4b", "subnet-7f6e7724"], ["vpc-b743abd1", "subnet-33bfda55"], ["vpc-b743abd1", "subnet-1e3e5d45"], ["vpc-b743abd1", "subnet-f37ae1ba"], ["vpc-7338151b", "subnet-de0768a4"], ["vpc-7338151b", "subnet-1da84042"], ["vpc-7338151b", "subnet-f789da9f"], ["vpc-076eba7798d283a7a", "subnet-0f4ddf103d24d4832"], ["vpc-076eba7798d283a7a", "subnet-0f468c5230b064550"], ["vpc-a7b745c1", "subnet-a99235cf"], ["vpc-a7b745c1", "subnet-b69d0fef"], ["vpc-a7b745c1", "subnet-bed700f6"], ["vpc-30f41256", "subnet-00a9d058"], ["vpc-30f41256", "subnet-886f97c0"], ["vpc-30f41256", "subnet-d0c30db6"], ["vpc-dde763b7", "subnet-ac08a6e0"], ["vpc-dde763b7", "subnet-374b904b"], ["vpc-dde763b7", "subnet-0382ee69"], ["vpc-0805f0179e2e62625", "subnet-01fe39e6c750a233f"], ["vpc-0805f0179e2e62625", "subnet-0dec6f603b47855ce"], ["vpc-0805f0179e2e62625", "subnet-0d01d1e310cb17949"], ["vpc-0805f0179e2e62625", "subnet-07d033d55f2218981"], ["vpc-01788980ef0ecf4a0", "subnet-09ed0e28537283cb5"], ["vpc-0b2d8976", "subnet-883e65c5"], ["vpc-0b2d8976", "subnet-1260e874"], ["vpc-0b2d8976", "subnet-03b40f9d130c6a200"], ["vpc-08c860b62e0557266", "subnet-08710f101abb1be48"], ["vpc-08c860b62e0557266", "subnet-09df744590a8f42e3"], ["vpc-08c860b62e0557266", "subnet-09791630534b77dbb"], ["vpc-08c860b62e0557266", "subnet-0c6705e9f19ef879a"], ["vpc-08c860b62e0557266", "subnet-00ced30a43c508012"], ["vpc-08c860b62e0557266", "subnet-0f94f0b79874dcdc9"], ["vpc-012b5fedf8c312c06", "subnet-08fcf38b3d8a475e4"], ["vpc-012b5fedf8c312c06", "subnet-0cb6bdda08786dce5"], ["vpc-0439836f", "subnet-5610b23d"], ["vpc-0439836f", "subnet-0625d8546cb402bf6"], ["vpc-068eec30493749de6", "subnet-0546cf8b5652d6cfc"], ["vpc-068eec30493749de6", "subnet-0a44b91cca3f79bf4"], ["vpc-068eec30493749de6", "subnet-040b8307ab31d4a0b"], ["vpc-068eec30493749de6", "subnet-0050051074866f165"], ["vpc-068eec30493749de6", "subnet-01e52a7fc870a3268"], ["vpc-068eec30493749de6", "subnet-0513b160f689f54fc"], ["vpc-06eb721831776b3cc", "subnet-08b6f3d218310371c"], ["vpc-06eb721831776b3cc", "subnet-0c4f4b6e6369c1209"], ["vpc-06eb721831776b3cc", "subnet-0c220f8d32bc44438"], ["vpc-06eb721831776b3cc", "subnet-0ae855bad36239d55"], ["vpc-0eae1843ceb46fdde", "subnet-0781541e2c3898f2d"], ["vpc-0eae1843ceb46fdde", "subnet-0cd2b72e2f900ea4a"], ["vpc-0eae1843ceb46fdde", "subnet-05d3db763326fb413"], ["vpc-0eae1843ceb46fdde", "subnet-04035a0341378028c"], ["vpc-00f12532614589308", "subnet-0128450193605122c"], ["vpc-00f12532614589308", "subnet-0e4757410484fec53"], ["vpc-00f12532614589308", "subnet-0d5ca49d56d507d77"], ["vpc-00f12532614589308", "subnet-0e36ab197eb04cf61"], ["vpc-f3905b95", "subnet-10a11b76"], ["vpc-f3905b95", "subnet-6ad00630"], ["vpc-0e5eaa0a70cff2299", "subnet-0be24ee2b463031ba"], ["vpc-0e5eaa0a70cff2299", "subnet-025517d35089e8f2d"], ["vpc-0e5eaa0a70cff2299", "subnet-064d8085157cba018"], ["vpc-363e624e", "subnet-6e8a3233"], ["vpc-363e624e", "subnet-1617b96e"], ["vpc-363e624e", "subnet-7019d23a"], ["vpc-363e624e", "subnet-60faca4b"], ["subnet-0d58260129b8d423c", "i-094e6ae45b8c887d5"], ["subnet-0d58260129b8d423c", "i-0956f2bcb4cd5da01"], ["subnet-0d58260129b8d423c", "i-09167b62869e8bbf1"], ["subnet-0d58260129b8d423c", "i-0d3e99bbca6b16767"], ["subnet-0d58260129b8d423c", "i-070b866171a2207e8"], ["subnet-0d58260129b8d423c", "i-0b4dfd0815c983c2c"], ["subnet-0d58260129b8d423c", "i-00b8da219eb1152f2"], ["subnet-01dda75472358a76e", "i-0c7178c0ac1aeb2e9"], ["subnet-01dda75472358a76e", "i-00e45066f250079e3"], ["subnet-01dda75472358a76e", "i-07657329b9b03c2db"], ["subnet-01dda75472358a76e", "i-00381874e8f0f7dfb"], ["subnet-01dda75472358a76e", "i-0e8359b4fcc5470ed"], ["subnet-01dda75472358a76e", "i-003f99e09ee2dc48d"], ["subnet-01088e4037bcca301", "i-09f40592cfc93d821"], ["subnet-01088e4037bcca301", "i-043ed684823f0f5fa"], ["subnet-01088e4037bcca301", "i-05f215a90c82368cb"], ["subnet-01088e4037bcca301", "i-0bbece17961818b67"], ["subnet-01088e4037bcca301", "i-0022d229a42c77189"], ["subnet-01088e4037bcca301", "i-0d98de00181292ba6"], ["subnet-01fe39e6c750a233f", "i-0f80aa86173ecab33"], ["subnet-01fe39e6c750a233f", "i-000566957bba2e29e"], ["subnet-01fe39e6c750a233f", "i-081c9443edfcf019d"], ["subnet-01fe39e6c750a233f", "i-0fbde287907c08000"], ["subnet-09ed0e28537283cb5", "i-02652b6f65733605d"], ["subnet-0c6705e9f19ef879a", "i-0fbfeb6f45ef715a9"], ["subnet-0f94f0b79874dcdc9", "i-0737aaf86e43b8967"], ["subnet-08fcf38b3d8a475e4", "i-08b7a015a020efaf6"], ["subnet-08fcf38b3d8a475e4", "i-0852e6c71d932d151"], ["subnet-0a44b91cca3f79bf4", "i-0c074bd8d2a83681d"], ["subnet-0a44b91cca3f79bf4", "i-0d80393aff31c7365"], ["subnet-040b8307ab31d4a0b", "i-0293cb3f9562d76de"], ["subnet-040b8307ab31d4a0b", "i-087a6cad7054d4d29"], ["subnet-040b8307ab31d4a0b", "i-0e484e68eda049f76"], ["subnet-0050051074866f165", "i-0a8c7b4d8fb4d2014"], ["subnet-0050051074866f165", "i-0768a52629434e63e"], ["subnet-0050051074866f165", "i-01e446944d0660d58"], ["subnet-0e36ab197eb04cf61", "i-0ae34748da83b2d5f"]]
#     return Response(dataGraph,status=status.HTTP_200_OK)
#SERVICE APPLICATION THREAT
@api_view(['GET'])
def service(request):
    application = {"httpcount": "238","ntpcount": "35868","smbcount": "3258","sipcount": "345","tftpcount": "576","telnetcount": "67678","httpname": "Http","ntpname": "NTP","smbname": "SMB","sipname": "SIP","tftpname": "TFTP","telnetname": "TELNET"
    }
    return Response(application,status=status.HTTP_200_OK)

#ATTACKER UP COUNT DATE WISE FAKE DATA
@api_view(['GET'])
def ip_count(request):
    ip = {
      "series1": [5, 5, 10, 8, 7, 5, 4, 0, 0, 0, 10, 10, 7, 8, 6, 9],
      "seriesname1": "124.45.00",
      "series2": [10, 15, 0, 12, 0, 10, 12, 15, 0, 0, 12, 0, 14, 0, 0, 0],
      "seriesname2": "127.10.30",
      "series3": [0, 0, 0, 0, 3, 4, 1, 3, 4, 6, 7, 9, 5, 0, 0, 0],
      "seriesname3": "127.10.31",
      "series4": [0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 9, 55, 0, 0, 0],
      "seriesname4": "127.10.32",
      "series5": [0, 0, 0, 0, 0, 1, 1, 13, 4, 60, 17, 9, 55, 0, 0, 0],
      "seriesname5": "127.10.33",
      "series6": [0, 0, 0, 0, 0, 14, 1, 13, 4, 0, 17, 9, 0, 0, 0, 0],
      "seriesname6": "127.10.34",
      "series7": [0, 0, 0, 0, 0, 0, 1, 13, 4, 66, 17, 9, 55, 0, 0, 0],
      "seriesname7": "127.10.35",
      "series8": [0, 0, 0, 0, 0, 14, 1, 13, 4, 66, 17, 9, 55, 0, 0, 0],
      "seriesname8": "127.10.36",
      "series9": [70, 0, 0, 0, 0, 14, 1, 13, 4, 66, 17, 9, 55, 0, 0, 0],
      "seriesname9": "127.10.37",
      "series10": [30, 0, 0, 57, 0, 14, 1, 13, 4, 66, 17, 9, 55, 0, 0, 0],
      "seriesname10": "127.10.38",
      "labels": ["01/10/2022", "02/10/2022", "03/10/2022", "04/10/2022", "05/10/2022", "06/10/2022", "07/10/2022", "08/10/2022", "09/10/2022", "10/10/2022", "11/10/2022", "12/10/2022", "13/10/2022", "14/10/2022", "15/10/2022"]
      }
    return Response(ip,status=status.HTTP_200_OK)

    #logs DATE WISE FAKE DATA
@api_view(['GET'])
def wazuh_data(request):
    wazuh = [
    {
      "id": "1",
      "timestamp": "2023-01-06T09:15:23.930+0000",
      "rule_level": 10,
      "rule_description": "Auditd: Device enables promiscuous mode.",
      "rule_id": "80710",
      "rule_firedtimes": 9,
      "rule_mail": "fals",
      "agent_id": "009",
      "agent_name": "fedora",
      "agent_ip": "172.16.140.117",
      "manager_name": "the-aurors-office",
      "full_log": "type=ANOM_PROMISCUOUS msg=audit(1672996523.882:1359): dev=vethbaea551 prom=0 old_prom=256 auid=4294967295 uid=0 gid=0 ses=4294967295\u001dAUID=\"unset\" UID=\"root\" GID=\"root\"",
      "decoder_parent": "auditd",
      "decoder_name": "auditd",
      "data_audit_type": "ANOM_PROMISCUOUS",
      "data_audit_id": "1359",
      "data_audit_dev": "vethbaea551",
      "data_audit_prom": "0",
      "data_audit_old_prom": "256",
      "data_audit_auid": "4294967295",
      "data_audit_uid": "0",
      "data_audit_gid": "0",
      "data_audit_session": "4294967295\u001dAUID=\"unset\"",
      "location": "/var/log/audit/audit.log",
      "epoch_time": 1672996526,
      "rule_gdpr": [
        "IV_30.1.g",
        "IV_35.7.d"
    ],
    "rule_gpg13": [
      "4.14"
  ]
    },
    {
      "id": "2",
      "timestamp": "2023-01-06T09:15:23.930+0000",
      "rule_level": 10,
      "rule_description": "Auditd: Device enables promiscuous mode.",
      "rule_id": "80710",
      "rule_firedtimes": 9,
      "rule_mail": "false",
      "agent_id": "009",
      "agent_name": "fedora",
      "agent_ip": "172.16.140.117",
      "manager_name": "the-aurors-office",
      "full_log": "type=ANOM_PROMISCUOUS msg=audit(1672996523.882:1359): dev=vethbaea551 prom=0 old_prom=256 auid=4294967295 uid=0 gid=0 ses=4294967295\u001dAUID=\"unset\" UID=\"root\" GID=\"root\"",
      "decoder_parent": "auditd",
      "decoder_name": "auditd",
      "data_audit_type": "ANOM_PROMISCUOUS",
      "data_audit_id": "1359",
      "data_audit_dev": "vethbaea551",
      "data_audit_prom": "0",
      "data_audit_old_prom": "256",
      "data_audit_auid": "4294967295",
      "data_audit_uid": "0",
      "data_audit_gid": "0",
      "data_audit_session": "4294967295\u001dAUID=\"unset\"",
      "location": "/var/log/audit/audit.log",
      "epoch_time": 1672996526,
      "rule_gdpr": [
        "IV_30.1.g",
        "IV_35.7.d"
    ],
    "rule_gpg13": [
      "4.14"
  ]
    },
    {
      "id": "3",
      "timestamp": "2023-01-06T09:15:23.930+0000",
      "rule_level": 10,
      "rule_description": "Auditd: Device enables promiscuous mode.",
      "rule_id": "80710",
      "rule_firedtimes": 9,
      "rule_mail": "false",
      "agent_id": "009",
      "agent_name": "fedora",
      "agent_ip": "172.16.140.117",
      "manager_name": "the-aurors-office",
      "full_log": "type=ANOM_PROMISCUOUS msg=audit(1672996523.882:1359): dev=vethbaea551 prom=0 old_prom=256 auid=4294967295 uid=0 gid=0 ses=4294967295\u001dAUID=\"unset\" UID=\"root\" GID=\"root\"",
      "decoder_parent": "auditd",
      "decoder_name": "auditd",
      "data_audit_type": "ANOM_PROMISCUOUS",
      "data_audit_id": "1359",
      "data_audit_dev": "vethbaea551",
      "data_audit_prom": "0",
      "data_audit_old_prom": "256",
      "data_audit_auid": "4294967295",
      "data_audit_uid": "0",
      "data_audit_gid": "0",
      "data_audit_session": "4294967295\u001dAUID=\"unset\"",
      "location": "/var/log/audit/audit.log",
      "epoch_time": 1672996526,
      "rule_gdpr": [
        "IV_30.1.g",
        "IV_35.7.d"
    ],
    "rule_gpg13": [
      "4.14"
  ]
    }
    ]
    return Response(wazuh,status=status.HTTP_200_OK)

@api_view(['GET'])
def graph(request):
    dataGraph = {'name': 'AWS Map', 'children': [{'name': 'ap-south-1', 'children': [{'name': 'vpc-a4c736cf', 'children': [{'name': 'subnet-3de4a871'}, {'name': 'subnet-5a667832'}, {'name': 'subnet-3a7deb41'}]}, {'name': 'vpc-05d8e866de3b16ed4', 'children': [{'name': 'subnet-0d1bb5462d44b48ed'}, {'name': 'subnet-0d58260129b8d423c', 'children': [{'name': 'i-094e6ae45b8c887d5'}, {'name': 'i-09167b62869e8bbf1'}, {'name': 'i-0d3e99bbca6b16767'}, {'name': 'i-070b866171a2207e8'}, {'name': 'i-00b8da219eb1152f2'}, {'name': 'i-00a154cd263371b8e'}, {'name': 'i-00e0415a2b756c279'}]}, {'name': 'subnet-0121d1fd8f8f3a4df'}, {'name': 'subnet-00ea14e23b246902f'}, {'name': 'subnet-01dda75472358a76e', 'children': [{'name': 'i-0c7178c0ac1aeb2e9'}, {'name': 'i-00e45066f250079e3'}, {'name': 'i-07657329b9b03c2db'}, {'name': 'i-00381874e8f0f7dfb'}, {'name': 'i-0e8359b4fcc5470ed'}, {'name': 'i-003f99e09ee2dc48d'}, {'name': 'i-0c15ce47b69fd7186'}, {'name': 'i-0e1b9caa678b6bbcb'}, {'name': 'i-00b1aa715dbe52af7'}]}, {'name': 'subnet-01088e4037bcca301', 'children': [{'name': 'i-09f40592cfc93d821'}, {'name': 'i-043ed684823f0f5fa'}, {'name': 'i-05f215a90c82368cb'}, {'name': 'i-0bbece17961818b67'}, {'name': 'i-0022d229a42c77189'}, {'name': 'i-0d98de00181292ba6'}, {'name': 'i-0b923f1858536d6c8'}, {'name': 'i-071664aca742542c4'}]}]}]}, {'name': 'eu-north-1', 'children': [{'name': 'vpc-068a336f', 'children': [{'name': 'subnet-7df74914'}, {'name': 'subnet-41b1683a'}, {'name': 'subnet-ee778fa3'}]}]}, {'name': 'eu-west-3', 'children': [{'name': 'vpc-919a6bf9', 'children': [{'name': 'subnet-48253921'}, {'name': 'subnet-62c2f519'}, {'name': 'subnet-7e522a33'}]}]}, {'name': 'eu-west-2', 'children': [{'name': 'vpc-c591c8ad', 'children': [{'name': 'subnet-bddb66f1'}, {'name': 'subnet-bfceedd6'}, {'name': 'subnet-31acc34b'}]}]}, {'name': 'eu-west-1', 'children': [{'name': 'vpc-a736e4de', 'children': [{'name': 'subnet-53a7b81b'}, {'name': 'subnet-3e1a1558'}, {'name': 'subnet-d9e5ac83'}]}]}, {'name': 'ap-northeast-3', 'children': [{'name': 'vpc-49b5c620', 'children': [{'name': 'subnet-a300edd8'}, {'name': 'subnet-76a6641f'}, {'name': 'subnet-dac86497'}]}]}, {'name': 'ap-northeast-2', 'children': [{'name': 'vpc-251ea64e', 'children': [{'name': 'subnet-1c14ff43'}, {'name': 'subnet-d3736a9f'}, {'name': 'subnet-5007612b'}, {'name': 'subnet-f4dc699f'}]}]}, {'name': 'ap-northeast-1', 'children': [{'name': 'vpc-2d7e9c4b', 'children': [{'name': 'subnet-61b91629'}, {'name': 'subnet-e49c2acf'}, {'name': 'subnet-7f6e7724'}]}]}, {'name': 'ca-central-1', 'children': [{'name': 'vpc-7338151b', 'children': [{'name': 'subnet-de0768a4'}, {'name': 'subnet-1da84042'}, {'name': 'subnet-f789da9f'}]}]}, {'name': 'sa-east-1', 'children': [{'name': 'vpc-b743abd1', 'children': [{'name': 'subnet-33bfda55'}, {'name': 'subnet-1e3e5d45'}, {'name': 'subnet-f37ae1ba'}]}]}, {'name': 'ap-southeast-1', 'children': [{'name': 'vpc-076eba7798d283a7a', 'children': [{'name': 'subnet-0f4ddf103d24d4832'}, {'name': 'subnet-0f468c5230b064550'}]}, {'name': 'vpc-a7b745c1', 'children': [{'name': 'subnet-a99235cf'}, {'name': 'subnet-b69d0fef'}, {'name': 'subnet-bed700f6'}]}]}, {'name': 'ap-southeast-2', 'children': [{'name': 'vpc-30f41256', 'children': [{'name': 'subnet-00a9d058'}, {'name': 'subnet-886f97c0'}, {'name': 'subnet-d0c30db6'}]}]}, {'name': 'eu-central-1', 'children': [{'name': 'vpc-dde763b7', 'children': [{'name': 'subnet-ac08a6e0'}, {'name': 'subnet-374b904b'}, {'name': 'subnet-0382ee69'}]}]}, {'name': 'us-east-1', 'children': [{'name': 'vpc-0805f0179e2e62625', 'children': [{'name': 'subnet-01fe39e6c750a233f', 'children': [{'name': 'i-0f80aa86173ecab33'}, {'name': 'i-000566957bba2e29e'}, {'name': 'i-081c9443edfcf019d'}, {'name': 'i-0fbde287907c08000'}]}, {'name': 'subnet-0dec6f603b47855ce'}, {'name': 'subnet-0d01d1e310cb17949'}, {'name': 'subnet-07d033d55f2218981'}]}, {'name': 'vpc-01788980ef0ecf4a0', 'children': [{'name': 'subnet-09ed0e28537283cb5', 'children': [{'name': 'i-02652b6f65733605d'}]}]}, {'name': 'vpc-0b2d8976', 'children': [{'name': 'subnet-883e65c5'}, {'name': 'subnet-1260e874', 'children': [{'name': 'i-03a0af07095e97787'}]}, {'name': 'subnet-03b40f9d130c6a200'}]}]}, {'name': 'us-east-2', 'children': [{'name': 'vpc-0439836f', 'children': [{'name': 'subnet-5610b23d', 'children': [{'name': 'i-03b725f9eccf271e8'}]}, {'name': 'subnet-0625d8546cb402bf6'}]}]}, {'name': 'us-west-1', 'children': [{'name': 'vpc-f3905b95', 'children': [{'name': 'subnet-10a11b76'}, {'name': 'subnet-6ad00630'}]}, {'name': 'vpc-0714f5065cce7284a', 'children': [{'name': 'subnet-0ab761a5fcf5bee09', 'children': [{'name': 'i-02759dae02c927409'}, {'name': 'i-0c145f2c12d6bd075'}, {'name': 'i-065946268a0d06a8e'}, {'name': 'i-00931ff560e8f3f94'}]}, {'name': 'subnet-0c34b084c616cc7d3', 'children': [{'name': 'i-012efc1a0ab20573b'}]}, {'name': 'subnet-0a6ac7082b777a4ac'}, {'name': 'subnet-012fbd71eaa429f2d'}]}]}, {'name': 'us-west-2', 'children': [{'name': 'vpc-363e624e', 'children': [{'name': 'subnet-6e8a3233'}, {'name': 'subnet-1617b96e'}, {'name': 'subnet-7019d23a'}, {'name': 'subnet-60faca4b'}]}]}]}
    return Response(dataGraph,status=status.HTTP_200_OK)

@api_view(['GET'])
def wazuh2_data(request):
    wazuh2 = [
           {
        "ID": 1,
        "Status": "active",
        "Name": "ds-lab-1",
        "IP": "10.1.0.34",
        "Group": "[\"default\"]",
        "Manager": "security-center",
        "Node": "node01",
        "Registration date": "2023-01-07T13:15:04Z",
        "Version": "Wazuh v4.3.10",
        "Last keep alive": "2023-01-11T11:01:51Z",
        "OS version architecture": "x86_64",
        "OS version build": "-",
        "OS code name": "bullseye",
        "OS version major": 11,
        "OS version minor": "-",
        "OS name": "Debian GNU/Linux",
        "OS platform": "debian",
        "OS uname": "Linux |ds-lab-1 |5.10.0-20-amd64 |#1 SMP Debian 5.10.158-2 (2022-12-13) |x86_64",
        "OS version": "11"
    },
    {
        "ID": 2,
        "Status": "active",
        "Name": "development-center",
        "IP": "10.1.3.15",
        "Group": "[\"default\"]",
        "Manager": "security-center",
        "Node": "node01",
        "Registration date": "2023-01-07T13:15:36Z",
        "Version": "Wazuh v4.3.10",
        "Last keep alive": "2023-01-11T11:01:45Z",
        "OS version architecture": "x86_64",
        "OS version build": "-",
        "OS code name": "Focal Fossa",
        "OS version major": 20,
        "OS version minor": "04",
        "OS name": "Ubuntu",
        "OS platform": "ubuntu",
        "OS uname": "Linux |development-center |5.4.0-136-generic |#153-Ubuntu SMP Thu Nov 24 15:56:58 UTC 2022 |x86_64",
        "OS version": "20.04.5 LTS"
    },
    {
        "ID": 3,
        "Status": "disconnected",
        "Name": "l015",
        "IP": "172.16.138.114",
        "Group": "[\"default\"]",
        "Manager": "security-center",
        "Node": "node01",
        "Registration date": "2023-01-07T13:15:43Z",
        "Version": "Wazuh v4.3.10",
        "Last keep alive": "2023-01-10T13:10:10Z",
        "OS version architecture": "x86_64",
        "OS version build": "-",
        "OS code name": "Workstation Edition",
        "OS version major": 37,
        "OS version minor": "-",
        "OS name": "Fedora Linux",
        "OS platform": "fedora",
        "OS uname": "Linux |l015 |6.0.17-300.fc37.x86_64 |#1 SMP PREEMPT_DYNAMIC Wed Jan 4 15:58:35 UTC 2023 |x86_64",
        "OS version": "37"
    },
    {
        "ID": 4,
        "Status": "active",
        "Name": "LAPTOP-ASBA11EE",
        "IP": "172.16.138.191",
        "Group": "[\"default\"]",
        "Manager": "security-center",
        "Node": "node01",
        "Registration date": "2023-01-09T04:22:04Z",
        "Version": "Wazuh v4.3.10",
        "Last keep alive": "2023-01-11T11:01:44Z",
        "OS version architecture": "-",
        "OS version build": "22000",
        "OS code name": "-",
        "OS version major": 10,
        "OS version minor": "0",
        "OS name": "Microsoft Windows 11 Home Single Language",
        "OS platform": "windows",
        "OS uname": "Microsoft Windows 11 Home Single Language",
        "OS version": "10.0.22000"
    },
    {
        "ID": 5,
        "Status": "active",
        "Name": "Whizemp0038",
        "IP": "172.16.138.142",
        "Group": "[\"default\"]",
        "Manager": "security-center",
        "Node": "node01",
        "Registration date": "2023-01-09T04:28:03Z",
        "Version": "Wazuh v4.3.10",
        "Last keep alive": "2023-01-11T11:01:47Z",
        "OS version architecture": "-",
        "OS version build": "22000",
        "OS code name": "-",
        "OS version major": 10,
        "OS version minor": "0",
        "OS name": "Microsoft Windows 11 Home Single Language",
        "OS platform": "windows",
        "OS uname": "Microsoft Windows 11 Home Single Language",
        "OS version": "10.0.22000"
    },
    {
        "ID": 6,
        "Status": "active",
        "Name": "koinahi",
        "IP": "172.16.140.85",
        "Group": "[\"default\"]",
        "Manager": "security-center",
        "Node": "node01",
        "Registration date": "2023-01-09T04:30:39Z",
        "Version": "Wazuh v4.3.10",
        "Last keep alive": "2023-01-11T11:01:47Z",
        "OS version architecture": "x86_64",
        "OS version build": "-",
        "OS code name": "Jammy Jellyfish",
        "OS version major": 22,
        "OS version minor": "04",
        "OS name": "Ubuntu",
        "OS platform": "ubuntu",
        "OS uname": "Linux |koinahi |5.15.0-57-generic |#63-Ubuntu SMP Thu Nov 24 13:43:17 UTC 2022 |x86_64",
        "OS version": "22.04.1 LTS"
    },
    {
        "ID": 7,
        "Status": "active",
        "Name": "LAPTOP-OGI4Q8MC",
        "IP": "172.16.138.113",
        "Group": "[\"default\"]",
        "Manager": "security-center",
        "Node": "node01",
        "Registration date": "2023-01-09T04:37:38Z",
        "Version": "Wazuh v4.3.10",
        "Last keep alive": "2023-01-11T11:01:44Z",
        "OS version architecture": "-",
        "OS version build": "22621",
        "OS code name": "-",
        "OS version major": 10,
        "OS version minor": "0",
        "OS name": "Microsoft Windows 11 Home Single Language",
        "OS platform": "windows",
        "OS uname": "Microsoft Windows 11 Home Single Language",
        "OS version": "10.0.22621"
    },
    {
        "ID": 8,
        "Status": "active",
        "Name": "fedora",
        "IP": "172.16.140.112",
        "Group": "[\"default\"]",
        "Manager": "security-center",
        "Node": "node01",
        "Registration date": "2023-01-09T04:44:12Z",
        "Version": "Wazuh v4.3.10",
        "Last keep alive": "2023-01-11T11:01:49Z",
        "OS version architecture": "x86_64",
        "OS version build": "-",
        "OS code name": "KDE Plasma",
        "OS version major": 36,
        "OS version minor": "-",
        "OS name": "Fedora Linux",
        "OS platform": "fedora",
        "OS uname": "Linux |fedora |6.0.16-200.fc36.x86_64 |#1 SMP PREEMPT_DYNAMIC Sat Dec 31 16:47:52 UTC 2022 |x86_64",
        "OS version": "36"
    },
    {
        "ID": 9,
        "Status": "active",
        "Name": "LAPTOP-0JT92MD0",
        "IP": "172.16.138.159",
        "Group": "[\"default\"]",
        "Manager": "security-center",
        "Node": "node01",
        "Registration date": "2023-01-09T04:44:15Z",
        "Version": "Wazuh v4.3.10",
        "Last keep alive": "2023-01-11T11:01:42Z",
        "OS version architecture": "-",
        "OS version build": "22621",
        "OS code name": "-",
        "OS version major": 10,
        "OS version minor": "0",
        "OS name": "Microsoft Windows 11 Home Single Language",
        "OS platform": "windows",
        "OS uname": "Microsoft Windows 11 Home Single Language",
        "OS version": "10.0.22621"
    },
    {
        "ID": 10,
        "Status": "active",
        "Name": "WhizEmp0026",
        "IP": "172.16.138.139",
        "Group": "[\"default\"]",
        "Manager": "security-center",
        "Node": "node01",
        "Registration date": "2023-01-09T04:56:34Z",
        "Version": "Wazuh v4.3.10",
        "Last keep alive": "2023-01-11T11:01:43Z",
        "OS version architecture": "-",
        "OS version build": "22000",
        "OS code name": "-",
        "OS version major": 10,
        "OS version minor": "0",
        "OS name": "Microsoft Windows 11 Home Single Language",
        "OS platform": "windows",
        "OS uname": "Microsoft Windows 11 Home Single Language",
        "OS version": "10.0.22000"
    }
    ]
    return Response(wazuh2,status=status.HTTP_200_OK)




 