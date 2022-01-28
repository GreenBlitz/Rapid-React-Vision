"""
For serializing data!
"""
from random import random
from struct import pack, unpack
from threading import Thread
from typing import Tuple

import serial

Location = Tuple[float, float, float]


class GBSerialize:
	"""
	Serializer class for sending data.
	"""

	# Serial connection
	# noinspection PyUnresolvedReferences
	__conn: serial.Serial
	__thread: Thread
	__thread_stop_lock: bool
	__data: Location

	# noinspection PyUnresolvedReferences
	def __init__(self):
		# Initiate serial instance
		self.__conn = serial.Serial()

		# Setup settings
		self.__conn.port = '/dev/ttyS0'
		self.__conn.baudrate = 9600
		self.__conn.bytesize = serial.EIGHTBITS
		self.__conn.parity = serial.PARITY_NONE
		self.__conn.stopbits = serial.STOPBITS_ONE
		self.__conn.xonxoff = False

		# Start the connection
		self.__conn.open()

		# Initiate the thread
		self.__thread = Thread(target=self.__monitor_connection)
		self.__thread.setDaemon(True)

	def start(self) -> None:
		"""
		Wrapper for thread methods.
		"""
		self.__thread_stop_lock = False
		self.__thread.start()

	def stop(self) -> None:
		"""
		Wrapper for thread methods.
		"""
		self.__thread_stop_lock = True

	def send_data(self, data: Location) -> None:
		"""
		Queues data to be sent over the network when the RoboRIO pings it for info.

		:param data: The data to send.
		"""
		self.__data = data

	def __monitor_connection(self) -> None:
		"""
		Constantly read the connection and see if the RoboRIO wants any info to be sent.
		"""
		single_byte: bytes
		while True:
			# Start by checking the lock
			if self.__thread_stop_lock:
				return
			# Get a byte
			single_byte = unpack('c', self.__conn.read(1))[0]
			# If the byte is not 0
			if single_byte != 0:
				# Send back our latest queued data
				# For each float in the tuple
				for flt in self.__data:
					self.__send_arbitrary_data(pack('>f', flt))

	def __send_arbitrary_data(self, data: bytes) -> None:
		"""
		Send any arbitrary data.
		Wrapper function for sending bytes.

		:param data: The bytes to send.
		"""
		# Send the data
		print(f"[{str(random())[-3:]}] Sent data: {data}")
		self.__conn.write(data)

	def is_open(self) -> bool:
		"""
		Returns True if the connection is active.
		"""
		return self.__conn.isOpen()
