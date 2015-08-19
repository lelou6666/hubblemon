import os, socket, sys, time
import data_loader
from datetime import datetime


hubblemon_path = os.path.abspath('..')
sys.path.append(hubblemon_path)

import common.core

jstat_preset = [['Survivor_0', 'Survivor_1', 'Eden', 'Old', 'Permanent'], 'YGC', 'YGCT', 'FGC', 'FGCT', 'GCT', ['YGC', 'FGC', 'GCT'], ['YGCT', 'FGCT']]

def jstat_view(path, title = ''):
	return common.core.default_loader(path, jstat_preset, title)


#
# chart list
#
jstat_cloud_map = {}
last_ts = 0

def init_plugin():
	global jstat_cloud_map

	global last_ts

	ts = time.time()
	if ts - last_ts < 300:
		return
	last_ts = ts


	print('#### jstat init ########')


	system_list = common.core.get_system_list()
	for system in system_list:
		instance_list = common.core.get_data_list(system, 'jstat_')
		if len(instance_list) > 0:
			jstat_cloud_map[system] = instance_list	

	print (jstat_cloud_map)
		
	


def get_chart_data(param):
	#print(param)
	global jstat_cloud_map


	type = 'jstat_stat'
	if 'type' in param:
		type = param['type']

	if 'instance' not in param or 'server' not in param:
		return None

	instance_name = param['instance']
	server_name = param['server']

	if type == 'jstat_stat':
		for node in jstat_cloud_map[server_name]:
			if node.startswith(instance_name):
				results = common.core.default_loader(server_name + '/' + node, jstat_preset, title=node)
				break

	return results



def get_chart_list(param):
	#print(param)

	if 'type' in param:
		type = param['type']

	return (['server', 'instance'], jstat_cloud_map)
	

