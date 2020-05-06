from __future__ import print_function

import requests
import sys

def bandwidth_in(host):
   bandwidth_in_query = (requests.get('{0}/api/v1/query'.format('http://' + host + ':9090'),params={'query': 'rate(node_network_receive_bytes_total{device="enp0s3",instance="localhost:9100",job="node"}[1m])'})).json()['data']['result']
   return bandwidth_in_query

def bandwidth_out(host):   
   bandwidth_out_query = (requests.get('{0}/api/v1/query'.format('http://' + host + ':9090'),params={'query': 'rate(node_network_transmit_bytes_total{device="enp0s3",instance="localhost:9100",job="node"}[1m])'})).json()['data']['result']
   return bandwidth_out_query

def cpu_utilization(host):
   cpu_util = requests.get('{0}/api/v1/query'.format('http://' + host + ':9090'),params={'query': '100 - (avg by (instance) (irate(node_cpu_seconds_total{job="node",mode="idle"}[5m])) * 100)'}).json()['data']['result']
#   results = bandwidth_in_query.json()
   return cpu_util

def memory_used_percentage(host):
   memory_usage = (requests.get('{0}/api/v1/query'.format('http://' + host + ':9090'),params={'query': '100 * (1 - ((node_memory_MemFree_bytes + node_memory_Cached_bytes + node_memory_Buffers_bytes) / node_memory_MemTotal_bytes))'})).json()['data']['result']
   return memory_usage

def total_bytes_disk_in(host):
   disk_in = (requests.get('{0}/api/v1/query'.format('http://' + host + ':9090'),params={'query': 'rate(node_disk_read_bytes_total{device="sda"}[1m])'})).json()['data']['result']
   return disk_in

def total_bytes_disk_out(host):
   disk_out = (requests.get('{0}/api/v1/query'.format('http://' + host + ':9090'),params={'query': 'rate(node_disk_written_bytes_total{device="sda"}[1m])'})).json()['data']['result']
   return disk_out

def metrics(host):
   host_dict = {}
   host_dict.update({'host': host})
   host_dict.update({'bandwidth_in': bandwidth_in(host)[0]['value'][1]})
   host_dict.update({'bandwidth_out': bandwidth_out(host)[0]['value'][1]})
   host_dict.update({'disk_read_bytes': total_bytes_disk_in(host)[0]['value'][1]})
   host_dict.update({'cpu_utilization': cpu_utilization(host)[0]['value'][1]})
   host_dict.update({'disk_written_bytes': total_bytes_disk_out(host)[0]['value'][1]})
   host_dict.update({'memory_usage': memory_used_percentage(host)[0]['value'][1]})
   return host_dict

##Exemplo que eu utilizei foi com esse IP
host="192.168.100.11"
bandwidth_in_query = 'rate(node_network_receive_bytes_total{device="enp0s3",instance="localhost:9100",job="node"}[1m])'
bandwidth_out_query = 'rate(node_network_transmit_bytes_total{device="enp0s3",instance="localhost:9100",job="node"}[1m])'
cpu_util = '100 - (avg by (instance) (irate(node_cpu_seconds_total{job="node",mode="idle"}[5m])) * 100)'

u = metrics(host)
print (u)
