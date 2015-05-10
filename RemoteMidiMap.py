from __future__ import with_statement 
from _Framework import ControlSurface
from _Framework.InputControlElement import InputControlElement, MIDI_CC_TYPE
from _Framework.SliderElement import SliderElement

import socket
import struct
#import time
from _Framework import Task

#=====================================================================
class RemoteMidiMap(ControlSurface.ControlSurface): 

	#=====================================================================
	def __init__(self, c_instance):
		super(RemoteMidiMap, self).__init__(c_instance) 

		with self.component_guard():
		
			UDP_IP = "127.0.0.1"
			UDP_PORT = 8002

			self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
			self.sock.bind((UDP_IP, UDP_PORT))
			self.sock.setblocking(0)

			#self.song().tempo = 177.

			self.counter = 0
			self._tasks.add(Task.loop(self.doStuff))


	#=====================================================================
	def doStuff(self,x):

		try:
			data, addr = self.sock.recvfrom(64) # buffer size is 1024 byte
			
			addressPattern = data[:data.find("\0")]

			#data = data.split(',i')
			#v = struct.unpack('>i',data[1][2:(2+4)])[0]
			data = data.split(',ii')
			v = struct.unpack('>ii',data[1][1:])

			track_number = v[0]
			midi_cc = v[1]

			b = SliderElement(1, 0, midi_cc)
			song = self.song()

			if (addressPattern == "/pan"):
				b.connect_to(song.tracks[track_number].mixer_device.panning)
			elif (addressPattern == "/volume"):
				b.connect_to(song.tracks[track_number].mixer_device.volume)
			self.show_message(addressPattern)
		except socket.error:
			pass




		