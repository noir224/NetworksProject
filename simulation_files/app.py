# Application layer simulation consists of two parts (sender, and receiver)
#
# The Sender APP:
# - create new message 
# - call transport layer rdt_sender to deliver messages through rd_send()


# The Receiver APP:
# - recieve message from the transport layer through deliver_data()
# - validate the information recieved 


import simpy
import random
import packet 
import sys
import matplotlib.pyplot as plt
import numpy as np
tot_mes = 0
import time as times
end_time=0


class SenderAPP(object):
	def __init__(self, env):
		self.env=env 
		self.rdt_sender = None
		self.total_messages=0


		self.env.process(self.app_process())

	def app_process(self):
		while True:
			#set a random timer to send messages within that selected simulation time
			time= random.randint(3,3)
			yield self.env.timeout(time)
			#generate a message and send it to the lower layer
			message="hello "+str(self.total_messages)
			print("TIME: ", self.env.now, "SenderAPP: a message was sent ")
			start_time = int(self.env.now)
			print(start_time, " this is start time")
			if self.rdt_sender.rdt_send(message,start_time):
				#this means the message has been successfully processed by the lower layer
				self.total_messages +=1 #some error is happening here basically it's incrementing just by the act of sending happenin
				#it should increment if message is sent and recieved



class ReceiverAPP(object): #only collects information

	def __init__(self,env):
		self.env = env 
		self.total_rec_messages = 0
		self.E2Es = []
		self.checks = []


	def deliver_data(self,pkt,start_time): #middle man between application layer and transport layer
		#This method is the middle-man between the application layer and the transport layer
		#to handle incoming packets
		#responsible of validating the information received 
		#for the purpose of this example: we will validate by checking if this is all lowercase message
		print ("Time: ",self.env.now, "ReceiverAPP: Received data message ", pkt.payload)
		end_time = int(self.env.now)
		print(end_time, " this is the end time")
		e2e = end_time - start_time
		print("e2e = ",e2e,"for message ", pkt.payload)

		if not  pkt.sequ_num in self.checks:
			self.E2Es.append(e2e)
			self.checks.append(pkt.sequ_num)
		if pkt.sequ_num == 500:
			print("average of e2e= ",sum(self.E2Es)/len(self.E2Es))
			plt.plot(self.E2Es)
			plt.ylabel("e2es")
			plt.xlabel("messages")
			plt.show()

			#print("average for rtt= ",(sum(rtts)/len(rtts)))
		#	sys.exit(0)

		if not (pkt.payload.islower()):
			print("ERORR!!!!!!")
			print("Stop simulation......")
			sys.exit(0)

		#otherwise we increment the number of received data
		self.total_rec_messages +=1




