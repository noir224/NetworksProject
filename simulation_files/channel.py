# simulation of the unreliable channel communications
# main features:
# - get corrupted data with probability corrupt_p
# - get lost data with probability lost_p
# - set the channel delay to be (delay) amount of simulation time


import simpy
import random
from packet import packet
import copy


class channel(object):
    def __init__(self, env, corrupt_p, lost_p, delay, name):

        self.env = env
        self.corrupt_p = corrupt_p
        self.lost_p = lost_p
        self.delay = delay

        self.receiver = None
        self.name = name

    def udt_send(self, s_pkt,start_time):
        pkt = copy.copy(s_pkt)
        print("TIME: ", self.env.now, self.name, ": udt_send called to send pkt ", pkt)
        self.env.process(self.deliver_packet(self.delay, pkt,start_time))

    def deliver_packet(self, delay, d_pkt,start_time):

        pkt = copy.copy(d_pkt)
        pkt2 = copy.copy(d_pkt)
        # testing for packet before delivering it to the upper layer (receiver side)

        if random.random() < self.corrupt_p: #corrupt data
            pkt.set_corrupt()
            print("TIME: ", self.env.now, self.name, ": packet is corrupted!!!")
            self.receiver.rdt_rcv(pkt,start_time)

        # self.udt_send(pkt)

        else:
            if random.random() < self.lost_p: #lose data
                pkt.set_corrupt()
                print("TIME: ", self.env.now, self.name, ": packet is lost!!!")

            # send the packet to the upper layer after delay time

            yield self.env.timeout(delay)
            self.receiver.rdt_rcv(pkt,start_time)

