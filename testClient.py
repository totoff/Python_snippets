#!/usr/bin/python2

from Tkinter import *

import threading
import time
import socket
import struct
import sys
import ctypes

# Global variables
dome_flow_max = 2.0
dome_flow_min = 0.0
high_purge_flow_max = 0.5
high_purge_flow_min = 0.0
air_intake_tube_flow_max = 2.0
air_intake_tube_flow_min = 0.0
output_flow_max = 5.0
output_flow_min = 0.0
pitch_angle_max = 30.0
pitch_angle_min = -30.0

ip_address = sys.argv[1] if(len(sys.argv)>1) else '127.0.0.1'
port = sys.argv[2] if (len(sys.argv)>2) else 44789

network_dt = 0.250
angle_dt = 2.0/(pitch_angle_max-pitch_angle_min)

class Application(Tk):
	def __init__(self,parent):
 		Tk.__init__(self,parent)
		self.parent = parent
		
		# Init GUI
	        self.initialize()

		# Init variables
		self.angleIsIncreasing = False
		self.angleIsDecreasing = False
		self.pitch_angle_var.set(0.0) # initial angle
		self.back_light_var.set(1) # initial angle
		
		# Init timers
		self.angleTimer = None	
		self.networkTimer = None	
		self.connectTimer = None	
	
		# Init network socket
		self.launchConnectTimer()

### GUI #######################################################################

	def initialize(self):
		self.grid()
		self.dome_flow_var = DoubleVar()
		dome_flow_lbl = Label(self, text="Dome flow (L/s)",width=20)
		dome_flow_lbl.grid(column=0,row=0,sticky='NS')
		dome_flow_scl = Scale(self, from_=dome_flow_max, to=dome_flow_min, tickinterval=0.5,resolution=0.01,length=200,variable=self.dome_flow_var)
		dome_flow_scl.grid(column=0,row=1,sticky='NS')
		
		self.high_purge_var = DoubleVar()
		high_purge_flow_lbl = Label(self, text="High purge flow (L/s)",width=20)
		high_purge_flow_lbl.grid(column=1,row=0,sticky='NS')
		high_purge_flow_scl = Scale(self, from_=high_purge_flow_max, to=high_purge_flow_min, tickinterval=0.1,resolution=0.01,length=200,variable=self.high_purge_var)
		high_purge_flow_scl.grid(column=1,row=1,sticky='NS')
		
		self.air_intake_tube_var = DoubleVar()
		air_intake_tube_flow_lbl = Label(self, text="Air intake tube flow (L/s)",width=20)
		air_intake_tube_flow_lbl.grid(column=2,row=0,sticky='NS')
		air_intake_tube_flow_scl = Scale(self, from_=air_intake_tube_flow_max, to=air_intake_tube_flow_min, tickinterval=0.5,resolution=0.01,length=200,variable=self.air_intake_tube_var)
		air_intake_tube_flow_scl.grid(column=2,row=1,sticky='NS')

		self.output_flow_var = DoubleVar()
		output_flow_lbl = Label(self, text="Output flow (L/s)")
		output_flow_lbl.grid(column=0,row=2,columnspan=3,sticky='EW')
		output_flow_scl = Scale(self, from_=output_flow_min, to=output_flow_max, tickinterval=0.5,resolution=0.01,orient=HORIZONTAL,variable=self.output_flow_var)
		output_flow_scl.grid(column=0,row=3,columnspan=3,sticky='EW')
		
		self.pitch_angle_var = DoubleVar()
		pitch_angle_lbl = Label(self, text="Pitch angle (degree)")
		pitch_angle_lbl.grid(column=0,row=4,columnspan=3,sticky='EW')
		pitch_angle_scl = Scale(self, from_=pitch_angle_min, to=pitch_angle_max, tickinterval=5,orient=HORIZONTAL,variable=self.pitch_angle_var)
		pitch_angle_scl.grid(column=0,row=5,columnspan=3,sticky='EW')
		pitch_angle_btn_up = Button(text="Up",width=4,command=self.increaseAngle)
		pitch_angle_btn_up.grid(column=3,row=5)
		pitch_angle_btn_down = Button(text="Down",command=self.decreaseAngle)
		pitch_angle_btn_down.grid(column=4,row=5)

		self.back_light_var = IntVar()
		back_light_chb = Checkbutton(self, text="Back light", variable=self.back_light_var)
		back_light_chb.grid(column=0,row=6,columnspan=3,sticky='EW')

		bad_msg_lbl = Label(self, text="Bad Message",width=20)
		bad_msg_lbl.grid(column=0,row=7,sticky='NS')
		self.bad_msg = False
		self.bad_msg_btn = Button(self, text="OFF", bg="green", command=self.switchBadMsg)
		self.bad_msg_btn.grid(column=1,row=7,columnspan=2,sticky='EW')

	# Quit the application
	def quit(self):
		#print "Quit the application !"
		if self.connectTimer != None:
			self.connectTimer.cancel()
		if self.networkTimer != None:
			self.networkTimer.cancel()
		if self.sock != None:
			self.sock.close()
		if self.angleTimer != None:
			self.angleTimer.cancel()

### Callbacks #################################################################

	# Callback called when the "Up" button is clicked
	def increaseAngle(self):
		# If the angle is decreasing, we stop the timer
		if self.angleIsDecreasing:
			self.angleTimer.cancel()
		self.angleIsIncreasing = True
		self.angleIsDecreasing = False
		# Then we restart the timer to increase the timer
		self.angleTimer = threading.Timer(angle_dt,self.increaseAngle)
		self.angleTimer.start()
		angle = self.pitch_angle_var.get()
		# We stop the timer when the angle is max
		if angle<pitch_angle_max:
			self.pitch_angle_var.set(angle+1.0)
		else:
			self.angleTimer.cancel()
	
	# Callback called when the "Down" button is clicked
	def decreaseAngle(self):
		# If the angle is increasing, we stop the timer
		if self.angleIsIncreasing:
			self.angleTimer.cancel()
		self.angleIsIncreasing = False
		self.angleIsDecreasing = True
		# Then we restart the timer to decrease the timer
		self.angleTimer = threading.Timer(angle_dt, self.decreaseAngle)
		self.angleTimer.start()
		angle = self.pitch_angle_var.get()
		# We stop the timer when the angle is mim
		if angle>pitch_angle_min:
			self.pitch_angle_var.set(angle-1.0)
		else:
			self.angleTimer.cancel()

	def switchBadMsg(self):
		self.bad_msg = not self.bad_msg
		if self.bad_msg:
			self.bad_msg_btn.config(text="ON", bg="red")
		else:
			self.bad_msg_btn.config(text="OFF", bg="green")


### Network ###################################################################

	def launchConnectTimer(self):
		try:
			self.sock = socket.socket(socket.AF_INET, # Internet
					socket.SOCK_STREAM) # TCP
			self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.sock.connect((ip_address, port))
			print "Connected"
			self.launchNetworkTimer()
		except:
			self.sock = None
			self.connectTimer = threading.Timer(network_dt, self.launchConnectTimer)
			self.connectTimer.start()

	# Launch the timer sending network messages
	def launchNetworkTimer(self):
		timestamp = ctypes.c_uint32(int(time.time()*1000.0)) # ms
		if self.bad_msg:
			timestamp = ctypes.c_uint32(0) # ms
			data=struct.pack(
					'IfffffI',
					timestamp.value,
					float(-1.0),
					float(0.7),
					float(2.1),
					float(5.1),
					float(31.0),
					ctypes.c_uint32(2).value
					)
		else:
			data=struct.pack(
					'IfffffI',
					timestamp.value,
					float(self.dome_flow_var.get()),
					float(self.high_purge_var.get()),
					float(self.air_intake_tube_var.get()),
					float(self.output_flow_var.get()),
					float(self.pitch_angle_var.get()),
					ctypes.c_uint32(self.back_light_var.get()).value
					)
		if self.sock != None:
                    try:
			self.sock.send(data)
			self.networkTimer = threading.Timer(network_dt, self.launchNetworkTimer)
			self.networkTimer.start()
                    except:
			print "Disconnected"
			self.launchConnectTimer()

### Main ######################################################################

if __name__ == "__main__":
	app = Application(None)
	app.title('Client')
	app.mainloop()
	app.quit()
