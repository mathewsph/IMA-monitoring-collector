import time
from utils.prometheus_wrapper import PrometheusWrapper
#from monitoring_modules.utils.prometheus_wrapper import PrometheusWrapper

'''
Metrics: Bandwidth, packet loss, RX/TX
'''
class EdgeMonitoring(object):
    def __init__(self, slps):
        self.slps = slps
        self.prometheus = PrometheusWrapper()
    
    #especificar o job exemplo:{job="edge-slice-monitor"}
    def EdgeMonitoringCollector(self, slps):
      instances = []
      for slp in slps:
        instances.append(slp['edge_address']+':19999')
      metrics_per_instance = {}
      metrics_per_instance['slice_parts'] = {}

#      instances = ['demo.robustperception.io:9100']
      for instance in instances:
        instance_str = ("instance='" + instance + "'")
        query = '100 - netdata_system_cpu_percentage_average{instance="' + instance + '", dimension="idle"} or netdata_system_ram_MB_average{instance="' + instance + '", dimension="used", job="edge-slice-monitor"} or sum(0-netdata_net_net_kilobits_persec_average{instance="' + instance + '",job="edge-slice-monitor",dimension="sent"}) or netdata_disk_io_kilobytes_persec_average{instance="'+instance+'",job="edge-slice-monitor",dimension="reads"}'
#        query2 = 
        results = self.prometheus.runQuery(query)
#        r2 = self.prometheus.runQuery(query)
#       results = results + r2
        print (len(results))
        metrics_per_instance['slice_parts'][instance] = results
      
      for i in metrics_per_instance['slice_parts']:
        if len(metrics_per_instance['slice_parts'][i]) > 0:
          for a in (metrics_per_instance['slice_parts'][i]):
            if metrics_per_instance['slice_parts'][i].index(a) == 0:
              cpu = ({'cpu': a['value'][1]})
            elif metrics_per_instance['slice_parts'][i].index(a) == 1:
              mem_used = ({'memory_used': a['value'][1]})
            elif metrics_per_instance['slice_parts'][i].index(a) == 2:
              tx = ({'bandwidth_tx': a['value'][1]})
            elif metrics_per_instance['slice_parts'][i].index(a) == 3:
              disk_read = ({'disk_read': a['value'][1]})
          z = dict(list(cpu.items()) + list(mem_used.items()) + list(tx.items()) + list(disk_read.items()))
          metrics_per_instance['slice_parts'].update({i: z})

      for unit in instances:
        for mslp in slps:
          if (unit) == (mslp['edge_address']+":19999"):
            mslp['metrics'] = {}
            mslp['metrics'] = metrics_per_instance['slice_parts'][unit]
        
      return slps

    def _buildQuery(self):
        CPU = '100 - netdata_system_cpu_percentage_average{instance=$instance:$port, dimension="idle"}'
        Mem_usage = 'netdata_system_ram_MB_average{instance="$instance:$port", dimension="used", job="edge-slice-monitor"}'
        TX = 'sum(0-netdata_net_net_kilobits_persec_average{instance=$instance:$port,job="edge-slice-monitor",dimension="sent"})'
        RX = 'sum(netdata_net_net_kilobits_persec_average{instance="$instance:$port", job="edge-slice-monitor",dimension="received"})'
        Disk_in = 'sum(netdata_disk_io_kilobytes_persec_average{instance="10.7.227.175:19999",job="edge-slice-monitor",dimension="reads"})'
        Disk_out = 'sum(0-netdata_disk_io_kilobytes_persec_average{instance="10.7.227.175:19999",job="edge-slice-monitor",dimension="writes"})'

'''slps_edge = [{'type': 'EDGE', 'slice_part_name': 'core-dc-public', 'edge_address': '10.7.227.175', 'slice_part_id': 1, 'location': 'natal', 'vdus': [{'name': 'core-vm', 'ip_address': '166.172.78.230', 'mac_address': '02: 00: 00: 9d:f5:f3', 'id': 1}]}, {'type': 'EDGE', 'slice_part_name': 'core-dc-private', 'edge_address': '10.7.229.179', 'slice_part_id': 3, 'location': 'natal', 'vdus': [{'name': 'core-vm', 'ip_address': '107.199.197.230', 'mac_address': '02: 00: 00: 62:ca: 7a', 'id': 3}]}, {'type': 'EDGE', 'slice_part_name': 'core-dc-public', 'edge_address': 'demo.robustperception.io', 'slice_part_id': 1, 'location': 'natal', 'vdus': [{'name': 'core-vm', 'ip_address': '166.172.78.230', 'mac_address': '02: 00: 00: 9d:f5:f3', 'id': 1}]}, {'type': 'EDGE', 'slice_part_name': 'core-dc-private', 'edge_address': '10.7.229.64', 'slice_part_id': 1, 'location': 'natal', 'vdus': [{'name': 'core-vm', 'ip_address': '107.199.197.230', 'mac_address': '02: 00: 00: 62:ca: 7a', 'id': 1}]}]
exemplo = EdgeMonitoring(slps_edge)
results = exemplo.EdgeMonitoringCollector(slps_edge)
print (results)'''
