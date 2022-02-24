# all net constants go in this file
from tools import is_on_roborio_network

__is_on_roborio_network = is_on_roborio_network()

TCP_STREAM_IP = '10.45.90.22' if __is_on_roborio_network else '192.168.1.8'

TCP_STREAM_PORT = 1180
num_of_streams = -1
def get_stream_port():
	global num_of_streams
	num_of_streams += 1
	if num_of_streams == 11:
		raise ConnectionError("fms allows only 10 ports")
	return TCP_STREAM_PORT+num_of_streams
