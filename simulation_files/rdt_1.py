# The Transport Layer simulation (using Reliable Data Transport (rdt) protocol)
# rdt_1.0
import sys

# Sender Transport Layer 
# rdt_sender
# - receive message from the application layer 
# - run the rdt_1.0 protocol using udt_send() method 


# Receiver Transport Layer
# rdt_reecieve 
# - receive packet from the underlaying channel (lower layer) through rdt_rcv() method
# - delivers the packet to the upper layer (applicaiton layer)


#two types of rdt one fro sender and one for reciever
import simpy
import random
from packet import packet


class rdt_sender(object):
	def __init__(self, env):
		self.env=env #create an enviroment
		self.channel= None #create a connection
		self.seq_num =0 #to count how many sequences i need to know, so far we only need 0

	def rdt_send(self, msg,start_time):
		# create a packet
		# send it through the channel udt_send() method
		# confirm to the upper layer the sent message #print and increment if successfully sent

		pkt= packet(seq_num=self.seq_num, payload=msg)
		self.seq_num +=1 #count how many messages i got
		self.channel.udt_send(pkt,start_time) #send through udt
		#every class has an instant of another class to call it

		if (pkt.sequ_num == 501):
			print("all messages sent")
			sys.exit(0)
		return True

	def rdt_rcv(self,pkt,start_time):
		# in other versions of the rdt protocol.. you will need a method that will 
		# handle the incoming packets from the receivers
		# in specific (ACK and NAK messages)
		print("not yet implemented!!!!")
		pass


class rdt_receiver(object):
	
	def __init__ (self,env):
		self.env= env
		self.ReceiverAPP= None
		self.channel= None #has two connections one go up one go down if im gonna do ack

	def rdt_rcv(self, pkt,start_time):

		# received a packet from lower layer
		# check for corruption, then
		# deliver the packet to upper layer method deliver_data()

		if not (pkt.corrupted):
			self.ReceiverAPP.deliver_data(pkt.payload,start_time) #call the reciever that collects the data
