#
# The unfinished memory guard for opening a million files and crashing your computer
#
#

def memory():
	"""
	Get node total memory and memory usage
	"""
	with open('/proc/meminfo','r') as mem:
		ret = {}
		tmp = 0
		for i in mem:
			sline = i.split()
			if str(sline[0])=='MemTotal:':
				ret['total'] = int(sline[1]*1.0e-6)
	return ret
	
	
